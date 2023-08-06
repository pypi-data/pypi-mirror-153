#  ---------------------------------------------------------------------------------
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2022.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#  ---------------------------------------------------------------------------------

from contextlib import suppress
import logging
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import zipfile

import requests

from bosun.model_connector.constants import ModelPackageConstants


class DockerLabels:
    MLOPS_LABEL = "mlops"
    AGENT_LABEL = "mlops.agent"
    RABBITMQ_LABEL = "mlops.rabbitmq"
    REVERSE_PROXY_LABEL = "mlops.reverse_proxy"
    MLOPS_DEPLOYMENT = "mlops.deployment"
    DEPLOYMENT_ID_LABEL = "mlops.deployment_id"
    MODEL_ID_LABEL = "mlops.model_id"
    PREDICTION_PORT = "mlops.prediction_port"
    MODEL_EXECUTION_TYPE_LABEL = "model_execution_type"


def get_containers_with_label(client, label, value=None, force_one=False):
    container_list = client.containers.list()
    containers = []
    for c in container_list:
        found = False
        if label in c.labels:
            if value:
                if c.labels[label] == value:
                    found = True
            else:
                found = True
        if found:
            containers.append(c)

    if force_one:
        if len(containers) > 1:
            raise Exception("Found more then one container for the same deployment")
    return containers


class DockerHelper:
    # Need to use /tmp for now because it is the easiest way so we can run both natively on the host
    # OS and also in a docker container (with /tmp from the host OS mounted in).
    MODEL_ARCHIVE_DIR = Path("/tmp/bosun-docker_plugin-model_archives")

    def __init__(self, docker_client, config):
        self._client = docker_client
        self._logger = logging.getLogger("{}.{}".format(
            self.__class__.__module__, self.__class__.__name__))
        self._config = config

    def _container_name(self, deployment_id, model_id):
        return "{}{}_{}".format(self._config.container_name_prefix, deployment_id, model_id)

    def get_running_deployment_containers(self, deployment_id=None, force_one=False, model_id=None):
        container_list = self._client.containers.list()
        cm_containers = []
        for c in container_list:
            found = False
            if DockerLabels.DEPLOYMENT_ID_LABEL in c.labels:
                if deployment_id:
                    if c.labels[DockerLabels.DEPLOYMENT_ID_LABEL] == deployment_id:
                        if model_id:
                            if c.labels[DockerLabels.MODEL_ID_LABEL] == model_id:
                                found = True
                        else:
                            found = True
                else:
                    found = True
            if found:
                cm_containers.append(c)

        if force_one:
            if len(cm_containers) > 1:
                raise Exception("Found more then one container for the same deployment")
        return cm_containers

    def is_deployment_container_running(self, deployment_id):
        cl = self.get_running_deployment_containers(deployment_id=deployment_id)
        if len(cl) == 0:
            return False
        else:
            return True

    @property
    def running_in_container(self):
        return os.path.exists("/.dockerenv")

    @staticmethod
    def get_model_id(container):
        if DockerLabels.MODEL_ID_LABEL in container.labels:
            return container.labels[DockerLabels.MODEL_ID_LABEL]
        return None

    @staticmethod
    def find_port(container, internal_port):
        for port in container.ports:
            port_str = internal_port + "/tcp"
            if port == port_str:
                host_port = container.ports[port][0]["HostPort"]
                return host_port
        return None

    def stop_container(self, container, remove=False):
        self._logger.info("Stopping container: {}".format(container.name))
        container.stop()
        if remove:
            self._logger.info("Removing container: {}".format(container.name))
            container.remove()
            self.remove_model_archive(container.name)

    def save_model_archive(self, archive_path, container_name):
        # Saves the model archive to a location we control so we can maintain the lifecycle of
        # th file based on the lifecycle of the deployment.
        self.MODEL_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        dest = self.MODEL_ARCHIVE_DIR / "{}.mlpkg".format(container_name)
        with suppress(shutil.SameFileError):
            shutil.copyfile(archive_path, dest)
        # Make sure to give read access to everyone since we share the file between containers
        # that can be running as completely different users (i.e. root and datarobot-service).
        dest.chmod(0o644)
        return dest

    def remove_model_archive(self, container_name):
        # Model replacements in DR result in new containers so it should be safe to remove the
        # .mlpkg file finally when this occurs.
        with suppress(FileNotFoundError):
            pkg_name = "{}.mlpkg".format(container_name)
            (self.MODEL_ARCHIVE_DIR / pkg_name).unlink()

    @staticmethod
    def _container_labels(container_name,
                          deployment_id,
                          deployment_predict_path,
                          deployment_ping_path,
                          model_id,
                          model_execution_type,
                          host_port,
                          container_predict_path,
                          container_ping_path="/ping",
                          ):
        # The rule that send the request with the specific deployment id to this container
        predict_router = container_name + "_predict"
        ping_router = container_name + "_ping"

        predict_router_rule_label = "traefik.http.routers.{}.rule".format(predict_router)
        predict_router_rule_label_value = "Path(`{}`)".format(deployment_predict_path)

        ping_router_rule_label = "traefik.http.routers.{}.rule".format(ping_router)
        ping_router_rule_label_value = "Path(`{}`)".format(deployment_ping_path)

        predict_middleware = container_name + "_predict"
        ping_middleware = container_name + "_ping"

        predict_middleware_label = \
            "traefik.http.middlewares.{}.replacepath.path".format(predict_middleware)
        predict_middleware_value = container_predict_path

        ping_middleware_label = "traefik.http.middlewares.{}.replacepath.path".format(
            ping_middleware)
        ping_middleware_value = container_ping_path

        # Attaching the middleware to the router (which has the rule)
        predict_router_middleware_label = \
            "traefik.http.routers.{}.middlewares".format(predict_router)
        predict_router_middleware_label_value = "{}@docker".format(predict_middleware)

        ping_router_middleware_label = \
            "traefik.http.routers.{}.middlewares".format(ping_router)
        ping_router_middleware_label_value = "{}@docker".format(ping_middleware)

        return {
            DockerLabels.MLOPS_LABEL: None,
            DockerLabels.PREDICTION_PORT: "{}".format(host_port),
            DockerLabels.DEPLOYMENT_ID_LABEL: deployment_id,
            DockerLabels.MODEL_ID_LABEL: model_id,
            DockerLabels.MODEL_EXECUTION_TYPE_LABEL: model_execution_type,
            predict_router_rule_label: predict_router_rule_label_value,
            predict_middleware_label: predict_middleware_value,
            predict_router_middleware_label: predict_router_middleware_label_value,
            ping_router_rule_label: ping_router_rule_label_value,
            ping_middleware_label: ping_middleware_value,
            ping_router_middleware_label: ping_router_middleware_label_value,
        }


class CMDockerHelper(DockerHelper):
    CM_SERVER_INTERNAL_PORT = "6788"

    def __init__(self, docker_client, config):
        super(CMDockerHelper, self).__init__(docker_client, config)

    def ping_prediction_server(self, deployment_id, container, count=10, sleep_time=1):
        if self.running_in_container:
            url = "http://{}:{}/".format(container.name, self.CM_SERVER_INTERNAL_PORT)
        else:
            host_port = self.find_port(container, self.CM_SERVER_INTERNAL_PORT)
            if not host_port:
                raise Exception("Could not find container host port (deployment: {})"
                                .format(deployment_id))

            self._logger.debug("Found server port, host port: {}".format(host_port))
            url = "http://0.0.0.0:{}/".format(host_port)
        self._logger.info("Checking deployment: {} status, url: {}".format(deployment_id, url))
        last_error = None
        for ii in range(0, count):
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    return True, ""
                else:
                    last_error = "request status: {}".format(res.status_code)
            except Exception as e:
                self._logger.info("Failed sending request... will try again")
                last_error = e
            self._logger.info("ping: count {} going to sleep".format(ii))
            time.sleep(sleep_time)

        raise Exception("Could not ping cm server deployment_id: {} : error {}"
                        .format(deployment_id, last_error))

    def build_cm_container(self, di):
        with tempfile.TemporaryDirectory() as tmp_dir:
            with zipfile.ZipFile(di.model_artifact, "r") as zip_ref:
                zip_ref.extractall(tmp_dir)

            installer = os.path.join(tmp_dir, "cm_pps_installer.sh")
            if not os.path.exists(installer):
                raise Exception("Missing custom model installer: {}".format(installer))

            # Build docker image
            cmd = ["bash", installer, "--skip-agent-install"]
            build_process = subprocess.Popen(cmd, cwd=tmp_dir, stdout=subprocess.PIPE)
            exit_code = build_process.wait()
            self._logger.info("Building docker image complete with exit code: {}".format(exit_code))

        image_tag = "cm_pps_{}".format(di.model_id)
        if not self._client.images.list(name=image_tag):
            raise Exception("Image {} was not created successfully".format(image_tag))

        return image_tag

    def run_cm_container(self,
                         image_tag,
                         host_port,
                         deployment_id,
                         model_id,
                         monitor_settings,
                         deployment_predict_path,
                         deployment_ping_path):

        container_name = self._container_name(deployment_id, model_id)
        labels = self._container_labels(container_name,
                                        deployment_id,
                                        deployment_predict_path,
                                        deployment_ping_path,
                                        model_id,
                                        ModelPackageConstants.MODEL_EXECUTION_CUSTOM_INFERENCE,
                                        host_port,
                                        "/predict/")
        ports = {"{}/tcp".format(self.CM_SERVER_INTERNAL_PORT): host_port}
        env = {
            "ADDRESS": "0.0.0.0:{}".format(self.CM_SERVER_INTERNAL_PORT),
            "MODEL_ID": model_id,
            "DEPLOYMENT_ID": deployment_id,
            "MONITOR": str(self._config.do_mlops_monitoring),
            "MONITOR_SETTINGS": monitor_settings,
            "PRODUCTION": "1",
        }
        self._client.containers.run(image_tag,
                                    name=container_name,
                                    environment=env,
                                    ports=ports,
                                    detach=True,
                                    labels=labels,
                                    network=self._config.docker_network)


class PPSDockerHelper(DockerHelper):
    SERVER_INTERNAL_PORT = "8080"

    def __init__(self, docker_client, base_image, config):
        super(PPSDockerHelper, self).__init__(docker_client, config)
        self._base_image = base_image

    def run_pps_container(self,
                          deployment_id,
                          model_id,
                          model_artifact,
                          monitor_settings,
                          deployment_predict_path,
                          deployment_ping_path):

        container_name = self._container_name(deployment_id, model_id)
        labels = self._container_labels(container_name,
                                        deployment_id,
                                        deployment_predict_path,
                                        deployment_ping_path,
                                        model_id,
                                        ModelPackageConstants.MODEL_EXECUTION_DEDICATED,
                                        "0",
                                        "/predictions")

        persisted_archive_path = self.save_model_archive(model_artifact, container_name)
        pps_artifact_path = Path("/opt/ml/model/") / persisted_archive_path.name

        env = {
            "PREDICTION_API_MODEL_REPOSITORY_PATH": str(pps_artifact_path),
            "PREDICTION_API_MONITORING_ENABLED": str(self._config.do_mlops_monitoring),
            "MONITORING_AGENT": "False",
            "PREDICTION_API_MONITORING_SETTINGS": monitor_settings,
            "PORTABLE_PREDICTION_API_MONITORING_SETTINGS": monitor_settings,
            "MLOPS_DEPLOYMENT_ID": deployment_id,
            "MLOPS_MODEL_ID": model_id,
        }
        ports = {"{}/tcp".format(self.SERVER_INTERNAL_PORT): "0"}

        volumes = {str(persisted_archive_path.absolute()): {"bind": str(pps_artifact_path),
                                                            "mode": "ro"}}

        self._client.containers.run(self._base_image,
                                    name=container_name,
                                    environment=env,
                                    ports=ports,
                                    detach=True,
                                    labels=labels,
                                    volumes=volumes,
                                    network=self._config.docker_network)

    def ping_prediction_server(self, deployment_id, container, count=60, sleep_time=1):
        if self.running_in_container:
            url = "http://{}:{}/ping".format(container.name, self.SERVER_INTERNAL_PORT)
        else:
            host_port = self.find_port(container, self.SERVER_INTERNAL_PORT)
            if not host_port:
                raise Exception("Could not find container host port (deployment: {})"
                                .format(deployment_id))

            self._logger.debug("Found server port, host port: {}".format(host_port))
            url = "http://0.0.0.0:{}/ping".format(host_port)
        self._logger.info("Checking deployment: {} status, url: {}".format(deployment_id, url))
        last_error = None
        for ii in range(0, count):
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    return True, ""
                else:
                    last_error = "request status: {}".format(res.status_code)
            except Exception as e:
                self._logger.info("Failed sending request... will try again")
                last_error = e
            self._logger.info("ping: count {} going to sleep".format(ii))
            time.sleep(sleep_time)

        raise Exception("Could not ping pps server deployment_id: {} : error {}"
                        .format(deployment_id, last_error))

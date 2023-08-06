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

import logging
import pprint
import time
import traceback

import docker
import yaml

from bosun.model_connector.constants import ModelPackageConstants
from bosun.plugin.action_status import ActionStatus, ActionStatusInfo, ActionDataFields
from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.constants import DeploymentState
from bosun.plugin.deployment_info import DeploymentInfo
from bosun.plugin.docker.docker_helper import DockerHelper, CMDockerHelper, PPSDockerHelper, \
    DockerLabels, get_containers_with_label
from bosun.plugin.docker.docker_plugin_config import DockerPluginConfig
from bosun.plugin.docker.mlops_monitoring import MLOpsMonitoringHelper
from bosun.plugin.exceptions import DeploymentLaunchException, DeploymentStopException

# TODO: collect all existing deployments - AM request
# TODO: add a way for the plugin runner to get status of all currently running deployments
# TODO: Add support for auto restart on failure?
# TODO: Add support for memory limitation
# TODO: fix PPS/CM to use same internal endpoints and payload configuraiton (YG fix)
# TODO: Add support for tarballs models (YG)


class DockerPlugin(BosunPluginBase):

    def __init__(self, plugin_config, private_config_file, pe_info, dry_run):
        super().__init__(plugin_config, private_config_file, pe_info, dry_run)

        self._client = docker.from_env()
        info = self._client.info()
        self._logger.debug("Docker client info:\n", pprint.pformat(info))
        self._read_config_file()
        self._config = DockerPluginConfig(self._plugin_config)
        self._rabbitmq_queue_url = "amqp://drum:drum123@rabbit"
        self._rabbitmq_queue_name = "drum"
        self._mlops_helper = MLOpsMonitoringHelper(
            self._client,
            agent_image=self._config.agent_image,
            rabbitmq_image=self._config.rabbit_image,
            rabbitmq_queue_url=self._rabbitmq_queue_url,
            rabbitmq_queue_name=self._rabbitmq_queue_name,
            datarobot_url=self._config.datarobot_app_url,
            datarobot_api_token=self._config.datarobot_api_key,
            docker_network=self._config.docker_network,
            dry_run=self._dry_run
        )

    @property
    def _monitor_settings(self):
        return "spooler_type=rabbitmq;rabbitmq_queue_url={};rabbitmq_queue_name={}".format(
            self._rabbitmq_queue_url,
            self._rabbitmq_queue_name
        )

    @staticmethod
    def _deployment_base_path(di):
        return "/deployments/{}".format(di.id)

    @staticmethod
    def _deployment_predict_path(di):
        return "{}/predictions".format(DockerPlugin._deployment_base_path(di))

    @staticmethod
    def _deployment_ping_path(di):
        return "{}/ping".format(DockerPlugin._deployment_base_path(di))

    def _read_config_file(self):
        """
        Reading the plugin specific config file is such is provided. And overriding this plugin
        configuration
        :return:
        """
        if not self._private_config_file:
            return

        self._logger.info("Docker plugin private config file: {}".format(self._private_config_file))
        with open(self._private_config_file) as conf_file:
            config = yaml.safe_load(conf_file)
        self._logger.info(config)
        self._plugin_config.update(config)
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(self.get_sanitized_config(self._plugin_config))

    def clean_stopped_reverse_proxy_container_if_any(self):
        reverse_proxy_container = self._client.containers.list(
            filters={"label": DockerLabels.REVERSE_PROXY_LABEL, "status": "exited"}
        )
        if len(reverse_proxy_container) == 0:
            return
        if reverse_proxy_container[0].status == "exited":
            self._logger.info("Removing stopped reverse proxy container")
            reverse_proxy_container[0].remove()

    def _start_reverse_proxy(self):
        self.clean_stopped_reverse_proxy_container_if_any()
        self._logger.info("Starting reverse proxy container")

        if self._config.traefik_port_mapping:
            ports = {str(k): str(v) for k, v in self._config.traefik_port_mapping.items()}
        else:
            ports = {
                "80": "80",
                "8080": "8080"
            }
        self._logger.info("Reverse proxy port mapping: '{}'".format(ports))
        labels = {
            DockerLabels.REVERSE_PROXY_LABEL: "reverse_proxy",
            DockerLabels.MLOPS_LABEL: None
        }
        volumes = {
            "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "ro"}
        }

        if self._is_reverse_proxy_running():
            self._logger.info("Reverse Proxy container is already running skipping")
            return

        if self._dry_run:
            self._logger.info("DRYRUN: running traefik container.")
        else:
            self._client.containers.run(self._config.traefik_image,
                                        command="--api.insecure=true --providers.docker",
                                        name="reverse_proxy",
                                        network=self._config.docker_network,
                                        ports=ports,
                                        volumes=volumes,
                                        detach=True,
                                        labels=labels)

    def _stop_reverse_proxy(self):

        if self._dry_run:
            self._logger("DRYRUN: skipping traefik stop")
        else:
            self._logger.info("Stopping reverse proxy container")
            reverse_proxy_container = self._get_running_reverse_proxy_containers()
            for container in reverse_proxy_container:
                container.stop()
                container.remove()

    def _get_running_reverse_proxy_containers(self):
        return get_containers_with_label(self._client, label=DockerLabels.REVERSE_PROXY_LABEL)

    def _is_reverse_proxy_running(self):
        cl = self._get_running_reverse_proxy_containers()
        if len(cl) == 0:
            return False
        else:
            return True

    def plugin_start(self):
        self._logger.info("Docker plugin start called")
        if self._config.do_mlops_monitoring:
            self._mlops_helper.start(self._config.rabbitmq_port_mapping)

        self._start_reverse_proxy()
        return ActionStatusInfo(ActionStatus.OK)

    def plugin_stop(self):
        self._logger.info("Docker plugin stop called")
        cm_helper = DockerHelper(self._client, self._config)
        container_list = cm_helper.get_running_deployment_containers()
        for c in container_list:
            self._logger.info("Container {} is still running".format(c))

        # Taking down the MLOps monitoring containers.
        if self._config.do_mlops_monitoring:
            self._mlops_helper.stop()
        self._stop_reverse_proxy()
        return ActionStatusInfo(ActionStatus.OK)

    def _deploy_cm_model(self, di):
        port = int(di.kv_config.get("port", "0"))
        model_id = di.new_model_id if di.new_model_id is not None else di.model_id
        cm_helper = CMDockerHelper(self._client, self._config)
        image_tag = cm_helper.build_cm_container(di)

        cm_helper.run_cm_container(image_tag=image_tag,
                                   host_port=port,
                                   deployment_id=di.id,
                                   model_id=model_id,
                                   monitor_settings=self._monitor_settings,
                                   deployment_predict_path=self._deployment_predict_path(di),
                                   deployment_ping_path=self._deployment_ping_path(di))

        # Waiting some time before we start pinging - otherwise the first few requests of the ping
        # will fail every time - It takes about 2 seconds to start drum inside the container and
        # start serving the model.
        time.sleep(2)

        container = cm_helper.get_running_deployment_containers(deployment_id=di.id,
                                                                model_id=model_id)[0]
        cm_helper.ping_prediction_server(di.id, container)

        msg = "Deployment {} launched, image tag: {} container id {}" \
            .format(di.id, image_tag, container.id)
        return msg

    def _deploy_dr_model(self, di):
        base_image = di.kv_config.get(DeploymentInfo.BASE_IMAGE_KEY, self._config.pps_base_image)
        pps_helper = PPSDockerHelper(self._client, base_image, self._config)
        model_id = di.new_model_id if di.new_model_id is not None else di.model_id
        pps_helper.run_pps_container(deployment_id=di.id,
                                     model_id=model_id,
                                     model_artifact=di.model_artifact,
                                     monitor_settings=self._monitor_settings,
                                     deployment_predict_path=self._deployment_predict_path(di),
                                     deployment_ping_path=self._deployment_ping_path(di)
                                     )

        # Waiting some time before we start pinging - otherwise the first few requests of the ping
        # will fail every time - It takes about 2 seconds to start drum inside the container and
        # start serving the model.
        time.sleep(10)
        container = pps_helper.get_running_deployment_containers(deployment_id=di.id,
                                                                 model_id=model_id)[0]
        pps_helper.ping_prediction_server(di.id, container)

        msg = "Deployment {} launched, image tag: {} container id {}" \
            .format(di.id, self._config.pps_base_image, container.id)
        return msg

    def _deploy_model(self, di):
        # According to the model type we decide how to run the container
        # We have 2 options - DataRobot models using PPS and User Models using DRUM
        if di.model_execution_type == ModelPackageConstants.MODEL_EXECUTION_DEDICATED:
            self._logger.info("Got a DataRobot Native model to deploy")
            msg = self._deploy_dr_model(di)
        elif di.model_execution_type == ModelPackageConstants.MODEL_EXECUTION_CUSTOM_INFERENCE:
            self._logger.info("Got a User Custom Inference model to deploy")
            msg = self._deploy_cm_model(di)
        else:
            raise Exception("This plugin does not support model of type: {}"
                            .format(di.model_execution_type))
        return msg

    def _apply_deployment(self, di):
        """
        Making sure the deployment is correctly applied. This means, taking down containers serving
        old models, and creating containers serving new models
        :param di:
        :return:
        """
        # Find existing containers
        helper = DockerHelper(self._client, self._config)
        containers = helper.get_running_deployment_containers(di.id)
        containers_to_stop = []
        containers_to_keep = []
        for container in containers:
            model_id = helper.get_model_id(container)
            if model_id == di.model_id and di.new_model_id is None:
                containers_to_keep.append(container)
            else:
                containers_to_stop.append(container)
        self._logger.info("Containers to stop: {}".format(len(containers_to_stop)))
        self._logger.info("Containers to keep: {}".format(len(containers_to_keep)))

        # Check if we need to deploy new containers, and if so deploy one
        if len(containers_to_keep) > 0:
            msg = "Not deploying any new container"
            self._logger.info(msg)
        else:
            if self._dry_run:
                self._logger.info("DRYRUN: Deploying new container")
                msg = "DRY RUN deploy"
            else:
                self._logger.info("Deploying a new container")
                try:
                    msg = self._deploy_model(di)
                except Exception as ex:
                    raise DeploymentLaunchException(ex, "Failed to launch container")

        # Take down the original container(s)
        if len(containers_to_stop) > 0:
            for c in containers_to_stop:
                m = "Stopping container: {}".format(c.name)
                if self._dry_run:
                    self._logger.info("DRYRUN: " + m)
                else:
                    self._logger.info(m)
                    try:
                        helper.stop_container(c, remove=True)
                    except Exception as ex:
                        raise DeploymentStopException(ex, "Failed to stop container")

        return msg

    def deployment_start(self, deployment_info):
        """
        Add a cron job per deployment
        :return:
        """
        di = DeploymentInfo(deployment_info)
        self._logger.info("Launching deployment {}".format(di.id))

        msg = self._apply_deployment(di)

        prediction_url = \
            self._config.outfacing_prediction_url_prefix + self._deployment_predict_path(di)
        data = {
            ActionDataFields.PREDICTION_URL: prediction_url
        }
        return ActionStatusInfo(ActionStatus.OK, msg, state=DeploymentState.READY,
                                data=data)

    def deployment_stop(self, deployment_data):
        """
        Stop the cron job and delete it
        :return:
        """
        self._logger.info("Stopping cm container - this action will take down the model !!!")
        deployment_id = deployment_data["id"]

        helper = DockerHelper(self._client, self._config)
        container_list = helper.get_running_deployment_containers(deployment_id=deployment_id)
        if len(container_list) == 0:
            status = ActionStatus.OK
            status_msg = "No container for deployment {} was found - skipping stop" \
                .format(deployment_id)
        elif len(container_list) > 1:
            status = ActionStatus.WARN
            status_msg = "More then one container was found for deployment {} ... stopping all" \
                .format(deployment_id)

            for c in container_list:
                helper.stop_container(c)
        else:
            helper.stop_container(container_list[0], remove=True)
            status = ActionStatus.OK
            status_msg = "Container stopped"

        self._logger.info(status_msg)
        return ActionStatusInfo(status=status, msg=status_msg, state=DeploymentState.STOPPED)

    def deployment_replace_model(self, deployment_info):
        """
        Will put a model artifact in a place the cronjob can consume it
        :param deployment_info: Info about the deployment
        :param model_artifact_path:
        :return:
        """
        di = DeploymentInfo(deployment_info)
        self._logger.info(
            "-- Replacing model for deployment: {} dry_run: {}".format(di.id, self._dry_run))
        try:
            msg = self._apply_deployment(di)
        except DeploymentLaunchException:
            # In case of launch failure, plugin did not stop the old container, so indicate
            # that in the status response
            msg = "Failed to replace model -\n{}\nContinuing with old model".format(
                traceback.format_exc()
            )
            return ActionStatusInfo(
                ActionStatus.ERROR,
                msg=msg,
                state=DeploymentState.ERROR,
                data={ActionDataFields.OLD_MODEL_IN_USE: True}
            )
        return ActionStatusInfo(ActionStatus.OK, msg="Model replaced successfully: {}".format(msg),
                                state=DeploymentState.READY)

    def pe_status(self):
        """
        Do status check
        :return:
        """
        self._logger.info("Getting status of docker environment")
        try:
            helper = DockerHelper(self._client, self._config)
            container_list = helper.get_running_deployment_containers()
            status_msg = "Number of containers: {}".format(len(container_list))
            status = ActionStatus.OK
        except Exception as e:
            status_msg = "Error checking PE status: {}".format(e)
            status = ActionStatus.ERROR

        if self._config.do_mlops_monitoring:
            mlops_status = self._mlops_helper.status()
            if mlops_status is False and status == ActionStatus.OK:
                status = ActionStatus.WARN
                status_msg = "Error - mlops monitoring is not functioning properly"

        reverse_proxy_status = self._is_reverse_proxy_running()
        if reverse_proxy_status is False:
            status = ActionStatus.ERROR
            status_msg += "Reverse proxy is not running"

        pe_status = ActionStatusInfo(status=status, msg=status_msg)
        all_deployments_status = {}
        for deployment in self._pe_info.deployments:
            deployment_id = deployment["id"]
            self._logger.info("Checking status for deployment: {}".format(deployment_id))
            d_status = self.deployment_status(deployment)
            all_deployments_status[deployment_id] = d_status.to_dict()
            self._logger.info(d_status.to_yaml())
        if bool(all_deployments_status):
            pe_status.data = {ActionDataFields.DEPLOYMENTS_STATUS: all_deployments_status}
        self._logger.info("pe_status: {} {}".format(pe_status.status, pe_status.msg))
        return pe_status

    def deployment_status(self, deployment_info):
        """
        :param deployment_info: Info about the deployment to check
        Do status check
        :return:
        """
        self._logger.info("Getting status for python batch deployment")
        di = DeploymentInfo(deployment_info)

        # TODO: create a DockerHelperFactory
        if di.model_execution_type == ModelPackageConstants.MODEL_EXECUTION_DEDICATED:
            docker_helper = PPSDockerHelper(self._client, self._config.pps_base_image, self._config)
        elif di.model_execution_type == ModelPackageConstants.MODEL_EXECUTION_CUSTOM_INFERENCE:
            docker_helper = CMDockerHelper(self._client, self._config)
        else:
            raise Exception("This plugin does not support model of type: {}"
                            .format(di.model_execution_type))

        containers = docker_helper.get_running_deployment_containers(deployment_id=di.id)

        if len(containers) == 0:
            final_status = ActionStatusInfo(
                ActionStatus.ERROR,
                msg="Error: could not find a container for deployment {}".format(di.id),
                state="errored"
            )
        elif len(containers) > 1:
            # In case of model replacement it is possible that more than 1 containers are
            # running for the same deployment.  As long as at least one container is in OK
            # state, we will return that status.  It is possible that model replacement may
            # fail, and that status will be captured in the subsequent status request
            found_one_good_container = False
            status_data = None
            msg = "Found {} containers for deployment {} ".format(len(containers), di.id)
            for index, container in enumerate(containers):
                cont_status = self._get_deployment_status(docker_helper, di.id, container)
                msg += " - Container {} id {}: {}".format(index, container.id, cont_status.msg)
                if cont_status.status == ActionStatus.OK:
                    found_one_good_container = True
                    status_data = cont_status.data
            if not found_one_good_container:
                final_status = ActionStatusInfo(ActionStatus.ERROR, msg=msg, state="errored")
            else:
                final_status = ActionStatusInfo(
                    ActionStatus.OK, msg=msg, state="ready", data=status_data
                )
        else:
            final_status = self._get_deployment_status(docker_helper, di.id, containers[0])
        self._logger.info(final_status.msg)
        return final_status

    def _get_deployment_status(self, docker_helper, deployment_id, container):
        result = docker_helper.ping_prediction_server(
            deployment_id=deployment_id, container=container
        )
        if result:
            status = ActionStatus.OK
            status_msg = "Deployment {} is doing well".format(deployment_id)
            state = "ready"
            current_model_id = container.labels[DockerLabels.MODEL_ID_LABEL]
            data = {ActionDataFields.CURRENT_MODEL_ID: current_model_id}
        else:
            status = ActionStatus.ERROR
            status_msg = "Could not ping prediction server"
            state = "errored"
            data = None
        self._logger.info(status_msg)
        return ActionStatusInfo(status, msg=status_msg, state=state, data=data)

    def deployment_list(self):
        self._logger.info("Getting the list of running deployments")
        try:
            helper = DockerHelper(self._client, self._config)
            container_list = helper.get_running_deployment_containers()
            status_msg = "Number of cm containers: {}".format(len(container_list))
            status = ActionStatus.OK
        except Exception as e:
            status_msg = "Error checking PE status: {}".format(e)
            status = ActionStatus.ERROR
            return ActionStatusInfo(status=status, msg=status_msg)

        if len(container_list) == 0:
            status_msg = "No containers running"
            self._logger.info(status_msg)
            return ActionStatusInfo(status, msg=status_msg)

        deployments_map = {}
        for deployment_container in container_list:
            if DockerLabels.DEPLOYMENT_ID_LABEL in deployment_container.labels:
                deployment_id = deployment_container.labels[DockerLabels.DEPLOYMENT_ID_LABEL]
            else:
                continue

            model_execution_type = None
            if DockerLabels.MODEL_EXECUTION_TYPE_LABEL in deployment_container.labels:
                model_execution_type = deployment_container.labels[
                    DockerLabels.MODEL_EXECUTION_TYPE_LABEL
                ]

            if model_execution_type == ModelPackageConstants.MODEL_EXECUTION_DEDICATED:
                docker_helper = PPSDockerHelper(
                    self._client, self._config.pps_base_image, self._config
                )
            elif model_execution_type == ModelPackageConstants.MODEL_EXECUTION_CUSTOM_INFERENCE:
                docker_helper = CMDockerHelper(
                    self._client, self._config
                )
            else:
                self._logger.warn(
                    "This plugin does not support model of type: {}".format(model_execution_type)
                )
                continue

            deployments_map[deployment_id] = self._get_deployment_status(
                docker_helper, deployment_id, deployment_container
            ).__dict__

        self._logger.info(status_msg)
        self._logger.info("Containers: " + str(deployments_map))
        return ActionStatusInfo(status, msg=status_msg, data=deployments_map)

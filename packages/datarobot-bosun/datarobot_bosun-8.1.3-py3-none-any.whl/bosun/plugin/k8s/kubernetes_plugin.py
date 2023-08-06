#  ---------------------------------------------------------------------------------
#  Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
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
import subprocess
import tarfile
import time
from contextlib import suppress
from functools import partial
from pathlib import Path
from tempfile import TemporaryFile, TemporaryDirectory
from urllib.parse import urljoin
from zipfile import ZipFile, BadZipFile

from bosun.model_connector.constants import ModelPackageConstants
from bosun.plugin.action_status import ActionStatus, ActionStatusInfo, ActionDataFields
from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.constants import DeploymentState
from bosun.plugin.deployment_info import DeploymentInfo

from .client import get_client, ClientError, ClientErrorList, codes, make_selector
from .config import KubernetesPluginConfig
from .manifests import COMPONENT_LABEL_NAME
from .manifests import DEPLOYMENT_LABEL_NAME
from .manifests import MODEL_LABEL_NAME
from .manifests import PRED_ENV_LABEL_NAME
from .manifests import ResourceBuilder

logger = logging.getLogger(__name__)

MB = 2**20

# TODO: make these timeouts user configurable
# Make sure to keep these deadlines under the 30 min global action timeout so we have time to
# cleanup if we need to.
ACTION_TIMEOUT_SECONDS = 60 * 27.5

# Allow the image building to use up the bulk of the Action timeout duration since it is the most
# time consuming part.
IMAGE_BUILD_DEADLINE_SECONDS = ACTION_TIMEOUT_SECONDS - 40


class DeploymentNotFound(Exception):
    pass


class KubernetesPlugin(BosunPluginBase):
    def __init__(self, plugin_config, private_config_file, pe_info, dry_run):
        super().__init__(plugin_config, private_config_file, pe_info, dry_run)
        self._config = KubernetesPluginConfig.from_files(self._plugin_config,
                                                         self._private_config_file)
        self._client = get_client(
            context=self._config.kubernetes_config_context,
            namespace=self._config.kubernetes_namespace)
        self._renderer = ResourceBuilder(self._config, self._pe_info)

    def plugin_start(self):
        """
        Perform simple sanity checks that the plugin has been configured correctly and can
        communicate with Kubernetes. It is **not** an exhaustive check.
        """
        # TODO: If we wanted a more complete check that things will work at deployment launch time
        #      we could try launching a _fake_ deployment, build a simple image, etc.
        self._logger.info("Management Agent K8s Plugin - start called")
        self._logger.info("Connected to K8s: %s\n%s",
                          self._client.api.configuration.host, self._client.version_info)
        self._logger.info("Using k8s namespace: %s", self._client.namespace)
        status_msg = "Connected to Kubernetes cluster: {} {}".format(
            self._client.api.configuration.host,
            self._client.version_info.git_version,
        )
        # Make sure the cluster is a supported version
        self._renderer.validate_k8s_version(self._client.version_info)

        # Check that we can perform at least one basic API call
        self._client.get_deployments("noMatch=selector")

        # Cleanup any cruft that may have been left from a crashed process
        # TODO: looks like Bosun doesn't send in pe_info data on plugin_start :'(
        # labels = {COMPONENT_LABEL_NAME: "imageBuilder", PRED_ENV_LABEL_NAME: self._pe_info.id}
        # results = self._client.delete("v1", "Pod", label_selector=make_selector(labels))
        # if results.items:
        #     self._logger.info("Cleaned up Pods from prior run: %s",
        #                       [i.metadata.name for i in results.items])
        return ActionStatusInfo(ActionStatus.OK, msg=status_msg)

    def plugin_stop(self):
        """
        No-op
        """
        self._logger.info("Management Agent K8s Plugin - stop called")
        return ActionStatusInfo(ActionStatus.OK)

    def deployment_list(self):
        """
        List all deployments managed by this Bosun instance and return their status.
        """
        self._logger.info("Getting the list of running deployments")
        deployments_map = self._list_deployments()
        if len(deployments_map) == 0:
            status_msg = "No Deployments running"
            self._logger.info(status_msg)
            return ActionStatusInfo(ActionStatus.OK, msg=status_msg)
        status_msg = "Number of deployments: {}".format(len(deployments_map))
        self._logger.info(status_msg)
        return ActionStatusInfo(ActionStatus.OK, msg=status_msg, data=deployments_map)

    def pe_status(self):
        """
        Checks to see that the K8s API is still functioning correctly. We also implement the
        the extended health check functionality by returning the status of the managed deployments.
        """
        self._logger.info("Getting status of k8s environment")
        try:
            self._client.version_api.get_code()  # sanity check to confirm we can talk to k8s API
        except ClientError as err:
            return ActionStatusInfo(ActionStatus.ERROR, msg="Kubernetes API Issue: {}".format(err))

        k8s_deployments = self._list_deployments()
        pe_deployments = {}
        data = None
        for di in (DeploymentInfo(deployment) for deployment in self._pe_info.deployments):
            if di.id in k8s_deployments:
                pe_deployments[di.id] = k8s_deployments[di.id]
            else:
                status_msg = "No record of deployment running in Kubernetes."
                pe_deployments[di.id] = ActionStatusInfo(ActionStatus.UNKNOWN, msg=status_msg,
                                                         state=DeploymentState.STOPPED).to_dict()

        expected_vs_reality = set(k8s_deployments) - set(pe_deployments)
        if expected_vs_reality:
            status = ActionStatus.WARN
            status_msg = "Orphaned deployments exist: {}".format(expected_vs_reality)
        else:
            status = ActionStatus.OK
            status_msg = "Cluster is Healthy"
        if bool(pe_deployments):
            data = {ActionDataFields.DEPLOYMENTS_STATUS: pe_deployments}
        return ActionStatusInfo(status, msg=status_msg, data=data)

    def deployment_status(self, deployment_info):
        """
        Return the health status of a MLOps deployment. We rely on the liveness/readiness probes
        setup on the Deployment resource to determine its health. We **do not** send traffic through
        the Ingress.

        The returned ActionStatusInfo can have the following (status, state) values:
            - status=UNKNOWN, state=STOPPED: if the Deployment does not exist in namespace
            - status=ERROR, state=ERROR: if the Deployment has no ready Pods
            - status=WARN, state=READY: if the Deployment has at least one ready Pod but less than
              desired
            - status=OK, state=READY: if the Deployment has all desired Pods ready
        """
        # TODO: we should have an optional status mode that checks health E2E (e.g. through external
        # ingress URL)
        self._logger.debug("Getting status for model deployment")
        di = DeploymentInfo(deployment_info)
        try:
            deployment = self._find_deployment(di)
            return self._deployment_status(deployment)
        except DeploymentNotFound as err:
            return ActionStatusInfo(
                ActionStatus.UNKNOWN,
                msg=str(err),
                state=DeploymentState.STOPPED)

    def deployment_start(self, deployment_info):
        """
        Create a new deployment. This function is idempotent so it can be called on an existing
        deployment (note, a new image will be built but any existing Deployment, Ingress, etc.
        resources will be left as-is).

        The action will wait for at least one replica is reporting ready to serve predictions
        before returning (status=OK, state=READY). Otherwise it will return an (ERROR, ERROR)
        ActionStatus.
        """
        start_time = time.time()
        di = DeploymentInfo(deployment_info)
        # Render the manifests first so we can make sure everything is valid before starting the
        # _long_ image building process. But it doesn't make sense to actually create them in K8s
        # until after we have a successful image build.
        rendered = self._renderer.get_pps_manifest(di)
        rendered["items"].insert(0, self._renderer.get_mlops_secret_manifest(di))

        self._build_pps_image(di)
        try:
            self._logger.info("Creating Prediction Server resources (%s items)",
                              len(rendered["items"]))
            self._client.create_from_dict(rendered)
        except KeyboardInterrupt:
            self._logger.info("shutdown detected while launching resources; rolling back")
            self._client.delete_from_dict(rendered)
            raise
        except ClientErrorList as err:
            if all(e.status == codes.CONFLICT for e in err.api_exceptions):
                # I don't think we want to consider this an error. There is the chance
                # though that the resources exist but aren't correct so maybe we would
                # want to do a PUT/PATCH instead but we can visit that when needed.
                self._logger.warning("some resources already exist: %s", err)
            else:
                # TODO: we should implement the annotation/label transaction marker
                # and get rid of this rollback
                self._logger.info("error while creating resources for deployment; rolling back")
                self._client.delete_from_dict(rendered)
                raise

        data = {
            ActionDataFields.PREDICTION_URL: self._get_prediction_url(di)
        }
        name = self._renderer.helpers.name(di)
        # TODO: use a watcher rather than polling
        # Wait for at least one replica in the Deployment to be ready before returning so we don't
        # cause flapping from the periodic status checks while Pods are starting up. At this point,
        # all resources have been successfully created in K8s so it is just a matter of waiting
        # for it to bring things up.
        self._logger.info("Waiting for at least one Prediction Server replica to become ready...")
        while (time.time() - start_time) < ACTION_TIMEOUT_SECONDS:
            deployment = self._client.get_deployment(name)
            status = self._deployment_status(deployment)
            if status.state == DeploymentState.READY:
                # Always return an OK status here because the launch was successful. A health check
                # make come and set it to WARN if all desired replicas are not ready yet.
                return ActionStatusInfo(ActionStatus.OK, state=DeploymentState.READY,
                                        msg=status.msg, data=data)
            time.sleep(15)
        status_msg = (
            "The deployment has been launched but is taking longer than expected to be ready."
            " We will continue to monitor its status and report any changes. We recommend you"
            " examine the cluster or you can attempt to relaunch the deployment to try again."
        )
        return ActionStatusInfo(ActionStatus.ERROR,
                                state=DeploymentState.ERROR,
                                msg=status_msg,
                                data=data)

    def deployment_stop(self, deployment_data):
        """
        Delete Deployment (and all related) resources from the cluster.
        """
        deployment_id = deployment_data["id"]
        labels = {DEPLOYMENT_LABEL_NAME: deployment_id,
                  PRED_ENV_LABEL_NAME: self._pe_info.id,
                  "app.kubernetes.io/managed-by": "Bosun"}
        selector = make_selector(labels)
        self._logger.info("Deleting all managed resources in K8s for deployment %s...",
                          deployment_id)
        # Ignore auth-errors because we recommend installing this agent in a least privileged manner
        # and this method will attempt to walk the full K8s API which is likely to generate a few
        # permission denied errors that are safe to ignore.
        items = self._client.delete_everything(selector, ignore_auth_errors=True)
        if items:
            self._logger.info("Deleted resources (%s):\n\t%s",
                              len(items),
                              "\n\t".join("Kind: {}; Name: {}".format(i.details.kind,
                                                                      i.details.name)
                                          for i in items))
        return ActionStatusInfo(ActionStatus.OK, state=DeploymentState.STOPPED)

    def deployment_replace_model(self, deployment_info):
        """
        Replace the model of an existing deployment with a new one. Updates are done in a rolling
        fashion to cause minimal service disruption.
        """
        # XXX hack until we cleanup `new_model_id` upstream. K8s is declarative so we don't care
        # about old vs. new model IDs -- just tell us what the end result should be.
        deployment_info["modelId"] = deployment_info.pop("newModelId")
        start_time = time.time()
        di = DeploymentInfo(deployment_info)
        self._build_pps_image(di)

        existing_deployment = self._find_deployment(di)
        name = existing_deployment.metadata.name
        current_model = existing_deployment.metadata.labels[MODEL_LABEL_NAME]

        new_spec = self._renderer.get_deployment_for_update(existing_deployment, di)

        # Until the rollout succeeds, we don't want to advertise that we are running the new
        # model_id as status update will incorrectly tell MLOps that model replacement succeeded.
        new_spec["metadata"]["labels"][MODEL_LABEL_NAME] = current_model
        try:
            self._logger.info("Rolling out new model to Prediction Server: %s", name)
            elapsed = time.time() - start_time
            adjusted_deadline = ACTION_TIMEOUT_SECONDS - elapsed
            self._client.update_deployment(name, new_spec, timeout=adjusted_deadline)
        except (ClientError, TimeoutError) as err:
            # In case of launch failure, k8s did not stop the old container, so indicate
            # that in the status response
            self._logger.exception("Deployment update failed")
            status_msg = "Failed to replace model -\n{}\nContinuing with old model".format(err)
            return ActionStatusInfo(
                ActionStatus.ERROR,
                msg=status_msg,
                state=DeploymentState.ERROR,
                data={ActionDataFields.OLD_MODEL_IN_USE: True},
            )

        # Now that the model update has completed, perform another update with the new label value
        # (this update should be almost instantaneous).
        self._logger.info("Recording that %s is now running model %s", di.id, di.model_id)
        new_spec["metadata"]["labels"][MODEL_LABEL_NAME] = di.model_id
        self._client.update_deployment(name, new_spec, timeout=120)
        return ActionStatusInfo(ActionStatus.OK, msg="Model replaced successfully",
                                state=DeploymentState.READY)

    def _list_deployments(self):
        """
        Fetches all deployments associated with our Prediction Environment. Returns
        a mapping of {deployment_id: ActionStatusInfo}.
        """
        deployments = {}
        # We use a labels to discover all the resources we _own_.
        selector = "{}={}".format(PRED_ENV_LABEL_NAME, self._pe_info.id)
        for item in self._client.get_deployments(selector).items:
            deployment_id = item.metadata.labels[DEPLOYMENT_LABEL_NAME]
            deployments[deployment_id] = self._deployment_status(item).to_dict()
        return deployments

    def _find_deployment(self, di):
        labels = {COMPONENT_LABEL_NAME: "predictionServer",
                  DEPLOYMENT_LABEL_NAME: di.id,
                  PRED_ENV_LABEL_NAME: self._pe_info.id}
        deployments = self._client.get_deployments(make_selector(labels)).items
        if len(deployments) == 1:
            return deployments[0]
        elif len(deployments) == 0:
            raise DeploymentNotFound("No Kubernetes deployment found for: {}".format(di.id))
        else:
            msg = "Got back too many resources associated with deployment {}: {}".format(
                di.id, [i.metadata.name for i in deployments]
            )
            raise RuntimeError(msg)

    def _deployment_status(self, deployment):
        """
        The workhorse of deployment_status(), see semantics of that method for details.
        """
        # For now this is just checking the health of the deployment resource (and assumes all
        # supporting infra such as the Service and Ingress are up and working. This is a good
        # minimum bar because checking the health E2E could end up being blocked by things outside
        # our control:
        #   - no network access to the external endpoint
        #   - the ingress may require auth that we don't have access to
        available_replicas = deployment.status.available_replicas
        requested_replicas = deployment.spec.replicas  # value from .spec is more authoritative

        if not available_replicas:  # API can return 0 or None
            status_msg = "There are no replicas available yet."
            if deployment.status.conditions is not None:
                for condition in deployment.status.conditions:
                    status_msg += " {} reason={} type={} status={}".format(
                        condition.message, condition.reason, condition.type, condition.status)
            return ActionStatusInfo(ActionStatus.ERROR, msg=status_msg, state=DeploymentState.ERROR)

        # We will consider the deployment state still ready if there is at least one replica but it
        # will be a warning if available is less than requested because capacity/redundancy is
        # degraded.
        status = ActionStatus.WARN if available_replicas < requested_replicas else ActionStatus.OK
        status_msg = "{}/{} Pods are ready.".format(available_replicas, requested_replicas)
        current_model_id = deployment.metadata.labels[MODEL_LABEL_NAME]
        return ActionStatusInfo(
            status,
            msg=status_msg,
            state=DeploymentState.READY,
            data={ActionDataFields.CURRENT_MODEL_ID: current_model_id}
        )

    def _get_prediction_url(self, di):
        """
        Based on model type, generate an appropriate URL based on the prefix the user configured.
        """
        if di.model_execution_type == ModelPackageConstants.MODEL_EXECUTION_DEDICATED:
            predict_path = "{}/predictions".format(di.id)
        else:
            predict_path = "{}/predict/".format(di.id)
        return urljoin(self._config.outfacing_prediction_url_prefix, predict_path)

    def _build_pps_image(self, di):
        """
        Build either a custom-model or native PPS image to serve predictions. We use a tool called
        Kaniko which is single use so for every new build request, we launch a new build Pod. The
        is left for K8s to garbage collect it until either the associated deployment in MLOps is
        stopped or a new build request is submitted (in which case we delete and recreate).
        """
        rendered = self._renderer.get_builder_manifest(di)
        try:
            self._start_new_image_builder(di, rendered)
        except ClientError as err:
            # Because of the way we name the image builder pod, we can recover from a conflict: it
            # means that a prior action for this deployment failed or completed successfully. Either
            # way we will simply retry the build.
            if err.status != codes.CONFLICT:
                raise
            # TODO: add optimization to reuse successful pods that match model_id and pps_version
            pod_name = rendered["metadata"]["name"]
            self._logger.info("Cleaning existing pod (%s) and retrying image build", pod_name)
            self._client.delete_pod(pod_name)
            self._start_new_image_builder(di, rendered)

    def _start_new_image_builder(self, di, rendered):
        """
        Starts a Kaniko Pod in a way that this plugin can attach to it and send it the Docker build
        context we generated to build either the Custom Model or the frozen native model + PPS
        environment. This method will wait for Kaniko to finish and raise an error if it failed.
        """
        pod_name = rendered["metadata"]["name"]
        # It is safer to just always cleanup this pod on exit to allow the cluster to reclaim
        # resources.
        start_time = time.time()
        with self._client.run(rendered, cleanup=True) as socket:
            if di.model_execution_type == ModelPackageConstants.MODEL_EXECUTION_DEDICATED:
                self._logger.info("Got a DataRobot Native model to deploy")
                self._send_pps_docker_context(socket, di)
            elif di.model_execution_type == ModelPackageConstants.MODEL_EXECUTION_CUSTOM_INFERENCE:
                self._logger.info("Got a User Custom Inference model to deploy")
                self._send_cm_docker_context(socket, di)
            else:
                msg = "This plugin does not support model of type: {}"
                raise RuntimeError(msg.format(di.model_execution_type))

            self._logger.info("Waiting for image builder to finish...")
            # XXX getting flaky behavior where this hangs indefinitely so only using it if we are
            # in debug mode.
            if self._logger.isEnabledFor(logging.DEBUG):
                # The pod will terminate when done so we can just follow them indefinitely.
                self._client.follow_pod_logs(pod_name,
                                             partial(self._logger.debug, "%s OUTPUT: %s", pod_name))

            elapsed = time.time() - start_time
            adjusted_deadline = IMAGE_BUILD_DEADLINE_SECONDS - elapsed
            self._client.wait_for_pod_completion(pod_name, timeout=adjusted_deadline)

    def _send_pps_docker_context(self, socket, di):
        """
        Build and send a Docker context over the socket that will bake a frozen DataRobot Portable
        Prediction API that includes the deployment's mlpkg ready to serve.
        """
        with TemporaryFile() as buff:
            tar = tarfile.open(mode="w:gz", fileobj=buff)
            self._logger.info("Preparing Docker context for image builder...")
            t = self._renderer.get_template("Dockerfile.pps-model.j2")
            content = t.render(di=di, config=self._config)
            self._logger.debug("Writing Dockerfile:\n%s", content)
            with TemporaryFile() as dockerfile:
                dockerfile.write(content.encode("utf8"))
                dockerfile.seek(0)
                tarinfo = tar.gettarinfo(arcname="Dockerfile", fileobj=dockerfile)
                self._logger.debug("adding to context: %s", tarinfo.get_info())
                tar.addfile(tarinfo, fileobj=dockerfile)
            with open(di.model_artifact, mode="rb") as fh:
                tarinfo = tar.gettarinfo(
                    arcname="model_{}.mlpkg".format(di.model_id), fileobj=fh
                )
                self._logger.debug("adding to context: %s", tarinfo.get_info())
                tar.addfile(tarinfo, fileobj=fh)
            tar.close()

            total_size = buff.tell()
            buff.seek(0)
            _send_chunked_data(socket, buff, total_size)
            socket.close()

    def _send_cm_docker_context(self, socket, di):
        """
        Using the provided install script from the Custom Model model package, build and send a
        Docker context over the socket.
        """
        cm_pps_image_name = "cm_pps_{}".format(di.model_id)
        with TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            try:
                with ZipFile(di.model_artifact, "r") as zip_ref:
                    zip_ref.extractall(tmp_dir)
            except BadZipFile:
                stats = "(file does not exist)"
                with suppress(FileNotFoundError):
                    stats = di.model_artifact.stat()
                    # Move to a place that hopefully won't get cleaned up right away. Only keep
                    # one instance of a corrupted package for now so we don't fill up the
                    # container with junk.
                    di.model_artifact.rename("/tmp/corrupt.mlpkg")
                self._logger.exception("%s looks to be corrupt: %s", di.model_artifact, stats)
                msg = "The model package was corrupted during transfer; please try again."
                raise RuntimeError(msg) from None

            installer = tmp_dir / "cm_pps_installer.sh"

            # Old versions of .mlpkg files need to have their installer script updated
            if not installer.exists() or not _can_output_docker_context(installer):
                t = self._renderer.get_template("cm_pps_installer.sh.j2")
                script = t.render(cm_pps_image_name=cm_pps_image_name)
                self._logger.debug("Replacing installer script with new version:\n%s", script)
                with open(installer, "w") as fp:
                    fp.write(script)

            cmd = ["bash", str(installer), "--skip-agent-install", "--output-docker-context"]
            try:
                output = subprocess.check_output(cmd, cwd=tmp_dir, stderr=subprocess.STDOUT)
                self._logger.debug("Built Custom Model docker context: %s", output.decode("utf8"))
            except subprocess.CalledProcessError as err:
                # Log command output here because top-level exception handler will not
                self._logger.error("cm_pps_installer.sh OUTPUT: %s", err.stdout.decode("utf8"))
                raise

            docker_context = tmp_dir / (cm_pps_image_name + "-context.tar.gz")
            total_size = docker_context.stat().st_size
            with open(docker_context, "rb") as fp:
                _send_chunked_data(socket, fp, total_size)
            socket.close()


def _can_output_docker_context(installer):
    """
    Helper script to deal with old Custom Model mlpkg files that don't contain a modern install
    script needed by this plugin.
    """
    output = subprocess.check_output(["bash", str(installer), "--help"], cwd=installer.parent,
                                     stderr=subprocess.STDOUT).decode("utf8")
    return "--output-docker-context" in output


def _send_chunked_data(socket, fp, total_size, chunk_size=5*MB):
    """
    Streams data to socket in managable chunks.
    """
    logger.info("Sending %s bytes to image builder...", total_size)
    since_last_status = time.time()
    size_sent = 0
    for chunk in iter(partial(fp.read, chunk_size), b""):
        # Make sure to give the user a status update every so often
        if (time.time() - since_last_status) > 29:
            uploaded_pct = int(size_sent / total_size * 100)
            logger.debug("Uploaded %s%%...", uploaded_pct)
            since_last_status = time.time()
        socket.write_stdin(chunk)
        size_sent += len(chunk)
    logger.info("Uploaded 100%...")

#  --------------------------------------------------------------------------------
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2022.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#
#  --------------------------------------------------------------------------------

import datetime
import glob
import json
import logging
import os
import time

import yaml

from bosun.plugin.action_status import ActionStatus, ActionStatusInfo, ActionDataFields
from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.constants import DeploymentState
from bosun.plugin.deployment_info import DeploymentInfo


class BosunTestPugin(BosunPluginBase):
    """
    A test plugin. This plugin is used to test Bosun agent behaviour. This plugin is not running
    any "real" action, but will call time.sleep instead and will print some information about the
    action being called into the logs.
    """
    CONFIG_FILE_ENTRY = "config_file"

    def __init__(self, plugin_config: object, private_config_file: str,
                 pe_info: object, dry_run: bool) -> object:
        super().__init__(plugin_config, private_config_file, pe_info, False)
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug("plugin config: {}".format(self.get_sanitized_config(plugin_config)))

        # The plugin config dictionary can contain a pointer to a private config file for this
        # specific plugin script. So we can get specific config in any format known only to this
        # implementation of the plugin.
        if private_config_file:
            with open(private_config_file) as config_fh:
                private_config = json.load(config_fh)
        else:
            private_config = {}

        self._launch_time_sec = private_config.get("launch_time_sec", 10)
        self._stop_time_sec = private_config.get("stop_time_sec", 8)
        self._replace_model_time = private_config.get("replace_model_time_sec", 10)
        self._pe_status_time = private_config.get("pe_status_time_sec", 3)
        self._deployment_status_time = private_config.get("deployment_status_time_sec", 2)
        self._deployment_list_time = private_config.get("deployment_list_time_sec", 2)
        self._raise_exception = private_config.get("raise_exception", False)
        self._plugin_start_time = private_config.get("plugin_start_time", 5)
        self._plugin_stop_time = private_config.get("plugin_stop_time", 5)
        self._plugin_tmp_dir = private_config.get("tmp_dir", "/tmp")

    def _raise_exception_if_set(self):
        if self._raise_exception:
            raise Exception("Bosun Test plugin is raising an exception")

    def _get_pe_filename(self):
        return os.path.join(
            self._plugin_tmp_dir, "pe_" + self._plugin_config["MLOPS_BOSUN_PRED_ENV_ID"] + ".yaml"
        )

    def _get_deployment_filename(self, deployment_info):
        return self._get_deployment_filename_from_id(deployment_info["id"])

    def _get_deployment_filename_from_id(self, deployment_id):
        return os.path.join(self._plugin_tmp_dir, "deployment_" + deployment_id + ".yaml")

    @staticmethod
    def _get_deployment_content(deployment_info):
        content = {
            "name": deployment_info["name"],
            "model_id": deployment_info["modelId"],
            "key_value_config": deployment_info["keyValueConfig"],
            "model_execution_type": deployment_info["modelExecutionType"],
            "model_artifact": deployment_info["modelArtifact"],
            "state": "running",
        }
        if "newModelId" in deployment_info:
            content["new_model_id"] = deployment_info["newModelId"]
        return content

    def plugin_start(self):
        self._logger.info("Plugin start for Test plugin- nothing to do")
        self._raise_exception_if_set()
        time.sleep(self._plugin_start_time)
        self._logger.info("Done plugin start for Test plugin")
        with open(self._get_pe_filename(), "w") as pe:
            pe.write(yaml.safe_dump({"state": "running"}))
        return ActionStatusInfo(ActionStatus.OK)

    def plugin_stop(self):
        self._logger.info("Plugin stop for Test plugin")
        self._raise_exception_if_set()
        time.sleep(self._plugin_stop_time)
        self._logger.info("Done plugin stop for Test plugin")
        pe_file = self._get_pe_filename()
        if os.path.exists(pe_file):
            os.remove(pe_file)
        return ActionStatusInfo(ActionStatus.OK)

    def deployment_start(self, deployment_info):
        """
        Add a cron job per deployment
        :return:
        """
        self._logger.info("start deployment_launch")
        self._raise_exception_if_set()
        time.sleep(self._launch_time_sec)
        with open(self._get_deployment_filename(deployment_info), "w") as deployment_file:
            content = self._get_deployment_content(deployment_info)
            deployment_file.write(yaml.safe_dump(content))

        self._logger.info("done  deployment_launch")
        return ActionStatusInfo(ActionStatus.OK, msg="Launch successful", state="ready")

    def deployment_stop(self, deployment_data):
        """
        Stop the cron job and delete it
        :return:
        """
        self._logger.info("start deployment_stop")
        self._raise_exception_if_set()
        deployment_path = self._get_deployment_filename_from_id(deployment_data["id"])
        if os.path.exists(deployment_path):
            os.remove(deployment_path)

        time.sleep(self._stop_time_sec)
        self._logger.info("done  deployment_stop")
        return ActionStatusInfo(ActionStatus.OK, msg="Stop Successful", state="stopped")

    def deployment_replace_model(self, deployment_info):
        """
        Will put a model artifact in a place the cronjob can consume it
        :param deployment_info: Info about the deployment
        :param model_artifact_path:
        :return:
        """
        model_artifact_path = deployment_info["modelArtifact"]
        self._logger.info("start replacing model: {}".format(model_artifact_path))
        time.sleep(self._replace_model_time)
        deployment_path = self._get_deployment_filename(deployment_info)
        try:
            self._raise_exception_if_set()
            with open(deployment_path, "w") as deployment_file:
                content = self._get_deployment_content(deployment_info)
                if "new_model_id" in content:
                    content["model_id"] = content["new_model_id"]
                deployment_file.write(yaml.safe_dump(content))
        except Exception as ex:
            if os.path.exists(deployment_path):
                with open(deployment_path, "r") as deployment_file:
                    content = yaml.safe_load(deployment_file.read())
                    if content["model_id"] != deployment_info["modelId"]:
                        return ActionStatusInfo(
                            ActionStatus.ERROR,
                            msg="Failed to replace model, continuing with old one",
                            state=DeploymentState.ERROR,
                            data={ActionDataFields.OLD_MODEL_IN_USE: True},
                        )
                    else:
                        raise ex

        self._logger.info("done  replacing model: {}".format(model_artifact_path))
        return ActionStatusInfo(ActionStatus.OK, msg="Model replaced successfully Path: {}".format(
            model_artifact_path), state="ready")

    def pe_status(self):
        """
        Do status check
        :return:
        """
        self._logger.info("start pe_status")
        self._raise_exception_if_set()
        time.sleep(self._pe_status_time)
        pe_file = self._get_pe_filename()
        if os.path.exists(pe_file):
            with open(pe_file, "r+") as pe_file:
                content = yaml.safe_load(pe_file.read())
                content["status_timestamp"] = datetime.datetime.utcnow().isoformat()
                pe_file.seek(0)
                pe_file.write(yaml.safe_dump(content))
                pe_file.truncate()

            all_deployments_status = {}

            print(self._pe_info)
            for deployment in self._pe_info.deployments:
                di = DeploymentInfo(deployment)
                self._logger.info("Checking status of deployment: {}".format(di.id))
                deployment_status = self._deployment_status(di.id)
                self._logger.info(deployment_status)
                all_deployments_status[di.id] = deployment_status.to_dict()
            data = {
                ActionDataFields.DEPLOYMENTS_STATUS: all_deployments_status
            }
            action_status = ActionStatusInfo(ActionStatus.OK,
                                             msg="PE Health looks awesome",
                                             data=data)

        else:
            action_status = ActionStatusInfo(ActionStatus.ERROR, msg="PE not found")
        self._logger.info("done  pe_status: {}".format(action_status))
        return action_status

    def deployment_status(self, deployment_info):
        """
        :param deployment_info: Info about the deployment to check
        Do status check
        :return:
        """
        self._logger.info("start deployment_status")
        self._raise_exception_if_set()
        time.sleep(self._deployment_status_time)
        di = DeploymentInfo(deployment_info)
        return self._deployment_status(di.id)

    def _deployment_status(self, deployment_id):
        deployment_path = self._get_deployment_filename_from_id(deployment_id)
        if os.path.exists(deployment_path):
            with open(deployment_path, "r+") as deployment_file:
                content = yaml.safe_load(deployment_file.read())
                content["status_timestamp"] = datetime.datetime.utcnow().isoformat()
                deployment_file.seek(0)
                deployment_file.write(yaml.safe_dump(content))
                deployment_file.truncate()
                action_status = ActionStatusInfo(
                    ActionStatus.OK,
                    msg="Deployment health looks good",
                    state="ready",
                    data={ActionDataFields.CURRENT_MODEL_ID: content["model_id"]}
                )
        else:
            action_status = ActionStatusInfo(
                ActionStatus.ERROR, msg="Deployment not found", state="errored"
            )
        self._logger.info("done deployment_status")
        return action_status

    def deployment_list(self):
        """
        Get the list of running deployments
        :return:
        """
        self._logger.info("start deployment list")
        self._raise_exception_if_set()
        time.sleep(self._deployment_list_time)
        current_deployment_files = glob.glob(os.path.join("/tmp", "deployment_*.yaml"))

        deployments_map = {}
        for file in current_deployment_files:
            deployment_id = os.path.basename(file).split("_")[1].split(".")[0]
            with open(file, "r") as f:
                deployment_info = yaml.safe_load(f.read())
                deployments_map[deployment_id] = deployment_info

        return ActionStatusInfo(ActionStatus.OK, msg="Deployment list", data=deployments_map)

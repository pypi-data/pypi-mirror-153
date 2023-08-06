
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

from abc import ABC, abstractmethod
import datetime

import pytz
import yaml

from bosun.model_connector.constants import ModelPackageConstants, ModelConnectorConstants


class ActionStatus:
    OK = "passing"
    WARN = "warning"
    ERROR = "failing"

    @classmethod
    def is_valid(self, status_string):
        if status_string in (ActionStatus.OK, ActionStatus.WARN, ActionStatus.ERROR):
            return True
        return False


class ActionStatusInfo:
    def __init__(self, status, model_path=None, msg=None, duration=None):
        if ActionStatus.is_valid(status):
            self.status = status
        else:
            raise Exception("Bad Status: {}".format(status))
        self.msg = msg
        self.duration = duration
        d = datetime.datetime.utcnow()
        d_with_timezone = d.replace(tzinfo=pytz.UTC)
        d_with_timezone.isoformat()
        self.timestamp = str(d_with_timezone)

        self.model_path = model_path

    def to_yaml(self):
        return yaml.dump(self.__dict__, indent=4)


def find_or_throw(info, item, parent_item):
    if item in info:
        return info[item]

    err_msg = "Could not find {} in {} information".format(item, parent_item)
    raise Exception(err_msg)


class ModelPackage:
    def __init__(self, info):
        self._info = info

        self.model_id = find_or_throw(info,
                                      ModelPackageConstants.MODEL_ID_KEY,
                                      ModelPackageConstants.MODEL_PACKAGE_KEY)

        self.model_execution_type = find_or_throw(info,
                                                  ModelPackageConstants.MODEL_EXECUTION_TYPE_KEY,
                                                  ModelPackageConstants.MODEL_PACKAGE_KEY)

        self.model_format = None
        if ModelPackageConstants.MODEL_FORMAT_KEY in info:
            self.model_format = info[ModelPackageConstants.MODEL_FORMAT_KEY]

        description = find_or_throw(info,
                                    ModelPackageConstants.MODEL_DESCRIPTION_KEY,
                                    ModelPackageConstants.MODEL_PACKAGE_KEY)

        self.location = find_or_throw(description,
                                      ModelPackageConstants.MODEL_LOCATION_KEY,
                                      ModelPackageConstants.MODEL_DESCRIPTION_KEY)

    def __str__(self):
        return "model_id: {} execution_type: {} location: {}".format(
            self.model_id, self.model_execution_type, self.location)

    def to_yaml(self):
        content = {
            "model_id": self.model_id,
            "deployment_id": self.deployment_id,
            "model_execution_type": self.model_execution_type,
            "location": self.location,
        }
        return yaml.safe_dump(content)


class ModelConnectorConfig:
    def __init__(self, config):
        self._config = config.copy()

        self.tmp_dir = find_or_throw(config, ModelConnectorConstants.TMP_DIR_KEY,
                                     ModelConnectorConstants.MODEL_CONNECTOR_CONFIG_KEY)
        self.dr_url = find_or_throw(config, ModelConnectorConstants.DR_URL_KEY,
                                    ModelConnectorConstants.MODEL_CONNECTOR_CONFIG_KEY)
        self.dr_token = find_or_throw(config, ModelConnectorConstants.DR_TOKEN_KEY,
                                      ModelConnectorConstants.MODEL_CONNECTOR_CONFIG_KEY)

    def set_output_dir(self, output_dir):
        self.tmp_dir = output_dir

    def set_mlops_url(self, url):
        self.dr_url = url

    def set_mlops_token(self, token):
        self.dr_token = token

    def __str__(self):
        return "tmp_dir: {} url: {} token: {}".format(self.tmp_dir, self.dr_url, self.dr_token[-4:])


class ModelConnectorBase(ABC):
    def __init__(self, config, logger):
        """
        The base class constructor.
        :param config:  The plugin config dict
        :param logger: The logger
        """
        self._config = config
        self._logger = logger

    @abstractmethod
    def get_model(self, model_package):
        pass

    def run_action(self, action, config):

        try:
            if action == "get_model":
                action_status = self.get_model(config)

                if action_status.model_path is None:
                    raise Exception("get_model operation should return a model_path "
                                    "field in status")

            else:
                raise Exception("Action is not supported: {}".format(action))
            if not isinstance(action_status, ActionStatusInfo):
                raise Exception("Action {} provide - did not return ActionStatusInfo object"
                                .format(action))
        except Exception as e:
            msg = "Exception occurred while running action {} : error {}".format(action, e)
            self._logger.error(msg)
            action_status = ActionStatusInfo(ActionStatus.ERROR, msg=msg)

        return action_status

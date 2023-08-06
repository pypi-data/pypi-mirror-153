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

import logging
import time
import traceback
from abc import ABC, abstractmethod

from bosun.plugin.action_status import ActionStatus, ActionStatusInfo
from bosun.plugin.constants import BosunPluginActions, BosunPluginConfigConstants
from bosun.plugin.pe_info import PEInfo


class BosunPluginBase(ABC):
    def __init__(self, plugin_config, private_config_file, pe_info, dry_run):
        """
        The baseclass constructor.
        :param plugin_config:  The plugin config dict
        :param pe_info: The PE info dict
        """
        self._plugin_config = plugin_config
        self._private_config_file = private_config_file
        if pe_info:
            self._pe_info = PEInfo(pe_info)
        else:
            self._pe_info = pe_info
        self._logger = logging.getLogger("{}.{}".format(self.__class__.__module__,
                                                        self.__class__.__name__))
        self._dry_run = dry_run

    @abstractmethod
    def plugin_start(self):
        pass

    @abstractmethod
    def plugin_stop(self):
        pass

    @abstractmethod
    def deployment_list(self):
        pass

    @abstractmethod
    def deployment_start(self, deployment_info):
        pass

    @abstractmethod
    def deployment_stop(self, deployment_info):
        pass

    @abstractmethod
    def deployment_replace_model(self, deployment_info):
        pass

    @abstractmethod
    def pe_status(self):
        """
        Check status of PE - possibly also reporting status on each deployment in this pe.
        :return:
        """
        pass

    @abstractmethod
    def deployment_status(self, deployment_info):
        pass

    def deployment_relaunch(self, deployment_info):
        """
        Default relaunch implementation for now is "stop" + "start", but if any plugin
        wants to implement a different logic, it should implement its own relaunch mechanism

        :param deployment_info:
        :return:
        """
        self._logger.info("Processing deployment relaunch")
        status = self.deployment_stop(deployment_info)
        self._logger.info("Deployment stop status: {}".format(status))
        # Default processing ignores any stop errors, because deployment is going to be launched
        # again soon.  But, if plugin wants to handle the stop error, then it will need its own
        # deployment_relaunch implementation
        return self.deployment_start(deployment_info)

    def run_action(self, action, deployment_info, status_file=None):

        action_start = time.time()
        try:

            if action == BosunPluginActions.PLUGIN_START:
                action_status = self.plugin_start()
            elif action == BosunPluginActions.PLUGIN_STOP:
                action_status = self.plugin_stop()
            elif action == BosunPluginActions.DEPLOYMENT_START:
                action_status = self.deployment_start(deployment_info)
            elif action == BosunPluginActions.DEPLOYMENT_STOP:
                action_status = self.deployment_stop(deployment_info)
            elif action == BosunPluginActions.DEPLOYMENT_REPLACE_MODEL:
                action_status = self.deployment_replace_model(deployment_info)
            elif action == BosunPluginActions.DEPLOYMENT_STATUS:
                action_status = self.deployment_status(deployment_info)
            elif action == BosunPluginActions.PE_STATUS:
                action_status = self.pe_status()
            elif action == BosunPluginActions.DEPLOYMENT_LIST:
                action_status = self.deployment_list()
            elif action == BosunPluginActions.DEPLOYMENT_RELAUNCH:
                action_status = self.deployment_relaunch(deployment_info)
            else:
                raise Exception("Action is not supported: {}".format(action))
            if not isinstance(action_status, ActionStatusInfo):
                raise Exception("Action {} provide - did not return ActionStatusInfo object"
                                .format(action))
        except Exception as e:
            msg = "Exception occurred while running action {} : error {}".format(action, e)
            self._logger.error(msg)
            traceback.print_exc()
            action_status = ActionStatusInfo(ActionStatus.ERROR, msg=msg, state="errored")

        action_end = time.time()
        action_status.set_duration(round(action_end - action_start, 4))
        action_status.write_to_file(status_file=status_file)

        return action_status

    @staticmethod
    def get_sanitized_config(parsed_config):
        sanitized = parsed_config.copy()
        if BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY in sanitized:
            masked = sanitized[BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY][:12] + "*******"
            sanitized[BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY] = masked
        return sanitized

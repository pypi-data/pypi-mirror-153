
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

import argparse
import logging
import os
from pprint import pformat
import sys

import yaml

from bosun.model_connector.constants import ModelConnectorConstants
from bosun.model_connector.mc_bosun import MCBosun
from bosun.model_connector.model_connector_base import ActionStatusInfo, ActionStatus


class MCRunner:
    MODEL_CONFIG_TEMPLATE = {
        "scratchDir": "/tmp/models",
        "datarobotUrl": "https://app.datarobot.com",
        "name": "train_1 (v1.0)",
        "modelId": "5eaa29d511bf057c2147fe6d",
        "id": "5eaa29d511bf057c2147fe6d",
        "modelExecutionType": "external",
        "location": "file:///opt/model/my_model.zip"
    }

    def __init__(self, config_file, action, status_file):
        self._logger = logging.getLogger("{}.{}".format(self.__class__.__module__,
                                                        self.__class__.__name__))
        self._config_file = config_file
        self._action = action
        self._status_file = status_file

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()

        parser.add_argument("--logfile", default=None, help="Path to log file")
        parser.add_argument("--log-level",
                            default="INFO",
                            type=str.upper,
                            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                            help="Set the logging level")
        parser.add_argument("--gen-config", action="store_true", default=False,
                            help="Generate a sample configuration")
        parser.add_argument("--config", help="Configuration file to use")
        parser.add_argument("--action", help="Action to perform")
        parser.add_argument("--status-file", help="Where to write status JSON")
        parser.add_argument("--show-status", action="store_true",
                            help="Print status file at end of run")

        options = parser.parse_args()
        if options.gen_config is False and (
                options.config is None or options.action is None or options.status_file is None):
            print("Error: arguments --config --action --status-file are required")
            sys.exit(1)

        return options

    @staticmethod
    def get_config(config_file, logger):
        with open(config_file) as config_fh:
            config = yaml.safe_load(config_fh)
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(pformat(MCBosun.get_sanitized_config(config)))
            # Getting the DataRobot token from the environment and adding it to the config
            if ModelConnectorConstants.DR_TOKEN_ENV not in os.environ:
                raise Exception("Error: Could not find {} in environment".format(
                    ModelConnectorConstants.DR_TOKEN_ENV))
            config[ModelConnectorConstants.DR_TOKEN_KEY] = os.environ[
                ModelConnectorConstants.DR_TOKEN_ENV
            ]
            return config

    def run(self):
        logger = logging.getLogger("main")

        try:
            config = self.get_config(self._config_file, logger)
            mc = MCBosun(config)
            action_status = mc.run_action(self._action, config)
        except Exception as e:
            msg = "Exception occurred while running action {} : error {}".format(self._action, e)
            self._logger.exception(msg)
            action_status = ActionStatusInfo(ActionStatus.ERROR, msg=msg)

        if self._status_file:
            with open(self._status_file, "w") as status_fh:
                status_fh.write(action_status.to_yaml())


def main():
    options = MCRunner.parse_args()

    logging.root.setLevel(options.log_level)

    if options.logfile:
        handler = logging.FileHandler(options.logfile)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(options.log_level)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s %(message)s")
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)

    if options.gen_config:
        print("# The following is an example of a config file for the model connector runner")
        print("")
        print(yaml.dump(MCRunner.MODEL_CONFIG_TEMPLATE, indent=4))
    else:
        MCRunner(config_file=options.config, action=options.action,
                 status_file=options.status_file).run()
        if options.show_status:
            with open(options.status_file) as sf:
                status_str = sf.read(4096)
                print("\n-- action status --")
                print(status_str)


if __name__ == "__main__":
    main()

#  --------------------------------------------------------------------------------
#  Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
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

import time

import yaml


class ActionDataFields:
    """
    Name of additional fields that the plugin can create inside the data section of the
    ActionStatus Info YAML Bosun will read.
    """
    PREDICTION_URL = "predictionUrl"
    OLD_MODEL_IN_USE = "oldModelInUse"
    DEPLOYMENTS_STATUS = "deploymentsStatus"
    CURRENT_MODEL_ID = "currentModelId"


class ActionStatus:
    OK = "passing"
    WARN = "warning"
    ERROR = "failing"
    UNKNOWN = "unknown"

    to_numeric = {
       OK: 0,
       ERROR: 1,
       WARN: 2,
       UNKNOWN: 3,
    }

    @classmethod
    def is_valid(self, status_string):
        if status_string in (
                ActionStatus.OK, ActionStatus.WARN, ActionStatus.ERROR, ActionStatus.UNKNOWN):
            return True
        return False


class ActionStatusInfo:
    def __init__(self, status, msg=None, state=None, duration=None, data=None):
        if ActionStatus.is_valid(status):
            self.status = status
        else:
            raise Exception("Bad Status: {}".format(status))
        self.msg = msg
        self.duration = duration
        self.timestamp = int(time.time() * 1000)
        self.state = state
        self.data = data

    def set_duration(self, duration):
        self.duration = duration

    def to_yaml(self):
        return yaml.safe_dump(self.__dict__, indent=4)

    def to_dict(self):
        return self.__dict__.copy()

    def __str__(self):
        return self.to_yaml()

    def write_to_file(self, status_file=None):
        if status_file:
            with open(status_file, "w") as status_fh:
                status_fh.write(self.to_yaml())

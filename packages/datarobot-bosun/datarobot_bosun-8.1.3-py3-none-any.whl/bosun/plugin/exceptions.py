#  --------------------------------------------------------------------------------
#  Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2021.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#
#  --------------------------------------------------------------------------------

class DeploymentException(Exception):
    """
    Indicates an exception during deployment actions like launch, stop
    """
    def __init__(self, exception, msg):
        self.exception = exception
        self.msg = msg


class DeploymentLaunchException(DeploymentException):
    """
    Indicates exception during deployment launch
    """


class DeploymentStopException(DeploymentException):
    """
    Indicates exception during deployment stop
    """

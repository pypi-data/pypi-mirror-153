#  --------------------------------------------------------------------------------
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
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

class BosunPluginActions:
    PLUGIN_START = "plugin_start"
    PLUGIN_STOP = "plugin_stop"
    DEPLOYMENT_START = "deployment_start"
    DEPLOYMENT_STOP = "deployment_stop"
    DEPLOYMENT_REPLACE_MODEL = "deployment_replace_model"
    DEPLOYMENT_STATUS = "deployment_status"
    PE_STATUS = "pe_status"
    DEPLOYMENT_LIST = "deployment_list"
    DEPLOYMENT_RELAUNCH = "deployment_relaunch"

    @staticmethod
    def all_actions():
        return [value for name, value in vars(BosunPluginActions).items() if
                not name.startswith(
                    "_") and name != "all_actions" and name != "require_deployment_info"]

    @staticmethod
    def require_deployment_info():
        return [BosunPluginActions.DEPLOYMENT_START,
                BosunPluginActions.DEPLOYMENT_STATUS,
                BosunPluginActions.DEPLOYMENT_STOP,
                BosunPluginActions.DEPLOYMENT_REPLACE_MODEL]


class BosunPluginConfigConstants:
    PLUGIN_CONFIG_KEY = "pluginConfig"
    MLOPS_URL_KEY = "MLOPS_BOSUN_MONITORING_URL"
    MLOPS_API_TOKEN_ENV = "MLOPS_API_TOKEN"
    MLOPS_API_TOKEN_KEY = "mlopsApiToken"

    MLOPS_BOSUN_PRED_ENV_TYPE_KEY = "MLOPS_BOSUN_PRED_ENV_TYPE"
    MLOPS_BOSUN_PRED_ENV_PLATFORM_KEY = "MLOPS_BOSUN_PRED_ENV_PLATFORM"
    MLOPS_BOSUN_PRED_ENV_ID_KEY = "MLOPS_BOSUN_PRED_ENV_ID"
    MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING_KEY = "MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING"
    COMMAND_KEY = "command"


class PeInfoConfigConstants:
    PE_INFO_KEY = "peInfo"


class DeploymentInfoConfigConstants:
    DEPLOYMENT_INFO_KEY = "deploymentInfo"
    MODEL_FORMAT_MLPKG = "datarobot"
    MODEL_FORMAT_SCORING_CODE = "datarobotScoringCode"

    @staticmethod
    def model_artifact_suffix(model_format):
        model_suffix_for_format = {
            DeploymentInfoConfigConstants.MODEL_FORMAT_MLPKG: "mlpkg",
            DeploymentInfoConfigConstants.MODEL_FORMAT_SCORING_CODE: "jar",
        }
        return model_suffix_for_format.get(model_format, "")


class DeploymentState:
    READY = "ready"
    STOPPED = "stopped"
    ERROR = "errored"


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


class ModelConnectorConstants:
    MODEL_CONNECTOR_CONFIG_KEY = "modelConnectorConfig"
    TMP_DIR_KEY = "scratchDir"
    DR_URL_KEY = "mlopsUrl"
    DR_TOKEN_ENV = "MLOPS_API_TOKEN"
    DR_TOKEN_KEY = "mlopsApiToken"


class ModelPackageConstants:

    MODEL_PACKAGE_ID_KEY = "id"
    MODEL_CONNECTOR_CONFIG_KEY = "modelConnectorConfig"
    MODEL_PACKAGE_KEY = "modelPackage"
    MODEL_NAME_KEY = "name"
    MODEL_ID_KEY = "modelId"
    MODEL_EXECUTION_TYPE_KEY = "modelExecutionType"
    MODEL_EXECUTION_DEDICATED = "dedicated"
    MODEL_EXECUTION_CUSTOM_INFERENCE = "custom_inference_model"
    MODEL_EXECUTION_EXTERNAL = "external"

    MODEL_FORMAT_KEY = "modelFormat"
    MODEL_FORMAT_MLPKG = "datarobot"
    MODEL_FORMAT_SCORING_CODE = "datarobotScoringCode"

    MODEL_DESCRIPTION_KEY = "modelDescription"
    MODEL_LOCATION_KEY = "location"

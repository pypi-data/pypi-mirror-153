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

from pathlib import Path

from schema import Schema, And, Use, Optional, Or
import yaml


class DeploymentInfo:
    """
    A wrapper for the deployment info dict (from the deployment info YAML)
    """
    BASE_IMAGE_KEY = "baseImage"

    # TODO: the kev_value_config should be all optional and validated by the specific plugin
    def __init__(self, deployment_info):
        schema = Schema({
            "id": And(str, len),
            "modelId": And(str, len),
            "modelExecutionType": And(str, len),
            Optional("keyValueConfig", default={}): dict,
            Optional("name"): str,
            Optional("description"): Or(None, str),
            Optional("modelArtifact"): Or(None, And(str, len, Use(Path))),
            Optional("modelFormat"): Or(None, str),
            Optional("newModelId"): And(str, len),
        }, ignore_extra_keys=True)

        self._deployment_info = schema.validate(deployment_info)

    def to_yaml(self):
        tmp = self._deployment_info.copy()
        if "modelArtifact" in tmp:
            # convert Path to str if present in the data
            tmp["modelArtifact"] = str(tmp["modelArtifact"])
        return yaml.safe_dump(tmp, indent=4)

    def __str__(self):
        return self.to_yaml()

    @property
    def id(self):
        return self._deployment_info["id"]

    @property
    def name(self):
        return self._deployment_info.get("name")

    @property
    def description(self):
        return self._deployment_info.get("description")

    @property
    def model_id(self):
        return self._deployment_info["modelId"]

    @property
    def model_artifact(self):
        return self._deployment_info.get("modelArtifact")

    @property
    def model_format(self):
        return self._deployment_info.get("modelFormat")

    @property
    def model_execution_type(self):
        return self._deployment_info["modelExecutionType"]

    @property
    def kv_config(self):
        return self._deployment_info["keyValueConfig"]

    @property
    def new_model_id(self):
        return self._deployment_info.get("newModelId")

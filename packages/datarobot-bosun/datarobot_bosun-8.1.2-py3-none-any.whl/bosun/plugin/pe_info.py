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

import dateutil.parser
from schema import Schema, And, Optional, Or, Use
import yaml


class PEInfo:
    """
    A wrapper for the PE info dict (from the PE info YAML)
    """
    def __init__(self, pe_info):
        schema = Schema({
            Optional("name"): str,
            "id": And(str, len),
            Optional("description"): Or(None, str),
            Optional("createdOn"): Or(None, Use(dateutil.parser.isoparse)),
            Optional("createdBy"): Or(None, str),
            Optional("deployments"): list,
            Optional("keyValueConfig"): dict
        }, ignore_extra_keys=True)

        self._pe_info = schema.validate(pe_info)

    def to_yaml(self):
        return yaml.safe_dump(self._pe_info, indent=4)

    def __str__(self):
        return self.to_yaml()

    @property
    def id(self):
        return self._pe_info["id"]

    @property
    def name(self):
        return self._pe_info.get("name")

    @property
    def description(self):
        return self._pe_info.get("description")

    @property
    def deployments(self):
        return self._pe_info.get("deployments")

    @property
    def created_on(self):
        return self._pe_info.get("createdOn")

    @property
    def created_by(self):
        return self._pe_info.get("createdBy")

    @property
    def kv_config(self):
        return self._deployment_info.get("keyValueConfig")

#  ---------------------------------------------------------------------------------
#  Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2022.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#  ---------------------------------------------------------------------------------

import logging

from bosun.plugin.constants import BosunPluginConfigConstants


class S3PluginConfig:
    BUCKET_NAME_KEY = "bucketName"
    BASE_DIR_KEY = "baseDir"
    DEPLOYMENT_DIR_PREFIX_KEY = "deploymentDirPrefix"
    DEPLOYMENT_INFO_FILE = "deploymentInfoFile"

    def __init__(self, plugin_config):
        log = logging.getLogger("{}.{}".format(self.__class__.__module__, self.__class__.__name__))
        self._config = plugin_config

        schema = {
            S3PluginConfig.BUCKET_NAME_KEY: str,
            S3PluginConfig.BASE_DIR_KEY: str,
            S3PluginConfig.DEPLOYMENT_DIR_PREFIX_KEY: str,
            S3PluginConfig.DEPLOYMENT_INFO_FILE: str,
            BosunPluginConfigConstants.MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING_KEY: bool,
        }
        for f in schema:
            if f not in self._config:
                raise Exception("Field {} is missing in plugin config {}".format(f, self._config))

            log.debug("self._config[f]: {} {}".format(self._config[f], type(self._config[f])))
            if type(self._config[f]) != schema[f]:
                raise Exception("Field {} type: {} is not as expected: {}"
                                .format(f, type(self._config[f]), schema[f]))

        if self._config[BosunPluginConfigConstants.MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING_KEY]:
            log.warn("Model monitoring is enabled for this PE but ignored by this plugin")

    @property
    def datarobot_app_url(self):
        return self._config[BosunPluginConfigConstants.MLOPS_URL_KEY]

    @property
    def datarobot_api_key(self):
        return self._config[BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY]

    @property
    def bucket_name(self):
        return self._config[S3PluginConfig.BUCKET_NAME_KEY]

    @property
    def base_dir(self):
        return self._config[S3PluginConfig.BASE_DIR_KEY]

    @property
    def deployment_dir_prefix(self):
        return self._config[S3PluginConfig.DEPLOYMENT_DIR_PREFIX_KEY]

    @property
    def deployment_info_file(self):
        return self._config[S3PluginConfig.DEPLOYMENT_INFO_FILE]

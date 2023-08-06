
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
from urllib.parse import urlparse

from bosun.model_connector.constants import ModelConnectorConstants, ModelPackageConstants
from bosun.model_connector.file_uri_fetcher import FileURIFetcher
from bosun.model_connector.model_connector_base import ModelConnectorBase, ActionStatus, \
    ActionStatusInfo

# TODO: Fix logging issue - no logs when running in cmdline
# TODO: Live status update on the status file
# TODO: list available actions
# TODO: print stack trace when error happens inside the mc
# TODO: move to something nicer using schema
# from bosun.model_connector.mc_config import MCConfig
# from bosun.model_connector.model_info import ModelInfo

from datarobot.mlops.connected.client import MLOpsClient


# TODO: move operations to be constants
#
# TODO: Download DR model
# TODO: implement a local cache if the model already exists then do not download
# TODO: CM can be downloaded via API so this can be a good starting point

# TODO: Add a structure for parsing the location and adding parser per location prefix
# TODO: Add file:// parsing support to external type models
# TODO: Add s3:// parsing support to external type models
# TODO: add git:// parsing support to external type models


class MCBosun(ModelConnectorBase):
    def __init__(self, config):
        """
        The base class constructor.
        :type config: configuration dictionary
        :param config: The plugin config dict
        """
        super().__init__(config, logging.getLogger("{}.{}".format(self.__class__.__module__,
                                                                  self.__class__.__name__)))
        file_fetcher = FileURIFetcher(config[ModelConnectorConstants.TMP_DIR_KEY])
        self._external_model_fetchers = {
            file_fetcher.get_prefix(): file_fetcher
        }

        try:
            from bosun.model_connector.s3_uri_fetcher import S3Fetcher
            s3 = S3Fetcher(config[ModelConnectorConstants.TMP_DIR_KEY])
            self._external_model_fetchers[s3.get_prefix()] = s3
        except ImportError:
            self._logger.info("S3 support is not available")

    def _handle_external_model(self, config):
        url = config[ModelPackageConstants.MODEL_LOCATION_KEY]
        self._logger.info(
            "Found external model .. handling via location: {}".format(url))

        result = urlparse(url)
        if result.scheme not in self._external_model_fetchers:
            raise Exception(
                "URL Scheme is not supported: {} (for uri: {})".format(result.scheme, url))

        fetcher = self._external_model_fetchers[result.scheme]
        try:
            local_path = fetcher.fetch_artifact(url)
        except Exception as e:
            raise Exception("Error fetching external uri: {} {}".format(url, str(e)))
        self._logger.info("Model is in: {}".format(local_path))
        return local_path

    def _handle_custom_models(self, config):
        return self._handle_model(config, download_scoring_code=False, download_pps_installer=True)

    def _handle_dr_native_model(self, config):
        model_format = config.get(ModelPackageConstants.MODEL_FORMAT_KEY)

        if model_format not in [
            ModelPackageConstants.MODEL_FORMAT_SCORING_CODE,
            ModelPackageConstants.MODEL_FORMAT_MLPKG
        ]:
            raise Exception(
                "Model format '{}' is not supported for DataRobot models".format(
                    model_format
                )
            )
        download_scoring_code = False
        if model_format == ModelPackageConstants.MODEL_FORMAT_SCORING_CODE:
            download_scoring_code = True
        return self._handle_model(config, download_scoring_code=download_scoring_code)

    def _handle_model(self, config, download_scoring_code=False, download_pps_installer=False):
        dr_url = config[ModelConnectorConstants.DR_URL_KEY]
        dr_token = config[ModelConnectorConstants.DR_TOKEN_KEY]
        output_dir = config[ModelConnectorConstants.TMP_DIR_KEY]

        mlops = MLOpsClient(service_url=dr_url, api_key=dr_token)
        model_package_id = config[ModelPackageConstants.MODEL_PACKAGE_ID_KEY]
        model_artifact_path = mlops.download_model_package_from_registry(
            model_package_id,
            output_dir,
            download_scoring_code=download_scoring_code,
            scoring_code_binary=True,
            download_pps_installer=download_pps_installer,
            timeout=600,
        )

        self._logger.info("Model download complete. Model at {}".format(model_artifact_path))
        return model_artifact_path

    def get_model(self, config):
        """
        :param config: configuration dictionary
        """
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info("get_model: {}".format(self.get_sanitized_config(config)))
        et = config[ModelPackageConstants.MODEL_EXECUTION_TYPE_KEY]

        if et == ModelPackageConstants.MODEL_EXECUTION_EXTERNAL:
            model_path = self._handle_external_model(config)
            return ActionStatusInfo(ActionStatus.OK, model_path=model_path)
        elif et == ModelPackageConstants.MODEL_EXECUTION_DEDICATED:
            self._logger.info("Found dedicated model .. downloading")
            model_path = self._handle_dr_native_model(config)
            return ActionStatusInfo(ActionStatus.OK, model_path=model_path)
        elif et == ModelPackageConstants.MODEL_EXECUTION_CUSTOM_INFERENCE:
            self._logger.info("Found custom model .. downloading")
            model_path = self._handle_custom_models(config)
            return ActionStatusInfo(ActionStatus.OK, model_path=model_path)
        else:
            raise Exception("Model execution type: {} is not recognized".format(et))

    @staticmethod
    def get_sanitized_config(parsed_config):
        sanitized = parsed_config.copy()
        if ModelConnectorConstants.DR_TOKEN_KEY in sanitized:
            masked = sanitized[ModelConnectorConstants.DR_TOKEN_KEY][:12] + "*******"
            sanitized[ModelConnectorConstants.DR_TOKEN_KEY] = masked
        return sanitized

#  ---------------------------------------------------------------------------------
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
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

logger = logging.getLogger(__name__)


class DockerPluginConfig:
    DOCKER_NETWORK = "dockerNetwork"
    TRAEFIK_IMAGE_KEY = "traefikImage"
    TRAEFIK_PORT_MAPPING = "traefikPortMapping"
    AGENT_IMAGE_KEY = "agentImage"
    RABBIT_IMAGE_KEY = "rabbitmqImage"
    RABBITMQ_PORT_MAPPING = "rabbitmqPortMapping"
    PPS_BASE_IMAGE_KEY = "ppsBaseImage"
    OUTFACING_PREDICTION_URL_PREFIX = "outfacingPredictionURLPrefix"
    GENERATED_IMAGE_PREFIX = "generatedImagePrefix"
    CONTAINER_NAME_PREFIX = "containerNamePrefix"

    def __init__(self, plugin_config):
        self._config = plugin_config

        schema = {
            BosunPluginConfigConstants.MLOPS_URL_KEY: str,
            BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY: str,
            BosunPluginConfigConstants.MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING_KEY: bool,
            DockerPluginConfig.DOCKER_NETWORK: str,
            DockerPluginConfig.TRAEFIK_IMAGE_KEY: str,
            DockerPluginConfig.RABBIT_IMAGE_KEY: str,
            DockerPluginConfig.AGENT_IMAGE_KEY: str,
            DockerPluginConfig.PPS_BASE_IMAGE_KEY: str,
            DockerPluginConfig.OUTFACING_PREDICTION_URL_PREFIX: str,
            DockerPluginConfig.GENERATED_IMAGE_PREFIX: str,
            DockerPluginConfig.CONTAINER_NAME_PREFIX: str,
            DockerPluginConfig.TRAEFIK_PORT_MAPPING: dict,
            DockerPluginConfig.RABBITMQ_PORT_MAPPING: dict,
        }
        for f in schema:
            if f not in self._config:
                raise Exception("Field {} is missing in plugin config {}".format(f, self._config))

            logger.debug("self._config[f]: {} {}".format(self._config[f], type(self._config[f])))
            if type(self._config[f]) != schema[f]:
                raise Exception("Field {} type: {} is not as expected: {}"
                                .format(f, type(self._config[f]), schema[f]))
            if f in [
                DockerPluginConfig.RABBITMQ_PORT_MAPPING, DockerPluginConfig.TRAEFIK_PORT_MAPPING
            ]:
                port_mapping = self._config[f]
                for key in port_mapping:
                    if type(key) != int or key < 0:
                        raise Exception("Invalid port mapping key: '{}' for config '{}'".format(
                            str(key), str(f)
                        ))
                    value = port_mapping[key]
                    if type(value) != int or value < 0:
                        raise Exception("Invalid port mapping value: '{}' for config '{}'".format(
                            str(value), str(f)
                        ))
        # Specific to docker plugin, if the docker server is running on localhost, change its url
        if self._config[BosunPluginConfigConstants.MLOPS_URL_KEY].startswith("http://localhost"):
            self._config[BosunPluginConfigConstants.MLOPS_URL_KEY] = self._config[
                BosunPluginConfigConstants.MLOPS_URL_KEY
            ].replace("http://localhost", "http://host.docker.internal")

    @property
    def datarobot_app_url(self):
        return self._config[BosunPluginConfigConstants.MLOPS_URL_KEY]

    @property
    def datarobot_api_key(self):
        return self._config[BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY]

    @property
    def docker_network(self):
        return self._config[DockerPluginConfig.DOCKER_NETWORK]

    @property
    def do_mlops_monitoring(self):
        return self._config[BosunPluginConfigConstants.MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING_KEY]

    @property
    def traefik_image(self):
        return self._config[DockerPluginConfig.TRAEFIK_IMAGE_KEY]

    @property
    def outfacing_prediction_url_prefix(self):
        return self._config[DockerPluginConfig.OUTFACING_PREDICTION_URL_PREFIX]

    @property
    def rabbit_image(self):
        return self._config[DockerPluginConfig.RABBIT_IMAGE_KEY]

    @property
    def agent_image(self):
        return self._config[DockerPluginConfig.AGENT_IMAGE_KEY]

    @property
    def pps_base_image(self):
        return self._config[DockerPluginConfig.PPS_BASE_IMAGE_KEY]

    @property
    def container_name_prefix(self):
        return self._config[DockerPluginConfig.CONTAINER_NAME_PREFIX]

    @property
    def generated_image_name_prefix(self):
        return self._config[DockerPluginConfig.GENERATED_IMAGE_PREFIX]

    @property
    def traefik_port_mapping(self):
        return self._config[DockerPluginConfig.TRAEFIK_PORT_MAPPING]

    @property
    def rabbitmq_port_mapping(self):
        return self._config[DockerPluginConfig.RABBITMQ_PORT_MAPPING]

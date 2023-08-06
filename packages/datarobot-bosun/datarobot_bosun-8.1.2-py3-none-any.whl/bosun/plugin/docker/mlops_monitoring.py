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
import time
from urllib.parse import urlparse

from bosun.plugin.docker.docker_helper import get_containers_with_label, DockerLabels


class MLOpsMonitoringHelper:
    """
    Perform actions to start/stop/status the Agent+RabbitMQ Container for MLOps monitoring
    """
    def __init__(self,
                 docker_client,
                 agent_image,
                 rabbitmq_image,
                 rabbitmq_queue_url,
                 rabbitmq_queue_name,
                 datarobot_url,
                 datarobot_api_token,
                 docker_network,
                 dry_run,
                 ):
        self._client = docker_client
        self._agent_image = agent_image
        self._rabbitmq_image = rabbitmq_image
        self._rabbitmq_queue_url = rabbitmq_queue_url
        self._rabbitmq_queue_name = rabbitmq_queue_name
        self._datarobot_url = datarobot_url
        self._datarobot_api_token = datarobot_api_token
        self._docker_network = docker_network
        self._dry_run = dry_run
        self._nr_agents = 1
        self._logger = logging.getLogger("{}.{}".format(self.__class__.__module__,
                                                        self.__class__.__name__))

    def _get_running_agent_containers(self):
        return get_containers_with_label(self._client, label=DockerLabels.AGENT_LABEL)

    def _get_running_rabbit_containers(self):
        return get_containers_with_label(self._client, label=DockerLabels.RABBITMQ_LABEL)

    def clean_stopped_agent_container_if_any(self):
        agent_containers = self._client.containers.list(
            filters={"label": DockerLabels.AGENT_LABEL, "status": "exited"}
        )
        return self._clean_stopped_containers(agent_containers, "agent")

    def clean_stopped_rabbit_container_if_any(self):
        rabbit_containers = self._client.containers.list(
            filters={"label": DockerLabels.RABBITMQ_LABEL, "status": "exited"}
        )
        return self._clean_stopped_containers(rabbit_containers, "rabbit")

    def _clean_stopped_containers(self, containers, name):
        if len(containers) == 0:
            return
        if containers[0].status == "exited":
            self._logger.info("Removing stopped {} container".format(name))
            containers[0].remove()

    def is_agent_running(self):
        cl = self._get_running_agent_containers()
        if len(cl) == 0:
            return False
        else:
            return True

    def is_rabbit_running(self):
        cl = self._get_running_rabbit_containers()
        if len(cl) == 0:
            return False
        else:
            return True

    def _run_rabbit_container(self, rabbitmq_port_mapping=None):
        parsed_url = urlparse(self._rabbitmq_queue_url)
        env = {
            "RABBITMQ_DEFAULT_USER": parsed_url.username,
            "RABBITMQ_DEFAULT_PASS": parsed_url.password,
        }
        if rabbitmq_port_mapping:
            ports = {str(k): str(v) for k, v in rabbitmq_port_mapping.items()}
        else:
            ports = {
                "15672": "15672",
                "5672": "5672"
            }
        self._logger.info("RabbitMQ port mapping: '{}'".format(ports))
        labels = {
            DockerLabels.RABBITMQ_LABEL: "rabbit",
            DockerLabels.MLOPS_LABEL: None
        }

        if self._dry_run:
            self._logger.info("DRYRUN: running rabbit container")
        else:
            self._client.containers.run(self._rabbitmq_image,
                                        name="rabbit",
                                        network=self._docker_network,
                                        ports=ports,
                                        environment=env,
                                        detach=True,
                                        labels=labels)
            time.sleep(10)

    def _run_agent_container(self):

        env = {
            "MLOPS_SERVICE_URL": self._datarobot_url,
            "MLOPS_API_TOKEN": self._datarobot_api_token,
            "START_DELAY": "10",
            "MLOPS_SPOOLER_TYPE": "RABBITMQ",
            "MLOPS_RABBITMQ_QUEUE_URL": self._rabbitmq_queue_url,
            "MLOPS_RABBITMQ_QUEUE_NAME": self._rabbitmq_queue_name,
        }
        labels = {
            DockerLabels.AGENT_LABEL: "agent",
            DockerLabels.MLOPS_LABEL: None
        }

        if self._dry_run:
            self._logger.info("DRYRUN: running agent container")
        else:
            self._client.containers.run(
                self._agent_image,
                name="mlops_agent",
                network=self._docker_network,
                detach=True,
                labels=labels,
                environment=env,
            )

    def start(self, rabbitmq_port_mapping=None):
        # Cleanup in case previous shutdown was not clean
        self.clean_stopped_agent_container_if_any()
        self.clean_stopped_rabbit_container_if_any()

        is_agent_running = self.is_agent_running()
        is_rabbit_running = self.is_rabbit_running()
        self._logger.info("Starting MLOps monitoring: rabbit: {} agent: {}"
                          .format(is_rabbit_running, is_agent_running))

        if is_rabbit_running is False:
            self._logger.info("Rabbit container is not running - starting it")
            self._run_rabbit_container(rabbitmq_port_mapping)
        else:
            self._logger.info("Rabbit container is already running - skipping")

        if is_agent_running is False:
            self._logger.info("Agent container is not running - starting it")
            self._run_agent_container()
        else:
            self._logger.info("Agent container is already running - skipping")

    def stop(self):
        is_agent_running = self.is_agent_running()
        is_rabbit_running = self.is_rabbit_running()
        self._logger.info("Stopping MLOps monitoring: rabbit: {} agent: {}"
                          .format(is_rabbit_running, is_agent_running))

        if is_agent_running is True:
            self._logger.info("Agent container is running - stopping it")
            agent_containers = self._get_running_agent_containers()
            for container in agent_containers:
                if self._dry_run:
                    self._logger.info("DRYRUN: Stopping agent container")
                else:
                    container.stop()
                    container.remove()
        else:
            self._logger.info("Agent container is not running - skipping")

        if is_rabbit_running is True:
            self._logger.info("Rabbit container is running - stopping it")
            agent_containers = self._get_running_rabbit_containers()
            for container in agent_containers:
                if self._dry_run:
                    self._logger.info("DRYRUN: stopping rabbit container")
                else:
                    container.stop()
                    container.remove()
        else:
            self._logger.info("Rabbit container is not running - skipping")

    def status(self):
        """
        Return status of agent and Rabbit
        TODO: also return number of monitoring messages so far from Agent status file?
        :return:
        """
        is_agent_running = self.is_agent_running()
        is_rabbit_running = self.is_rabbit_running()
        self._logger.info("Status MLOps monitoring: rabbit: {} agent: {}"
                          .format(is_rabbit_running, is_agent_running))

        return is_agent_running and is_rabbit_running

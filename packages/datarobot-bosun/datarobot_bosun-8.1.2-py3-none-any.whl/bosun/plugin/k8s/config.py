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
import re
from urllib.parse import urlparse

import yaml
from schema import Optional, Or, Regex, Schema, SchemaError

from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.constants import BosunPluginConfigConstants

log = logging.getLogger(__name__)

PATTERN_IP_ADDR = re.compile(r"[0-9.:]+")


class KubernetesPluginConfig:
    AGENT_IMAGE = "agentImage"
    AGENT_RESOURCES = "agentResources"
    AGENT_SECURITY = "agentSecurityContext"
    AGENT_SIDECAR = "agentSidecar"
    PPS_BASE_IMAGE = "ppsBaseImage"
    PPS_SERVICE_ACCOUNT = "ppsServiceAccount"
    PPS_RESOURCES = "ppsResources"
    PPS_CPU_UTILIZATION = "ppsCpuUtilizationPercent"
    PPS_POD_SECURITY = "ppsPodSecurityContext"
    PPS_SECURITY = "ppsSecurityContext"
    PPS_ANNOTATIONS = "ppsAnnotations"
    PPS_SELECTOR = "ppsNodeSelector"
    PPS_TOLERATIONS = "ppsTolerations"
    PPS_AFFINITY = "ppsAffinity"
    PPS_EXTRA_ENV = "ppsExtraEnvironment"
    PPS_EXTRA_VOL = "ppsExtraVolumes"
    PPS_EXTRA_VOLM = "ppsExtraVolumeMounts"
    OUTFACING_PREDICTION_URL_PREFIX = "outfacingPredictionURLPrefix"
    GENERATED_IMAGE_REPO = "generatedImageRepo"
    KUBE_CONFIG_CONTEXT = "kubeConfigContext"
    KUBE_NAMESPACE = "kubeNamespace"
    INGRESS_CLASS = "ingressClass"
    INGRESS_TYPE = "ingressType"
    KANIKO_IMAGE = "kanikoImage"
    KANIKO_CONFIG = "kanikoConfigmapName"
    KANIKO_SECRET = "kanikoSecretName"
    KANIKO_SERVICE_ACCOUNT = "kanikoServiceAccount"
    KANIKO_RESOURCES = "kanikoResources"
    KANIKO_POD_SECURITY = "kanikoPodSecurityContext"
    KANIKO_SECURITY = "kanikoSecurityContext"
    KANIKO_ANNOTATIONS = "kanikoAnnotations"
    KANIKO_SELECTOR = "kanikoNodeSelector"
    KANIKO_TOLERATIONS = "kanikoTolerations"
    KANIKO_AFFINITY = "kanikoAffinity"
    KANIKO_INSECURE_REG = "kanikoInsecureRegistries"
    KANIKO_SKIP_VERIFY_REG = "kanikoSkipSslVerifyRegistries"
    KANIKO_EXTRA_ARGS = "kanikoExtraArguments"
    KANIKO_EXTRA_VOL = "kanikoExtraVolumes"
    KANIKO_EXTRA_VOLM = "kanikoExtraVolumeMounts"
    IMAGE_PULL_SECRETS = "imagePullSecrets"
    LOG_FORMAT = "logFormat"
    SPOOLER_SETTINGS = "spoolerSettings"

    def __init__(self, plugin_config):
        def validate_repo_no_tag(s):
            parts = s.split(":")
            # If we can split string into 3 parts then we know it has a tag and is invalid, i.e.
            #    docker.io:5000/datarobot/search:stable-1.4.2
            if len(parts) == 3:
                msg = 'Repo for generated images must not contain a tag: ":{}"'.format(parts[2])
                raise SchemaError(msg)

            # Otherwise if we split into two parts we need to make sure it is
            #    this -> docker.io:5000/datarobot/search
            #    not  -> docker.io/datarobot/search:stable-1.4.2
            elif len(parts) == 2 and parts[1].find("/") == -1:
                msg = 'Repo for generated images must not contain a tag: ":{}"'.format(parts[1])
                raise SchemaError(msg)
            return True

        schema = Schema({
            # You need to use a versioned PPS image tag (e.g. not latest) so we can track what
            # env version was baked with the .mlpkg file.
            KubernetesPluginConfig.PPS_BASE_IMAGE:
                Regex(r":\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$",
                      error="PPS image must use a versioned tag (i.e. 1.2.3): {}"),
            KubernetesPluginConfig.OUTFACING_PREDICTION_URL_PREFIX:
                Regex(r"^https?://.+", error="Not a valid URL prefix: {}"),
            KubernetesPluginConfig.GENERATED_IMAGE_REPO:
                validate_repo_no_tag,
            BosunPluginConfigConstants.MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING_KEY: bool,
            Optional(BosunPluginConfigConstants.MLOPS_URL_KEY):
                Regex(r"^https?://.+", error="Not a valid URL: {}"),
            Optional(KubernetesPluginConfig.AGENT_SIDECAR, default=True): bool,
            Optional(KubernetesPluginConfig.AGENT_IMAGE): Or(None, str),
            Optional(KubernetesPluginConfig.AGENT_RESOURCES, default={}): dict,
            Optional(KubernetesPluginConfig.AGENT_SECURITY, default={}): dict,
            Optional(BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY): str,
            # Passing a null value actually has special meaning here. It means use the
            # default context that the K8s API client wants to use (either set via env var or
            # defined in the users ~/.kube/config file). By default we assume this plugin is running
            # inside a k8s Pod.
            Optional(KubernetesPluginConfig.KUBE_CONFIG_CONTEXT, default="IN_CLUSTER"):
                Or(None, str),
            Optional(KubernetesPluginConfig.KUBE_NAMESPACE): Or(None, str),
            Optional(KubernetesPluginConfig.INGRESS_CLASS): Or(None, str),
            Optional(KubernetesPluginConfig.INGRESS_TYPE, default="nginx"):
                Or("nginx", "openshift"),
            Optional(KubernetesPluginConfig.PPS_SERVICE_ACCOUNT, default="default"): str,
            Optional(KubernetesPluginConfig.PPS_RESOURCES, default={}): dict,
            Optional(KubernetesPluginConfig.PPS_CPU_UTILIZATION): int,
            Optional(KubernetesPluginConfig.PPS_POD_SECURITY, default={}): dict,
            Optional(KubernetesPluginConfig.PPS_SECURITY, default={}): dict,
            Optional(KubernetesPluginConfig.PPS_AFFINITY, default={}): dict,
            Optional(KubernetesPluginConfig.PPS_ANNOTATIONS, default={}): dict,
            Optional(KubernetesPluginConfig.PPS_SELECTOR, default={}): dict,
            Optional(KubernetesPluginConfig.PPS_TOLERATIONS, default=[]): list,
            Optional(KubernetesPluginConfig.PPS_EXTRA_ENV, default=[]): Schema([dict]),
            Optional(KubernetesPluginConfig.PPS_EXTRA_VOL, default=[]): Schema([dict]),
            Optional(KubernetesPluginConfig.PPS_EXTRA_VOLM, default=[]): Schema([dict]),
            Optional(KubernetesPluginConfig.KANIKO_IMAGE,
                     default="gcr.io/kaniko-project/executor:v1.6.0"): str,
            Optional(KubernetesPluginConfig.KANIKO_CONFIG): Or(None, str),
            Optional(KubernetesPluginConfig.KANIKO_SECRET): Or(None, str),
            # Every namespace gets a "default" ServiceAccount so use it if unset.
            Optional(KubernetesPluginConfig.KANIKO_SERVICE_ACCOUNT, default="default"): str,
            Optional(KubernetesPluginConfig.KANIKO_INSECURE_REG, default=[]): Schema([str]),
            Optional(KubernetesPluginConfig.KANIKO_SKIP_VERIFY_REG, default=[]): Schema([str]),
            Optional(KubernetesPluginConfig.KANIKO_EXTRA_ARGS, default=[]): Schema([str]),
            Optional(KubernetesPluginConfig.KANIKO_EXTRA_VOL, default=[]): Schema([dict]),
            Optional(KubernetesPluginConfig.KANIKO_EXTRA_VOLM, default=[]): Schema([dict]),
            Optional(KubernetesPluginConfig.KANIKO_RESOURCES, default={}): dict,
            Optional(KubernetesPluginConfig.KANIKO_POD_SECURITY, default={}): dict,
            Optional(KubernetesPluginConfig.KANIKO_SECURITY, default={}): dict,
            Optional(KubernetesPluginConfig.KANIKO_AFFINITY, default={}): dict,
            Optional(KubernetesPluginConfig.KANIKO_ANNOTATIONS, default={}): dict,
            Optional(KubernetesPluginConfig.KANIKO_SELECTOR, default={}): dict,
            Optional(KubernetesPluginConfig.KANIKO_TOLERATIONS, default=[]): list,
            Optional(KubernetesPluginConfig.IMAGE_PULL_SECRETS, default=[]): Schema([dict]),
            # This tries to control the output format of the long running services it launches
            # (i.e. tracking-agent, etc) -- it does not adjust the output format of the plugin
            # itself or the Kaniko pods.
            Optional(KubernetesPluginConfig.LOG_FORMAT, default="plain"): str,
            Optional(KubernetesPluginConfig.SPOOLER_SETTINGS): str,
        }, ignore_extra_keys=True)

        self._config = schema.validate(plugin_config)
        if self.do_mlops_monitoring:
            errmsg = "{} is required when monitoring is enabled."
            if self.agent_sidecar:
                if not self.agent_image:
                    raise ValueError(errmsg.format(KubernetesPluginConfig.AGENT_IMAGE))
                if not self.datarobot_api_key:
                    raise ValueError(errmsg.format(BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY))
                if not self.datarobot_app_url:
                    raise ValueError(errmsg.format(BosunPluginConfigConstants.MLOPS_URL_KEY))
            else:
                if not self.spooler_settings:
                    raise ValueError(errmsg.format(KubernetesPluginConfig.SPOOLER_SETTINGS))

        if self.kaniko_configmap_name and self.kaniko_secret_name:
            errmsg = "{} and {} are mutually exclusive."
            raise ValueError(errmsg.format(KubernetesPluginConfig.KANIKO_CONFIG,
                                           KubernetesPluginConfig.KANIKO_SECRET))

    @classmethod
    def from_files(cls, bosun_config, extra_config_file=None):
        if extra_config_file:
            log.info("Kubernetes plugin private config file: {}".format(extra_config_file))
            with open(extra_config_file) as fp:
                config = yaml.safe_load(fp)
            bosun_config.update(config)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(BosunPluginBase.get_sanitized_config(bosun_config))
        return cls(bosun_config)

    @property
    def datarobot_app_url(self):
        return self._config.get(BosunPluginConfigConstants.MLOPS_URL_KEY)

    @property
    def do_mlops_monitoring(self):
        return self._config[BosunPluginConfigConstants.MLOPS_BOSUN_PRED_ENV_ENABLE_MONITORING_KEY]

    @property
    def agent_sidecar(self):
        return self._config[KubernetesPluginConfig.AGENT_SIDECAR]

    @property
    def agent_image(self):
        return self._config.get(KubernetesPluginConfig.AGENT_IMAGE)

    @property
    def agent_resources(self):
        return self._config[KubernetesPluginConfig.AGENT_RESOURCES]

    @property
    def agent_security_context(self):
        return self._config[KubernetesPluginConfig.AGENT_SECURITY]

    @property
    def log_format(self):
        return self._config[KubernetesPluginConfig.LOG_FORMAT]

    @property
    def spooler_settings(self):
        # When running as a sidecar, we force use of the FS spooler.
        sidecar_settings = \
            "spooler_type=filesystem;directory=/tmp/ta;max_files=50;file_max_size=10240000"
        return (sidecar_settings if self.agent_sidecar
                else self._config.get(KubernetesPluginConfig.SPOOLER_SETTINGS))

    @property
    def datarobot_api_key(self):
        return self._config.get(BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY)

    @property
    def outfacing_prediction_url_prefix(self):
        url = self._config[KubernetesPluginConfig.OUTFACING_PREDICTION_URL_PREFIX]
        # Make sure the prefix always ends with a '/' so urljoin() deals with it correctly
        if not url.endswith("/"):
            return url + "/"
        return url

    @property
    def pps_base_image(self):
        return self._config[KubernetesPluginConfig.PPS_BASE_IMAGE]

    @property
    def pps_resources(self):
        return self._config[KubernetesPluginConfig.PPS_RESOURCES]

    @property
    def pps_cpu_utilization(self):
        return self._config.get(KubernetesPluginConfig.PPS_CPU_UTILIZATION)

    @property
    def _has_pps_cpu_request(self):
        if "requests" not in self.pps_resources:
            return False
        return "cpu" in self.pps_resources["requests"]

    @property
    def _has_agent_cpu_request(self):
        if "requests" not in self.agent_resources:
            return False
        return "cpu" in self.agent_resources["requests"]

    @property
    def ready_for_hpa(self):
        # HPA **needs** CPU requests based on the current way we are using it. However, since
        # tracking-agent runs in the same pod as the prediction server we also need requests there
        # too if tracking is enabled.
        # See https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
        # TODO: when `Container Resource Metrics` goes beta/GA we can simplify the logic if we
        #       update our HPA spec.
        if self.pps_cpu_utilization is None:
            return False
        if self.do_mlops_monitoring:
            return self._has_pps_cpu_request and self._has_agent_cpu_request
        else:
            return self._has_pps_cpu_request

    @property
    def pps_pod_security_context(self):
        return self._config[KubernetesPluginConfig.PPS_POD_SECURITY]

    @property
    def pps_security_context(self):
        return self._config[KubernetesPluginConfig.PPS_SECURITY]

    @property
    def pps_annotations(self):
        return self._config[KubernetesPluginConfig.PPS_ANNOTATIONS]

    @property
    def pps_node_selector(self):
        return self._config[KubernetesPluginConfig.PPS_SELECTOR]

    @property
    def pps_tolerations(self):
        return self._config[KubernetesPluginConfig.PPS_TOLERATIONS]

    @property
    def pps_affinity(self):
        return self._config[KubernetesPluginConfig.PPS_AFFINITY]

    @property
    def pps_version(self):
        return self.pps_base_image.split(":")[-1]

    @property
    def pps_environment(self):
        return self._config[KubernetesPluginConfig.PPS_EXTRA_ENV]

    @property
    def pps_volumes(self):
        return self._config[KubernetesPluginConfig.PPS_EXTRA_VOL]

    @property
    def pps_volume_mounts(self):
        return self._config[KubernetesPluginConfig.PPS_EXTRA_VOLM]

    @property
    def generated_image_repo(self):
        return self._config[KubernetesPluginConfig.GENERATED_IMAGE_REPO]

    @property
    def kubernetes_config_context(self):
        return self._config[KubernetesPluginConfig.KUBE_CONFIG_CONTEXT]

    @property
    def kubernetes_namespace(self):
        return self._config.get(KubernetesPluginConfig.KUBE_NAMESPACE)

    @property
    def ingress_class(self):
        return self._config.get(KubernetesPluginConfig.INGRESS_CLASS)

    @property
    def ingress_type(self):
        return self._config[KubernetesPluginConfig.INGRESS_TYPE]

    @property
    def force_ssl(self):
        url = self._config[KubernetesPluginConfig.OUTFACING_PREDICTION_URL_PREFIX]
        # Put it in a format that can be directly used by our YAML template.
        return str(urlparse(url).scheme == "https").lower()

    @property
    def ingress_host(self):
        url = self._config[KubernetesPluginConfig.OUTFACING_PREDICTION_URL_PREFIX]
        host = urlparse(url).hostname
        if PATTERN_IP_ADDR.match(host):
            # Ingress resources don't support an IP Addr for the Host: field but it is valid for
            # the user to pass this in our config param as they should know the IP that the ingress
            # is exposed on. If we detect this case, don't return a host value at all.
            return None
        return host

    @property
    def ingress_path(self):
        url = self._config[KubernetesPluginConfig.OUTFACING_PREDICTION_URL_PREFIX]
        # Strip off any trailing '/' from the path so it is easy to join it in our
        # YAML template.
        return urlparse(url).path.rstrip("/")

    @property
    def kaniko_image(self):
        return self._config[KubernetesPluginConfig.KANIKO_IMAGE]

    @property
    def kaniko_configmap_name(self):
        return self._config.get(KubernetesPluginConfig.KANIKO_CONFIG)

    @property
    def kaniko_secret_name(self):
        return self._config.get(KubernetesPluginConfig.KANIKO_SECRET)

    @property
    def pps_service_account(self):
        return self._config[KubernetesPluginConfig.PPS_SERVICE_ACCOUNT]

    @property
    def kaniko_service_account(self):
        return self._config[KubernetesPluginConfig.KANIKO_SERVICE_ACCOUNT]

    @property
    def kaniko_resources(self):
        return self._config[KubernetesPluginConfig.KANIKO_RESOURCES]

    @property
    def kaniko_pod_security_context(self):
        return self._config[KubernetesPluginConfig.KANIKO_POD_SECURITY]

    @property
    def kaniko_security_context(self):
        return self._config[KubernetesPluginConfig.KANIKO_SECURITY]

    @property
    def kaniko_annotations(self):
        return self._config[KubernetesPluginConfig.KANIKO_ANNOTATIONS]

    @property
    def kaniko_node_selector(self):
        return self._config[KubernetesPluginConfig.KANIKO_SELECTOR]

    @property
    def kaniko_tolerations(self):
        return self._config[KubernetesPluginConfig.KANIKO_TOLERATIONS]

    @property
    def kaniko_affinity(self):
        return self._config[KubernetesPluginConfig.KANIKO_AFFINITY]

    @property
    def insecure_registires(self):
        return self._config[KubernetesPluginConfig.KANIKO_INSECURE_REG]

    @property
    def skip_tls_verify_registry(self):
        return self._config[KubernetesPluginConfig.KANIKO_SKIP_VERIFY_REG]

    @property
    def image_pull_secrets(self):
        return self._config[KubernetesPluginConfig.IMAGE_PULL_SECRETS]

    @property
    def kaniko_args(self):
        return (["--skip-tls-verify-registry={}".format(r)
                 for r in self._config[KubernetesPluginConfig.KANIKO_SKIP_VERIFY_REG]]
                + ["--insecure-registry={}".format(r)
                   for r in self._config[KubernetesPluginConfig.KANIKO_INSECURE_REG]]
                + self._config[KubernetesPluginConfig.KANIKO_EXTRA_ARGS])

    @property
    def kaniko_volumes(self):
        vols = []
        if self._config.get(KubernetesPluginConfig.KANIKO_CONFIG):
            vols.append({"configMap": {"name": self._config[KubernetesPluginConfig.KANIKO_CONFIG]},
                         "name": "docker-config"})
        elif self._config.get(KubernetesPluginConfig.KANIKO_SECRET):
            vols.append({
                "secret": {"secretName": self._config[KubernetesPluginConfig.KANIKO_SECRET],
                           "items": [{"key": ".dockerconfigjson", "path": "config.json"}]},
                "name": "docker-config",
            })
        return vols + self._config[KubernetesPluginConfig.KANIKO_EXTRA_VOL]

    @property
    def kaniko_volume_mounts(self):
        volM = []
        if (self._config.get(KubernetesPluginConfig.KANIKO_CONFIG)
           or self._config.get(KubernetesPluginConfig.KANIKO_SECRET)):
            volM.append({"mountPath": "/kaniko/.docker/", "name": "docker-config"})
        return volM + self._config[KubernetesPluginConfig.KANIKO_EXTRA_VOLM]

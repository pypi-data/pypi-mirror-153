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
from base64 import b64encode
from math import floor
import os

import yaml
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader, StrictUndefined

log = logging.getLogger(__name__)

TEMPLATE_PACKAGE = "bosun.plugin.k8s"

#
# IMPORTANT: These labels are used to identify resources in K8s. Making changes to them will be a
#            breaking change unless handled correctly so do so with caution.
#
# Add a label to make it easy for an operator to find all deployments associated to a given
# Prediction Environment (i.e. `kubectl get -A deployment -l bosun.datarobot.com/env=<id>`)
# Changing this break deployment_list on already deployed models.
PRED_ENV_LABEL_NAME = "bosun.datarobot.com/env"

# Add a label to make it easy for an operator to find all resources associated to a given DataRobot
# Deployment (i.e. `kubectl get -A all -l bosun.datarobot.com/deployment=<id>`)
# Changing this will break deployment_list and pe_status on already deployed models.
DEPLOYMENT_LABEL_NAME = "bosun.datarobot.com/deployment"

# Add a label to make it easy for an operator to find all pods associated to a given deployed
# model (i.e. `kubectl get -A pod -l bosun.datarobot.com/model=<id>`)
MODEL_LABEL_NAME = "bosun.datarobot.com/model"

# Label used to help identify parts of our system
COMPONENT_LABEL_NAME = "app.kubernetes.io/component"

_unsupported_label_start_end_chars_regex = re.compile(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9]$")
_unsupported_label_chars_regex = re.compile(r"[^-a-zA-Z0-9.]")


class ManifestGenerationError(Exception):
    pass


def _raise_manifest_error(msg):
    raise ManifestGenerationError(msg)


def base64_encode(value):
    """
    convert bytes to b64 encoded string
    :param value: bytes
    :return: str b64 encoded
    """
    return b64encode(str.encode(value)).decode("utf-8")


def clean_as_kubernetes_label(value):
    """
    Kubernetes label value can consist of alphanumeric characters and '-', '_' or '.'.
    Unless if empty, it must begin and end with an alphanumeric character ([a-z0-9A-Z]))
    There is also a max length of 63 characters.
    :param value: Optional[str]
    :return: str with replaced unsupported characters or None
    """
    # See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set # noqa
    if not value:
        return None
    value = _unsupported_label_chars_regex.sub("_", value)
    prev_value = value
    while value:
        value = _unsupported_label_start_end_chars_regex.sub("", prev_value)
        if prev_value == value:
            break
        prev_value = value
    return _truncate_middle(value, 63)


def _truncate_middle(s, max_length):
    if len(s) <= max_length:
        return s
    # half of the size, minus the 3 .'s
    n_2 = floor(max_length / 2) - 3
    n_1 = max_length - n_2 - 3  # whatever's left
    return "{}...{}".format(s[:n_1], s[-n_2:])


def clean_as_kubernetes_name(value):
    """
    Kubernetes name can consist of lowercase alphanumeric characters, '-', or '.'.
    It must start and end with an an alphanumeric characters.
    There is also a max length of 253 characters.
    Note: for resources that only allow 63 characters, it is the caller's responsibility
          to truncate the name since these resource types are less common.
    :param value: str
    :return: str with replaced unsupported characters
    """
    # See https://kubernetes.io/docs/concepts/overview/working-with-objects/names/
    value = value[:min(253, len(value))].lower()
    value = _unsupported_label_chars_regex.sub("-", value)
    prev_value = value
    while value:
        value = _unsupported_label_start_end_chars_regex.sub("", prev_value)
        if prev_value == value:
            break
        prev_value = value
    return value


def get_render_engine(plugin_config, pe_info):
    env = Environment(
        loader=ChoiceLoader([
            FileSystemLoader(os.environ.get("BOSUN_K8S_TEMPLATE_DIR", "/override/templates/")),
            PackageLoader(TEMPLATE_PACKAGE),
        ]),
        # Make sure blocks don't mess with our YAML formatting:
        trim_blocks=True,
        lstrip_blocks=True,
        # Let's be very strict about things...
        undefined=StrictUndefined,
        autoescape=True,
    )
    env.filters["b64encode"] = base64_encode
    env.filters["k8slabel"] = clean_as_kubernetes_label
    env.filters["k8sname"] = clean_as_kubernetes_name
    env.globals["ABORT"] = _raise_manifest_error
    env.globals["config"] = plugin_config
    env.globals["pei"] = pe_info
    env.globals["PRED_ENV_LABEL_NAME"] = PRED_ENV_LABEL_NAME
    env.globals["DEPLOYMENT_LABEL_NAME"] = DEPLOYMENT_LABEL_NAME
    env.globals["MODEL_LABEL_NAME"] = MODEL_LABEL_NAME
    env.globals["COMPONENT_LABEL_NAME"] = COMPONENT_LABEL_NAME
    return env


class ResourceBuilder:
    DEPLOYMENT_WITH_INGRESS = "model-resources.yaml.j2"
    DEPLOYMENT_ONLY = "model-resources/deployment.yaml.j2"
    IMAGE_BUILDER = "image-builder.yaml.j2"
    MLOPS_SECRET = "mlops-api-secret.yaml.j2"

    def __init__(self, config, pe_info):
        self._env = get_render_engine(config, pe_info)

    @property
    def helpers(self):
        return self.get_template("_helpers.j2").module

    def get_template(self, name):
        return self._env.get_template(name)

    def render(self, template, disable_logging=False, **kwargs):
        t = self.get_template(template)
        rendered = t.render(**kwargs)
        if not disable_logging:
            log.debug("Rendered template '%s':\n%s", template, rendered)
        return yaml.safe_load(rendered)

    def get_mlops_secret_manifest(self, di):
        return self.render(self.MLOPS_SECRET, disable_logging=True, di=di)

    def get_builder_manifest(self, di):
        return self.render(self.IMAGE_BUILDER, di=di)

    @staticmethod
    def get_replica_settings(di):
        desired_replicas = int(di.kv_config.get("replicas", "1"))
        min_replicas = int(di.kv_config.get("minReplicas", "0"))
        max_replicas = int(di.kv_config.get("maxReplicas", "0"))
        # Setting *both* a min and max replica counts implies autoscaling
        is_autoscale = bool(min_replicas and max_replicas)

        if is_autoscale:
            # Crop the desired count into the [min,max] range
            desired_replicas = max(min_replicas, desired_replicas)
            desired_replicas = min(desired_replicas, max_replicas)
            log.info("Configuring autoscaling: min=%s,max=%s,desired=%s",
                     min_replicas, max_replicas, desired_replicas)
        return {
            "desired_replicas": desired_replicas,
            "min_replicas": min_replicas,
            "max_replicas": max_replicas,
            "is_autoscale": is_autoscale,
        }

    def get_pps_manifest(self, di):
        replica_settings = self.get_replica_settings(di)
        name = self.helpers.name(di)
        return self.render(self.DEPLOYMENT_WITH_INGRESS, name=name, di=di, **replica_settings)

    def get_deployment_for_update(self, existing_deployment, di):
        # We can't rename a resource as part of an update so make sure to use the existing name
        name = existing_deployment.metadata.name
        manifest = self.render(self.DEPLOYMENT_ONLY, name=name, di=di, desired_replicas=None)[0]

        # The selector is immutable after creation so we won't try to modify it...
        del manifest["spec"]["selector"]

        # ...and therefore we will also merge the existing labels with the new labels in the event
        # the existing selector relies on the existing labels.
        merged_labels = existing_deployment.spec.template.metadata.labels.copy()
        new_pod_labels = manifest["spec"]["template"]["metadata"]["labels"]
        merged_labels.update(new_pod_labels)
        manifest["spec"]["template"]["metadata"]["labels"] = merged_labels
        return manifest

    @staticmethod
    def validate_k8s_version(version_info):
        """
        Our manifests are only designed to support specific versions of K8s.

        Raises ValueError if provided an unsupported version of K8s.
        """
        # .minor isn't always a pure number so use a regexp to validate
        if version_info.major != "1" or not re.match(r"(1[6-9]|2[0-1]).*", version_info.minor):
            status_msg = "K8s server version must be between: 1.16 - 1.21"
            raise ValueError(status_msg)

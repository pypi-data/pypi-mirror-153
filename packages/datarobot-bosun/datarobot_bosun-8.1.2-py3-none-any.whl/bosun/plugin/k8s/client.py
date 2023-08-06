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
import math
import random
import time
from contextlib import contextmanager
from functools import wraps
from itertools import chain

from kubernetes import client, config, watch, utils
from kubernetes.config.kube_config import list_kube_config_contexts
from kubernetes.dynamic import DynamicClient
from kubernetes.dynamic.resource import ResourceList
from kubernetes.stream import stream
from requests import codes
import yaml


DEPLOYMENT_CHECK_DELAY = 3
DEFAULT_MAX_RETRY_DELAY = 30
SERVICE_NAMESPACE_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/namespace"

log = logging.getLogger(__name__)
logd = logging.getLogger(__name__ + ".dedupe")

# Wrap Kubernetes exceptions so callers of our client don't need to be aware that we are just a thin
# wrapper.
ClientError = client.rest.ApiException
ClientErrorList = utils.FailToCreateError


class FailToDeleteError(ClientErrorList):
    pass


class _SimpleDedupe(logging.Filter):
    """Simple log filter to hush consecutive duplicate log messages."""
    def __init__(self):
        self.last_sent = None
        self.last_message = None

    def filter(self, record):
        # Only display duplicate logs every so often
        if record.msg == self.last_message and (time.time() - self.last_sent) < 240:
            return False
        else:
            self.last_sent = time.time()
            self.last_message = record.msg
            return True


logd.addFilter(_SimpleDedupe())


# TODO there is a lot of use for wait_for that we should look at and try to use a watcher (with
# retries and use of resourceVersion) more intelligently to be lighter on the API. This is what
# kubectl does.
def wait_for(
    checker,
    timeout=60,
    exception=TimeoutError,
    max_retry_delay=DEFAULT_MAX_RETRY_DELAY,
    initial_delay=0,
):
    """
    Sometimes it just doesn't make sense to use a watcher and we need to fall back to polling.
    This is a generic function that takes a user defined condition and waits for it to return
    True.
    """
    start_time = time.monotonic()
    if initial_delay:
        time.sleep(initial_delay)
    i = 0
    while True:
        success = checker(i, start_time)
        if success:
            # Return the value back from the checker() in case it isn't just a True/False
            # value and the caller can do something useful with it.
            return success
        elapsed = time.monotonic() - start_time
        if elapsed > timeout:
            raise exception("Timed out after {}s".format(elapsed))

        # Randomize the actual wait to get even spread as illustrated here:
        # https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter It is prudent to
        # have a sleep in here because most checkers() are going to be calling into the k8s API and
        # while it can handle a lot of load, it is a finite resource so we need some sleeps before
        # checks.
        wait = random.uniform(1, min(max_retry_delay, 2 ** i))  # nosec
        log.debug(
            "Polling k8s API for condition to be met", extra={"wait": wait}
        )
        time.sleep(wait)
        i = i + 1


def minify(data, excluder=lambda key_name: False):
    """
    When given a complex `data`structure (i.e. resource.to_dict()) we will return a copy of the data
    with all _empty_ entries removed (recursively). Empty values include, empty lists, strings,
    dicts or None or a key that is associated with an empty value. Also, an optional `excluder`
    function can be provided that will remove keys based on custom logic.
    """
    def is_empty(t):
        return isinstance(t, (list, dict, str)) and not minify(t, excluder)

    def has_data(t):
        return t is not None and not is_empty(t)

    if isinstance(data, dict):
        return {k: minify(v, excluder) for k, v in data.items()
                if has_data(v) and not excluder(k)}
    elif isinstance(data, (list, tuple)):
        return [minify(x, excluder) for x in data if has_data(x)]
    else:
        return data


def make_selector(mapping):
    """
    Given a mapping of label names and values, generate a selector expression to use in API
    requests.
    """
    return ",".join("{}={}".format(k, v) for k, v in mapping.items())


def json_pointer(value):
    """
    Correctly escapes values for use as JSON Pointers
    http://jsonpatch.com/#json-pointer
    """
    return value.replace("~", "~0").replace("/", "~1")


def retry_kubernetes(max_attempts=5, retry_on_timeout=False):
    """
    Decorate your k8s API wrappers with this function to add built in retries and handling of
    re-auth if your wrapper can take a long time (i.e. waiting for a deployment change to roll-out).
    """
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            attempt = 1
            while True:
                level = logging.ERROR
                try:
                    return func(*args, **kwargs)
                except ConnectionError:
                    if attempt == max_attempts:
                        raise
                    msg = "Error during kubernetes connection, retry"
                except ClientError as e:
                    is_unauthorized_request = e.status == codes.UNAUTHORIZED
                    is_timeout_request = e.status == codes.GATEWAY_TIMEOUT
                    is_internal_server_error = (
                        e.status == codes.INTERNAL_SERVER_ERROR
                    )
                    # We have authorization flakes, so let's retry We will detect auth issue during
                    # smoke test, so that's ok to retry here
                    if is_unauthorized_request:
                        if attempt == max_attempts:
                            raise
                        # Token has 15 minutes expiration time, so let's reload config to update
                        # token
                        level = logging.INFO
                        msg = "Kubernetes authorization error"
                        self = args[0]
                        self.reload_settings()
                    elif is_timeout_request and retry_on_timeout:
                        if attempt == max_attempts:
                            raise
                        msg = "Timeout during request to kubernetes"
                    # At scale / under load, we have seen the k8s API be flaky with this error:
                    # "rpc error: code = Unavailable desc = transport is closing" simply retrying
                    # the API call a few times has been a practical solution.
                    elif is_internal_server_error:
                        if attempt == max_attempts:
                            raise
                        level = logging.ERROR
                        msg = "Internal error in kubernetes"
                    else:
                        raise

                log.log(
                    level,
                    msg,
                    extra={"attempt": attempt, "max_attempts": max_attempts},
                )
                attempt += 1
                wait = random.uniform(0.5, 2)  # Always add a little randomness to sleeps
                time.sleep(wait)

        return inner_wrapper
    return wrapper


class K8sClient:
    """
    The upstream Kubernetes Python client is just a thin wrapper around the autogenerated Swagger
    code. This is our attempt to wrap that client to make the API a little more friendly to use.
    """

    def __init__(self, api_client, context=None, config_file=None, namespace=None):
        self.api = api_client
        self.__dynamic_client = DynamicClient(api_client)
        self.namespace = namespace or "default"  # "default" namespace is a k8s convention
        self.config_file = config_file
        self.context = context
        self.__version_info = None

    @classmethod
    def from_config(cls, context=None, config_file=None, namespace=None):
        """
        Returns a new API Client that is configured from loading the normal kubectl config files. We
        also support a special 'IN_CLUSTER' context which means we are running *inside* a Kubernetes
        cluster so no extra configuration is necessary.
        """
        api_client, default_namespace = cls.load_settings(context, config_file)

        if namespace is None:
            namespace = default_namespace
        return cls(api_client, context=context, config_file=config_file, namespace=namespace)

    @classmethod
    def load_settings(cls, context=None, config_file=None):
        """
        Returns a new API Client that is configured from loading the normal kubectl config files. We
        also support a special 'IN_CLUSTER' context which means we are running *inside* a Kubernetes
        cluster so no extra configuration is necessary.
        """
        namespace = None
        if context == "IN_CLUSTER":
            client_config = client.Configuration()
            config.load_incluster_config(client_config)
            api_client = client.ApiClient(configuration=client_config)

            # If we are running in a k8s cluster, it provides the namespace we are running in so use
            # that as the default.
            with open(SERVICE_NAMESPACE_FILENAME) as fh:
                namespace = fh.read()
        else:
            api_client = config.new_client_from_config(
                context=context, config_file=config_file, persist_config=False
            )

            config_contexts, active_context = list_kube_config_contexts(config_file=config_file)
            # A kubeconfig-context can *optionally* specify a namespace so try and fetch from there.
            if context is None:
                namespace = active_context["context"].get("namespace")
            else:
                for c in config_contexts:
                    if c["name"] == context:
                        namespace = c["context"].get("namespace")
                        break

        return api_client, namespace

    def reload_settings(self):
        api_client, _ = self.load_settings(
            self.context, self.config_file
        )
        self.api = api_client
        self.__dynamic_client = DynamicClient(api_client)
        self.__version_info = None

    # If we decide to optimize that method, be careful with reference to self.api. ApiClient token
    # can expire, and then reloaded settings won't apply to cached property automatically.
    @property
    def core_api(self):
        return client.CoreV1Api(self.api)

    @property
    def version_api(self):
        return client.VersionApi(self.api)

    @property
    def apps_api(self):
        return client.AppsV1Api(self.api)

    @property
    def extensions_api(self):
        return client.ExtensionsV1beta1Api(self.api)

    @property
    def version_info(self):
        if self.__version_info is None:
            self.__version_info = self.version_api.get_code()
        return self.__version_info

    def create_from_dict(self, data):
        """Simple wrapper around the kubernetes-lib function of the same name. Pass it a dict-like
        manifest of a k8s *List kind.
        """
        return utils.create_from_dict(self.api, data, namespace=self.namespace)

    def delete_everything(self, label_selector, ignore_auth_errors=False):
        """
        Given a `label_selector` try and really delete every k8s object that matches (we iterate
        over all known object types looking for matching resources). If `ignore_auth_errors` we will
        skip resource types we do not have permission to list but will still raise an error if we
        fail to delete a found resource.
        """
        api_exceptions = []
        k8s_objects = []
        for resource in chain.from_iterable(self.resources):
            if isinstance(resource, ResourceList):
                continue
            try:
                resp = resource.get(namespace=self.namespace, label_selector=label_selector)
                log.debug("found %s item(s) to delete of type: %s", len(resp.items), resource)
            except ClientError as err:
                # A quirk with k8s, some resources don't support listing. They seem ok to skip
                # though because we never would have been able to create instances of these
                # resource types anyway.
                if err.status == codes.METHOD_NOT_ALLOWED:
                    log.debug("resource %s doesn't support listing items; skipping...", resource)
                    continue
                elif err.status == codes.FORBIDDEN and ignore_auth_errors:
                    log.debug("permission denied when listing %s items; skipping...", resource)
                    continue
                log.error("Failed searching for resources of type: %s", resource)
                raise

            for item in resp.items:
                try:
                    resp = resource.delete(namespace=self.namespace, name=item.metadata.name)
                    log.debug("deleted %s: %s",
                              item.kind, item.metadata.name, extra=dict(response=resp))
                    k8s_objects.append(resp)
                except ClientError as err:
                    api_exceptions.append(err)
        if api_exceptions:
            raise FailToDeleteError(api_exceptions)
        return k8s_objects

    def delete_from_dict(self, data):
        """Inspired by the kubernetes-lib create_from_dict function, this is an easy way to delete
        all the resources that were created by `create_from_dict` when given the same k8s *List
        manifest (or at least enough of a manifest to resolve the resource (api,kind,name) tuple.
        """
        if "List" in data["kind"]:
            # Could be "List" or "Pod/Service/...List"
            # This is a list type. iterate within its items
            items = data["items"]
        else:
            # This is a single object so wrap it in a list
            items = [data]

        api_exceptions = []
        k8s_objects = []
        for item in items:
            kind = item["kind"]
            try:
                api_version = item["apiVersion"]
            except KeyError:
                api_version = item["api_version"]  # to support OpenApiObjects being passed to us
            name = item["metadata"]["name"]
            try:
                response = self.delete(api_version, kind, name=name)
                k8s_objects.append(response)
                log.debug("deleted %s: %s", kind, name, extra=dict(response=response))
            except ClientError as err:
                api_exceptions.append(err)
        if api_exceptions:
            raise FailToDeleteError(api_exceptions)
        return k8s_objects

    @contextmanager
    def cleanup_resource(self, resource, noop=False):
        """
        Delete a single (or list) of resources when the block exits. The `resource` param can
        either be an API object or a dict. If noop is set then we don't actually delete anything.
        """
        try:
            yield
        finally:
            if not noop:
                if hasattr(resource, "to_dict"):
                    resource = resource.to_dict()
                self.delete_from_dict(resource)

    @property
    def resources(self):
        return self.__dynamic_client.resources

    @retry_kubernetes(retry_on_timeout=True)
    def get(self, api_version, kind, sub=None, **kwargs):
        api = self.resources.get(api_version=api_version, kind=kind)
        if api.namespaced:
            kwargs["namespace"] = self.namespace
        if sub:
            api = getattr(api, sub)
        return api.get(**kwargs)

    @retry_kubernetes()
    def create(self, api_version, kind, sub=None, **kwargs):
        api = self.resources.get(api_version=api_version, kind=kind)
        if api.namespaced:
            kwargs["namespace"] = self.namespace
        if sub:
            api = getattr(api, sub)
        return api.create(**kwargs)

    @retry_kubernetes()
    def delete(self, api_version, kind, sub=None, **kwargs):
        api = self.resources.get(api_version=api_version, kind=kind)
        if api.namespaced:
            kwargs["namespace"] = self.namespace
        if sub:
            api = getattr(api, sub)
        try:
            return api.delete(**kwargs)
        except ClientError as err:
            if err.status != codes.NOT_FOUND:
                raise
            # We don't consider this an error because it simplifies the code to be more declarative
            # in nature (i.e. if a client asked to delete a resource and it doesn't exist, then we
            # are in the state the client wishes so it's a noop).
            log.warning("%s doesn't exist: %s", kind, kwargs.get("name"))
            return

    @retry_kubernetes()
    def replace(self, api_version, kind, sub=None, **kwargs):
        api = self.resources.get(api_version=api_version, kind=kind)
        if api.namespaced:
            kwargs["namespace"] = self.namespace
        if sub:
            api = getattr(api, sub)
        return api.replace(**kwargs)

    @retry_kubernetes()
    def patch(self, api_version, kind, sub=None, **kwargs):
        api = self.resources.get(api_version=api_version, kind=kind)
        if api.namespaced:
            kwargs["namespace"] = self.namespace
        if sub:
            api = getattr(api, sub)
        return api.patch(**kwargs)

    @retry_kubernetes()
    def watch(self, api_version, kind, sub=None, **kwargs):
        # TODO we should probably be managing the `resource_version` for the caller during retries
        # so we don't miss events.
        api = self.resources.get(api_version=api_version, kind=kind)
        if api.namespaced:
            kwargs["namespace"] = self.namespace
        if sub:
            api = getattr(api, sub)
        for e in api.watch(**kwargs):
            yield e

    @contextmanager
    def run(self, manifest, cleanup=True, start_timeout=1200):
        """
        This is a context manager that takes a dict-like object of a Pod v1 API `manifest`. It
        is up to the caller to make sure the name of the pod is unique. The function will wait until
        the pod is running and then yield a websocket stream attached to stdin, stdout, and stderr
        to the caller. Upon exiting of the context, we will wait for the pod to terminate and
        optionally delete it if `cleanup` is set. The context manager will wait `start_timeout`
        seconds for the pod to be ready before aborting.

        Raises TimeoutError if pod doesn't become ready within `start_timeout` seconds.
               RuntimeError if the pod doesn't complete successfully or we detect issues with it
                            starting up.
        """
        # If create() fails, I don't think we need to worry about cleaning up or running any of the
        # other finally code.
        pod = self.create("v1", "Pod", body=manifest, namespace=self.namespace)
        log.debug("created Pod: %s", pod)
        name = pod.metadata.name
        try:
            def pod_is_running(_, start_time):
                resp = self.get_pod(name)
                log.debug("Pod status: %s", resp.status)
                if resp.status.phase == "Running":
                    return True

                if resp.status.phase != "Pending":
                    raise RuntimeError("Pod '{}' bypassed 'Running' state".format(name))

                elapsed = time.monotonic() - start_time
                if elapsed < 180:  # wait at least a few minutes before short-circuit
                    return False

                # Some conditions aren't worth waiting the full amount of time.
                if resp.status.container_statuses is not None:
                    for container in resp.status.container_statuses:
                        if container.state.waiting.reason == "ImagePullBackOff":
                            msg = "Aborted waiting for Pod '{}' to be ready because: {}"
                            raise RuntimeError(msg.format(name, container.state.waiting.message))
                return False

            # Timeout should be pretty long here because we may need to wait for the cluster to
            # scale up before it can run our pod.
            log.info("waiting up-to %ss for Pod to be ready: %s", start_timeout, name)
            wait_for(pod_is_running, max_retry_delay=3, initial_delay=1, timeout=start_timeout)

            yield stream(self.core_api.connect_get_namespaced_pod_attach,
                         name,
                         self.namespace,
                         stderr=True, stdin=True,
                         stdout=True, tty=False,
                         _preload_content=False)
        finally:
            # Need to capture useful info before we cleanup the pod
            pod = self.get_pod(name)
            log.debug("%s/pod/%s status: %s", self.namespace, name, pod.status)
            self.check_successful_run(pod, cleanup=cleanup)

    def check_successful_run(self, pod, cleanup=False):
        """
        Given an API `pod` object, check to see if it has completed successfully. If `cleanup`
        is set, delete the pod before returning. This will only raise an error if the pod is
        in a terminal state and that terminal state is not success. However, for Pending and Running
        pods, we will attempt to log the container stdout/err and will log the pod status.

        Raises: RuntimeError if the pod did not complete successfully.
        """
        def pretty_status(resource):
            data = resource.status.to_dict()
            s = minify(data, lambda t: t in {"container_id", "image_id", "conditions", "pod_i_ps"})
            return yaml.dump(dict(status=s))

        with self.cleanup_resource(pod, noop=(not cleanup)):
            if pod.status.phase != "Succeeded":
                try:
                    pod_output = self.get_pod_log(pod.metadata.name, tail_lines=75)
                    log.error("%s/Pod/%s OUTPUT:\n%s",
                              self.namespace, pod.metadata.name, pod_output)
                except ClientError as err:
                    # You can't always get the logs of pods (i.e. in Pending state or Evicted) so
                    # try and craft a useful generic message to inform what went wrong.
                    log.warning("Failed to get logs from %s/Pod/%s: %s",
                                self.namespace, pod.metadata.name, err)

                # We won't raise a RuntimeError for a pod still in the `Pending` or `Running` phases
                # because we don't want to predict the future. The caller should raise an error if
                # it feels the pod should be finished. This allows us to be called in a
                # finally-block as a means of logging useful information about an ephemeral pod.
                status = pretty_status(pod)
                if pod.status.phase in {"Pending", "Running"}:
                    log.error("%s/Pod/%s is still %s:\n%s",
                              self.namespace,
                              pod.metadata.name,
                              pod.status.phase,
                              status)
                else:
                    msg = "{}/Pod/{} terminated unsuccessfully:\n{}".format(self.namespace,
                                                                            pod.metadata.name,
                                                                            status)
                    raise RuntimeError(msg)

    @retry_kubernetes(retry_on_timeout=True)
    def get_pod(self, name):
        response = self.core_api.read_namespaced_pod(name, self.namespace)
        return response

    @retry_kubernetes(retry_on_timeout=True)
    def delete_pod(self, name):
        response = self.core_api.delete_namespaced_pod(name, self.namespace)

        # Deleting a Pod doesn't happen instantly. The containers are sent a shutdown signal and
        # given a chance to terminate gracefully. However, we want a synchronous call that will
        # return when the resource is actually gone in the event we want to turn around and
        # re-create it.
        watcher = watch.Watch()
        for event in watcher.stream(
            self.core_api.list_namespaced_pod,
            self.namespace,
            field_selector="metadata.name={}".format(name),
            resource_version=response.metadata.resource_version,
            timeout_seconds=420,
        ):
            log.debug("got event: %s", event)
            if event["type"] == "DELETED":
                return response  # it has been completely deleted
        raise TimeoutError("Timed out deleting Pod: {}/{}".format(self.namespace, name))

    def wait_for_pod_completion(self, name, timeout=60, poll_interval=3, raise_on_failure=False):
        """
        Waits `timeout` seconds for the pod with `name to reach a terminal state by checking its
        status every `poll_interval` seconds. `Unknown` is considered a terminal state by this
        function. If `raise_on_failure` is set, we will raise an error if the pod terminated but not
        with a successful status.

        Raises: TimeoutError if the pod does not complete in `timeout` seconds
                RuntimeError if the pod does not complete with success (and raise_on_failure is set)
        """
        # TODO convert to using a watcher so we are less heavy on the API.
        def pod_not_running(*args):
            resp = self.get_pod(name)
            log.debug("Pod status: %s", resp.status)
            if resp.status.phase == "Unknown":
                log.warning("Pod '%s' is in 'Unknown' phase; assuming it is not running", name)
            return resp.status.phase not in {"Running", "Pending"}

        try:
            wait_for(pod_not_running, max_retry_delay=poll_interval, timeout=timeout)
        finally:
            if raise_on_failure:
                pod = self.get_pod(name)
                log.debug("%s/pod/%s status: %s", self.namespace, name, pod.status)
                self.check_successful_run(pod)

    def wait_for_deployment_rollout(
        self,
        name,
        timeout=900,
        max_retry_delay=DEFAULT_MAX_RETRY_DELAY,
    ):
        # https://github.com/kubernetes/kubectl/blob/7b01e2757cc74b1145976726b05cc1108ad2911d/pkg/cmd/rollout/rollout_status.go
        @retry_kubernetes(retry_on_timeout=True)
        def checker(*args):
            try:
                deployment = self.apps_api.read_namespaced_deployment_status(
                    name, self.namespace
                )
            except ClientError as err:
                if err.status != codes.NOT_FOUND:
                    raise
                logd.warning(
                    "Deployment is not found after creation",
                    extra={
                        "deployment_name": name,
                        "namespace_id": self.namespace,
                    },
                )
                return False
            # Too early to perform check
            if not deployment.status.conditions:
                logd.info(
                    "Deployment has not started progressing yet",
                    extra={
                        "deployment_name": name,
                        "namespace_id": self.namespace,
                    },
                )
                return False
            cond = [
                cond
                for cond in deployment.status.conditions
                if cond.type == "Progressing"
            ]
            if cond and cond[0].reason == "ProgressDeadlineExceeded":
                # The caller specified a specific timeout for this rollout which we will honor;
                # this deadline being exceeded is just a good thing to log as it may lead to an
                # eventual timeout.
                conditions = "\n\t".join(c.message for c in deployment.status.conditions)
                logd.warning(
                    "Deployment is not progressing in a timely manner (exceeded deadline):\n\t%s",
                    conditions,
                    extra={
                        "deployment_name": name,
                        "namespace_id": self.namespace,
                    },
                )
                return False
            replicas = deployment.spec.replicas
            if not deployment.status.updated_replicas:
                logd.info(
                    "Don't have enough info about deployment status to process check",
                    extra={
                        "namespace_id": self.namespace,
                        "deployment_name": name,
                        "updated_replicas": deployment.status.updated_replicas,
                        "replicas": replicas,
                    },
                )
                return False
            if replicas and deployment.status.updated_replicas < replicas:
                logd.info(
                    "Waiting for deployment rollout to finish, wait for new replicas",
                    extra={
                        "namespace_id": self.namespace,
                        "deployment_name": name,
                        "updated_replicas": deployment.status.updated_replicas,
                        "replicas": replicas,
                    },
                )
                return False
            if deployment.status.replicas > deployment.status.updated_replicas:
                logd.info(
                    "Waiting for deployment rollout to finish, old replicas pending termination.",
                    extra={
                        "namespace_id": self.namespace,
                        "deployment_name": name,
                        "updated_replicas": deployment.status.updated_replicas,
                        "replicas": deployment.status.replicas,
                    },
                )
                return False
            if not deployment.status.available_replicas:
                logd.info(
                    "Don't have enough info about new replicas availability",
                    extra={
                        "namespace_id": self.namespace,
                        "deployment_name": name,
                        "updated_replicas": deployment.status.updated_replicas,
                        "replicas": deployment.status.available_replicas,
                    },
                )
                return False
            if (
                deployment.status.available_replicas
                < deployment.status.updated_replicas
            ):
                logd.info(
                    "Waiting for deployment rollout to finish, wait for new replicas availability.",
                    extra={
                        "namespace_id": self.namespace,
                        "deployment_name": name,
                        "updated_replicas": deployment.status.updated_replicas,
                        "available_replicas": deployment.status.available_replicas,
                    },
                )
                return False
            log.info(
                "Deployment successfully rolled out.",
                extra={
                    "deployment_name": name,
                    "namespace_id": self.namespace,
                },
            )
            return True

        # Default value in cluster is 600 Deployment should return status with
        # ProgressDeadlineExceeded after progressDeadlineSeconds. Adding twice the max retry delay
        # so we don't timeout earlier.
        log.info("Waiting for deployment to rollout: %s/%s", self.namespace, name)
        wait_for(
            checker,
            timeout=timeout,
            initial_delay=DEPLOYMENT_CHECK_DELAY,
            max_retry_delay=max_retry_delay,
        )

    @retry_kubernetes(retry_on_timeout=True)
    def get_deployments(self, label_selector):
        response = self.apps_api.list_namespaced_deployment(
            namespace=self.namespace, label_selector=label_selector
        )
        return response

    @retry_kubernetes(retry_on_timeout=True)
    def get_deployment(self, name):
        response = self.apps_api.read_namespaced_deployment(name, self.namespace)
        return response

    @retry_kubernetes()
    def update_deployment(self, name, body, timeout=900):
        """Update a deployment."""
        response = self.apps_api.patch_namespaced_deployment(
            name, self.namespace, body=body
        )
        log.debug("updated deployment", extra=dict(response=response))
        try:
            self.wait_for_deployment_rollout(
                # We want to be a little more responsive so half the max wait time
                name, timeout=timeout, max_retry_delay=math.ceil(DEFAULT_MAX_RETRY_DELAY/2)
            )
        except (TimeoutError, KeyboardInterrupt):
            log.info("Timed out waiting for Deployment to update; issuing roll-back...")
            self.rollback_deployment(name)
            raise

    @retry_kubernetes()
    def rollback_deployment(self, name):
        """
        Rolls back a named Deployment to its previous ReplicaSet. We don't wait for the rollback
        to complete.
        """
        deployment = self.get_deployment(name)
        selector = make_selector(deployment.spec.selector.match_labels)
        # This logic is inspired by the code for `kubectl rollout undo <deployment>`
        revision_key = "deployment.kubernetes.io/revision"

        associated_replica_sets = self.apps_api.list_namespaced_replica_set(
            namespace=self.namespace,
            label_selector=selector,
        )

        revision_ordered_replica_sets = sorted(
            associated_replica_sets.items,
            key=lambda e: e.metadata.annotations[revision_key],
            reverse=True
        )
        log.debug("found ReplicaSet(s):\n\t%s",
                  "\n\t".join(e.metadata.name for e in revision_ordered_replica_sets))

        rollback_replica_set = (
            revision_ordered_replica_sets[0]
            if len(revision_ordered_replica_sets) == 1
            else revision_ordered_replica_sets[1]
        )

        rollback_revision_number = rollback_replica_set.metadata.annotations[revision_key]
        log.info("Rolling back deployment %s to revision %s: %s",
                 name, rollback_revision_number, rollback_replica_set.metadata.name)
        patch = [
            {
                "op": "replace",
                "path": "/spec/template",
                "value": rollback_replica_set.spec.template
            },
            {
                "op": "replace",
                "path": "/metadata/annotations/{}".format(json_pointer(revision_key)),
                "value": rollback_revision_number,
            }
        ]

        log.debug("rolling back deployment %s:\n%s", name, patch)
        self.apps_api.patch_namespaced_deployment(
            body=patch,
            name=name,
            namespace=self.namespace
        )

    @retry_kubernetes()
    def get_pod_log(self, name, **kwargs):
        return self.core_api.read_namespaced_pod_log(name=name, namespace=self.namespace, **kwargs)

    @retry_kubernetes()
    def follow_pod_logs(self, name, handler):
        """Attaches to the log stream of a pod and follows it, calling the passed `handler` function
        with each line of output. The `handler` function should consume a single argument which will
        be one or more lines of output from the pod. The `handler` can raise a `StopIteration`
        exception to stop streaming the logs, otherwise streaming will end when the pod terminates.
        """
        watcher = watch.Watch()
        log.debug("Setting up watcher for pod/%s/%s", self.namespace, name)
        for line in watcher.stream(self.core_api.read_namespaced_pod_log, name=name,
                                   namespace=self.namespace):
            try:
                handler(line)
            except StopIteration:
                log.debug("Got stop signal; shutting down watcher")
                watcher.stop()


def get_client(**kwargs):
    return K8sClient.from_config(**kwargs)

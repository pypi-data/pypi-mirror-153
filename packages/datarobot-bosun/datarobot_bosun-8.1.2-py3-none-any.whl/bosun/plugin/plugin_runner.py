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

import argparse
import importlib
import inspect
import logging
import logging.config
import os
import pprint
import signal
import sys
import textwrap
from collections import OrderedDict

import yaml

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.action_status import ActionStatus
from bosun.plugin.action_status import ActionStatusInfo
from bosun.plugin.constants import BosunPluginActions
from bosun.plugin.constants import BosunPluginConfigConstants
from bosun.plugin.constants import DeploymentInfoConfigConstants
from bosun.plugin.constants import PeInfoConfigConstants

# TODO: add ability for plugin to generate private config file template
# TODO: add ability for plugin to generate plugin description
# TODO: A test to verify gen-config option
# TODO: change bosun python package to datarobot-bosun (bosun is already used on pip).
# TODO: pass pe_info config to pe_status
# TODO: fix filesystem plugin to return status for all deployments in pe_info status


class PluginRunner:
    description = """
        Run a Bosun deployment plugin and provide configuration and action to the plugin to use.
        The plugin is provided as a python file that contains a class that implement
        the BosunPluginBase base class.

        The plugin runner contains the following built in plugins:
        1. test - a plugin that simply sleep for some time and print info to the
           logs about the provided action.
        2. docker - a plugin that runs a container of PPS
        3. filesystem - a plugin that copies a model into a directory structure

        To get a list of the builtin plugins use the --list-plugins option.

        If you would like to use any of the builtin plugins, just use the above name in the
        --plugin command line option.

        If your plugin was installed as a python module (using pip), you can provide the name
        of the module that contains the plugin class. For example --plugin sample_plugin.my_plugin

        If your plugin is in a directory, you can provide the name of the plugin as the path to the
        file that contains your plugin class. For example:  --plugin sample_plugin/my_plugin.py
    """

    builtin_plugins = OrderedDict([
        ("test", {"module": "bosun.plugin.bosun_test_plugin", "names": ["test"]}),
        ("filesystem", {"module": "bosun.plugin.filesystem.filesystem_plugin",
                        "names": ["filesystem_plugin", "filesystem"]}),
        ("docker", {"module": "bosun.plugin.docker.docker_plugin",
                    "names": ["docker-plugin", "docker"]}),
        ("s3", {"module": "bosun.plugin.s3.s3_plugin", "names": ["s3_plugin", "s3"]}),
        ("k8s", {"module": "bosun.plugin.k8s.kubernetes_plugin",
                 "names": ["k8s-plugin", "k8s", "kubernetes"]}),
    ])

    def __init__(self, plugin, config_file, private_config_file, action, status_file, dry_run):
        self._plugin = plugin
        self._config_file = config_file
        self._private_config_file = private_config_file
        self._action = action
        self._status_file = status_file
        self._dry_run = dry_run
        self._logger = logging.getLogger("{}.{}".format(self.__class__.__module__,
                                                        self.__class__.__name__))

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description=textwrap.dedent(PluginRunner.description))

        parser.add_argument("--logfile", default=None,
                            help="Path to log file")
        parser.add_argument("--log-level",
                            default="INFO",
                            type=str.upper,
                            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                            help="Set the logging level")
        parser.add_argument("--log-config", default=None,
                            help="Path to a YAML file to be used for configuring python logging."
                                 " If this option is provided, the --logfile, --loglevel"
                                 " options will not be used")
        parser.add_argument("--plugin", help="Plugin to use")
        parser.add_argument("--config", help="Configuration file to use")
        parser.add_argument("--private-config",
                            help="Private configuration file used directly by plugin")
        parser.add_argument("--action", help="Action to perform - see --list-actions for a list "
                                             "of supported actions")
        parser.add_argument("--status-file", help="Where to write the status of the action (YAML)")
        parser.add_argument("--show-status", action="store_true",
                            help="Print status file at end of run. This should only be used when "
                                 "locally developing or debugging a plugin")
        parser.add_argument("--exit-codes", action="store_true",
                            help="Exit with a status based on the ActionStatus returned by the "
                                 "Action -- non-zero for all but `OK`.")
        parser.add_argument("--list-actions", action="store_true",
                            help="List all plugin actions", default=False)
        parser.add_argument("--dry-run", action="store_true", default=False,
                            help="Dry run mode, not performing any action")
        parser.add_argument("--gen-config", metavar="FILE", action="store",
                            default=None, const="-", nargs="?",
                            help="Generate an action config file example."
                                 "If an argument is provided then the config file will be saved"
                                 "to the file provided, otherwise printed to STDOUT."
                                 "Edit the config file to suite your needs")
        parser.add_argument("--list-plugins", action="store_true", default=False,
                            help="List the builtin bosun deployment plugins")

        options = parser.parse_args()
        if options.gen_config is None and options.list_actions is False  \
                and options.list_plugins is False and (
                options.plugin is None or
                options.config is None or
                options.action is None or
                options.status_file is None):
            print("Error: arguments --plugin --config --action --status-file are required")
            sys.exit(1)
        return options

    @staticmethod
    def get_configs(config_file, logger, requires_deployment_config=False):
        with open(config_file) as config_fh:
            config = yaml.safe_load(config_fh)
            logger.debug(pprint.pformat(config))

            if BosunPluginConfigConstants.PLUGIN_CONFIG_KEY not in config:
                raise Exception("Missing {} section in configuration yaml".format(
                    BosunPluginConfigConstants.PLUGIN_CONFIG_KEY))
            plugin_config = config[BosunPluginConfigConstants.PLUGIN_CONFIG_KEY]

            # Taking api token from environment and adding to plugin_config if present
            if BosunPluginConfigConstants.MLOPS_API_TOKEN_ENV in os.environ:
                plugin_config[BosunPluginConfigConstants.MLOPS_API_TOKEN_KEY] = os.environ[
                    BosunPluginConfigConstants.MLOPS_API_TOKEN_ENV]

            if PeInfoConfigConstants.PE_INFO_KEY not in config:
                raise Exception("Missing {} section in configuration yaml".format(
                    PeInfoConfigConstants.PE_INFO_KEY))
            pe_info = config[PeInfoConfigConstants.PE_INFO_KEY]

            deployment_info = None
            if DeploymentInfoConfigConstants.DEPLOYMENT_INFO_KEY in config:
                deployment_info = config[DeploymentInfoConfigConstants.DEPLOYMENT_INFO_KEY]

            if requires_deployment_config:
                if deployment_info is None:
                    raise Exception("{} section is missing in configuration".format(
                        DeploymentInfoConfigConstants.DEPLOYMENT_INFO_KEY
                    ))
            return plugin_config, pe_info, deployment_info

    def _get_builtin_plugin_by_name(self, plugin_name):
        for plugin in PluginRunner.builtin_plugins:
            if plugin_name in PluginRunner.builtin_plugins[plugin]["names"]:
                return PluginRunner.builtin_plugins[plugin]
        return None

    def _load_plugin_from_file(self, plugin_file_path):

        plugin_file_path = os.path.splitext(plugin_file_path)[0]
        module_dir = os.path.dirname(plugin_file_path)
        orig_module_name = plugin_file_path
        module_name = os.path.basename(plugin_file_path)

        self._logger.debug("Trying to load plugin from directory: {}".format(module_dir))
        if len(module_dir) > 0:
            sys.path.insert(0, module_dir)
            self._logger.debug("Added {} to path. Trying to import {}".format(
                module_dir, os.path.basename(module_name)))
            plugin_module = importlib.import_module(module_name)
            self._logger.debug("Module successfully loaded")
            return plugin_module, module_name
        else:
            self._logger.error("Failed to load module: {}".format(orig_module_name))

            self._logger.error("And no directory structure was detected in module name {}"
                               .format(orig_module_name))
            sys.exit(1)

    def load_plugin_object(self, module_name, plugin_config, private_config_file, pe_info):
        try:
            plugin_module = importlib.import_module(module_name)
            self._logger.debug("Plugin was loaded using import statement")
        except ImportError:
            if not os.path.exists(module_name):
                raise
            plugin_module, module_name = self._load_plugin_from_file(module_name)

        possible_plugins = []
        for name, obj in inspect.getmembers(plugin_module):
            self._logger.debug(name)
            if inspect.isclass(obj):
                self._logger.debug("Class: {}  module: {}".format(obj, obj.__module__))
                if issubclass(obj, BosunPluginBase) and obj.__module__ == module_name:
                    self._logger.debug("Plugin class: {}".format(obj))
                    possible_plugins.append(obj)
        if len(possible_plugins) == 0:
            raise Exception(
                "No plugin implementation was detected in module: {}".format(module_name))

        if len(possible_plugins) > 1:
            raise Exception("Too many implementations of bosun plugin detected: {}"
                            .format(possible_plugins))

        return possible_plugins[0](plugin_config, private_config_file, pe_info, self._dry_run)

    def run(self):

        logger = logging.getLogger("main")

        require_deployment_info = True if self._action in \
            BosunPluginActions.require_deployment_info() else False
        plugin_config, pe_info, deployment_info = self.get_configs(self._config_file,
                                                                   logger,
                                                                   require_deployment_info)
        try:
            plugin_info = self._get_builtin_plugin_by_name(self._plugin)
            plugin_module = plugin_info["module"] if plugin_info else self._plugin
            pbe = self.load_plugin_object(
                plugin_module, plugin_config, self._private_config_file, pe_info
            )
        except Exception as e:
            msg = "Exception occurred while loading plugin object for action {}: error {}"\
                .format(self._action, e)
            logger.exception(msg)
            action_status = ActionStatusInfo(ActionStatus.ERROR, msg=msg, state="errored")

            action_status.write_to_file(status_file=self._status_file)
            return

        pbe.run_action(self._action, deployment_info, status_file=self._status_file)


action_to_config = {
    BosunPluginActions.PLUGIN_START: "plugin_start_config.yaml",
    BosunPluginActions.PLUGIN_STOP:  "plugin_stop_config.yaml",
    BosunPluginActions.PE_STATUS: "pe_status_config.yaml",
    BosunPluginActions.DEPLOYMENT_START: "deployment_start_config.yaml",
    BosunPluginActions.DEPLOYMENT_STOP: "deployment_stop_config.yaml",
    BosunPluginActions.DEPLOYMENT_LIST: "deployment_list_config.yaml",
    BosunPluginActions.DEPLOYMENT_STATUS: "deployment_status_config.yaml",
    BosunPluginActions.DEPLOYMENT_REPLACE_MODEL: "deployment_replace_model_config.yaml",
}


def gen_config_sample(config_file, action):
    of = sys.stdout
    if config_file != "-":
        of = open(config_file, "w")

    if action not in action_to_config:
        print("Unable to generate a sample config file for action: {}".format(action))
        raise SystemExit(1)

    print("# The following is an example of plugin configuration file", file=of)
    print("# for action: {}".format(action), file=of)
    print("#----------------------------------------------------------", file=of)
    print("", file=of)

    from . import config_samples  # relative-import the *package* containing the templates
    sample_content = pkg_resources.read_text(config_samples, action_to_config[action])
    print(textwrap.dedent(sample_content), file=of)


def set_logging(options):
    if options.log_config:
        with open(options.log_config, "r") as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.root.setLevel(options.log_level)
        if options.logfile:
            handler = logging.FileHandler(options.logfile)
        else:
            handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(options.log_level)
        formatter = logging.Formatter("%(asctime)s %(levelname)s: %(name)s %(message)s")
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)


def main():
    options = PluginRunner.parse_args()
    set_logging(options)
    if options.gen_config:
        if options.action is None:
            print("Error: Please use --action [ACTION] to specify for which action to generate "
                  "sample config")
            raise SystemExit(1)
        gen_config_sample(options.gen_config, options.action)
    elif options.list_plugins:
        for plugin_info in PluginRunner.builtin_plugins.values():
            print(",".join(plugin_info["names"]))
    elif options.list_actions:
        print("\n".join(BosunPluginActions.all_actions()))
    else:
        # Running an action
        signal.signal(signal.SIGTERM, handle_shutdown_signal)
        PluginRunner(plugin=options.plugin,
                     config_file=options.config,
                     private_config_file=options.private_config,
                     action=options.action,
                     status_file=options.status_file,
                     dry_run=options.dry_run).run()
        if options.show_status:
            with open(options.status_file) as sf:
                status_str = sf.read(4096)
                print("\n-- action status --")
                print(status_str)

        if options.exit_codes:
            status = yaml.safe_load(open(options.status_file))["status"]
            raise SystemExit(ActionStatus.to_numeric[status])


def handle_shutdown_signal(*args):
    logging.info("Got signal; starting shutdown")
    raise KeyboardInterrupt


if __name__ == "__main__":
    main()

"""This module contains the configurator for midas scenarios."""
import os
import pprint
from importlib import import_module

from midas.scenario import LOG
from midas.util.config_util import get_config_files, load_configs, normalize

# from midas.tools import config
from midas.util.dict_util import convert, update

# from midas.util.logging_util import setup_logging
from midas.util.runtime_config import RuntimeConfig
from ruamel.yaml import YAML

MODULES = [
    ("powergrid", "PowergridModule"),
    ("sbdata", "SimbenchDataModule"),
    ("sndata", "SmartNordDataModule"),
    ("comdata", "CommercialDataModule"),
    ("dlpdata", "DLPDataModule"),
    ("pwdata", "PVWindDataModule"),
    ("bhvdata", "BremerhavenDataModule"),
    ("weather", "WeatherDataModule"),
    ("der", "PysimmodsModule"),
    ("goa", "GridOperatorModule"),
    ("messages", "MessagesModule"),
]


class Configurator:
    """This is the main configurator for midas scenarios.

    The configurator takes at least a scenario name to create a fully-
    configured mosaik scenario.

    Parameters
    ----------
    scenario_name : str
        A *str* containing the name of the scenario_name which should
        be run.
    params : dict
        A *dict* with the pre-configuration for the scenario.
        Can be empty.
    config : str
        A *string* containing the path to a custom config file.

    Attributes
    ----------
    custom_cfg : str
        Stores the path to the custom configuration if provided
    params : dict
        A *dict* containing the configuration of the scenario. The dict
        is extended during the configuration.
    scenario : dict
        A *dict* containing references to everything that is created
        during the configuration of the senario.
    scenario_name : str
        The name of the scenario created

    """

    def __init__(self, inipath=None, datapath=None, autocfg=False):
        self.scenario_name: str
        self.params: dict
        self.custom_cfgs: list
        self.scenario: dict

    def configure(
        self,
        scenario_name,
        params,
        custom_cfgs=None,
        no_script=False,
        no_yaml=False,
    ):
        """Configure the midas scenario.

        Will use the information provided during initialization.

        Parameters
        ----------
        scenario_name: str
            The name of the scenario to run. This is a toplevel key in
            a scenario file.
        params: dict
            A dict containing parameters that should overwrite values
            from the scenario file.
        custom_cfgs: List[str], optional
            A list containing paths to additional scenario files.
        no_script: bool, optional
            If set to True, no autoscript file will be generated.
        no_yaml: bool, optional
            If set to True, the full configuration will not be saved as
            new yaml file.

        Returns
        -------
        dict
            A *dict* containing everything that was defined during
            configuration.

        """
        LOG.info(
            "Starting configuration of the scenario '%s'...", scenario_name
        )
        self.scenario_name = scenario_name
        self.params = params
        self.custom_cfgs = custom_cfgs

        files = get_config_files(self.custom_cfgs)

        if len(files) == 0:
            LOG.error("No configuration files found. Aborting!")
            return dict()

        configs = load_configs(files)
        if len(configs) <= 0:
            LOG.error(
                "Something went wrong during loading the config files. "
                "Please consult the logs to find the reason. Aborting!"
            )
            return dict()

        params = self._organize_params(configs)
        self.scenario = {"scenario_name": self.scenario_name}
        self._apply_modules(self.scenario, params)

        if not no_yaml:
            self._save_config(self.scenario_name, params)
        if not no_script:
            self._save_script(self.scenario["script"])
        LOG.info("Configuration finished.")
        return self.scenario

    def run(self):
        """Run the scenario configured before."""

        if self.scenario is None:
            LOG.error(
                "Scenario is not configured. "
                "Maybe you forgot to call configure?"
            )
            return

        LOG.info("Starting the scenario ...")
        self.scenario["world"].run(
            until=self.scenario["end"],
            print_progress=not self.params["silent"],
        )
        LOG.info("Scenario finished.")

    def _organize_params(self, configs):
        """Sort params in correct order."""
        try:
            cfg_chain = [configs[self.scenario_name]]
        except KeyError as k_e:
            LOG.critical(
                "%s not found in config files. Cannot process any further.",
                self.scenario_name,
            )
            raise k_e

        parent = cfg_chain[0].get("parent", None)
        while parent is not None and parent != "None":
            cfg_chain.append(configs[parent])
            parent = cfg_chain[-1].get("parent", None)

        LOG.debug("Ordering the configs ...")
        modules = list()
        final_params = dict()
        for cfg in reversed(cfg_chain):
            modules += cfg["modules"]
            update(final_params, cfg)
        final_params["modules"] = modules

        update(final_params, self.params)
        LOG.debug("Normalizing the config ...")
        normalize(final_params)

        return final_params

    def _save_config(self, name, params):
        """Save a copy of the current config."""
        yaml = YAML(typ="safe", pure=True)
        path = os.path.join(
            RuntimeConfig().paths["output_path"], f"{name}_cfg.yml"
        )
        params = convert(params)
        LOG.debug("Current config is %s.", pprint.pformat(params))
        LOG.info("Saving current config to %s.", path)
        with open(path, "w") as cfg_out:
            yaml.indent(mapping=4, sequence=6, offset=3)
            yaml.dump({"myconfig": params}, cfg_out)

    def _save_script(self, script):
        fname = os.path.join(
            RuntimeConfig().paths["output_path"],
            f"{self.scenario_name}_auto_script.py",
        )
        fctn = ""
        order = [
            "imports",
            "definitions",
            "simconfig",
            "sim_start",
            "model_start",
            "connects",
            "world_start",
        ]
        for part in order:
            for line in script[part]:
                fctn += line
            fctn += "\n"
        with open(fname, "w") as sfile:
            sfile.write(fctn)

    def _apply_modules(self, scenario, params):
        """Apply all required modules in the correct order."""

        LOG.debug("Creating base configuration.")
        base = import_module("midas.scenario.modules.base")
        scenario = base.configure(scenario, params)

        LOG.debug("Attempt to add database.")
        if scenario["with_db"]:
            from midas.scenario.modules.database import DatabaseModule

            DatabaseModule().upgrade(scenario, params)
        LOG.debug("Attempt to add time simulator.")
        if scenario["with_timesim"]:
            from midas.scenario.modules.timesim import TimeSimModule

            TimeSimModule().upgrade(scenario, params)

        LOG.debug("Now adding further modules (if any).")
        for (module, clazz) in MODULES:
            # Preserve ordering of modules
            if module in params["modules"]:
                LOG.debug("Adding module %s.", module)
                mod = import_module(f"midas.scenario.modules.{module}")
                getattr(mod, clazz)().upgrade(scenario, params)

        self._apply_custom_modules(scenario, params)

        scenario["params"] = params
        scenario["script"]["definitions"].append(
            f"sensors = {scenario['sensors']}\n"
        )
        scenario["script"]["definitions"].append(
            f"actuators = {scenario['actuators']}\n"
        )
        return scenario

    def _apply_custom_modules(self, scenario, params):
        if "custom_modules" not in params:
            return
        if params["custom_modules"] is None:
            return

        LOG.debug(
            "Trying to load %d custom module(s) ...",
            len(params["custom_modules"]),
        )
        for (module, cmod) in params["custom_modules"]:
            # All custom module are loaded
            if ":" in cmod:
                mod, clazz = cmod.split(":")
            else:
                mod, clazz = cmod.rplit(".", 1)
            LOG.debug("Adding module %s.", module)
            mod = import_module(mod)
            getattr(mod, clazz)().upgrade(scenario, params)

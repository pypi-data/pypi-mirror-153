"""This module contains the abstract base class for all upgrade
modules. Provides a basic workflow for the definition of new
upgrades.

"""
import logging
from abc import ABC, abstractmethod

LOG = logging.getLogger(__name__)


class UpgradeModule(ABC):
    """Base class for upgrade modules."""

    def __init__(self, name, log=None):
        self.name = name
        self.world = None
        self.scenario = None
        self.params = None
        self.sim_params = None
        self.sim_key = None
        self.sim_name = None
        # self.sim_names = dict()

        if log is None:
            self.logger = LOG
        else:
            self.logger = log

    def upgrade(self, scenario, params):
        """Upgrade the scenario with this module.

        Adds the functionality provided by this upgrade to the
        scenario, i.e., define and start a simulator in the mosaik
        world, instantiate models, and add connections to other
        existing models.

        Parameters
        ----------
        scenario : dict
            The scenario *dict* containing reference to everything
            created in former upgrades.
        params : dict
            A *dict* containing the content of the config files and
            additional information generated during other upgrades.

        """
        self.world = scenario["world"]
        self.scenario = scenario
        self.params = params
        module_params = self.check_module_params()

        for sim_name, sim_params in module_params.items():
            if not isinstance(sim_params, dict):
                continue

            # self.sim_names[sim_name] = sim_params
            self.sim_name = sim_name
            self.sim_params = sim_params

            self.check_sim_params(module_params)

            self._start_simulator()

            self.start_models()

            self.connect()
            if params["arl"]:
                self.get_sensors()
                self.get_actuators()

            if scenario["with_db"]:
                self.connect_to_db()

            if scenario["with_timesim"]:
                self.connect_to_timesim()

    @abstractmethod
    def check_module_params(self):
        """Is called from within the upgrade method."""
        raise NotImplementedError

    @abstractmethod
    def check_sim_params(self, module_params, **kwargs):
        """Is called from within the upgrade method."""
        raise NotImplementedError

    def _start_simulator(self):
        """Start a certain simulator instance."""

        cmd = self.sim_params.pop("cmd")
        import_str = self.sim_params.pop("import_str")
        # Place model in the world's *sim_config*
        self.world.sim_config[self.sim_params["sim_name"]] = {cmd: import_str}
        self.scenario["script"][
            "simconfig"
        ] = f"sim_config = {self.world.sim_config}\n"

        # Create a unique simulator key
        self.sim_key = f"{self.name}_{self.sim_params['sim_name']}_sim".lower()

        # Start the simulator if it was not started before
        if self.sim_key not in self.scenario:
            self.scenario[self.sim_key] = self.world.start(**self.sim_params)
            self.logger.debug(
                "Started simulator %s (key: %s).",
                getattr(self.scenario[self.sim_key], "_sim").sid,
                self.sim_key,
            )
            self.scenario["script"]["definitions"].append(
                f"{self.sim_key}_params = {self.sim_params}\n"
            )
            self.scenario["script"]["sim_start"].append(
                f"{self.sim_key} = world.start(**{self.sim_key}_params)\n"
            )
        self.sim_params["cmd"] = cmd
        self.sim_params["import_str"] = import_str

    @abstractmethod
    def start_models(self):
        raise NotImplementedError

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def connect_to_db(self):
        raise NotImplementedError

    def connect_to_timesim(self):
        pass

    def start_model(self, mod_key, mod_name, params):
        self.scenario[mod_key] = getattr(
            self.scenario[self.sim_key], mod_name
        )(**params)
        self.logger.debug(
            "Created model %s (key: %s).",
            self.scenario[mod_key].full_id,
            mod_key,
        )

        self.scenario["script"]["definitions"].append(
            f"{mod_key}_params = {params}\n"
        )
        self.scenario["script"]["model_start"].append(
            f"{mod_key} = {self.sim_key}.{mod_name}(**{mod_key}_params)\n"
        )

    def connect_entities(self, from_entity, to_entity, attrs, **kwargs):
        """Connect the *attrs* of two entities."""
        self.world.connect(from_entity, to_entity, *attrs, **kwargs)
        # if key_value_logs:

        # else:
        self.logger.debug(
            "Connected %s to %s (%s).",
            from_entity.full_id,
            to_entity.full_id,
            attrs,
        )

    def connect_entities2(self, from_ent_key, to_ent_key, attrs, **kwargs):
        from_entity = self.scenario[from_ent_key]
        to_entity = self.scenario[to_ent_key]
        self.world.connect(from_entity, to_entity, *attrs, **kwargs)
        self.logger.debug(
            "Connected %s to %s (%s).",
            from_entity.full_id,
            to_entity.full_id,
            attrs,
        )
        self.scenario["script"]["connects"].append(
            f"world.connect({from_ent_key}, {to_ent_key}, *{attrs}, "
            f"**{kwargs})\n"
        )

    def get_sensors(self):
        pass

    def get_actuators(self):
        pass

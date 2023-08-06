import logging

from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class BlackstartModule(UpgradeModule):
    """Blackstart agents upgrade module for MIDAS."""

    def __init__(self, name="blackstart"):
        super().__init__(name, LOG)

        self.default_name = "midasmv"
        self.default_sim_name = "BlackstartAgents"
        self.default_import_str = (
            "blackstart.blackstart_mas.mango_mosaik_api:MangoSimulator"
        )
        self.models = dict()
        self.port_off = 0

    def check_module_params(self):
        """Check the module params and provide default values."""
        module_params = self.params.setdefault(f"{self.name}_params", dict())
        if not module_params:
            LOG.debug(
                "No configuration provided. Creating default configuration."
            )
            module_params.setdefault(self.default_name, dict())

        module_params.setdefault("sim_name", self.default_sim_name)
        module_params.setdefault("cmd", "python")
        module_params.setdefault("import_str", self.default_import_str)
        module_params.setdefault("step_size", self.scenario["step_size"])
        module_params.setdefault("start_date", self.scenario["start_date"])
        module_params.setdefault("host", "localhost")
        module_params.setdefault("port", 5655)
        module_params.setdefault("check_inbox_interval", 0.1)
        module_params.setdefault(
            "schedule_length",
            int(
                self.scenario["forecast_horizon_hours"]
                * 3600
                / module_params["step_size"]
            ),
        )
        return module_params

    def check_sim_params(self, module_params, **kwargs):
        """Check the params for a certain simulator instance."""
        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("host", module_params["host"])
        self.sim_params.setdefault(
            "port", int(module_params["port"]) + self.port_off
        )
        self.port_off += 1
        self.sim_params.setdefault("check_inbox_interval", 0.1)
        self.sim_params.setdefault(
            "schedule_length", module_params["schedule_length"]
        )
        self.sim_params.setdefault("holon_topology", create_default_topology())
        self.sim_params.setdefault("der_mapping", create_default_der_mapping())
        self.sim_params.setdefault(
            "load_mapping", create_default_load_mapping()
        )
        self.sim_params.setdefault(
            "switch_mapping", create_default_switch_mapping()
        )
        self.sim_params.setdefault("bc_agent_id", "BlackstartSwitchAgent-7")
        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        if self.scenario["deny_rng"]:
            self.sim_params["seed"] = 0
        else:
            self.sim_params.setdefault(
                "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
            )

    def start_models(self):
        """Start all models defined in the mapping of a certain simulator."""
        mod_ctr = 0
        model = "BlackstartUnitAgent"
        for _ in self.sim_params["der_mapping"]:

            mod_key = self.gen_mod_key(model.lower(), mod_ctr)
            mod_params = {
                "check_inbox_interval": self.sim_params["check_inbox_interval"]
            }
            self.start_model(mod_key, model, mod_params)
            mod_ctr += 1

        for _ in self.sim_params["load_mapping"]:
            mod_key = self.gen_mod_key(model.lower(), mod_ctr)
            mod_params = {
                "check_inbox_interval": self.sim_params["check_inbox_interval"]
            }
            self.start_model(mod_key, model, mod_params)
            mod_ctr += 1

        model = "BlackstartSwitchAgent"
        for _ in self.sim_params["switch_mapping"]:
            mod_key = self.gen_mod_key(model.lower(), mod_ctr)
            mod_params = {
                "check_inbox_interval": self.sim_params["check_inbox_interval"]
            }
            self.start_model(mod_key, model, mod_params)
            mod_ctr += 1

    def connect(self):
        """Connect the models to existing other models."""
        print("Now connecting models.")
        mod_ctr = 0
        mod_ctr = self._connect_to_ders(mod_ctr)
        mod_ctr = self._connect_to_loads(mod_ctr)
        self._connect_to_switches(mod_ctr)

        # Define connections for unit agents

        # for pv, unit_agent in zip(pv_models, unit_agents):
        #     world.connect(pv, unit_agent, "flexibilities")
        #     world.connect(
        #         unit_agent,
        #         pv,
        #         "schedule",
        #         time_shifted=True,
        #         initial_data={"schedule": None},
        #     )

        # # Define connections for load agents
        # for load, load_agent in zip(load_models, load_agents):
        #     bus_number = household_params["household_mapping"][load.eid]
        # ["bus"]
        #     world.connect(loads[bus_number], load_agent, "p_mw")

        # # Define connections for switch agents
        # for switch_agent in switch_agents:
        #     for switch in mas_params["switch_mapping"][switch_agent.eid][
        #         "adjacent_switches"
        #     ].keys():
        #         switch_id_components = switch.split("-")
        #         switch_number = int(switch_id_components[1])
        #         world.connect(
        #             switches[switch_number], switch_agent, ("closed",
        # "switch_state")
        #         )
        #         world.connect(
        #             switch_agent,
        #             switches[switch_number],
        #             ("switch_state", "closed"),
        #             time_shifted=True,
        #             initial_data={"switch_state": False},
        #         )

    def _connect_to_ders(self, mod_ctr):

        model = "BlackstartUnitAgent"
        for unit_model in self.sim_params["der_mapping"].values():
            mod_key = self.gen_mod_key(model.lower(), mod_ctr)
            unit_mod = self.get_unit_model(unit_model)
            agent = self.scenario[mod_key]
            self.connect_entities(unit_mod, agent, ["flexibilities"])
            self.connect_entities(
                agent,
                unit_mod,
                ["schedule"],
                time_shifted=True,
                initial_data={"schedule": None},
            )
            mod_ctr += 1
        return mod_ctr

    def _connect_to_loads(self, mod_ctr):
        # Define connections for load agents

        model = "BlackstartUnitAgent"
        for load_model in self.sim_params["load_mapping"].values():
            mod_key = self.gen_mod_key(model.lower(), mod_ctr)
            load_mod = self.get_load_model(load_model)

            # bus_number = household_params['household_mapping']
            # [load.eid]['bus']
            self.connect_entities(load_mod, self.scenario[mod_key], ["p_mw"])
            # world.connect(loads[bus_number], load_agent, 'p_mw')
            mod_ctr += 1
        return mod_ctr

    def _connect_to_switches(self, mod_ctr):
        model = "BlackstartSwitchAgent"
        for switch_cfg in self.sim_params["switch_mapping"].values():
            mod_key = self.gen_mod_key(model.lower(), mod_ctr)
            agent = self.scenario[mod_key]
            for switch in switch_cfg["adjacent_switches"]:

                switch_mod = self.get_switch_model(switch)

                self.connect_entities(
                    switch_mod, agent, [("closed", "switch_state")]
                )
                self.connect_entities(
                    agent,
                    switch_mod,
                    [("switch_state", "closed")],
                    time_shifted=True,
                    initial_data={"switch_state": False},
                )
            mod_ctr += 1

        return mod_ctr

    def connect_to_db(self):
        """Connect the models to db."""
        LOG.debug("Agents are too proud to connect to a database.")

    def gen_mod_key(self, mod_name, eidx):
        return f"{self.name}_{self.sim_name}_{mod_name}_{eidx}"

    def get_unit_model(self, full_id):
        sid, eid = full_id.split(".")
        mod_name, eidx = eid.split("-")
        for key, entity in self.scenario.items():
            if key.startswith(f"der_{self.sim_name}"):
                if "mapping" in key:
                    continue

                if eidx in key:
                    return entity

    def get_load_model(self, load_model):
        src, mod_type, eidx = load_model
        for key, entity in self.scenario.items():
            if key.startswith(f"{src}_{self.sim_name}"):

                # FIXME: select the first matching model
                if f"{mod_type}_{eidx}" in key:
                    return entity

        grid_key = f"powergrid_{self.sim_name}"
        grid = self.scenario[grid_key]
        for entity in grid.children:
            eid, bus = entity["eid"].rsplit("-", 1)

            # FIXME: select the first matching model
            if int(eidx) == int(eid):
                return entity

    def get_switch_model(self, switch):
        # _, eidx = switch.split("-")
        grid_key = f"powergrid_{self.sim_name}"
        grid = self.scenario[grid_key]
        switches = [e for e in grid.children if switch in e.eid]

        return switches[0]


def create_default_topology():
    topo = (
        {
            "agent8": [
                "BlackstartSwitchAgent-6",
                "BlackstartSwitchAgent-7",
                "BlackstartSwitchAgent-8",
            ],
            "agent3": ["BlackstartUnitAgent-2", "BlackstartUnitAgent-3"],
            "agent1": ["BlackstartUnitAgent-1", "BlackstartUnitAgent-5"],
            "agent2": ["BlackstartUnitAgent-0", "BlackstartUnitAgent-4"],
        },
    )
    return topo


def create_default_der_mapping():
    der_map = {
        "BlackstartUnitAgent-0": "Pysimmods-0.Photovoltaic-0",
        "BlackstartUnitAgent-1": "Pysimmods-0.Photovoltaic-1",
        "BlackstartUnitAgent-2": "Pysimmods-0.Photovoltaic-2",
        "BlackstartUnitAgent-3": "Pysimmods-0.Photovoltaic-3",
    }
    return der_map


def create_default_load_mapping():
    load_map = {
        "BlackstartUnitAgent-4": ("sndata", "Land", 0),
        "BlackstartUnitAgent-5": ("sndata", "Land", 1),
    }
    return load_map


def create_default_switch_mapping():
    switch_map = {
        "BlackstartSwitchAgent-6": {
            "own_bus": 1,
            "adjacent_switches": {
                "switch-0": {"other_bus": 2, "access": True}
            },
            "assigned_speaker": "BlackstartUnitAgent-2",
        },
        "BlackstartSwitchAgent-7": {
            "own_bus": 2,
            "adjacent_switches": {
                "switch-0": {"other_bus": 1, "access": False},
                "switch-1": {"other_bus": 3, "access": True},
            },
            "assigned_speaker": "BlackstartUnitAgent-0",
        },
        "BlackstartSwitchAgent-8": {
            "own_bus": 3,
            "adjacent_switches": {
                "switch-1": {"other_bus": 2, "access": False}
            },
            "assigned_speaker": "BlackstartUnitAgent-1",
        },
    }
    return switch_map

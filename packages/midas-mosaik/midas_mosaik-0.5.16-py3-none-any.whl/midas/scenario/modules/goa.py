"""This module contains the MIDAS upgrade for the grid operator
simulator.
"""
import logging

from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class GridOperatorModule(UpgradeModule):
    """Grid operator upgrade module for MIDAS."""

    def __init__(self):
        super().__init__("goa", LOG)

        self.default_name = "midasmv"
        self.default_sim_name = "GridOperator"
        self.default_import_str = "midas.core:GridOperatorSimulator"
        self.models = {
            "GOA": {
                "grid_load_sensor": ("load", ["p_mw", "q_mvar"]),
                "grid_sgen_sensor": ("sgen", ["p_mw", "q_mvar"]),
                "grid_busvm_sensor": ("bus", ["vm_pu"]),
                "grid_busload_sensor": ("bus", ["p_mw", "q_mvar"]),
                "der_load_sensor": ("load", ["p_mw", "q_mvar"]),
                "der_load_forecast_sensor": ("load", ["schedule"]),
                "der_sgen_sensor": ("sgen", ["p_mw", "q_mvar"]),
                "der_sgen_forecast_sensor": ("sgen", ["schedule"]),
                "goa_output": [
                    "health",
                    "error",
                    "max_overvoltage",
                    "min_undervoltage",
                    "num_voltage_violations",
                ],
            }
        }

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
        module_params.setdefault("data_path", self.scenario["data_path"])
        module_params.setdefault("grid_load_sensor", False)
        module_params.setdefault("grid_sgen_sensor", False)
        module_params.setdefault("grid_busvm_sensor", False)
        module_params.setdefault("grid_busload_sensor", True)
        module_params.setdefault("der_load_sensor", False)
        module_params.setdefault("der_load_forecast_sensor", False)
        module_params.setdefault("der_sgen_sensor", False)
        module_params.setdefault("der_sgen_forecast_sensor", False)
        module_params.setdefault("undervoltage_pu", 0.9)
        module_params.setdefault("overvoltage_pu", 1.1)
        module_params.setdefault("run_forecast", False)
        module_params.setdefault("forecast_horizon_hours", 0.25)

        return module_params

    def check_sim_params(self, module_params, **kwargs):
        """Check the params for a certain simulator instance."""
        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault(
            "grid_load_sensor", module_params["grid_load_sensor"]
        )
        self.sim_params.setdefault(
            "grid_sgen_sensor", module_params["grid_sgen_sensor"]
        )
        self.sim_params.setdefault(
            "grid_busvm_sensor", module_params["grid_busvm_sensor"]
        )
        self.sim_params.setdefault(
            "grid_busload_sensor", module_params["grid_busload_sensor"]
        )
        self.sim_params.setdefault(
            "der_load_sensor", module_params["der_load_sensor"]
        )
        self.sim_params.setdefault(
            "der_load_forecast_sensor",
            module_params["der_load_forecast_sensor"],
        )
        self.sim_params.setdefault(
            "der_sgen_sensor", module_params["der_sgen_sensor"]
        )
        self.sim_params.setdefault(
            "der_sgen_forecast_sensor",
            module_params["der_sgen_forecast_sensor"],
        )
        self.sim_params.setdefault(
            "undervoltage_pu", module_params["undervoltage_pu"]
        )
        self.sim_params.setdefault(
            "overvoltage_pu", module_params["overvoltage_pu"]
        )
        self.sim_params.setdefault(
            "run_forecast", module_params["run_forecast"]
        )
        self.sim_params.setdefault(
            "forecast_horizon_hours", module_params["forecast_horizon_hours"]
        )
        self.sim_params.setdefault("gridfile", self.default_name)

        self.gather_mappings()

        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        if self.scenario["deny_rng"]:
            self.sim_params["seed"] = 0
        else:
            self.sim_params.setdefault(
                "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
            )

    def start_models(self):
        """Start all models for this simulator."""

        for model in self.models:
            mod_key = self.gen_mod_key(model)
            self.start_model(mod_key, model, {"params": self.sim_params})

    def connect(self):
        """Connect the models to existing other models."""
        for model, sensors in self.models.items():
            goa = self.gen_mod_key(model)

            for sensor, info in sensors.items():
                if sensor.startswith("grid") and self.sim_params[sensor]:
                    self._connect_to_grid_entites(goa, info)
                elif sensor.startswith("der") and self.sim_params[sensor]:
                    self._connect_to_der_entities(goa, info)

    def _connect_to_grid_entites(self, goa, info):
        # grid = self.scenario[f"powergrid_{self.sim_name}"]
        for key, entity in self.scenario.items():
            if hasattr(entity, "eid") and info[0] in entity.eid:
                self.connect_entities2(key, goa, info[1])

    def _connect_to_der_entities(self, goa, info):
        for key, entity in self.scenario.items():
            if key.startswith(f"der_{self.sim_name}"):
                if "mapping" not in key:
                    self.connect_entities2(key, goa, info[1])

    def connect_to_db(self):
        for model, sensors in self.models.items():
            attrs = sensors["goa_output"]
            goa = self.gen_mod_key(model)
            self.connect_entities2(goa, "database", attrs)

    def gen_mod_key(self, model):
        return f"{self.name}_{self.sim_name}_{model.lower()}"

    def get_sensors(self):
        for model, sensors in self.models.items():
            # attrs = sensors["goa_output"]
            goa = self.scenario[self.gen_mod_key(model)]
            self.scenario["sensors"].append(
                {
                    "sensor_id": f"{goa.full_id}.health",
                    "observation_space": (
                        "Box(low=0, high=1.2, shape=(1,), dtype=np.float32)"
                    ),
                }
            )

            self.scenario["sensors"].append(
                {
                    "sensor_id": f"{goa.full_id}.error",
                    "observation_space": (
                        "Box(low=0, high=2.0, shape=(1,), dtype=np.float32)"
                    ),
                }
            )

    def gather_mappings(self):
        relevant = ["sbdata", "sndata", "comdata", "der"]
        load_mapping = dict()
        sgen_mapping = dict()
        der_mapping = dict()
        for key, val in self.scenario.items():
            for rel in relevant:
                if not key.startswith(rel):
                    continue
                elif self.sim_name not in key:
                    continue
                elif "eid_mapping" in key:
                    self._collect_eids(der_mapping, val)
                elif "load_mapping" in key:
                    self._collect_entities(load_mapping, val)
                elif "sgen_mapping" in key:
                    self._collect_entities(sgen_mapping, val)
        self.sim_params.setdefault("load_mapping", dict())
        if not self.sim_params["load_mapping"]:
            self.sim_params["load_mapping"] = load_mapping

        self.sim_params.setdefault("sgen_mapping", dict())
        if not self.sim_params["sgen_mapping"]:
            self.sim_params["sgen_mapping"] = sgen_mapping

        self.sim_params.setdefault("der_mapping", dict())
        if not self.sim_params["der_mapping"]:
            self.sim_params["der_mapping"] = der_mapping

    def _collect_entities(self, store_in, mapping):
        for bus, entities in mapping.items():
            store_in.setdefault(bus, list())
            store_in[bus].extend(entities)

    def _collect_eids(self, store_in, mapping):
        for eid, info in mapping.items():
            store_in[eid] = info

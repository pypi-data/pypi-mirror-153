"""This module contains the MIDAS powergrid upgrade."""
import logging
import os

from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class PowergridModule(UpgradeModule):
    """The MIDAS powergrid update module."""

    def __init__(self):
        super().__init__("powergrid", LOG)
        self.default_name = "midasmv"
        self.default_sim_name = "Powergrid"
        self.default_import_str = "midas.core:PandapowerSimulator"

        self.models = {
            "Line": [("loading_percent", 0.0, 1.0)],
            "Trafo": [("loading_percent", 0.0, 1.0)],
            "Bus": [("vm_pu", 0.8, 1.2), ("va_degree", -1.0, 1.0)],
            "Load": [("p_mw", 0, 1.0), ("q_mvar", -1.0, 1.0)],
            "Sgen": [("p_mw", 0, 1.0), ("q_mvar", -1.0, 1.0)],
            "Storage": [("p_mw", 0, 1.0), ("q_mvar", -1.0, 1.0)],
            "Ext_grid": [("p_mw", 0, 1.0), ("q_mvar", -1.0, 1.0)],
        }

    def check_module_params(self):
        """Check the module params for this upgrade."""

        module_params = self.params.setdefault(f"{self.name}_params", dict())

        if not module_params:
            module_params[self.default_name] = dict()

        module_params.setdefault("sim_name", self.default_sim_name)
        module_params.setdefault("cmd", "python")
        module_params.setdefault("import_str", self.default_import_str)
        module_params.setdefault("step_size", self.scenario["step_size"])
        module_params.setdefault("plotting", False)
        module_params.setdefault("use_constraints", False)
        module_params.setdefault("constraints", list())
        module_params.setdefault(
            "plot_path",
            os.path.abspath(
                os.path.join(self.scenario["output_path"], "plots")
            ),
        )
        module_params.setdefault("save_grid_json", False)

        return module_params

    def check_sim_params(self, module_params, **kwargs):
        """Check simulator params for a certain simulator."""

        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("gridfile", self.sim_name)
        self.sim_params.setdefault(
            "use_constraints", module_params["use_constraints"]
        )
        self.sim_params.setdefault("constraints", module_params["constraints"])
        self.sim_params.setdefault("grid_params", dict())
        self.sim_params.setdefault("with_ts", False)
        self.sim_params.setdefault("plotting", module_params["plotting"])
        self.sim_params.setdefault("plot_path", module_params["plot_path"])
        # self.sim_params.setdefault("plot_name", f"{self.sim_name}")
        self.sim_params.setdefault(
            "save_grid_json", module_params["save_grid_json"]
        )

    def start_models(self):
        """Start all models for this simulator.

        Since we want the grids to be able to be interconnected with
        each other, each grid model should have its own simulator.

        Parameters
        ----------
        sim_name : str
            The sim name, not to be confused with *sim_name* for
            mosaik's *sim_config*. **This** sim_name is the simulator
            key in the configuration yaml file.

        """
        mod_key = f"{self.name}_{self.sim_name}"

        mod_name = "Grid"
        if self.sim_params["with_ts"]:
            mod_name += "TS"
        params = {
            "gridfile": self.sim_params["gridfile"],
            "plotting": self.sim_params["plotting"],
            "use_constraints": self.sim_params["use_constraints"],
            "constraints": self.sim_params["constraints"],
        }
        if self.sim_params["grid_params"]:
            params["grid_params"] = self.sim_params["grid_params"]

        self.start_model(mod_key, mod_name, params)

        for entity in self.scenario[mod_key].children:
            parts = entity.eid.split("-")
            child_key = f"{mod_key}"
            for part in parts[1:]:
                child_key += f"_{part}"

            self.scenario["script"]["model_start"].append(
                f"{child_key} = [e for e in {mod_key}.children "
                f'if e.eid == "{entity.eid}"][0]\n'
            )
            self.scenario[child_key] = entity

    def connect(self, *args):
        # Nothing to do so far
        # Maybe to other grids in the future?
        pass

    def connect_to_db(self):
        """Add connections to the database."""

        grid_key = f"{self.name}_{self.sim_name}"

        for key, entity in self.scenario.items():
            if grid_key not in key:
                continue
            mod_key = key
            if entity.type in self.models:
                self.connect_entities2(
                    mod_key,
                    "database",
                    [a[0] for a in self.models[entity.type]],
                )

        additional_attrs = ["health"]
        if self.sim_params["save_grid_json"]:
            additional_attrs.append("grid_json")

        self.connect_entities2(grid_key, "database", additional_attrs)

    def get_sensors(self):
        grid = self.scenario[f"{self.name}_{self.sim_name}"]
        for entity in grid.children:
            if entity.type in self.models:
                for attr in self.models[entity.type]:
                    name, low, high = attr
                    self.scenario["sensors"].append(
                        {
                            "sensor_id": f"{entity.sid}.{entity.eid}.{name}",
                            "observation_space": f"Box(low={low}, "
                            f"high={high}, shape=(1,), dtype=np.float32)",
                        }
                    )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{grid.full_id}.health",
                "observation_space": (
                    "Box(low=0, high=1.2, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{grid.full_id}.grid_json",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )

    def get_actuators(self):
        grid = self.scenario[f"{self.name}_{self.sim_name}"]
        for entity in grid.children:
            if entity.type == "Trafo":
                self.scenario["actuators"].append(
                    {
                        "actuator_id": f"{entity.sid}.{entity.eid}.tap_pos",
                        "action_space": (
                            "Box(low=-10, high=10, shape=(1,), dtype="
                            "np.int32)"
                        ),
                    }
                )
            if entity.type in ("Load", "Sgen"):
                self.scenario["actuators"].append(
                    {
                        "actuator_id": f"{entity.sid}.{entity.eid}.p_mw",
                        "action_space": (
                            "Box(low=0, high=0.5, shape=(1,), dtype="
                            "np.float32)"
                        ),
                    }
                )
                self.scenario["actuators"].append(
                    {
                        "actuator_id": f"{entity.sid}.{entity.eid}.q_mvar",
                        "action_space": (
                            "Box(low=0, high=0.5, shape=(1,), dtype="
                            "np.float32)"
                        ),
                    }
                )

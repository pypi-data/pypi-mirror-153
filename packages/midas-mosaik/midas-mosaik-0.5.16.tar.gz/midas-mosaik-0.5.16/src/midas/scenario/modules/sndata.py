"""MIDAS upgrade module for Smart Nord data simulator."""
import logging

from midas.util.runtime_config import RuntimeConfig

from .sbdata import SimbenchDataModule

LOG = logging.getLogger(__name__)


class SmartNordDataModule(SimbenchDataModule):
    def __init__(self):
        super().__init__("sndata", LOG)
        self.default_grid = "midasmv"
        self.default_sim_name = "SmartNordData"
        self.default_import_str = "midas.core:SmartNordDataSimulator"
        self.models = {
            "household": ["p_mw", "q_mvar"],
            "land": ["p_mw", "q_mvar"],
        }

    def check_sim_params(self, module_params, **kwargs):
        """Check the params for a certain simulator instance."""
        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault("cos_phi", module_params["cos_phi"])
        self.sim_params.setdefault("interpolate", module_params["interpolate"])
        self.sim_params.setdefault(
            "randomize_data", module_params["randomize_data"]
        )
        self.sim_params.setdefault(
            "randomize_cos_phi", module_params["randomize_cos_phi"]
        )
        self.sim_params.setdefault(
            "noise_factor", module_params["noise_factor"]
        )
        self.sim_params.setdefault("household_mapping", dict())
        self.sim_params.setdefault("land_mapping", dict())
        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        self.sim_params.setdefault(
            "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
        )
        self.sim_params.setdefault(
            "filename", RuntimeConfig().data["smart_nord"][0]["name"]
        )

    def create_default_mapping(self, model):
        default_mapping = dict()
        if self.sim_name == self.default_grid:
            if model == "land":
                default_mapping = {
                    1: [[0, 1.0], [2, 1.0], [3, 3.0], [6, 2.0], [7, 1.0]],
                    3: [[0, 1.0], [2, 1.0], [3, 1.0], [6, 1.0], [7, 1.0]],
                    4: [[0, 3.0], [3, 2.0], [7, 1.0]],
                    5: [[3, 2.0], [7, 1.0]],
                    6: [[0, 1.0], [3, 2.0]],
                    7: [[0, 3.0], [2, 1.0], [3, 2.0], [7, 1.0]],
                    8: [[0, 2.0], [3, 1.0], [6, 1.0]],
                    9: [[2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
                    10: [[0, 2.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
                    11: [[0, 2.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]],
                }

        return default_mapping

    def start_models(self):
        """Start models of a certain simulator."""
        for model in self.models:
            self._instantiate_models(model, "load")

    def connect(self):
        for model, attrs in self.models.items():
            mapping = self.sim_params[f"{model}_mapping"]
            self.connect_to_grid(model, mapping, attrs, "load")

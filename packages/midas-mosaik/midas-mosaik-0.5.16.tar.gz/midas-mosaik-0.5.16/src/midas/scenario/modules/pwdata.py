"""MIDAS upgrade module for PV and Wind timeseries data simulator."""
import logging

from midas.util.runtime_config import RuntimeConfig
from .sbdata import SimbenchDataModule

LOG = logging.getLogger(__name__)


class PVWindDataModule(SimbenchDataModule):
    def __init__(self):
        super().__init__("pwdata", LOG)
        self.default_grid = "midasmv"
        self.default_sim_name = "PVWindData"
        self.default_import_str = "midas.core:PVWindDataSimulator"
        self.models = {
            "PV": ["p_mw", "q_mvar"],
            "Wind": ["p_mw", "q_mvar"],
            "WindOffshore": ["p_mw", "q_mvar"],
        }

    def check_sim_params(self, module_params, **kwargs):
        self.sim_params.setdefault("sim_name", module_params["sim_name"])
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
        self.sim_params.setdefault("peak_mapping", dict())
        self.sim_params.setdefault("scale_mapping", dict())
        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        self.sim_params.setdefault(
            "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
        )
        self.sim_params.setdefault(
            "filename", RuntimeConfig().data["generator_timeseries"][0]["name"]
        )

    def create_default_mapping(self):
        default_mapping = dict()
        if self.sim_name == self.default_grid:
            default_mapping = {13: [["Wind", 1.0]]}

        return default_mapping

    def start_models(self):
        peak_key = "peak_mapping"
        scale_key = "scale_mapping"

        if not self.sim_params[peak_key]:
            self.sim_params[peak_key] = self.create_default_mapping()

        mapping = self.scenario.setdefault(
            f"{self.name}_{self.sim_name}_mapping", dict()
        )
        for map_key in [peak_key, scale_key]:
            for bus, entities in self.sim_params[map_key].items():
                mapping.setdefault(bus, list())
                for eidx, (model, scale) in enumerate(entities):
                    mod_key = self.gen_mod_key(model, bus, eidx)
                    scaling = scale * float(
                        self.sim_params.get("scaling", 1.0)
                    )
                    if "peak" in map_key:
                        params = {"p_peak_mw": scaling}
                    else:
                        params = {"scaling": scaling}

                    self.start_model(mod_key, model, params)
                    info = self.scenario[self.sim_key].get_data_info()[
                        self.scenario[mod_key].eid
                    ]
                    mapping[bus].append((model, info["p_mwh_per_a"]))

    def connect(self):
        grid_key = f"powergrid_{self.sim_name}"
        attrs = ["p_mw", "q_mvar"]
        mapping = self.scenario[f"{self.name}_{self.sim_name}_mapping"]

        for bus, entities in mapping.items():
            for eidx, (model, _) in enumerate(entities):
                entity_key = self.gen_mod_key(model, bus, eidx)
                grid_entity_key = self.get_grid_entity(grid_key, "sgen", bus)
                self.connect_entities2(entity_key, grid_entity_key, attrs)

    def connect_to_db(self):
        """Connect the models to db."""

        attrs = ["p_mw", "q_mvar"]
        mapping = self.scenario[f"{self.name}_{self.sim_name}_mapping"]

        for bus, entities in mapping.items():
            for eidx, (model, _) in enumerate(entities):
                mod_key = self.gen_mod_key(model, bus, eidx)
                self.connect_entities2(mod_key, "database", attrs)

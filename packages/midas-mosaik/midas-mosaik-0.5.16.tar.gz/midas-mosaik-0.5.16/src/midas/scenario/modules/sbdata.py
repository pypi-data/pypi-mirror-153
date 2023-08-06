"""MIDAS upgrade module for simbench data simulator."""
import logging
import os
import pandas as pd
from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class SimbenchDataModule(UpgradeModule):
    """Upgrade module for simbench data.

    Other, similar data modules can derive from this class.

    """

    def __init__(self, name="sbdata", log=None):
        if log is None:
            UpgradeModule.__init__(self, name, LOG)
        else:
            UpgradeModule.__init__(self, name, log)

        self.default_grid = "sbrural3"
        self.default_sim_name = "SimbenchData"
        self.default_import_str = "midas.core:SimbenchDataSimulator"
        self.models = {
            "load": ["p_mw", "q_mvar"],
            "sgen": ["p_mw", "q_mvar"],
            "storage": ["p_mw", "q_mvar"],
        }

    def check_module_params(self):
        """Check the module params and provide default values."""

        module_params = self.params.setdefault(f"{self.name}_params", dict())

        if not module_params:
            module_params[self.default_grid] = dict()

        module_params.setdefault("sim_name", self.default_sim_name)
        module_params.setdefault("cmd", "python")
        module_params.setdefault("import_str", self.default_import_str)
        module_params.setdefault("step_size", self.scenario["step_size"])
        module_params.setdefault("start_date", self.scenario["start_date"])
        module_params.setdefault("data_path", self.scenario["data_path"])
        module_params.setdefault("cos_phi", self.scenario["cos_phi"])
        module_params.setdefault("interpolate", False)
        module_params.setdefault("noise_factor", 0.2)
        module_params.setdefault("load_scaling", 1.0)
        module_params.setdefault("sgen_scaling", 1.0)
        module_params.setdefault("storage_scaling", 1.0)

        if self.scenario["deny_rng"]:
            module_params["randomize_data"] = False
            module_params["randomize_cos_phi"] = False
        else:
            module_params.setdefault("randomize_data", False)
            module_params.setdefault("randomize_cos_phi", False)

        return module_params

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
        self.sim_params.setdefault(
            "load_scaling", module_params["load_scaling"]
        )
        self.sim_params.setdefault(
            "sgen_scaling", module_params["sgen_scaling"]
        )
        self.sim_params.setdefault(
            "storage_scaling", module_params["storage_scaling"]
        )
        self.sim_params.setdefault("load_mapping", "default")
        self.sim_params.setdefault("sgen_mapping", "default")
        self.sim_params.setdefault("storage_mapping", "default")
        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        self.sim_params.setdefault(
            "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
        )
        gridfile = self.params["powergrid_params"][self.sim_name]["gridfile"]
        self.sim_params.setdefault(
            "filename",
            f"{gridfile}.hdf5",
        )

    def start_models(self):
        """Start models of a certain simulator."""
        for model in self.models:
            self._instantiate_models(model, model)

    def _instantiate_models(self, model, mtype):
        """Start all models as specified in the mappings."""

        map_key = f"{model}_mapping"

        if isinstance(self.sim_params[map_key], str):
            self.sim_params[map_key] = self.create_default_mapping(model)

        mapping = self.scenario.setdefault(
            f"{self.name}_{self.sim_name}_{mtype}_mapping", dict()
        )
        for bus, entities in self.sim_params[map_key].items():
            mapping.setdefault(bus, list())
            for (eidx, scale) in entities:
                mod_key = self.gen_mod_key(model, bus, eidx)
                scaling = scale * float(
                    self.sim_params.get(f"{model}_scaling", 1.0)
                )

                params = {"scaling": scaling, "eidx": eidx}
                self.start_model(mod_key, model.capitalize(), params)

                info = self.scenario[self.sim_key].get_data_info()[
                    self.scenario[mod_key].eid
                ]
                mapping[bus].append((model, info["p_mwh_per_a"]))

    def create_default_mapping(self, model):
        """Create a default mapping.

        Tries to read the default mapping from hdf5 db that stores
        the data.
        """

        info = self.scenario[self.sim_key].get_data_info()
        num_models = f"max_{model}s"
        self.sim_params[num_models] = info[num_models]

        self.logger.debug(
            "Try to load %s default mapping from hdf5 db ...", model
        )
        file_path = os.path.join(
            self.sim_params["data_path"], self.sim_params["filename"]
        )

        default_mapping = dict()
        try:
            mapping = pd.read_hdf(file_path, f"{model}_default_mapping")
        except KeyError:
            self.logger.debug("No default mapping for %s in database.", model)
            mapping = None

        for eidx in range(self.sim_params[num_models]):
            try:
                bus = mapping.loc[eidx]["bus"]
            except TypeError:
                bus = eidx
            except KeyError:
                break
            default_mapping.setdefault(bus, list())
            default_mapping[bus].append([eidx, 1.0])

        return default_mapping

    def connect(self):
        """Create connections to other entities."""
        for model, attrs in self.models.items():
            map_key = f"{model}_mapping"
            self.connect_to_grid(model, self.sim_params[map_key], attrs, model)

    def connect_to_grid(self, model, mapping, attrs, mtype):
        """Connect to the grid model."""
        grid_key = f"powergrid_{self.sim_name}"

        for bus, entities in mapping.items():
            for (eidx, _) in entities:

                entity_key = self.gen_mod_key(model, bus, eidx)
                grid_entity_key = self.get_grid_entity(grid_key, mtype, bus)
                self.connect_entities2(entity_key, grid_entity_key, attrs)

    def connect_to_db(self):
        """Connect the models to db."""

        for model, attrs in self.models.items():
            map_key = f"{model}_mapping"

            for bus, entities in self.sim_params[map_key].items():
                for (eidx, _) in entities:
                    mod_key = self.gen_mod_key(model, bus, eidx)
                    self.connect_entities2(mod_key, "database", attrs)

    def gen_mod_key(self, mod_name, bus, eidx=None):
        key = f"{self.name}_{self.sim_name}_{mod_name}_{bus}"
        if eidx is not None:
            key = f"{key}_{eidx}"
        return key

    def get_grid_entity(self, grid_key, mtype, bus):
        for entity in self.scenario[grid_key].children:
            if mtype in entity.eid and int(entity.eid.split("-")[-1]) == bus:
                key = grid_key
                parts = entity.eid.split("-")
                for part in parts[1:]:
                    key += f"_{part}"
                return key
                # return entity

        self.logger.info(
            "Grid entity for %s, %s at bus %d not found", grid_key, mtype, bus
        )
        raise ValueError(
            f"Grid entity for {grid_key}, {mtype} at bus {bus} not found!"
        )

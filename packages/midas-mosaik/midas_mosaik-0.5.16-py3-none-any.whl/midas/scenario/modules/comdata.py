"""MIDAS upgrade module for the commercial data simulator."""
import logging

from .sbdata import SimbenchDataModule

LOG = logging.getLogger(__name__)


class CommercialDataModule(SimbenchDataModule):
    def __init__(self, name="comdata"):
        super().__init__(name, LOG)
        self.default_grid = "midasmv"
        self.default_sim_name = "CommercialData"
        self.default_import_str = "midas.core:CommercialDataSimulator"
        attrs = ["p_mw", "q_mvar"]
        self.models = {
            "FullServiceRestaurant": attrs,
            "Hospital": attrs,
            "LargeHotel": attrs,
            "LargeOffice": attrs,
            "MediumOffice": attrs,
            "MidriseApartment": attrs,
            "OutPatient": attrs,
            "PrimarySchool": attrs,
            "QuickServiceRestaurant": attrs,
            "SecondarySchool": attrs,
            "SmallHotel": attrs,
            "SmallOffice": attrs,
            "StandaloneRetail": attrs,
            "StripMall": attrs,
            "SuperMarket": attrs,
            "Warehouse": attrs,
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
        self.sim_params.setdefault("load_mapping", dict())
        self.sim_params.setdefault("sgen_mapping", dict())
        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        self.sim_params.setdefault(
            "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
        )
        self.sim_params.setdefault("filename", "CommercialsRefTMY3.hdf5")

    def create_default_mapping(self, model):
        default_mapping = dict()
        if self.sim_name == self.default_grid:
            default_mapping = {
                13: [["SuperMarket", 0.089]],
                14: [["SmallHotel", 0.022]],
            }

        return default_mapping

    def start_models(self):
        """Start models of a certain simulator."""
        for model in self.models:
            self._instantiate_models(model)

    def _instantiate_models(self, model):
        """Start all models as specified in the mappings."""

        if not self.sim_params["mapping"]:
            self.sim_params["mapping"] = self.create_default_mapping(model)

        mapping = self.scenario.setdefault(
            f"{self.name}_{self.sim_name}_load_mapping", dict()
        )
        for bus, entities in self.sim_params["mapping"].items():
            mapping.setdefault(bus, list())
            for eidx, (name, scale) in enumerate(entities):
                if model != name:
                    continue
                mod_key = self.gen_mod_key(model.lower(), bus, eidx)
                params = {"scaling": scale}
                self.start_model(mod_key, model, params)

                info = self.scenario[self.sim_key].get_data_info()
                info = info[self.scenario[mod_key].eid]
                # info = self.scenario[self.sim_key].get_data_info(
                #     self.scenario[mod_key].eid
                # )
                mapping[bus].append((model, info["p_mwh_per_a"]))

        # self.scenario[f"{self.name}_{self.sim_name}_load_mapping"] = mapping
        # mapping[bus].append((model, scale))

    def connect(self):
        for model, attrs in self.models.items():
            self.connect_to_grid(
                model, self.sim_params["mapping"], attrs, "load"
            )

    def connect_to_grid(self, model, mapping, attrs, mtype):
        """Connect to the grid model."""
        grid_key = f"powergrid_{self.sim_name}"

        for bus, entities in mapping.items():
            for eidx, (name, _) in enumerate(entities):
                if model != name:
                    continue
                entity = self.gen_mod_key(model.lower(), bus, eidx)

                grid_entity = self.get_grid_entity(grid_key, mtype, bus)
                self.connect_entities2(entity, grid_entity, attrs)

    def connect_to_db(self):
        """Connect the models to db."""

        for model, attrs in self.models.items():

            for bus, entities in self.sim_params["mapping"].items():
                for eidx, (name, _) in enumerate(entities):
                    if model != name:
                        continue
                    mod_key = self.gen_mod_key(model.lower(), bus, eidx)
                    self.connect_entities2(mod_key, "database", attrs)

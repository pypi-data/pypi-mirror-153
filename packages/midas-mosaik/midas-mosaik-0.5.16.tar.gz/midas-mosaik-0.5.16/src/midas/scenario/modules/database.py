"""MIDAS scenario upgrade module.

This module adds a mosaikhdf database to the scenario.

"""
import logging
import os

from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class DatabaseModule(UpgradeModule):
    def __init__(self):
        super().__init__("mosaikdb", LOG)
        self.default_name = "database"
        self.default_sim_name = "MosaikDB"
        self.default_import_str = "midas.core.store:MidasHdf5"
        self.filename = None

    def check_module_params(self):
        """Check module params for this upgrade."""

        module_params = self.params.setdefault(f"{self.name}_params", dict())
        module_params.setdefault(self.default_name, dict())
        module_params.setdefault("sim_name", self.default_sim_name)
        module_params.setdefault("cmd", "python")
        module_params.setdefault("import_str", self.default_import_str)
        module_params.setdefault("step_size", self.scenario["step_size"])
        module_params.setdefault("buffer_size", 0)
        module_params.setdefault("overwrite", True)
        module_params.setdefault("filename", f"{self.default_name}.hdf5")
        if module_params["filename"] is not None:
            module_params["filename"] = os.path.abspath(
                os.path.join(
                    self.scenario["output_path"], module_params["filename"]
                )
            )
        return module_params

    def check_sim_params(self, module_params, **kwargs):
        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        # self.sim_params.setdefault("filename", module_params["filename"])
        self.filename = module_params["filename"]

        if "mosaik" in self.sim_params["import_str"]:
            self.scenario["db_restricted"] = True
            self.sim_params["duration"] = self.scenario["end"]
        else:
            self.sim_params.setdefault(
                "buffer_size", module_params["buffer_size"]
            )
            self.sim_params.setdefault("overwrite", module_params["overwrite"])

    def start_models(self):
        mod_key = "database"
        params = {"filename": self.filename}

        if "midas" in self.sim_params["import_str"]:
            params["buffer_size"] = self.sim_params["buffer_size"]
            params["overwrite"] = self.sim_params["overwrite"]

        self.start_model(mod_key, "Database", params)

    def connect(self):
        pass

    def connect_to_db(self):
        pass

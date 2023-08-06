"""MIDAS scenario upgrade module.

This module adds a mosaikhdf database to the scenario.

"""
import logging
from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class TimeSimModule(UpgradeModule):
    def __init__(self):
        super().__init__("timesim", LOG)
        self.default_name = "timesim"
        self.default_sim_name = "TimeSim"
        self.default_import_str = "midas.core.time:TimeSimulator"

    def check_module_params(self):
        """Check module params for this upgrade."""
        module_params = self.params.setdefault(f"{self.name}_params", dict())
        module_params.setdefault(self.default_name, dict())
        module_params.setdefault("sim_name", self.default_sim_name)
        module_params.setdefault("cmd", "python")
        module_params.setdefault("import_str", self.default_import_str)
        module_params.setdefault("step_size", self.scenario["step_size"])
        module_params.setdefault("time_schedule", None)

        return module_params

    def check_sim_params(self, module_params, **kwargs):
        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("start_date", self.scenario["start_date"])
        self.sim_params.setdefault(
            "time_schedule", module_params["time_schedule"]
        )

    def start_models(self):
        mod_key = "timegenmodel"

        self.start_model(mod_key, "Timegenerator", dict())

    def connect(self):
        pass

    def connect_to_db(self):
        attrs = [
            "sin_day_time",
            "sin_week_time",
            "sin_year_time",
            "cos_day_time",
            "cos_week_time",
            "cos_year_time",
            "utc_time",
            "local_time",
        ]
        self.connect_entities2("timegenmodel", "database", attrs)
        # scenario["world"].connect(from_entity, to_entity, *attrs)
        # LOG.debug(
        #     "Connected %s to %s (%s).",
        #     from_entity.full_id,
        #     to_entity.full_id,
        #     attrs,
        # )
        # scenario["script"]["connects"].append(
        #     f"world.connect(timegenmodel, database, *{attrs})\n"
        # )

    def get_sensor(self):
        timesim = self.scenario["timegenmodel"]

        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.sin_day_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.sin_week_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.sin_year_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.cos_day_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.cos_week_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )
        self.scenario["sensors"].append(
            {
                "sensor_id": f"{timesim.full_id}.cos_year_time",
                "observation_space": (
                    "Box(low=0, high=1, shape=(1,), dtype=np.float32)"
                ),
            }
        )

"""MIDAS upgrade module for the weather data simulator."""
import logging

# from mosaik.util import connect_many_to_one
from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class WeatherDataModule(UpgradeModule):
    def __init__(self, name="weather"):
        super().__init__(name)

        # Since the default weather data are from Bremen
        self.default_name = "bremen"
        self.default_sim_name = "WeatherData"
        self.default_import_str = "midas.core:WeatherDataSimulator"
        attrs = [
            "t_air_deg_celsius",
            "day_avg_t_air_deg_celsius",
            "bh_w_per_m2",
            "dh_w_per_m2",
        ]
        self.models = {
            "WeatherCurrent": attrs,
            "WeatherForecast": [f"forecast_{attr}" for attr in attrs],
        }

    def check_module_params(self):
        """Check the module params and provide default values."""

        module_params = self.params.setdefault(f"{self.name}_params", dict())

        if not module_params:
            module_params[self.default_name] = dict()

        module_params.setdefault("sim_name", self.default_sim_name)
        module_params.setdefault("cmd", "python")
        module_params.setdefault("import_str", self.default_import_str)
        module_params.setdefault("step_size", self.scenario["step_size"])
        module_params.setdefault("start_date", self.scenario["start_date"])
        module_params.setdefault("interpolate", False)
        module_params.setdefault("data_path", self.scenario["data_path"])
        module_params.setdefault(
            "filename", self.scenario["default_weather_name"]
        )
        module_params.setdefault(
            "forecast_horizon_hours",
            self.scenario["forecast_horizon_hours"]
            # + module_params["step_size"] / 3_600,
        )
        module_params.setdefault("forecast_error", 0.05)
        if self.scenario["deny_rng"]:
            module_params["randomize"] = False
        else:
            module_params.setdefault("randomize", False)

        return module_params

    def check_sim_params(self, module_params, **kwargs):
        """Check the params for a certain simulator instance."""

        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("interpolate", module_params["interpolate"])
        self.sim_params.setdefault("randomize", module_params["randomize"])
        self.sim_params.setdefault("weather_mapping", dict())
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault("filename", module_params["filename"])
        self.sim_params.setdefault(
            "forecast_horizon_hours", module_params["forecast_horizon_hours"]
        )
        self.sim_params.setdefault(
            "forecast_error", module_params["forecast_error"]
        )
        # self.sim_params.setdefault("filename", "WeatherBre")
        if not self.sim_params["weather_mapping"]:
            self.sim_params["weather_mapping"]["WeatherCurrent"] = [
                {
                    "interpolate": self.sim_params["interpolate"],
                    "randomize": self.sim_params["randomize"],
                }
            ]

        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        self.sim_params.setdefault(
            "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
        )

    def start_models(self):
        """Start models of a certain simulator."""
        for model, configs in self.sim_params["weather_mapping"].items():
            model_low = model.lower()

            for idx, config in enumerate(configs):
                mod_key = self.gen_mod_key(model_low, idx)
                self.start_model(mod_key, model, config)

    def connect(self):
        if self.scenario["with_timesim"]:
            for model in self.models:
                if model not in self.sim_params["weather_mapping"]:
                    continue
                for idx, _ in enumerate(
                    self.sim_params["weather_mapping"][model]
                ):
                    timesim = "timegenmodel"
                    entity = self.gen_mod_key(model.lower(), idx)
                    self.connect_entities2(
                        timesim, entity, [("local_time", "now")]
                    )
        # No initial connections
        pass

    def connect_to_db(self):
        """Connect models to db."""
        for model, attrs in self.models.items():
            if model == "WeatherForecast":
                # mosaikhdf cannot store arrays/lists
                continue

            for idx, _ in enumerate(self.sim_params["weather_mapping"][model]):
                entity = self.gen_mod_key(model.lower(), idx)
                self.connect_entities2(entity, "database", attrs)

    def gen_mod_key(self, model, idx):
        return f"{self.name}_{self.sim_name}_{model}_{idx}"

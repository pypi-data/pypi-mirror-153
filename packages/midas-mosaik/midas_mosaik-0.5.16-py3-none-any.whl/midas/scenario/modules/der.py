"""MIDAS upgrade module for the weather data simulator."""
import logging

from midas.adapter.pysimmods.presets import get_presets
from midas.scenario.upgrade_module import UpgradeModule
from mosaik.exceptions import ScenarioError

LOG = logging.getLogger(__name__)


class PysimmodsModule(UpgradeModule):
    """Pysimmods upgrade module for MIDAS."""

    def __init__(self, name="der"):
        super().__init__(name, LOG)

        self.default_name = "midasmv"
        self.default_sim_name = "Pysimmods"
        self.default_import_str = (
            "pysimmods.mosaik.pysim_mosaik:PysimmodsSimulator"
        )
        self.models = {
            "PV": (
                "Photovoltaic",
                "sgen",
                ["bh_w_per_m2", "dh_w_per_m2", "t_air_deg_celsius"],
                ["p_mw", "q_mvar", "inverter_inductive"],
            ),
            "HVAC": (
                "HVAC",
                "load",
                ["t_air_deg_celsius"],
                ["p_mw", "q_mvar"],
            ),
            "CHP": (
                "CHP",
                "sgen",
                ["day_avg_t_air_deg_celsius"],
                ["p_mw", "q_mvar"],
            ),
            "DIESEL": ("DieselGenerator", "sgen", [], ["p_mw", "q_mvar"]),
            "BAT": (
                "Battery",
                "storage",
                [],
                ["p_mw", "q_mvar", "soc_percent"],
            ),
            "Biogas": ("Biogas", "sgen", [], ["p_mw", "q_mvar"]),
        }
        self.sensors = list()
        self.actuators = list()

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
        module_params.setdefault("cos_phi", self.scenario["cos_phi"])
        module_params.setdefault("grid_name", "midasmv")
        module_params.setdefault("q_control", "p_set")
        module_params.setdefault("inverter_mode", "inductive")
        module_params.setdefault(
            "forecast_horizon_hours", self.scenario["forecast_horizon_hours"]
        )
        module_params.setdefault("provide_flexibilities", False)
        module_params.setdefault(
            "flexibility_horizon_hours",
            self.scenario["flexibility_horizon_hours"],
        )
        module_params.setdefault("num_schedules", 10)
        module_params.setdefault("unit", "mw")
        module_params.setdefault("use_decimal_percent", False)
        module_params.setdefault("priorize_setpoint", False)
        return module_params

    def check_sim_params(self, module_params, **kwargs):
        """Check the params for a certain simulator instance."""

        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("grid_name", module_params["grid_name"])
        self.sim_params.setdefault("cos_phi", module_params["cos_phi"])
        self.sim_params.setdefault("q_control", module_params["q_control"])
        self.sim_params.setdefault(
            "inverter_mode", module_params["inverter_mode"]
        )
        self.sim_params.setdefault(
            "forecast_horizon_hours", module_params["forecast_horizon_hours"]
        )
        self.sim_params.setdefault(
            "provide_flexibilities", module_params["provide_flexibilities"]
        )
        self.sim_params.setdefault(
            "flexibility_horizon_hours",
            module_params["flexibility_horizon_hours"],
        )
        self.sim_params.setdefault(
            "num_schedules", module_params["num_schedules"]
        )
        self.sim_params.setdefault("unit", module_params["unit"])
        self.sim_params.setdefault(
            "use_decimal_percent", module_params["use_decimal_percent"]
        )
        self.sim_params.setdefault(
            "priorize_setpoint", module_params["priorize_setpoint"]
        )
        self.sim_params.setdefault("mapping", dict())
        self.sim_params.setdefault("weather_provider_mapping", dict())
        self.sim_params.setdefault("weather_forecast_mapping", dict())

        self.sim_params.setdefault("seed_max", self.scenario["seed_max"])
        if self.scenario["deny_rng"]:
            self.sim_params["seed"] = 0
        else:
            self.sim_params.setdefault(
                "seed", self.scenario["rng"].randint(self.scenario["seed_max"])
            )

    def start_models(self):
        """Start all models defined in the mapping of a certain simulator."""
        for model, info in self.models.items():
            self._instantiate_models(model, info)

    def _instantiate_models(self, model, info):
        """Start all models as specified in the mappings."""
        if not self.sim_params["mapping"]:
            self.sim_params["mapping"] = create_default_mapping()

        eid_mapping = self.scenario.setdefault(
            f"der_{self.sim_name}_eid_mapping", dict()
        )
        if self.sim_params["use_decimal_percent"]:
            high = "1.0"
        else:
            high = "100"
        mod_ctr = dict()
        for bus, entities in self.sim_params["mapping"].items():
            for name, p_peak_mw in entities:
                if model != name:
                    continue

                mod_ctr.setdefault(model, 0)
                mod_key = self.gen_mod_key(model.lower(), bus, mod_ctr[model])
                params = self.gen_mod_params(mod_key, model, p_peak_mw)
                self.start_model(mod_key, info[0], params)

                eid_mapping[self.scenario[mod_key].full_id] = {
                    "p_mw": p_peak_mw,
                    "bus": bus,
                    "type": info[1],
                    "sn_mva": params.get("sn_mva", p_peak_mw),
                }

                self.actuators.append(
                    {
                        "actuator_id": (
                            f"{self.scenario[mod_key].full_id}.set_percent"
                        ),
                        "action_space": (
                            f"Box(low=0, high={high}, shape=(1,), "
                            "dtype=np.float32)"
                        ),
                    }
                )
                if model in ["PV"]:
                    self.actuators.append(
                        {
                            "actuator_id": (
                                f"{self.scenario[mod_key].full_id}"
                                ".inverter_inductive"
                            ),
                            "action_space": "Discrete(2)",
                        }
                    )

                for attr in self.models[model][3]:
                    self.sensors.append(
                        {
                            "sensor_id": (
                                f"{self.scenario[mod_key].full_id}.{attr}"
                            ),
                            "observation_space": (
                                "Box(low=0, high=100, shape=(1,), "
                                "dtype=np.float32)"
                            ),
                        }
                    )

                # self.sim_params["eid_mapping"] = eid_mapping
                mod_ctr[model] += 1

    def connect(self):
        """Connect the models to existing other models."""

        for model, info in self.models.items():
            self._connect_to_weather(model, info)
            try:
                self._connect_to_grid(model, info)
            except KeyError:
                LOG.warning(
                    "No grid for %s found. Will output only to database "
                    "(if configured).",
                    self.sim_params["sim_name"],
                )

    def _connect_to_weather(self, model, info):

        wpm = "weather_provider_mapping"

        if not self.sim_params[wpm]:
            self.sim_params[wpm] = self.create_default_wpm()

        mod_ctr = dict()
        for bus, entities in self.sim_params["mapping"].items():
            for name, _ in entities:
                if model != name:
                    continue

                mod_ctr.setdefault(model, 0)
                mod_key = self.gen_mod_key(model.lower(), bus, mod_ctr[model])

                weather_entity = self.get_weather_model(model, mod_ctr[model])
                try:
                    self.connect_entities2(weather_entity, mod_key, info[2])
                except KeyError:
                    LOG.critical("Weather mapping missing for %s", model)
                    raise KeyError("No weather mapping defined for %s", model)

                weather_fc_entity = self.get_weather_model(
                    model, mod_ctr[model], True
                )
                if weather_fc_entity is not None:
                    fc_attrs = [f"forecast_{a}" for a in info[2]]
                    self.connect_entities2(
                        weather_fc_entity, mod_key, fc_attrs
                    )

                mod_ctr[model] += 1

    def _connect_to_grid(self, model, info):

        mod_ctr = dict()
        for bus, entities in self.sim_params["mapping"].items():
            for name, _ in entities:
                if model != name:
                    continue

                mod_ctr.setdefault(model, 0)
                mod_key = self.gen_mod_key(model.lower(), bus, mod_ctr[model])

                grid_entity = self.get_grid_entity(info[1], bus)
                try:
                    self.connect_entities2(mod_key, grid_entity, info[3][:2])
                except ScenarioError as e:
                    LOG.warning(
                        "Encountered scenario error while connecting %s"
                        "to grid entity %s: %s",
                        mod_key,
                        grid_entity,
                        e,
                    )
                except KeyError:
                    LOG.warning(
                        "Entity missing for %s: %s or grid: %s.",
                        model,
                        mod_key,
                        grid_entity,
                    )
                mod_ctr[model] += 1

    def connect_to_db(self):
        """Connect the models to db."""
        for model, info in self.models.items():
            mod_ctr = dict()
            for bus, entities in self.sim_params["mapping"].items():
                for name, _ in entities:
                    if model != name:
                        continue

                    mod_ctr.setdefault(model, 0)
                    mod_key = self.gen_mod_key(
                        model.lower(), bus, mod_ctr[model]
                    )

                    fc_attrs = info[3] + ["target"]
                    try:
                        self.connect_entities2(
                            mod_key,
                            "database",
                            fc_attrs,
                        )
                    except ScenarioError:
                        self.connect_entities(
                            self.scenario[mod_key],
                            self.scenario["database"],
                            info[3],
                        )
                    mod_ctr[model] += 1

    def connect_to_timesim(self):
        for model, info in self.models.items():
            mod_ctr = dict()
            for bus, entities in self.sim_params["mapping"].items():
                for name, _ in entities:
                    if model != name:
                        continue

                    mod_ctr.setdefault(model, 0)
                    mod_key = self.gen_mod_key(
                        model.lower(), bus, mod_ctr[model]
                    )

                    self.connect_entities2(
                        "timegenmodel",
                        mod_key,
                        ["local_time"],
                    )

                    mod_ctr[model] += 1

    def gen_mod_key(self, mod_name, bus, eidx):
        """Generate a model key."""
        return (
            f"{self.name}_{self.sim_params['grid_name']}_{mod_name}"
            + f"_{bus}_{eidx}"
        )

    def gen_mod_params(self, mod_key, model, p_peak_mw):
        """Load model params and initial configurations."""
        mod_params, mod_inits = get_presets(
            model,
            p_peak_mw,
            q_control=self.sim_params["q_control"],
            cos_phi=self.sim_params["cos_phi"],
            inverter_mode=self.sim_params["inverter_mode"],
        )
        self.sim_params.setdefault(mod_key, dict())
        self.sim_params[mod_key].setdefault("params", mod_params)
        self.sim_params[mod_key].setdefault("inits", mod_inits)
        return self.sim_params[mod_key]

    def create_default_wpm(self):
        """Create a default weather provider mapping."""
        wprovider = None
        for key, val in self.params["weather_params"].items():
            if isinstance(key, dict):
                try:
                    if len(val["weather_mapping"]["WeatherCurrent"]) > 0:
                        wprovider = key
                        break

                except KeyError:
                    pass

        wpmapping = dict()
        for models in self.sim_params["mapping"].values():
            for (model, _) in models:
                wpmapping.setdefault(model, dict())
                wpmapping[model].setdefault(wprovider, list())
                wpmapping[model][wprovider].append(0)

        return wpmapping

    def get_weather_model(self, model, idx, forecast=False):
        if forecast:
            wmn = "weatherforecast"
            mapping = self.sim_params["weather_forecast_mapping"]
        else:
            wmn = "weathercurrent"
            mapping = self.sim_params["weather_provider_mapping"]
        try:
            model_mapping = mapping[model]
        except KeyError:
            msg = (
                f"No {wmn} mapping for model {model} defined. This may "
                + "result in an error if the model depends on that inputs."
            )
            LOG.debug(msg)

            return None

        if isinstance(model_mapping, dict):
            for model_idx, (name, wpidx) in model_mapping.items():
                if model_idx != idx:
                    continue

                wp_key = f"_{name}_{wmn}_{wpidx}"

        elif isinstance(model_mapping, list):
            name = model_mapping[0]
            if isinstance(model_mapping[1], list):
                try:
                    wpidx = model_mapping[1][idx]
                except IndexError:
                    wpidx = model_mapping[1][0]
            else:
                wpidx = model_mapping[1]
            wp_key = f"_{name}_{wmn}_{wpidx}"
        else:
            raise ValueError("Weather provider mapping: Unknown format.")

        for key, val in self.scenario.items():
            if wp_key in key:
                return key

        return None

    def get_grid_entity(self, utype, bus):
        grid_key = f"powergrid_{self.sim_params['grid_name']}"
        grid = self.scenario[grid_key]
        for entity in grid.children:
            if utype in entity.eid and int(entity.eid.split("-")[-1]) == bus:
                key = grid_key
                parts = entity.eid.split("-")
                for part in parts[1:]:
                    key += f"_{part}"
                return key

        if utype == "storage":
            # The storage type may not be present in the grid
            # Attach the unit to load instead
            return self.get_grid_entity("load", bus)
        return None

    def get_sensors(self):
        for sensor in self.sensors:
            self.scenario["sensors"].append(sensor)
            LOG.debug("Created sensor entry %s.", sensor)

    def get_actuators(self):
        for actuator in self.actuators:
            self.scenario["actuators"].append(actuator)
            LOG.debug("Created actuator entry %s.", actuator)


def create_default_mapping():
    return {3: [("PV", 6)], 4: [("PV", 2)], 8: [("PV", 2)], 11: [("PV", 3)]}

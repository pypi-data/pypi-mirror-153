"""Test module for the weather simulator."""
import unittest
from datetime import datetime, timedelta

import pandas as pd
from midas.core.weather.model.provider import WeatherData
from midas.core.weather.simulator import WeatherSimulator
from midas.util.runtime_config import RuntimeConfig
from midas.util.dateformat import GER

# from midas.tools import config

# CFG = config.check_config(None)


class TestSimulator(unittest.TestCase):
    """Test class for the weather simulator."""

    def setUp(self):
        datapath = RuntimeConfig().paths["data_path"]

        # self.sim = WeatherSimulator()
        self.params = {
            "sid": "TestSimulator-0",
            "step_size": 900,
            "data_path": datapath,
            "start_date": "2018-05-19 14:00:00+0100",
        }

    def test_init(self):
        """Test the init function of the simulator."""

        sim = WeatherSimulator()
        sim.init(**self.params)
        meta = sim.meta

        self.assertIsInstance(meta, dict)
        self.assertIsInstance(sim.wdata, WeatherData)
        self.assertIsInstance(sim.now_dt, datetime)

    def test_create_weather(self):
        """Test to create a weather model."""
        sim = WeatherSimulator()
        sim.init(**self.params)

        entities = sim.create(num=1, model="Weather", interpolate=False)
        self.assertEqual(len(entities), 1)
        for entity in entities:
            self.assertIsInstance(entity, dict)

    def test_create_weather_forecast(self):
        """Test to create a weather forecast model."""
        sim = WeatherSimulator()
        sim.init(**self.params)

        entities = sim.create(
            num=1,
            model="WeatherForecast",
            forecast_horizon_hours=12,
            forecast_error=0,
            seed=0,
            interpolate=False,
        )
        self.assertEqual(len(entities), 1)
        for entity in entities:
            self.assertIsInstance(entity, dict)

    def test_step(self):
        """Test a simulation step with both a weather model and a
        weather forecast model.

        """
        sim = WeatherSimulator()
        sim.init(**self.params)

        sim.create(1, "WeatherCurrent", interpolate=False)
        sim.create(
            1,
            "WeatherForecast",
            forecast_horizon_hours=12,
            forecast_error=0,
            interpolate=False,
            seed=0,
        )

        sim.step(0, {})

        t_air = sim.models["WeatherCurrent-0"].t_air_deg_celsius
        self.assertIsInstance(t_air, float)

        fc_t_air = sim.models["WeatherForecast-1"].forecast_t_air_deg_celsius
        self.assertIsInstance(fc_t_air, pd.DataFrame)

        self.assertEqual(t_air, fc_t_air.iloc[0]["t_air_deg_celsius"])

    def test_get_data(self):
        """Test the get data function of the simulator."""
        sim = WeatherSimulator()
        sim.init(**self.params)

        sim.create(1, "WeatherCurrent", interpolate=False)
        sim.create(
            1,
            "WeatherForecast",
            forecast_horizon_hours=12,
            forecast_error=0,
            interpolate=False,
            seed=0,
        )
        sim.step(0, {})

        outputs = {
            "WeatherCurrent-0": [
                "t_air_deg_celsius",
                "day_avg_t_air_deg_celsius",
            ],
            "WeatherForecast-1": [
                "forecast_bh_w_per_m2",
                "forecast_dh_w_per_m2",
            ],
        }

        data = sim.get_data(outputs)

        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 2)
        for key, value in data.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)

            for attr, val in value.items():
                self.assertIsInstance(attr, str)
                if "forecast" in attr:
                    self.assertIsInstance(val, str)
                    val = pd.read_json(val).tz_localize("UTC")
                    self.assertEqual(val.size, 48)
                    self.assertIn(val.columns[0], attr)
                else:
                    self.assertIsInstance(val, float)

    @unittest.skip
    def test_complete_dataset(self):
        """Test if the whole dataset is usable.

        Takes very long, therefore disabled by default.
        """
        sim = WeatherSimulator()
        params = {
            "sid": "TestSimulator-0",
            "step_size": 3600,
            "data_path": RuntimeConfig().paths["data_path"],
            "start_date": "2008-12-31 23:00:00+0000",
        }
        sim.init(**params)
        sim.create(1, "WeatherCurrent", interpolate=False, randomize=False)
        sim.create(
            1,
            "WeatherForecast",
            interpolate=False,
            randomize=False,
            forecast_horizon_hours=2,
            forecast_error=0,
        )
        now_dt = datetime.strptime(params["start_date"], "%Y-%m-%d %H:%M:%S%z")
        years = ([8760, 8760, 8760, 8784] * 3)[:-1]
        time = 0
        wdata = sim.models["WeatherCurrent-0"].wdata.wdata
        for hours in years:
            for hour in range(hours):
                sim.step(time, dict())
                data = sim.get_data(
                    {
                        "WeatherCurrent-0": [
                            "t_air_deg_celsius",
                            "dh_w_per_m2",
                        ],
                        "WeatherForecast-1": ["forecast_t_air_deg_celsius"],
                    }
                )
                now_str = now_dt.strftime(GER)
                self.assertEqual(
                    data["WeatherCurrent-0"]["t_air_deg_celsius"],
                    wdata["t_air_degree_celsius"].loc[now_str],
                )
                try:
                    self.assertEqual(
                        data["WeatherCurrent-0"]["dh_w_per_m2"],
                        wdata["dh_w_per_m2"].loc[now_str],
                    )
                except AssertionError as err:
                    print()
                    raise err

                fc_start = (now_dt + timedelta(hours=1)).strftime(GER)
                fc_end = (now_dt + timedelta(hours=2)).strftime(GER)
                forecast = pd.read_json(
                    data["WeatherForecast-1"]["forecast_t_air_deg_celsius"]
                ).tz_localize("UTC")
                for val1, val2 in zip(
                    forecast["t_air_deg_celsius"].values,
                    wdata["t_air_degree_celsius"].loc[fc_start:fc_end].values,
                ):
                    self.assertAlmostEqual(val1, val2)

                time += 3600
                now_dt += timedelta(seconds=3600)
            print(sim.models["WeatherCurrent-0"].now_dt)
        print(hours)
        # print(len(years))


if __name__ == "__main__":
    unittest.main()

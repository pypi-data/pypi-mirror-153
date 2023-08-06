"""Test for the current-weather model."""
import unittest
from datetime import datetime, timezone, timedelta
from os.path import abspath, join

from midas.core.weather.model.current import WeatherCurrent
from midas.core.weather.model.provider import WeatherData
from midas.util.runtime_config import RuntimeConfig


class TestWeatherCurrent(unittest.TestCase):
    """Test class for the current-weather model."""

    def setUp(self):
        self.datapath = abspath(
            join(
                RuntimeConfig().paths["data_path"],
                RuntimeConfig().data["weather"][0]["name"],
            )
        )
        wdata = WeatherData(filename=self.datapath, seed=0)

        self.now_dt = datetime(
            year=2018,
            month=5,
            day=19,
            hour=13,
            minute=0,
            second=0,
            tzinfo=timezone.utc,
        )

        self.weather = WeatherCurrent(
            wdata=wdata,
            start_date=self.now_dt,
        )

    def test_init(self):
        """Test the init function."""
        weather = WeatherCurrent(
            wdata=WeatherData(filename=self.datapath), start_date=self.now_dt
        )
        self.assertIsInstance(weather.wdata, WeatherData)
        self.assertIsInstance(weather.now_dt, datetime)

    def test_step(self):
        """Test the step function."""
        weather = WeatherCurrent(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
            step_size=900,
        )
        weather.step()

        self.assertIsInstance(weather.t_air_deg_celsius, float)
        self.assertIsInstance(weather.day_avg_t_air_deg_celsius, float)
        self.assertIsInstance(weather.bh_w_per_m2, float)
        self.assertIsInstance(weather.dh_w_per_m2, float)

    def test_three_steps(self):
        """Test three calls of the step function."""
        weather = WeatherCurrent(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
        )

        # First step
        weather.now_dt = self.now_dt  # Redundant because of first step
        weather.step()
        bh_w_per_m2 = weather.bh_w_per_m2
        dh_w_per_m2 = weather.dh_w_per_m2
        t_air_deg_celsius = weather.t_air_deg_celsius
        day_avg_t_air_deg_celsius = weather.day_avg_t_air_deg_celsius

        # Second step, no changes due to resolution
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        self.assertEqual(t_air_deg_celsius, weather.t_air_deg_celsius)
        self.assertEqual(
            day_avg_t_air_deg_celsius, weather.day_avg_t_air_deg_celsius
        )
        self.assertEqual(bh_w_per_m2, weather.bh_w_per_m2)
        self.assertEqual(dh_w_per_m2, weather.dh_w_per_m2)

        weather.now_dt += timedelta(seconds=3600)
        weather.step()
        self.assertNotEqual(bh_w_per_m2, weather.bh_w_per_m2)
        self.assertNotEqual(dh_w_per_m2, weather.dh_w_per_m2)
        self.assertNotEqual(t_air_deg_celsius, weather.t_air_deg_celsius)
        self.assertEqual(
            day_avg_t_air_deg_celsius, weather.day_avg_t_air_deg_celsius
        )

    def test_interpolate(self):
        """Test interpolation of weather data."""
        weather = WeatherCurrent(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
            interpolate=True,
        )
        t_airs = []
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)

        for idx in range(1, len(t_airs)):
            self.assertGreater(t_airs[idx], t_airs[idx - 1])

    def test_seed(self):
        """Test randomization of weather data."""
        weather = WeatherCurrent(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
            step_size=900,
            seed=0,
            randomize=True,
        )
        t_airs = []
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)
        weather.now_dt += timedelta(seconds=900)
        weather.step()
        t_airs.append(weather.t_air_deg_celsius)

        for idx in range(1, len(t_airs)):
            self.assertNotEqual(t_airs[idx], t_airs[idx - 1])


if __name__ == "__main__":
    unittest.main()

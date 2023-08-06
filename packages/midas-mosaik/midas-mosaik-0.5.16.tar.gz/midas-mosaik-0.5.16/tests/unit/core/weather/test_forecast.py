"""This module contains the test for the weather-forecast model."""
import unittest
from datetime import datetime, timezone
from os.path import abspath, join

from midas.core.weather.model.forecast import WeatherForecast
from midas.core.weather.model.provider import WeatherData
from midas.util.runtime_config import RuntimeConfig


class TestWeatherForecast(unittest.TestCase):
    """Test class for the weather-forecast model."""

    def setUp(self):
        self.datapath = abspath(
            join(
                RuntimeConfig().paths["data_path"],
                RuntimeConfig().data["weather"][0]["name"],
            )
        )

        self.now_dt = datetime(
            year=2018,
            month=3,
            day=24,
            hour=22,
            minute=30,
            second=0,
            tzinfo=timezone.utc,
        )

    def test_init(self):
        """Test the init function."""
        weather = WeatherForecast(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
            forecast_horizon_hours=3,
        )
        self.assertIsInstance(weather.wdata, WeatherData)
        self.assertIsInstance(weather.now_dt, datetime)

    def test_step(self):
        """Test the step function."""
        weather = WeatherForecast(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
            step_size=900,
            forecast_horizon_hours=5,
            forecast_error=0,
        )

        weather.step()

        self.assertEqual(len(weather.t_air_deg_celsius), 20)
        self.assertEqual(len(weather.day_avg_t_air_deg_celsius), 20)
        self.assertEqual(len(weather.bh_w_per_m2), 20)
        self.assertEqual(len(weather.dh_w_per_m2), 20)

        expected = [
            7.0,
            7.1,
            7.1,
            7.1,
            7.1,
            7.1,
            7.1,
            7.1,
            7.1,
            6.8,
            6.8,
            6.8,
            6.8,
            6.3,
            6.3,
            6.3,
            6.3,
            5.8,
            5.8,
            5.8,
        ]
        self.assertEqual(weather.t_air_deg_celsius, expected)

    def test_interpolate(self):
        """Test the step function with interpolate option."""
        weather = WeatherForecast(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
            step_size=900,
            forecast_horizon_hours=4,
            forecast_error=0,
            interpolate=True,
        )

        weather.step()

        self.assertEqual(len(weather.t_air_deg_celsius), 16)
        self.assertEqual(len(weather.day_avg_t_air_deg_celsius), 16)
        self.assertEqual(len(weather.bh_w_per_m2), 16)
        self.assertEqual(len(weather.dh_w_per_m2), 16)

        expected = [
            [7.0, 7.1],
            [6.8, 7.1],
            [6.8, 7.1],
            [6.8, 7.1],
            [6.8, 7.1],
            [6.3, 6.8],
            [6.3, 6.8],
            [6.3, 6.8],
            [6.3, 6.8],
            [5.8, 6.3],
            [5.8, 6.3],
            [5.8, 6.3],
            [5.8, 6.3],
            [5.6, 6.8],
            [5.6, 6.8],
            [5.6, 6.8],
        ]
        for act, exp in zip(weather.t_air_deg_celsius, expected):
            self.assertTrue(exp[0] <= act <= exp[1])

    def test_with_error(self):
        """Test the step function with forecast_error option."""
        weather = WeatherForecast(
            wdata=WeatherData(filename=self.datapath),
            start_date=self.now_dt,
            step_size=900,
            forecast_horizon_hours=4,
            forecast_error=0.05,
            interpolate=False,
            seed=0,
            randomize=True,
        )

        weather.step()

        self.assertEqual(len(weather.t_air_deg_celsius), 16)
        self.assertEqual(len(weather.day_avg_t_air_deg_celsius), 16)
        self.assertEqual(len(weather.bh_w_per_m2), 16)
        self.assertEqual(len(weather.dh_w_per_m2), 16)

        expected = [
            7.0,
            7.1,
            7.1,
            7.1,
            7.1,
            6.8,
            6.8,
            6.8,
            6.8,
            6.3,
            6.3,
            6.3,
            6.3,
            5.8,
            5.8,
            5.8,
        ]
        self.assertNotEqual(weather.t_air_deg_celsius, expected)

    def test_forecast_returns_enough_values(self):
        for num in range(20):
            fch = num / 4
            weather = WeatherForecast(
                wdata=WeatherData(filename=self.datapath),
                start_date=self.now_dt,
                step_size=900,
                forecast_horizon_hours=fch,
                forecast_error=0.05,
                interpolate=False,
                seed=0,
                randomize=True,
            )

            weather.step()
            self.assertEqual(num, len(weather.forecast.index))


if __name__ == "__main__":
    unittest.main()

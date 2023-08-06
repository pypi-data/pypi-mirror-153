"""This module contains the test for the weather data provider."""
import unittest
from datetime import datetime, timedelta, timezone
from os.path import abspath, join

from midas.core.weather.model.provider import (
    AVG_T_AIR,
    DI,
    GHI,
    T_AIR,
    WIND,
    WINDDIR,
    WeatherData,
)
from midas.util.runtime_config import RuntimeConfig
from pandas.core.frame import DataFrame

# CFG = config.check_config(None)


class TestWeather(unittest.TestCase):
    """Test the weather data provider."""

    def setUp(self):
        self.datapath = abspath(
            join(
                RuntimeConfig().paths["data_path"],
                RuntimeConfig().data["weather"][0]["name"],
            )
        )
        self.wdp = WeatherData(filename=self.datapath, seed=0)

    def test_init(self):
        """Test the init function."""
        self.assertIsInstance(self.wdp.wdata, DataFrame)
        cols = self.wdp.wdata.columns
        self.assertIn(AVG_T_AIR, cols)
        self.assertIn(T_AIR, cols)
        self.assertIn(GHI, cols)
        self.assertIn(DI, cols)
        self.assertIn(WIND, cols)
        self.assertIn(WINDDIR, cols)

    def test_results(self):
        """Test the results."""
        now_dt = datetime(
            year=2018,
            month=5,
            day=19,
            hour=12,
            minute=0,
            second=0,
            tzinfo=timezone.utc,
        )

        data = self.wdp.select_hour(now_dt)
        t_air = data[0][0]
        day_avg_t_air = data[1][0]
        bh_w = data[2][0]
        dh_w = data[3][0]
        self.assertEqual(t_air, 16.6)
        self.assertAlmostEqual(day_avg_t_air, 12.31666667)
        self.assertAlmostEqual(dh_w, 386.1111111)
        self.assertAlmostEqual(bh_w, (411.1111111 - dh_w))

        data = self.wdp.select_hour(now_dt + timedelta(hours=1))
        self.assertEqual(data[0][0], 17.2)
        self.assertAlmostEqual(data[1][0], 12.316666667)
        self.assertAlmostEqual(data[3][0], 416.6666667)
        self.assertAlmostEqual(data[2][0], 450 - 416.6666667)

    def test_select_hour(self):
        """Test the select hour function."""
        now_dt = datetime(
            year=2017,
            month=12,
            day=31,
            hour=23,
            minute=0,
            second=0,
            tzinfo=timezone.utc,
        )

        data = self.wdp.select_hour(now_dt)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 1)
            for value in datum:
                self.assertIsInstance(value, float)

    def test_horizon_normal(self):
        """The forecast horizon function."""
        now_dt = datetime(
            year=2017,
            month=12,
            day=31,
            hour=23,
            minute=0,
            second=0,
            tzinfo=timezone.utc,
        )

        data = self.wdp.select_hour(now_dt, horizon=2)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 2)

    def test_horizon_special(self):
        """Test the forecast horizon function with day change.

        This list has one item more since the weather data have a
        hourly resolution and only full hours can be fetched.

        """
        now_dt = datetime(
            year=2018,
            month=1,
            day=1,
            hour=23,
            minute=15,
            second=0,
            tzinfo=timezone(offset=timedelta(seconds=3600)),
        )

        data = self.wdp.select_hour(now_dt, horizon=2)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 3)

    # Since now all data is usable, those tests fail.
    # Before that, data from the same year was reused
    # To fix those tests, the assert values must be checked
    # against the dataset.
    @unittest.skip
    def test_select_block(self):
        """Test the select block function."""
        wdp = WeatherData(filename=self.datapath, seed=0)
        now_dt = datetime(
            year=2018,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=timezone(offset=timedelta(seconds=3600)),
        )

        data = wdp.select_block(now_dt, horizon=2, frame=1)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 2)
        self.assertIn(data[0][0], [4.4, 6.7, 9.1])
        self.assertIn(data[0][1], [3.4, 6.7, 7.9])

    @unittest.skip
    def test_select_hour_year_change(self):
        """Test select hour functions with a year change.

        Data from the new year should be taken from the beginning of
        the dataset.

        """
        wdp = WeatherData(filename=self.datapath, seed=0)
        now_dt = datetime(
            year=2018,
            month=12,
            day=31,
            hour=23,
            minute=0,
            second=0,
            tzinfo=timezone(offset=timedelta(seconds=3600)),
        )

        data = wdp.select_hour(now_dt)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 1)
            for value in datum:
                self.assertIsInstance(value, float)

        data = wdp.select_hour(now_dt, horizon=2)

        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 2)
            for value in datum:
                self.assertIsInstance(value, float)

    @unittest.skip
    def test_select_block_year_change(self):
        """Test the select block function with a year change."""
        wdp = WeatherData(filename=self.datapath, seed=0)
        now_dt = datetime(
            year=2018,
            month=12,
            day=31,
            hour=23,
            minute=0,
            second=0,
            tzinfo=timezone(offset=timedelta(seconds=3600)),
        )
        data = wdp.select_block(now_dt, horizon=2, frame=1)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for datum in data:
            self.assertIsInstance(datum, list)
            self.assertEqual(len(datum), 2)
        self.assertIn(data[0][0], [6.7, 8.2, 4.2])
        self.assertIn(data[0][1], [6.7, 9.1, 4.4])


if __name__ == "__main__":
    unittest.main()

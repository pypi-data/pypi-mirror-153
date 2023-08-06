import unittest
from datetime import datetime, time, timedelta, timezone

from midas.core.time.simulator import TimeSimulator


class TestTimeSimulator(unittest.TestCase):
    def setUp(self):
        self.sd_1 = "2020-01-01 00:00:00+0100"
        self.sd_2 = "2020-01-01 00:00:00+0000"
        self.sd_3 = "2021-06-08 15:51:00+0200"

    def test_init1(self):
        """Test init method with start date 1."""
        timesim = TimeSimulator()
        timesim.init(sid="TimeSim-0", step_size=900, start_date=self.sd_1)

        self.assertEqual(2019, timesim._utc_now_dt.year)
        self.assertEqual(12, timesim._utc_now_dt.month)
        self.assertEqual(31, timesim._utc_now_dt.day)
        self.assertEqual(23, timesim._utc_now_dt.hour)
        self.assertEqual(0, timesim._utc_now_dt.minute)

        self.assertEqual(2020, timesim._local_now_dt.year)
        self.assertEqual(1, timesim._local_now_dt.month)
        self.assertEqual(1, timesim._local_now_dt.day)
        self.assertEqual(0, timesim._local_now_dt.hour)

        self.assertEqual(0, timesim._day_dif_td.total_seconds())
        self.assertEqual(0, timesim._year_dif_td.total_seconds())
        self.assertEqual(
            2 * 24 * 60 * 60, timesim._week_dif_td.total_seconds()
        )

    def test_init2(self):
        """Test init method with start date 2."""
        timesim = TimeSimulator()
        timesim.init(sid="TimeSim-0", step_size=900, start_date=self.sd_2)

        self.assertEqual(2020, timesim._utc_now_dt.year)
        self.assertEqual(1, timesim._utc_now_dt.month)
        self.assertEqual(1, timesim._utc_now_dt.day)
        self.assertEqual(0, timesim._utc_now_dt.hour)
        self.assertEqual(0, timesim._utc_now_dt.minute)
        self.assertEqual(0, timesim._utc_now_dt.second)

        self.assertEqual(2020, timesim._local_now_dt.year)
        self.assertEqual(1, timesim._local_now_dt.month)
        self.assertEqual(1, timesim._local_now_dt.day)
        self.assertEqual(0, timesim._local_now_dt.hour)
        self.assertEqual(0, timesim._local_now_dt.minute)
        self.assertEqual(0, timesim._local_now_dt.second)

        self.assertEqual(0, timesim._day_dif_td.total_seconds())
        self.assertEqual(0, timesim._year_dif_td.total_seconds())
        self.assertEqual(
            2 * 24 * 60 * 60, timesim._week_dif_td.total_seconds()
        )

    def test_init3(self):
        """Test init method with start date 3."""
        timesim = TimeSimulator()
        timesim.init(sid="TimeSim-0", step_size=900, start_date=self.sd_3)

        self.assertEqual(2021, timesim._utc_now_dt.year)
        self.assertEqual(6, timesim._utc_now_dt.month)
        self.assertEqual(8, timesim._utc_now_dt.day)
        self.assertEqual(13, timesim._utc_now_dt.hour)
        self.assertEqual(51, timesim._utc_now_dt.minute)
        self.assertEqual(0, timesim._utc_now_dt.second)

        self.assertEqual(2021, timesim._local_now_dt.year)
        self.assertEqual(6, timesim._local_now_dt.month)
        self.assertEqual(8, timesim._local_now_dt.day)
        self.assertEqual(15, timesim._local_now_dt.hour)
        self.assertEqual(51, timesim._local_now_dt.minute)
        self.assertEqual(0, timesim._local_now_dt.second)

        self.assertEqual(57060, timesim._day_dif_td.total_seconds())
        self.assertEqual(13708260, timesim._year_dif_td.total_seconds())
        self.assertEqual(
            1 * 24 * 60 * 60, timesim._week_dif_td.total_seconds()
        )

    def test_step1(self):
        """Test the step function with start date 1.

        The start date is the beginning of the year. Therefore, day and
        year start at the beginning (sin=0, cos=1). The weekday is a
        Wednesday and, therefore, the time has progressed a little bit.

        """
        timesim = TimeSimulator()
        timesim.init(sid="TimeSim-0", step_size=900, start_date=self.sd_1)
        timesim.create(1, "Timegenerator")
        timesim.step(0, dict())
        data = timesim.get_data(dict())[timesim.eid]
        self.assertEqual(0, data["sin_day_time"])
        self.assertTrue(0.97 < data["sin_week_time"] < 0.98)
        self.assertEqual(0, data["sin_year_time"])
        self.assertEqual(1, data["cos_day_time"])
        self.assertTrue(-0.23 < data["cos_week_time"] < -0.22)
        self.assertEqual(1, data["cos_year_time"])

        # Time does not progress in the first step
        self.assertEqual("2019-12-31 23:00:00+0000", data["utc_time"])
        self.assertEqual("2020-01-01 00:00:00+0100", data["local_time"])

    def test_step3(self):
        """Test the step function with start date 3.

        The start date is an arbitrary chosen date in the mids of the
        year (2021-06-08 15:51:00+0200). Therefore, all values are
        progressed, even if we only simulate one step.

        """
        timesim = TimeSimulator()
        timesim.init(sid="TimeSim-0", step_size=900, start_date=self.sd_3)
        timesim.create(1, "Timegenerator")
        timesim.step(0, dict())
        data = timesim.get_data(dict())[timesim.eid]

        self.assertTrue(-0.85 < data["sin_day_time"] < -0.84)
        self.assertTrue(0.78 < data["sin_week_time"] < 0.79)
        self.assertTrue(0.39 < data["sin_year_time"] < 0.4)
        self.assertTrue(-0.54 < data["cos_day_time"] < -0.53)
        self.assertTrue(0.62 < data["cos_week_time"] < 0.63)
        self.assertTrue(-0.92 < data["cos_year_time"] < -0.91)
        self.assertEqual("2021-06-08 13:51:00+0000", data["utc_time"])
        self.assertEqual("2021-06-08 15:51:00+0200", data["local_time"])


if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from midas.util.base_data_model import DataModel
from midas.util.dateformat import GER


class TestDataModel(unittest.TestCase):
    def setUp(self):
        self.data_p = pd.DataFrame(data=np.arange(10), columns=["p_mw"])
        self.now_dt = datetime.strptime("2009-01-01 00:00:00+0100", GER)

    def test_init(self):

        dm = DataModel(
            data_p=self.data_p["p_mw"],
            data_q=None,
            data_step_size=900,
            scaling=1.0,
        )

        self.assertEqual(900, dm.sps)
        self.assertEqual(180, dm.p_mwh_per_a)
        self.assertEqual(10, len(dm.data_p))
        self.assertAlmostEqual(3.02765035, dm.p_std)

    def test_step(self):
        dm = DataModel(
            data_p=self.data_p["p_mw"],
            data_q=None,
            data_step_size=900,
            scaling=1.0,
            interpolate=True,
        )
        # now_dt = datetime.strptime("2009-01-01 00:00:00+0100", GER)
        dm.cos_phi = 0.9
        dm.now_dt = self.now_dt
        # dm.step()

    def test_false_interpolate(self):
        """Test is the interpolation takes the second value from
        the beginning of the dataset if necessary.
        """
        dm = DataModel(
            data_p=self.data_p["p_mw"],
            data_q=None,
            data_step_size=900,
            scaling=1.0,
            interpolate=True,
        )
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
        for idx in range(12):
            dm.now_dt = self.now_dt
            res = dm._interpolate(idx % 10, dm.data_p)
            self.assertEqual(expected[idx], res)
            self.now_dt += timedelta(seconds=900)

    def test_true_interpolate(self):
        """Like above, but this time an interpolation is really
        required.
        """
        dm = DataModel(
            data_p=self.data_p["p_mw"],
            data_q=None,
            data_step_size=3600,
            scaling=1.0,
            interpolate=True,
        )
        expected = (
            [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]
            + [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75]
            + [4, 4.25, 4.5, 4.75, 5, 5.25, 5.5, 5.75]
            + [6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75]
            + [8, 8.25, 8.5, 8.75, 9, 6.75, 4.5, 2.25]
            + [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]
        )
        for idx in range(48):
            dm.now_dt = self.now_dt
            res = dm._interpolate(int(idx * 0.25) % 10, dm.data_p)
            self.assertEqual(expected[idx], res)
            self.now_dt += timedelta(seconds=900)

    def test_no_interpolation(self):
        """Test if the correct value is selected from the dataset."""
        dm = DataModel(
            data_p=self.data_p["p_mw"],
            data_q=None,
            data_step_size=900,
            scaling=1.0,
            interpolate=False,
        )
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
        for idx in range(12):
            dm.now_dt = self.now_dt
            dm._interpolation()
            self.assertEqual(expected[idx], dm.p_mw)
            self.now_dt += timedelta(seconds=900)

    def test_false_interpolation(self):
        dm = DataModel(
            data_p=self.data_p["p_mw"],
            data_q=None,
            data_step_size=900,
            scaling=1.0,
            interpolate=True,
        )
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
        for idx in range(12):
            dm.now_dt = self.now_dt
            dm._interpolation()
            self.assertEqual(expected[idx], dm.p_mw)
            self.now_dt += timedelta(seconds=900)

    def test_true_interpolation(self):
        """Like above, but this time an interpolation is really
        required.
        """
        dm = DataModel(
            data_p=self.data_p["p_mw"],
            data_q=None,
            data_step_size=3600,
            scaling=1.0,
            interpolate=True,
        )
        expected = (
            [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]
            + [2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75]
            + [4, 4.25, 4.5, 4.75, 5, 5.25, 5.5, 5.75]
            + [6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75]
            + [8, 8.25, 8.5, 8.75, 9, 6.75, 4.5, 2.25]
            + [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]
        )
        for idx in range(48):
            dm.now_dt = self.now_dt
            dm._interpolation()
            self.assertEqual(expected[idx], dm.p_mw)
            self.now_dt += timedelta(seconds=900)


if __name__ == "__main__":
    unittest.main()

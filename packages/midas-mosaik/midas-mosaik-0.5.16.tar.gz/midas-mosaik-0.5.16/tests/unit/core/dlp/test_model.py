import unittest
from datetime import datetime, timedelta

from midas.core.dlp.model import DLPModel
from midas.core.dlp.simulator import DLPSimulator
from midas.util.dateformat import GER
from midas.util.runtime_config import RuntimeConfig


class TestModel(unittest.TestCase):
    def setUp(self):
        sim_params = {
            "sid": "TestSimulator-0",
            "step_size": 900,
            "start_date": "2021-11-16 15:45:00+0100",
            "data_path": RuntimeConfig().paths["data_path"],
            "filename": "DefaultLoadProfiles.hdf5",
        }
        sim = DLPSimulator()
        sim.init(**sim_params)
        self.data = sim.data

    def test_init(self):
        """Test the different default settings for the model."""
        model_min = DLPModel(data=self.data["H0"], p_mwh_per_a=1.0, seed=0)
        model_full = DLPModel(
            data=self.data["H0"],
            p_mwh_per_a=1.0,
            seed=0,
            interpolate=False,
            randomize_data=False,
            randomize_data_scale=0.05,
            randomize_cos_phi=False,
            randomize_cos_phi_scale=0.01,
        )

        self.assertEqual(model_min._interpolate, model_full._interpolate)
        self.assertEqual(model_min._randomize_data, model_full._randomize_data)
        self.assertEqual(
            model_min._randomize_cos_phi, model_full._randomize_cos_phi
        )
        self.assertEqual(
            model_min._randomize_data_scale, model_full._randomize_data_scale
        )
        self.assertEqual(
            model_min._randomize_cos_phi_scale,
            model_full._randomize_cos_phi_scale,
        )
        self.assertEqual(model_min._rng.normal(), model_full._rng.normal())

    def test_step_winter_days(self):
        """Step different winter days and compare results.

        Monday, Tuesday, Saturday, and Sunday from different winter
        months are selected. Monday and Tuesday should be the same while
        Saturday and Sunday should be different from Monday and from
        each other.

        """
        model = DLPModel(data=self.data["H0"], p_mwh_per_a=1.0, seed=0)

        model.now_dt = datetime.strptime("2021-01-04 10:00:00+0100", GER)
        model.cos_phi = 0.9

        model.step()
        win_mon_p = model.p_mw

        model.now_dt = datetime.strptime("2021-02-02 10:00:00+0100", GER)
        model.cos_phi = 0.9

        model.step()
        win_tue_p = model.p_mw

        self.assertEqual(win_mon_p, win_tue_p)

        model.now_dt = datetime.strptime("2021-02-28 10:00:00+0100", GER)
        model.cos_phi = 0.9

        model.step()
        win_sun_p = model.p_mw

        self.assertNotEqual(win_sun_p, win_mon_p)

        model.now_dt = datetime.strptime("2020-12-26 10:00:00+0100", GER)
        model.cos_phi = 0.9

        model.step()
        win_sat_p = model.p_mw

        self.assertNotEqual(win_sun_p, win_sat_p)
        self.assertNotEqual(win_mon_p, win_sat_p)

    def test_conversion_pmwhpera_to_pmw(self):
        """Test if the model outputs p_mws with a total amount
        of p_mwh_per_a over a year.

        """

        model = DLPModel(data=self.data["H0"], p_mwh_per_a=1.0, seed=0)

        now_dt = datetime.strptime("2017-01-01 00:00:00+0100", GER)

        p_mws = list()
        for _ in range(35040):
            model.now_dt = now_dt
            model.cos_phi = 0.9

            model.step()
            p_mws.append(model.p_mw)

            now_dt += timedelta(seconds=900)

        # self.assertEqual("2018-01-01 00:00:00+0100", now_dt.strftime(GER))
        self.assertTrue(1.0 <= sum(p_mws) / 4 <= 1.01)

        self.assertEqual(73.2 * 1e-6, p_mws[0])

    def test_interpolate(self):
        model = DLPModel(
            data=self.data["H0"], p_mwh_per_a=1.0, seed=0, interpolate=True
        )

        model.now_dt = datetime.strptime("2021-01-04 10:00:00+0100", GER)
        model.cos_phi = 0.9
        model.step()
        first_p = model.p_mw

        self.assertAlmostEqual(119 * 1e-6, first_p)

        model.now_dt = datetime.strptime("2021-01-04 10:15:00+0100", GER)
        model.cos_phi = 0.9
        model.step()
        second_p = model.p_mw

        self.assertAlmostEqual(117.3 * 1e-6, second_p)

        model.now_dt = datetime.strptime("2021-01-04 10:05:00+0100", GER)
        model.cos_phi = 0.9
        model.step()
        inter1_p = model.p_mw

        expected = first_p + 1 / 3 * (second_p - first_p)
        self.assertAlmostEqual(expected, inter1_p)


if __name__ == "__main__":
    unittest.main()

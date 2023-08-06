import os
import unittest

import numpy as np
import pandas as pd
from midas.core.store import MidasHdf5


class TestMidasHdf5(unittest.TestCase):
    def setUp(self):
        self.inputs1 = {
            "Database": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-0": 0.1,
                    "DummySim-0.DummyHousehold-1": 0.2,
                    "DummySim-1.DummyPV-0": 0.3,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-0": 0.01,
                    "DummySim-0.DummyHousehold-1": 0.02,
                    "DummySim-1.DummyPV-0": 0.03,
                },
                "t_air": {
                    "DummyWeather-0.WeatherCurrent-0": 15.0,
                },
            }
        }
        self.inputs2 = {
            "Database": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-0": 0.02,
                    "DummySim-0.DummyHousehold-1": 0.02,
                    "DummySim-1.DummyPV-0": 0.03,
                    "DummySim-2.DummyCHP-0": 0.5,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-0": 0.01,
                    "DummySim-0.DummyHousehold-1": 0.015,
                    "DummySim-1.DummyPV-0": 0.01,
                },
                "t_air": {
                    "DummyWeather-0.WeatherCurrent-0": 15.0,
                },
                "wind": {
                    "DummyWeather-1.WeatherForecast-0": 20,
                },
            }
        }

    def test_setup(self):
        """Test store creation and ensure to allow only one instance."""
        dbsim = MidasHdf5()

        dbsim.init("MidasHdf5", step_size=900)

        # Only one instance allowed
        with self.assertRaises(AssertionError):
            dbsim.create(2, "Database", filename="there.hdf5")

        dbsim.create(1, "Database", filename="here.hdf5")

        self.assertIsNotNone(dbsim.database)
        self.assertEqual("here.hdf5", dbsim.filename)
        self.assertEqual(900, dbsim.step_size)

        # Only one instance allowed
        with self.assertRaises(AssertionError):
            dbsim.create(1, "Database", filename="there.hdf5")

    def test_step(self):
        dbsim = MidasHdf5()
        dbsim.init("MidasHdf5", step_size=900)
        dbsim.create(1, "Database", filename="here.hdf5")
        dbsim.step(0, self.inputs1)

        dbsim.step(900, self.inputs2)

        # print(dbsim.database["DummySim-0"])

    @unittest.skip
    def test_huge_dataset(self):
        """Test if a large dataset can be stored. Takes very long
        and should not be necessary most of the time.
        """
        dbsim = MidasHdf5()
        dbsim.init("MidasHdf5", step_size=900)
        dbsim.create(1, "Database", filename="here.hdf5")

        for idx in range(5 * 365 * 24 * 4):
            dbsim.step(idx * 900, self.inputs1)

            if idx % 96 == 0:
                print(idx / 96, end="\r")

        print()
        dbsim.finalize()

    @unittest.skip
    def test_huge_dataset2(self):
        dbsim = MidasHdf5()
        dbsim.init("MidasHdf5", step_size=900)
        dbsim.create(1, "Database", filename="here.hdf5")
        data = np.ones((5 * 365 * 24 * 4, 4))
        dbsim.database["DummySim-0"] = pd.DataFrame(
            data,
            columns=[
                "DummyMod-0.p_mw",
                "DummyMod-0.q_mvar",
                "DummyMod-1.p_mw",
                "DummyMod-1.q_mvar",
            ],
        )
        dbsim.database["DummySim-1"] = pd.DataFrame(
            data,
            columns=[
                "DummyMod-0.p_mw",
                "DummyMod-0.q_mvar",
                "DummyMod-1.p_mw",
                "DummyMod-1.q_mvar",
            ],
        )
        dbsim.database["DummySim-2"] = pd.DataFrame(
            data,
            columns=[
                "DummyMod-0.p_mw",
                "DummyMod-0.q_mvar",
                "DummyMod-1.p_mw",
                "DummyMod-1.q_mvar",
            ],
        )
        dbsim.finalize()
        print("saved", dbsim.database["DummySim-0"].shape)

    def test_threaded_store(self):
        """Test if the use of thread preserves all information."""
        dbfile = os.path.abspath("threads_here.hdf5")
        if os.path.exists(dbfile):
            os.remove(dbfile)

        dbsim = MidasHdf5()
        dbsim.init("MidasHdf5", step_size=900)
        dbsim.create(1, "Database", filename=dbfile, buffer_size=5)

        for step in range(16):
            dbsim.step(step * 900, self.inputs1)

        dbsim.finalize()

        db_restored = dict()
        for sid in ["DummySim-0", "DummySim-1", "DummyWeather-0"]:
            db_restored[sid] = pd.read_hdf(dbfile, sid)
            self.assertEqual(16, len(db_restored[sid].index))

        # Clean up
        os.remove(dbfile)

    def test_unthreaded_store(self):
        """Test if the store is still valid even without threads."""
        dbfile = os.path.abspath("no_threads_here.hdf5")
        if os.path.exists(dbfile):
            os.remove(dbfile)

        dbsim = MidasHdf5()
        dbsim.init("MidasHdf5", step_size=900)
        dbsim.create(1, "Database", filename=dbfile, buffer_size=0)

        for step in range(16):
            dbsim.step(step * 900, self.inputs1)

        dbsim.finalize()

        db_restored = dict()
        for sid in ["DummySim-0", "DummySim-1", "DummyWeather-0"]:
            db_restored[sid] = pd.read_hdf(dbfile, sid)
            self.assertEqual(16, len(db_restored[sid].index))

        # Clean up
        os.remove(dbfile)


if __name__ == "__main__":
    unittest.main()

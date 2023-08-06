"""
This module contains the test cases for the simbench data simulator.

"""
import unittest

from midas.core.pwdata.simulator import PVWindDataSimulator
from midas.util.base_data_model import DataModel
from midas.util.runtime_config import RuntimeConfig


class TestSimulator(unittest.TestCase):
    """Test case for the simbench data simulator."""

    def setUp(self):
        self.sim = PVWindDataSimulator()
        self.sim_params = {
            "sid": "TestSimulator-0",
            "step_size": 900,
            "start_date": "2019-11-16 15:45:00+0100",
            "data_path": RuntimeConfig().paths["data_path"],
        }

    def test_init(self):
        sim = self.sim
        meta = sim.init(**self.sim_params)

        self.assertIsInstance(meta, dict)

    def test_create(self):
        sim = self.sim
        sim.init(**self.sim_params)

        # Test create
        entities = sim.create(3, "PV")
        self.assertEqual(len(entities), 3)
        for entity in entities:
            self.assertIsInstance(entity, dict)
            self.assertIn(entity["eid"], sim.models)
            self.assertIsInstance(sim.models[entity["eid"]], DataModel)

        self.assertEqual("PV-0", entities[0]["eid"])

        entities = sim.create(2, "Wind")
        self.assertEqual(len(entities), 2)
        for entity in entities:
            self.assertIsInstance(entity, dict)
            self.assertIn(entity["eid"], sim.models)
            self.assertIsInstance(sim.models[entity["eid"]], DataModel)

        self.assertEqual("Wind-1", entities[1]["eid"])

        entities = sim.create(1, "PV", idx=1)
        self.assertEqual(len(entities), 1)
        self.assertEqual("PV-3", entities[0]["eid"])

    def test_step_and_get_data(self):

        sim = self.sim
        sim.init(**self.sim_params)

        pv_ent = sim.create(2, "PV")
        wind_ent = sim.create(1, "Wind")
        wind_off_ent = sim.create(1, "WindOffshore")
        sim.step(0, dict())

        data = sim.get_data(
            {
                pv_ent[0]["eid"]: ["p_mw", "q_mvar"],
                pv_ent[1]["eid"]: ["p_mw", "q_mvar"],
                wind_ent[0]["eid"]: ["p_mw", "q_mvar"],
                wind_off_ent[0]["eid"]: ["p_mw", "q_mvar"],
            }
        )

        self.assertEqual(758.0, data[pv_ent[0]["eid"]]["p_mw"])
        self.assertEqual(6418.04, data[wind_ent[0]["eid"]]["p_mw"])
        self.assertEqual(786.89, data[wind_off_ent[0]["eid"]]["p_mw"])

    def test_get_data_info(self):
        sim = PVWindDataSimulator()
        sim.init(**self.sim_params)
        sim.create(1, "PV", eidx=0, scaling=1)
        sim.create(1, "PV", eidx=0, scaling=2)
        sim.create(5, "Wind")
        info = sim.get_data_info()

        self.assertIn("PV-0", info)
        self.assertIn("PV-1", info)
        self.assertEqual(
            info["PV-0"]["p_mwh_per_a"] * 2, info["PV-1"]["p_mwh_per_a"]
        )
        self.assertEqual(2, info["num_pv"])
        self.assertEqual(5, info["num_wind"])
        self.assertEqual(0, info["num_wind_offshore"])
        self.assertEqual(7, info["num_sgens"])


if __name__ == "__main__":
    unittest.main()

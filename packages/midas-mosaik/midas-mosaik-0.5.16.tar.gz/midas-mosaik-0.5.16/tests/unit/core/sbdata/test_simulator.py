"""
This module contains the test cases for the simbench data simulator.

"""
import unittest
import pandas as pd
import numpy as np
from midas.core.sbdata import SimbenchDataSimulator
from midas.util.base_data_model import DataModel
from midas.util.runtime_config import RuntimeConfig


class TestSimulator(unittest.TestCase):
    """Test case for the simbench data simulator."""

    def setUp(self):

        self.sim_params = {
            "sid": "TestSimulator-0",
            "step_size": 900,
            "start_date": "2021-11-16 15:45:00+0100",
            "data_path": RuntimeConfig().paths["data_path"],
        }

    def test_init(self):
        sim = SimbenchDataSimulator()
        meta = sim.init(**self.sim_params)

        self.assertIsInstance(meta, dict)

    def test_create(self):
        sim = SimbenchDataSimulator()
        sim.init(**self.sim_params)

        # Test create
        entities = sim.create(3, "Load")
        self.assertEqual(len(entities), 3)
        for entity in entities:
            self.assertIsInstance(entity, dict)
            self.assertIn(entity["eid"], sim.models)
            self.assertIsInstance(sim.models[entity["eid"]], DataModel)

        self.assertEqual("Load-0", entities[0]["eid"])

        entities = sim.create(2, "Sgen")
        self.assertEqual(len(entities), 2)
        for entity in entities:
            self.assertIsInstance(entity, dict)
            self.assertIn(entity["eid"], sim.models)
            self.assertIsInstance(sim.models[entity["eid"]], DataModel)

        self.assertEqual("Sgen-1", entities[1]["eid"])

        entities = sim.create(1, "Load", idx=1)
        self.assertEqual(len(entities), 1)
        self.assertEqual("Load-3", entities[0]["eid"])

    def test_step_and_get_data(self):

        sim = SimbenchDataSimulator()
        sim.init(**self.sim_params)

        load_ent = sim.create(3, "Load")
        sgen_ent = sim.create(2, "Sgen")
        sim.step(0, dict())

        data = sim.get_data(
            {
                load_ent[0]["eid"]: ["p_mw", "q_mvar"],
                load_ent[1]["eid"]: ["p_mw", "q_mvar"],
                load_ent[2]["eid"]: ["p_mw", "q_mvar"],
                sgen_ent[0]["eid"]: ["p_mw", "q_mvar"],
                sgen_ent[1]["eid"]: ["p_mw", "q_mvar"],
            }
        )

        self.assertAlmostEqual(0.0003875, data[load_ent[0]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0000547, data[load_ent[0]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0005140, data[load_ent[1]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0000590, data[load_ent[1]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0000466, data[load_ent[2]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0000215, data[load_ent[2]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0002172, data[sgen_ent[0]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0001052, data[sgen_ent[0]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0004523, data[sgen_ent[1]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0002191, data[sgen_ent[1]["eid"]]["q_mvar"])

    def test_create_storage(self):
        sim = SimbenchDataSimulator()
        sim.init(**self.sim_params)
        sim.storage_p = pd.DataFrame(np.zeros((35136, 2)))
        sim.num_storages = 2

        entities = sim.create(1, "Storage")

        self.assertEqual("Storage-0", entities[0]["eid"])
        self.assertEqual(1, sim.storage_ctr)

    def test_get_data_info(self):
        sim = SimbenchDataSimulator()
        sim.init(**self.sim_params)
        sim.create(1, "Load", eidx=0, scaling=1)
        sim.create(1, "Load", eidx=0, scaling=2)
        sim.create(5, "Sgen")
        info = sim.get_data_info()

        self.assertIn("Load-0", info)
        self.assertIn("Load-1", info)
        self.assertEqual(
            info["Load-0"]["p_mwh_per_a"] * 2, info["Load-1"]["p_mwh_per_a"]
        )
        self.assertEqual(2, info["num_loads"])
        self.assertEqual(5, info["num_sgens"])
        self.assertEqual(0, info["num_storages"])


if __name__ == "__main__":
    unittest.main()

"""
This module contains the test cases for the simbench data simulator.

"""
import unittest

from midas.core.sndata import SmartNordDataSimulator
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
        sim = SmartNordDataSimulator()
        meta = sim.init(**self.sim_params)

        self.assertIsInstance(meta, dict)

    def test_create(self):
        sim = SmartNordDataSimulator()
        sim.init(**self.sim_params)

        # Test create
        entities = sim.create(3, "Land")
        self.assertEqual(len(entities), 3)
        for entity in entities:
            self.assertIsInstance(entity, dict)
            self.assertIn(entity["eid"], sim.models)
            self.assertIsInstance(sim.models[entity["eid"]], DataModel)

        self.assertEqual("Land-0", entities[0]["eid"])

        entities = sim.create(2, "Household")
        self.assertEqual(len(entities), 2)
        for entity in entities:
            self.assertIsInstance(entity, dict)
            self.assertIn(entity["eid"], sim.models)
            self.assertIsInstance(sim.models[entity["eid"]], DataModel)

        self.assertEqual("Household-1", entities[1]["eid"])

        entities = sim.create(1, "Land", idx=1)
        self.assertEqual(len(entities), 1)
        self.assertEqual("Land-3", entities[0]["eid"])

    def test_step_and_get_data(self):

        sim = SmartNordDataSimulator()
        sim.init(**self.sim_params)

        land_ent = sim.create(3, "Land")
        house_ent = sim.create(2, "Household")
        sim.step(0, dict())

        data = sim.get_data(
            {
                land_ent[0]["eid"]: ["p_mw", "q_mvar"],
                land_ent[1]["eid"]: ["p_mw", "q_mvar"],
                land_ent[2]["eid"]: ["p_mw", "q_mvar"],
                house_ent[0]["eid"]: ["p_mw", "q_mvar"],
                house_ent[1]["eid"]: ["p_mw", "q_mvar"],
            }
        )
        self.assertAlmostEqual(0.0170418, data[land_ent[0]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0082537, data[land_ent[0]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.1163297, data[land_ent[1]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0563410, data[land_ent[1]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0423342, data[land_ent[2]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0205034, data[land_ent[2]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0001192, data[house_ent[0]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0000577, data[house_ent[0]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0000580, data[house_ent[1]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0000281, data[house_ent[1]["eid"]]["q_mvar"])

    def test_get_data_info(self):
        sim = SmartNordDataSimulator()
        sim.init(**self.sim_params)
        sim.create(1, "Land", eidx=0, scaling=1)
        sim.create(1, "Land", eidx=0, scaling=2)
        sim.create(5, "Household")
        info = sim.get_data_info()

        self.assertIn("Land-0", info)
        self.assertIn("Land-1", info)
        self.assertEqual(
            info["Land-0"]["p_mwh_per_a"] * 2, info["Land-1"]["p_mwh_per_a"]
        )
        self.assertEqual(2, info["num_lands"])
        self.assertEqual(5, info["num_households"])
        # self.assertEqual(0, info["num_storages"])


if __name__ == "__main__":
    unittest.main()

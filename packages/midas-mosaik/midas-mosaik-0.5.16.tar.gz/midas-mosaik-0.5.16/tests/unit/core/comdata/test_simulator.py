import unittest
import pandas as pd
from midas.core.comdata.simulator import CommercialDataSimulator

from midas.util.runtime_config import RuntimeConfig


class TestCommercialDataSimulator(unittest.TestCase):
    def setUp(self):
        RuntimeConfig().load()
        self.data_path = RuntimeConfig().paths["data_path"]
        self.file_path = RuntimeConfig().data["commercials"][0]["name"]
        self.start_date = "2021-11-16 16:00:00+0100"

    def test_init(self):

        sim = CommercialDataSimulator()
        sim.init(
            "TestSimulator-0",
            start_date=self.start_date,
            data_path=self.data_path,
            filename=self.file_path,
        )

        self.assertIsInstance(sim.load_p, pd.DataFrame)
        self.assertFalse(sim.load_q)

    def test_create(self):
        sim = CommercialDataSimulator()
        sim.init(
            "TestSimulator-0",
            start_date=self.start_date,
            data_path=self.data_path,
            filename=self.file_path,
        )

        sim.create(1, "SmallHotel")

        self.assertEqual(1, len(sim.models))
        self.assertEqual(1, sim.num_models["SmallHotel"])

        sim.create(2, "SuperMarket")

        self.assertEqual(3, len(sim.models))
        self.assertEqual(1, sim.num_models["SmallHotel"])
        self.assertEqual(2, sim.num_models["SuperMarket"])

    def test_step_and_get_data(self):

        sim = CommercialDataSimulator()
        sim.init(
            "TestSimulator-0",
            start_date=self.start_date,
            data_path=self.data_path,
            filename=self.file_path,
        )

        qsr_ent = sim.create(1, "QuickServiceRestaurant")
        sm_ent = sim.create(2, "SmallOffice")

        sim.step(0, dict())

        data = sim.get_data(
            {
                qsr_ent[0]["eid"]: ["p_mw", "q_mvar"],
                sm_ent[0]["eid"]: ["p_mw", "q_mvar"],
                sm_ent[1]["eid"]: ["p_mw", "q_mvar"],
            }
        )

        self.assertAlmostEqual(0.0229005, data[qsr_ent[0]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0110912, data[qsr_ent[0]["eid"]]["q_mvar"])
        self.assertAlmostEqual(0.0142743, data[sm_ent[0]["eid"]]["p_mw"])
        self.assertAlmostEqual(0.0069134, data[sm_ent[0]["eid"]]["q_mvar"])
        self.assertAlmostEqual(
            data[sm_ent[0]["eid"]]["p_mw"], data[sm_ent[1]["eid"]]["p_mw"]
        )
        self.assertAlmostEqual(
            data[sm_ent[0]["eid"]]["q_mvar"], data[sm_ent[1]["eid"]]["q_mvar"]
        )


if __name__ == "__main__":
    unittest.main()

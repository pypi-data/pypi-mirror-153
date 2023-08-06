import unittest

from midas.core.dlp.meta import MODELS
from midas.core.dlp.simulator import DLPSimulator

from midas.util.runtime_config import RuntimeConfig


class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.sim_params = {
            "sid": "TestSimulator-0",
            "step_size": 900,
            "start_date": "2021-11-16 15:45:00+0100",
            "data_path": RuntimeConfig().paths["data_path"],
            "filename": "DefaultLoadProfiles.hdf5",
        }

    def test_init(self):
        sim = DLPSimulator()
        sim.init(**self.sim_params)
        profiles = [
            "G0",
            "G1",
            "G2",
            "G3",
            "G4",
            "G5",
            "G6",
            "H0",
            "L0",
            "L1",
            "L2",
        ]
        for profile in profiles:
            self.assertIn(profile, sim.data)

    def test_create(self):
        sim = DLPSimulator()
        sim.init(**self.sim_params)

        for model in MODELS:
            entities = sim.create(1, model, p_mwh_per_a=1.0)

            self.assertEqual(f"{model}-0", entities[0]["eid"])

        for model in MODELS:
            self.assertEqual(1, sim.num_models[model])

    def test_step_and_get_data(self):
        sim = DLPSimulator()
        sim.init(**self.sim_params)

        outputs = dict()
        for model in MODELS:
            entities = sim.create(1, model, p_mwh_per_a=1.0)
            outputs[entities[0]["eid"]] = ["p_mw", "q_mvar"]

        sim.step(0, dict())
        data = sim.get_data(outputs)

        for model in MODELS:
            self.assertNotEqual(0.0, data[f"{model}-0"]["p_mw"])
            self.assertNotEqual(0.0, data[f"{model}-0"]["q_mvar"])

    def test_get_data_info(self):
        sim = DLPSimulator()
        sim.init(**self.sim_params)

        for model in MODELS:
            sim.create(1, model, p_mwh_per_a=1.0)

        info = sim.get_data_info()
        for model in MODELS:
            self.assertEqual(1.0, info[f"{model}-0"]["p_mwh_per_a"])
            self.assertEqual(1, info[f"num_{model.lower()}"])


if __name__ == "__main__":
    unittest.main()

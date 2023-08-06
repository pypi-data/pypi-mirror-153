"""This module contains the test cases for the pandapower simulator."""
import os
import unittest

from midas.core.powergrid import PandapowerSimulator


class TestSimulator(unittest.TestCase):
    """Test cases for the pandapower mosaik simulator."""

    def test_init(self):
        """Test the simulator initialization."""
        sim = PandapowerSimulator()
        meta = sim.init(
            sid="TestSimulator-0", step_size=900, sim_params=dict()
        )

        self.assertTrue("api_version" in meta)
        self.assertTrue("models" in meta)
        self.assertTrue("Grid" in meta["models"])

    def test_create(self):
        """Test the creation of a model."""

        sim = PandapowerSimulator()
        sim.init(sid="TestSimulator-0", step_size=900, sim_params=dict())

        entities = sim.create(
            num=2, model="Grid", gridfile="simple_four_bus_system"
        )

        self.assertEqual(len(entities), 2)

        for idx, entity in enumerate(entities):
            self.assertEqual(len(entity), 4)
            self.assertEqual(entity["eid"], f"Grid-{idx}")
            self.assertEqual(len(entity["children"]), 11)

    def test_step(self):
        """Test the step of the simulator.

        Two grids are instantiated at the same time to see that the
        inputs are set to the correct grid.
        """
        sim = PandapowerSimulator()
        sim.init(sid="TestSimulator-0", step_size=900, sim_params=dict())
        sim.create(2, "Grid", gridfile="simple_four_bus_system")

        inputs = {
            "0-load-0-2": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-0": 0.02,
                    "DummySim-0.DummyHousehold-1": 0.02,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-0": 0.01,
                    "DummySim-0.DummyHousehold-1": 0.005,
                },
            },
            "1-load-1-3": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-2": 0.03,
                    "DummySim-0.DummyHousehold-3": 0.01,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-2": 0.005,
                    "DummySim-0.DummyHousehold-3": 0.01,
                },
            },
        }

        sim.step(0, dict())
        self.assertAlmostEqual(
            sim.models["Grid-0"].grid.res_bus.vm_pu[1], 0.996608
        )
        self.assertAlmostEqual(
            sim.models["Grid-1"].grid.res_bus.vm_pu[1], 0.996608
        )

        sim.step(0, inputs)
        self.assertAlmostEqual(
            sim.models["Grid-0"].grid.res_bus.vm_pu[1], 0.9952088
        )
        self.assertAlmostEqual(
            sim.models["Grid-1"].grid.res_bus.vm_pu[1], 0.9950847
        )

    def test_get_data(self):
        """Test the get data method of the simulator."""
        sim = PandapowerSimulator()
        sim.init(sid="TestSimulator-0", step_size=900, sim_params=dict())
        sim.create(2, "Grid", gridfile="simple_four_bus_system")
        sim.step(0, dict())

        outputs = {
            "0-bus-1": ["vm_pu", "va_degree"],
            "1-bus-2": ["vm_pu", "va_degree"],
            "0-line-0": ["loading_percent"],
            "Grid-0": ["health", "grid_json"],
        }

        data = sim.get_data(outputs)

        self.assertAlmostEqual(data["0-bus-1"]["vm_pu"], 0.996608)
        self.assertAlmostEqual(data["1-bus-2"]["vm_pu"], 0.9377604)
        self.assertAlmostEqual(data["0-line-0"]["loading_percent"], 31.2730992)
        self.assertAlmostEqual(data["Grid-0"]["health"], 0.9454563)

    def test_with_plotting(self):
        """Test if plotting works as expected."""
        plot_file = os.path.abspath(os.path.join(__file__, "..", "_plots"))
        sim = PandapowerSimulator()
        sim.init(
            sid="TestSimulator-0",
            step_size=900,
            plotting=True,
            plot_path=plot_file,
        )
        sim.create(1, "Grid", gridfile="simple_four_bus_system", plotting=True)

        sim.step(0, dict())

        self.assertTrue(os.path.isdir(plot_file))
        files = os.listdir(plot_file)
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith(".png"))

        # Clean up
        os.remove(os.path.join(plot_file, files[0]))
        os.rmdir(plot_file)


if __name__ == "__main__":
    unittest.main()

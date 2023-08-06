"""This module contains test cases for the pandapower grid model."""
import unittest
from midas.core.powergrid.model.static import PandapowerGrid


class TestPandapowerGrid(unittest.TestCase):
    """Test case for the pandapower grid wrapper."""

    def test_cigre_lv(self):
        """Test for *common* pandapower grids."""
        model = PandapowerGrid()
        model.setup("cigre_lv", 0)

        model.run_powerflow(0)
        outputs = model.get_outputs()
        self.assertTrue(outputs)

    def test_cigre_mv(self):
        """Test for *common* pandapower grids."""
        model = PandapowerGrid()
        model.setup("cigre_mv", 0)

        model.run_powerflow(0)
        outputs = model.get_outputs()
        self.assertTrue(outputs)

    def test_cigre_hv(self):
        """Test for *common* pandapower grids."""
        model = PandapowerGrid()
        model.setup("cigre_hv", 0)

        model.run_powerflow(0)
        outputs = model.get_outputs()
        self.assertTrue(outputs)

    def test_midas_mv(self):
        """Test for midas pandapower grid variants."""
        model = PandapowerGrid()
        model.setup("midasmv", 0)

        model.run_powerflow(0)
        outputs = model.get_outputs()
        self.assertTrue(outputs)

    def test_midas_lv(self):
        """Test for midas pandapower grid variants."""
        model = PandapowerGrid()
        model.setup("midaslv", 0)

        model.run_powerflow(0)
        outputs = model.get_outputs()
        self.assertTrue(outputs)

    def test_simbench(self):
        """Test for simbench grids."""
        model = PandapowerGrid()
        model.setup("1-LV-rural3--0-sw", 0)

        model.run_powerflow(0)
        outputs = model.get_outputs()
        self.assertTrue(outputs)

    def test_json(self):
        """Test for a json grid."""
        pass

    def test_excel(self):
        """Test for a xlsx grid."""
        pass

    def test_set_inputs_load(self):
        """Test to set an input for a load."""
        model = PandapowerGrid()
        model.setup("cigre_lv", 0)

        self.assertEqual(model.grid.load.p_mw[0], 0.19)
        self.assertEqual(model.grid.load.q_mvar[0], 0.06244998)
        self.assertTrue(model.grid.load.in_service[0])

        model.set_inputs(
            etype="Load",
            idx=0,
            data={"p_mw": 0.04, "q_mvar": 0.02, "in_service": False},
        )

        self.assertEqual(model.grid.load.p_mw[0], 0.04)
        self.assertEqual(model.grid.load.q_mvar[0], 0.02)
        self.assertFalse(model.grid.load.in_service[0])

    def test_get_outputs(self):
        """Test to get the outputs after the powerflow."""

        model = PandapowerGrid()
        model.setup("simple_four_bus_system", 0)
        output = model.get_outputs()

        self.assertAlmostEqual(output["0-bus-1"]["vm_pu"], 0.996608)
        self.assertAlmostEqual(output["0-bus-1"]["va_degree"], -0.2081273)

        self.assertAlmostEqual(
            output["0-line-0"]["loading_percent"], 31.27309916
        )
        self.assertAlmostEqual(output["0-trafo-0"]["va_lv_degree"], -0.2081273)

        self.assertEqual(output["0-load-0-2"]["p_mw"], 0.03)
        self.assertEqual(output["0-sgen-1-3"]["p_mw"], 0.015)


if __name__ == "__main__":
    unittest.main()

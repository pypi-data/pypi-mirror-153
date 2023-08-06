"""This module contains a wrapper for pandapower grids."""
from importlib import import_module

import pandapower as pp
import pandapower.networks as pn
from midas.core.powergrid import LOG
from midas.core.powergrid.custom import bhv, midaslv, midasmv


class PandapowerGrid:
    """A model for pandapower grids."""

    def __init__(self):
        self.entity_map = dict()
        self.grid = None
        self.grid_idx = None
        self.has_profiles = False
        self.time_step = 0
        self.ids = dict()
        self.cache = dict()
        self.grid_type = None

        self.run_diagnostic = False
        self.lf_converged = False
        self._output_map = {
            "bus": ["p_mw", "q_mvar", "vm_pu", "va_degree"],
            "load": ["p_mw", "q_mvar"],
            "sgen": ["p_mw", "q_mvar"],
            "trafo": ["va_lv_degree", "loading_percent"],
            "line": [
                "i_ka",
                "p_from_mw",
                "q_from_mvar",
                "p_to_mw",
                "q_to_mvar",
                "loading_percent",
            ],
            "ext_grid": ["p_mw", "q_mvar"],
            # "slack": ["p_mw", "q_mvar"],
            "switch": ["et", "type", "closed"],
            "storage": ["p_mw", "q_mvar"],
        }

    def setup(self, gridfile, grid_idx, grid_params=None):
        """Set up the grid model."""
        if grid_params is None:
            grid_params = dict()
        self.grid_idx = grid_idx
        self._load_case(gridfile, grid_params)
        self._load_grid_ids()
        self._load_entity_map()

        # To save some time during runtime
        self.run_powerflow(0)

    def set_inputs(self, etype, idx, data):
        """Set input from other simulators."""
        etype = etype.lower()
        if etype not in ["load", "sgen", "trafo", "switch", "storage"]:
            LOG.info("Invalid etype %s. Skipping.", etype)
            return False

        for name, value in data.items():
            # Add try/except
            self.grid[etype].at[idx, name] = value

    def run_powerflow(self, time):
        """Run the powerflow calculation."""
        try:
            pp.runpp(self.grid)
            self.lf_converged = True
        except pp.LoadflowNotConverged:
            LOG.info(
                "Loadflow did not converge. Set *run_diagnostic* to True "
                "to run pandapower diagnostics."
            )
            self.lf_converged = False

            if self.run_diagnostic:
                pp.diagnostic(self.grid)

        self.cache = dict()

    def get_outputs(self):
        """Gather all outputs for other simulators."""
        if self.cache:
            return self.cache

        for eid, attrs in self.entity_map.items():
            data = dict()

            etype = attrs["etype"].lower()
            if etype == "switch":
                key = etype
            else:
                key = f"res_{etype}"

            element = self.grid[key].iloc[attrs["idx"]]
            for output in self._output_map[etype]:
                if self.lf_converged:
                    data[output] = element[output]
                else:
                    data[output] = 0  # Return nan?

            self.cache[eid] = data

        return self.cache

    def to_json(self):
        return pp.to_json(self.grid)

    def _load_case(self, gridfile, grid_params):
        """Load the pandapower grid specified by the *gridfile*.

        *gridfile* can be either the name of a grid or a path to a json
        file containing the grid.

        :param gridfile: Specifies the grid to load
        :type gridfile: str

        """

        if gridfile.endswith(".json"):
            self.grid = pp.from_json(gridfile)
        elif gridfile.endswith(".xlsx"):
            self.grid = pp.from_excel(gridfile)
        elif not self._load_simbench(gridfile):

            if gridfile == "cigre_hv":
                self.grid = pn.create_cigre_network_hv(**grid_params)
                self.grid_type = "cigre"
            elif gridfile == "cigre_mv":
                self.grid = pn.create_cigre_network_mv(**grid_params)
                self.grid_type = "cigre"
            elif gridfile == "cigre_lv":
                self.grid = pn.create_cigre_network_lv(**grid_params)
                self.grid_type = "cigre"
            elif gridfile == "midasmv":
                self.grid = midasmv.build_grid(**grid_params)
                self.grid_type = "cigre"
            elif gridfile == "midaslv":
                self.grid = midaslv.build_grid(**grid_params)
                self.grid_type = "cigre"
            elif gridfile == "bhv":
                self.grid = bhv.build_grid(**grid_params)
            elif "." in gridfile:
                if ":" in gridfile:
                    mod, clazz = gridfile.split(":")
                else:
                    mod, clazz = gridfile.rsplit(".", 1)
                mod = import_module(mod)
                self.grid = getattr(mod, clazz)()

            else:
                self.grid = getattr(pn, gridfile)()

                # gridfile not supported yet
                # raise ValueError

    def _load_simbench(self, gridfile):
        try:
            sb = import_module("simbench")
            try:
                self.grid = sb.get_simbench_net(gridfile)
                self.grid_type = "simbench"
            except ValueError:
                return False
        except ImportError:
            return False

        return True

    def _load_grid_ids(self):
        """Create a dictionary containing the names of the components.

        Use generic names and map to actual names?

        """
        self.ids["slack"] = self.grid.ext_grid.bus.to_dict()
        self.ids["bus"] = self.grid.bus.name.to_dict()
        self.ids["load"] = self.grid.load.name.to_dict()
        self.ids["sgen"] = self.grid.sgen.name.to_dict()
        self.ids["line"] = self.grid.line.name.to_dict()
        self.ids["trafo"] = self.grid.trafo.name.to_dict()
        self.ids["switch"] = self.grid.switch.name.to_dict()
        self.ids["storage"] = self.grid.storage.name.to_dict()

    def _load_entity_map(self):
        """Load the entity map for the mosaik simulator."""

        self._get_slack()
        self._get_buses()
        self._get_loads()
        self._get_sgens()
        self._get_lines()
        self._get_trafos()
        self._get_switches()
        self._get_storages()

    def _get_slack(self):
        """Create an entity for the slack bus."""
        for idx in self.ids["slack"]:

            element = self.grid.ext_grid.iloc[idx]
            eid = self._create_eid("ext_grid", self.grid.ext_grid.bus[idx])

            self.entity_map[eid] = {
                "etype": "Ext_grid",
                "idx": int(idx),
                "static": {
                    "name": element["name"],
                    "vm_pu": float(element["vm_pu"]),
                    "va_degree": float(element["va_degree"]),
                },
            }

    def _is_slack_bus(self, bus_id):
        for bus in self.ids["slack"].values():
            if bus == bus_id:
                return True

        return False

    def _get_buses(self):
        """Create entities for buses."""
        for idx in self.ids["bus"]:
            if self._is_slack_bus(idx):
                continue

            element = self.grid.bus.loc[idx]
            eid = self._create_eid("bus", idx)
            self.entity_map[eid] = {
                "etype": "Bus",
                "idx": int(idx),
                "static": {
                    "name": element["name"],
                    "vn_kv": float(element["vn_kv"]),
                },
            }

    def _get_loads(self):
        """Create entities for loads."""
        for idx in self.ids["load"]:
            element = self.grid.load.loc[idx]
            eid = self._create_eid("load", idx, element["bus"])
            bid = self._create_eid("bus", element["bus"])
            element_data = element.to_dict()

            keys_to_del = [
                "profile",
                "voltLvl",
                "const_z_percent",
                "const_i_percent",
                "min_q_mvar",
                "min_p_mw",
                "max_q_mvar",
                "max_p_mw",
            ]
            element_data_static = {
                key: element_data[key]
                for key in element_data
                if key not in keys_to_del
            }

            self.entity_map[eid] = {
                "etype": "Load",
                "idx": int(idx),
                "static": element_data_static,
                "related": [bid],
            }

    def _get_sgens(self):
        """Create entities for sgens."""
        for idx in self.ids["sgen"]:
            element = self.grid.sgen.loc[idx]
            eid = self._create_eid("sgen", idx, element["bus"])
            bid = self._create_eid("bus", element["bus"])
            element_data = element.to_dict()

            keys_to_del = [
                "profile",
                "voltLvl",
                "min_q_mvar",
                "min_p_mw",
                "max_q_mvar",
                "max_p_mw",
            ]
            element_data_static = {
                key: element_data[key]
                for key in element_data
                if key not in keys_to_del
            }

            self.entity_map[eid] = {
                "etype": "Sgen",
                "idx": int(idx),
                "static": element_data_static,
                "related": [bid],
            }

    def _get_lines(self):
        """Create entities for lines."""
        for idx in self.ids["line"]:
            element = self.grid.line.loc[idx]
            eid = self._create_eid("line", idx)
            fbid = self._create_eid("bus", element["from_bus"])
            tbid = self._create_eid("bus", element["to_bus"])

            element_data = element.to_dict()
            keys_to_del = ["from_bus", "to_bus"]
            element_data_static = {
                key: element_data[key]
                for key in element_data
                if key not in keys_to_del
            }

            self.entity_map[eid] = {
                "etype": "Line",
                "idx": int(idx),
                "static": element_data_static,
                "related": [fbid, tbid],
            }

    def _get_trafos(self):
        """Create entities for trafos."""
        for idx in self.ids["trafo"]:
            element = self.grid.trafo.loc[idx]
            eid = self._create_eid("trafo", idx)
            hv_bid = self._create_eid("bus", element["hv_bus"])
            lv_bid = self._create_eid("bus", element["lv_bus"])

            element_data = element.to_dict()
            keys_to_del = ["hv_bus", "lv_bus"]
            element_data_static = {
                key: element_data[key]
                for key in element_data
                if key not in keys_to_del
            }

            self.entity_map[eid] = {
                "etype": "Trafo",
                "idx": int(idx),
                "static": element_data_static,
                "related": [hv_bid, lv_bid],
            }

    def _get_switches(self):
        """Create entities for switches."""
        for idx in self.ids["switch"]:
            element = self.grid.switch.loc[idx]
            eid = self._create_eid("switch", idx)
            bid = self._create_eid("bus", element["bus"])

            if element["et"] == "l":
                oid = self._create_eid("line", element["element"])
            elif element["et"] == "t":
                oid = self._create_eid("trafo", element["element"])
            elif element["et"] == "b":
                oid = self._create_eid("bus", element["element"])

            element_data = element.to_dict()
            keys_to_del = ["element"]
            element_data_static = {
                key: element_data[key]
                for key in element_data
                if key not in keys_to_del
            }

            self.entity_map[eid] = {
                "etype": "Switch",
                "idx": int(idx),
                "static": element_data_static,
                "related": [bid, oid],
            }

    def _get_storages(self):
        """Create entities for storages."""
        for idx in self.ids.get("storage", list()):
            element = self.grid.storage.loc[idx]
            eid = self._create_eid("storage", idx, element["bus"])
            bid = self._create_eid("bus", element["bus"])
            element_data = element.to_dict()

            keys_to_del = []
            element_data_static = {
                key: element_data[key]
                for key in element_data
                if key not in keys_to_del
            }

            self.entity_map[eid] = {
                "etype": "Storage",
                "idx": int(idx),
                "static": element_data_static,
                "related": [bid],
            }

    def _create_eid(self, name, idx, bus_id=None):
        eid = f"{self.grid_idx}-{name}-{idx}"
        if bus_id is not None:
            eid = f"{eid}-{bus_id}"
        return eid

"""This module implements the mosaik simulator API for the
pandapower model.

"""
import distutils.util

import mosaik_api
from midas.core.powergrid import LOG
from midas.util.dict_util import update
from midas.util.plotter import Plotter
from midas.util.print_format import mformat
from midas.util.runtime_config import RuntimeConfig

from .meta import META
from .model.static import PandapowerGrid
from .model.constrainted import ConstraintedGrid


class PandapowerSimulator(mosaik_api.Simulator):
    """The pandapower simulator."""

    def __init__(self):
        super().__init__(META)
        self.sid = None
        self.models = dict()
        self.entity_map = dict()
        self.entities = list()

        self.step_size = None
        self.now_dt = None
        self.cache = dict()

        self.plotter_cfg = dict()
        self.plotter = None

    def init(self, sid, **sim_params):
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.

        Returns
        -------
        dict
            The meta dict (set by mosaik_api.Simulator)

        """
        if "step_size" not in sim_params:
            LOG.debug(
                "Param *step_size* not provided. "
                + "Using default step_size of 900."
            )

        self.step_size = sim_params.get("step_size", 900)

        plotting = sim_params.get("plotting", False)
        if not isinstance(plotting, bool):
            try:
                plotting = bool(distutils.util.strtobool(plotting))
            except AttributeError:
                plotting = False

        if plotting:
            self.plotter = Plotter()
            self.plotter_cfg["plot_path"] = sim_params.get(
                "plot_path", "_plots"
            )

        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity)

        Returns
        -------
        list
            A list with information on the created entity.

        """

        entities = list()
        use_constraints = model_params.get("use_constraints", False)
        for _ in range(num):
            gidx = len(self.models)
            eid = f"{model}-{gidx}"

            if model == "Grid":
                if use_constraints:
                    self.models[eid] = ConstraintedGrid(
                        model_params.get("constraints", list())
                    )
                else:
                    self.models[eid] = PandapowerGrid()

            if model == "GridTS":
                # Add the time series grid here
                pass

            if "gridfile" not in model_params:
                LOG.debug(
                    "Param *gridfile* not provided in model_params. "
                    "Using default grid *midasmv*"
                )

            gridfile = model_params.get("gridfile", "midasmv")
            grid_params = model_params.get("grid_params", dict())
            self.models[eid].setup(gridfile, gidx, grid_params)
            self.plotter_cfg[eid] = {
                "grid_type": self.models[eid].grid_type,
                "plot_name": gridfile,
                "plotting": model_params.get("plotting", False),
            }

            children = list()
            for cid, attrs in sorted(self.models[eid].entity_map.items()):
                assert cid not in self.entity_map
                self.entity_map[cid] = attrs
                etype = attrs["etype"]

                # We'll only add relations from lines to nodes (and not
                # from nodes to lines) because this is sufficient for
                # mosaik to build the entity graph
                relations = list()
                if etype.lower() in [
                    "trafo",
                    "line",
                    "load",
                    "sgen",
                    "storage",
                ]:
                    relations = attrs["related"]

                children.append({"eid": cid, "type": etype, "rel": relations})

            entity = {
                "eid": eid,
                "type": model,
                "rel": list(),
                "children": children,
            }
            entities.append(entity)
            self.entities.append(entity)

        return entities

    def step(self, time, inputs, max_advance=0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation step (by convention in seconds since
            simulation start.
        inputs : dict
            A *dict* containing inputs for entities of this simulator.

        Returns
        -------
        int
            The next step this simulator wants to be stepped.

        """

        LOG.debug("At step %d received inputs %s", time, mformat(inputs))

        for eid, attrs in inputs.items():
            gidx = eid.split("-")[0]
            grid = self.models.get(
                f"Grid-{gidx}", self.models.get(f"GridTS-{gidx}", None)
            )

            if grid is None:
                LOG.critical("No grid found for grid index %s!", gidx)
                raise KeyError

            idx = self.entity_map[eid]["idx"]
            etype = self.entity_map[eid]["etype"]

            for attr, src_ids in attrs.items():
                setpoint = 0.0

                for src_id, val in src_ids.items():
                    setpoint += float(val)

                attrs[attr] = setpoint

            grid.set_inputs(etype, idx, attrs)

        for eid, model in self.models.items():
            model.run_powerflow(time)
            self.cache[eid] = model.get_outputs()
            for child, cache in self.cache[eid].items():
                self.cache[child] = cache

            if self.plotter is not None and self.plotter_cfg[eid]["plotting"]:

                self.plotter.grid = model.grid
                self.plotter.plot_path = self.plotter_cfg["plot_path"]
                self.plotter.plot_name = self.plotter_cfg[eid]["plot_name"]
                self.plotter.grid_type = self.plotter_cfg[eid]["grid_type"]
                self.plotter.plot(eid, int(time / self.step_size))

        return time + self.step_size

    def get_data(self, outputs):
        """Return the requested outputs (if feasible).

        Parameters
        ----------
        outputs : dict
            A *dict* containing requested outputs of each entity.

        Returns
        -------
        dict
            A *dict* containing the values of the requested outputs.

        """

        data = dict()
        grid_json = dict()
        for eid, attrs in outputs.items():

            if "Grid" in eid:
                if "health" in attrs:
                    data.setdefault(eid, dict())["health"] = (
                        self.models[eid].grid.res_bus.vm_pu.values[1:].mean()
                    )
                if "grid_json" in attrs:
                    grid_json.setdefault(eid, dict())[
                        "grid_json"
                    ] = self.models[eid].to_json()

                continue

            msg = {"id": f"{self.sid}_{eid}", "name": eid, "type": "etype"}
            for attr in attrs:
                val = self.cache[eid][attr]
                data.setdefault(eid, dict())[attr] = val
                # for child in self.entities[0]["children"]:
                # print(child["type"])
                msg[attr] = val

            if RuntimeConfig().misc["key_value_logs"]:
                LOG.info(msg)

        if not RuntimeConfig().misc["key_value_logs"]:
            LOG.debug("Gathered outputs %s", mformat(data))
        update(data, grid_json)
        return data


if __name__ == "__main__":
    mosaik_api.start_simulation(PandapowerSimulator())

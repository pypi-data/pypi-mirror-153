from midas.core.powergrid import LOG
from midas.core.powergrid.elements.bus import PPBus
from midas.core.powergrid.elements.line import PPLine
from midas.core.powergrid.elements.load import PPLoad
from midas.core.powergrid.elements.sgen import PPSgen
from midas.core.powergrid.elements.transformer import PPTransformer

from .static import PandapowerGrid


class ConstraintedGrid(PandapowerGrid):
    def __init__(self, constraints):
        super().__init__()

        self._constraints_to_load = constraints
        self.constraints = dict()

    def setup(self, gridfile, grid_idx, grid_params):
        super().setup(gridfile, grid_idx, grid_params)

        self._load_constraints()

    def set_inputs(self, etype, idx, data):
        etype = etype.lower()
        if etype not in ["load", "sgen", "trafo", "switch", "storage"]:
            LOG.info("Invalid etype %s. Skipping.", etype)
            return False

        for name, value in data.items():
            self.grid[etype].at[idx, name] = value

            if etype in self.constraints:
                # Constraint can change the value
                setattr(self.constraints[etype][idx], name, value)

    def run_powerflow(self, time):

        # Run once to check current state
        super().run_powerflow(0)

        state_changed = False
        # Now constraints can change the input state if necessary
        for elements in self.constraints.values():
            for element in elements:
                state_changed = element.step(time) or state_changed

        if state_changed:
            super().run_powerflow(0)

    def _load_constraints(self):
        for constr in self._constraints_to_load:
            etype, value = constr
            self.constraints.setdefault(etype, list())
            for idx in range(len(self.grid[etype])):
                self.constraints[etype].append(self._create(etype, idx, value))

    def _create(self, etype, index, value):
        if etype == "trafo":
            clazz = PPTransformer
        # if classname == PPTransformer:
        #     etype = self.grid[classname.pp_key()]["std_type"][index]

        #     return PPTransformer(index, self.grid)
        # TODO: elif other elements
        elif etype == "bus":
            clazz = PPBus
        elif etype == "load":
            clazz = PPLoad
        elif etype == "sgen":
            clazz = PPSgen
        elif etype == "line":
            clazz = PPLine
        return clazz(index, self.grid, value)

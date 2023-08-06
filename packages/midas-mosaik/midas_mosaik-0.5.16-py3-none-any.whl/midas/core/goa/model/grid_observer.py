"""This module contains the observer of the grid operator."""


class GridObserver:
    """The observer model.

    Runs the powerflow with currently known information.

    """

    def __init__(self, params, grid):

        self.model = grid
        self.config = params
        self.setpoints = None
        self.estimations = None

    def step(self):
        """Perform a simulation step."""

        if self.estimations is not None:
            self._assign_values(self.estimations)

        self._assign_values(self.setpoints)

        self.model.run_powerflow(0)

        self.setpoints = None
        self.estimations = None

    def _assign_values(self, setpoints):

        for etype, idxs in setpoints.items():
            for idx, attrs in idxs.items():
                self.model.set_inputs(etype, idx, attrs["attrs"])

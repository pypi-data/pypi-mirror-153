import logging

import pandapower as pp

from ..constraints.line_loading import ConstraintLineLoading
from .base import GridElement

LOG = logging.getLogger(__name__)


class PPLine(GridElement):
    @staticmethod
    def pp_key() -> str:
        return "line"

    @staticmethod
    def res_pp_key() -> str:
        return "res_load"

    def __init__(self, index, grid, value=100):
        super().__init__(index, grid, LOG)

        self.in_service = True
        self.max_percentage = value

        self._constraints.append(ConstraintLineLoading(self))

    def step(self, time):
        old_state = self.in_service
        self.in_service = True
        self._check(time)
        self.set_value("in_service", self.in_service)

        if not self.in_service:
            LOG.debug(f"At step {time}: Line {self.index} out of service.")
            pp.runpp(self.grid)

        return old_state != self.in_service

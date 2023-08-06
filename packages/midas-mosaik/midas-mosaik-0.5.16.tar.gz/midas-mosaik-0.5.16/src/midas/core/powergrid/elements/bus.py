import logging

from ..constraints.voltage_change import ConstraintVoltageChange
from .base import GridElement

LOG = logging.getLogger(__name__)


class PPBus(GridElement):
    @staticmethod
    def pp_key() -> str:
        return "bus"

    @staticmethod
    def res_pp_key() -> str:
        return "res_bus"

    def __init__(self, index, grid, value):
        super().__init__(index, grid, LOG)

        self.in_service = True
        self.add_constraint(ConstraintVoltageChange(self))

    def step(self, time):
        self.in_service = True
        self._check(time)

        self.set_value("in_service", self.in_service)

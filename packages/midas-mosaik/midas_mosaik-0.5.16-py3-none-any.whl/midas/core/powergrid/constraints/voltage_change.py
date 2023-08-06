import collections
from datetime import timedelta
from .base import Constraint

TimedVoltage = collections.namedtuple("TimedVoltage", ["time", "value"])


class ConstraintVoltageChange(Constraint):
    def __init__(self, element):
        super().__init__(element)

        self._expected_value = 0.02
        self._time_frame = timedelta(minutes=60)
        self._time_voltages = list()
        self._bus = self._element.grid[self._element.pp_key()].bus.loc[
            self._element.index
        ]

    def check(self, time) -> bool:
        self._satisfied = True
        voltage = self._element.grid.res_bus.vm_pu.loc[self._bus]
        self._time_voltages = [
            entry
            for entry in self._time_voltages
            if time - entry.time < self._time_frame.seconds
        ]
        current_t_v = TimedVoltage(time=time, value=voltage)
        self._time_voltages.append(current_t_v)

        voltage_values = [entry.value for entry in self._time_voltages]
        min_voltage = min(voltage_values)
        max_voltage = max(voltage_values)

        voltage_change_percent = abs(max_voltage - min_voltage) / min_voltage
        voltage_change_percent = round(voltage_change_percent, 6)

        if voltage_change_percent > self._expected_value:
            self._satisfied = False
            self._violated_value = voltage_change_percent

        return self._satisfied

    def handle_violation(self):
        self._element.in_service = False

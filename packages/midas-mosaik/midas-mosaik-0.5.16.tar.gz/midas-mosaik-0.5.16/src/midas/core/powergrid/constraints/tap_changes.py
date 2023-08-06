from .base import Constraint


class ConstraintTapChanges(Constraint):
    def __init__(self, element, expected_value):
        super().__init__(element)

        self._changes_per_hour = expected_value
        self._last_change = 0
        self._changes = dict()

    def check(self, time) -> bool:
        self._satisfied = True
        current_pos = self._element.grid[self._element.pp_key()][
            "tap_pos"
        ].loc[self._element.index]

        if current_pos != self._element.tap_pos:
            self._changes[time] = self._element.tap_pos

            start = max(0, time - 3600)
            num_changes = 0
            for t in range(start, time):
                if t in self._changes:
                    num_changes += 1

            if num_changes > self._changes_per_hour:
                self._satisfied = False

        return self._satisfied

    def handle_violation(self):
        self._element.tap_pos = self._element.grid[self._element.pp_key][
            "tap_pos"
        ].loc[self._element.index]

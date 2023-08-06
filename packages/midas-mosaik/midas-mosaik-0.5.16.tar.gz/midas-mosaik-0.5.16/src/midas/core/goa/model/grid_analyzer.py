"""This module contains the grid analyzer component."""
import numpy as np


class GridAnalyzer:
    """Grid analyzer of the grid operator."""

    def __init__(self, grid, config):
        self.model = grid
        self.config = config
        self.real_grid_data = dict()
        self.stats = dict()

    def step(self):
        """Perform a simulation step."""

        self._eval_grid_state()

    def _eval_grid_state(self):
        """Calculate different metrics describing the grid state.

        Currently, the average voltage p.u. is calculated.
        """
        self.stats = dict()
        self.eval_observation_error()
        self.eval_voltage_violations()

        self.stats["health"] = float(
            self.model.grid.res_bus.vm_pu.values[1:].mean()
        )

    def eval_observation_error(self):
        """Evaluate the observation error if feasible."""

        if not self.real_grid_data:
            # We don't have grid data
            self.stats["error"] = 0
            return

        if "Bus" in self.real_grid_data:
            # Move to function 'get_real_data'
            real = dict()
            for bus_id, attrs in self.real_grid_data["Bus"].items():
                # if bus_id == 0:
                #     # We skip the slack bus
                #     continue
                if self.config["grid_busvm_sensor"]:
                    real.setdefault("vm_pu", list()).append(attrs["vm_pu"])
                elif self.config["grid_busload_sensor"]:
                    real.setdefault("p_mw", list()).append(attrs["p_mw"])
                    real.setdefault("q_mvar", list()).append(attrs["q_mvar"])

            if self.config["grid_busvm_sensor"]:
                real["vm_pu"] = np.array(real["vm_pu"]).flatten()
                obs = np.array(
                    list(self.model.grid.res_bus.vm_pu.values[1:])
                ).flatten()
                self.stats["bus.vm_pu"] = {
                    "errors": real["vm_pu"] - obs,
                    "rmse": rmse(real["vm_pu"], obs),
                }
                self.stats["error"] = float(self.stats["bus.vm_pu"]["rmse"])

            elif self.config["grid_busload_sensor"]:
                real["p_mw"] = np.array(real["p_mw"]).flatten()
                real["q_mvar"] = np.array(real["q_mvar"]).flatten()
                obs = {
                    "p_mw": np.array(
                        list(self.model.grid.res_bus.p_mw.values[1:])
                    ).flatten(),
                    "q_mvar": np.array(
                        list(self.model.grid.res_bus.q_mvar.values[1:])
                    ).flatten(),
                }
                self.stats["bus.p_mw"] = {
                    "errors": real["p_mw"] - obs["p_mw"],
                    "rmse": rmse(real["p_mw"], obs["p_mw"]),
                }
                self.stats["bus.q_mvar"] = {
                    "errors": real["q_mvar"] - obs["q_mvar"],
                    "rmse": rmse(real["q_mvar"], obs["q_mvar"]),
                }
                self.stats["error"] = float(self.stats["bus.p_mw"]["rmse"])

            else:
                # Handle grid data other than buses
                self.stats["error"] = 0

    def eval_voltage_violations(self):
        """Evaluate possible voltage violations."""
        num_buses = len(self.model.grid.res_bus)

        lower_bounds = np.ones(num_buses) * self.config["undervoltage_pu"]
        upper_bounds = np.ones(num_buses) * self.config["overvoltage_pu"]

        lower_violations = self.model.grid.res_bus.vm_pu - lower_bounds
        upper_violations = self.model.grid.res_bus.vm_pu - upper_bounds

        self.stats["voltage_violations"] = {
            "lower_violations": lower_violations.values,
            "upper_violations": upper_violations.values,
            "max_overvoltage": float(max(0, upper_violations.max())),
            "min_undervoltage": float(min(0, lower_violations.min())),
            "num_violations": int(
                np.where(lower_violations < 0, 1, 0).sum()
                + np.where(upper_violations > 0, 1, 0).sum()
            ),
        }


def rmse(real, pred):
    """Compute the root mean squared error."""
    return ((real - pred) ** 2).sum() ** 0.5

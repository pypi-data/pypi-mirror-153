"""This module contains the forecaster of the grid operator."""
from datetime import timedelta
import numpy as np
import pandas as pd
from sortedcontainers import SortedDict

from midas.core.goa.model.grid_observer import GridObserver
from midas.core.goa.model.grid_analyzer import GridAnalyzer


class GridForecaster:
    """The grid forecaster calculates future grid states."""

    def __init__(self, grid, params, load_estimator):
        self.config = params
        self.observer = GridObserver(self.config, grid)
        self.analyzer = GridAnalyzer(grid, params)
        self.load_estimator = load_estimator
        self.outbox = None

        self.now_dt = None
        self.step_size = 0
        self.forecasts = None
        self._setpoints = None
        self.actions = None

    def step(self):
        """Perform a simulation step."""
        self.actions = dict()
        fc_dt = pd.date_range(
            self.now_dt + timedelta(seconds=self.step_size),
            periods=self.config["forecast_horizon_hours"]
            * 3_600
            / self.step_size,
            freq="{}S".format(self.step_size),
        )
        for date in fc_dt:
            self._run_forecast(date)
            self._recommend_actions(self.analyzer.stats, date)

        self._send_schedules()

    def _run_forecast(self, date):
        """Run the forecast for one step (*date*)."""
        setpoints = SortedDict()
        for etype, idxs in self.forecasts.items():
            setpoints.setdefault(etype, SortedDict())

            for idx, src_ids in idxs.items():
                setpoints[etype].setdefault(idx, SortedDict())
                setpoints[etype][idx].setdefault("static", src_ids["static"])
                setpoints[etype][idx].setdefault("attrs", SortedDict())

                self.load_estimator.now_dt = date
                self.load_estimator.step()

                for src_id, schedule in src_ids["src"].items():
                    if not isinstance(schedule, pd.DataFrame):
                        schedule = pd.read_json(schedule)
                        src_ids["src"][src_id] = schedule
                    for name in ["p_mw", "q_mvar"]:
                        setpoints[etype][idx]["attrs"].setdefault(name, 0)
                        val = float(schedule.loc[date][name])
                        if etype == "Sgen" and "Pysimmod" in src_id:
                            # Transform to load reference system
                            val *= -1
                        setpoints[etype][idx]["attrs"][name] += val

        # self.observer.estimations = self.load_estimator.setpoints
        self.observer.setpoints = setpoints
        self.observer.step()

        self.analyzer.eval_voltage_violations()

    def _recommend_actions(self, stats, date):
        """Analyze the results of the grid analyzer

        Currently, only the over voltage case is handled.

        """
        if stats["voltage_violations"]["num_violations"] == 0:
            # No action required
            return

        violation_idxs = np.where(
            stats["voltage_violations"]["upper_violations"] > 0.0
        )[0]

        for bus_idx in violation_idxs:
            for etype, idxs in self.forecasts.items():
                if etype in ["Load", "Sgen"]:
                    for _, srcs in idxs.items():

                        self._create_setpoints(
                            srcs["src"], date, bus_idx, more_power=False
                        )
                else:
                    # Handle tranformers, switch, etc
                    pass

        violation_idxs = np.where(
            stats["voltage_violations"]["lower_violations"] < 0.0
        )[0]

        for bus_idx in violation_idxs:
            for etype, idxs in self.forecasts.items():
                if etype in ["Load", "Sgen"]:
                    for _, srcs in idxs.items():

                        self._create_setpoints(
                            srcs["src"], date, bus_idx, more_power=True
                        )
                else:
                    # Handle tranformers, switch, etc
                    pass

    def _create_setpoints(self, srcs, date, bus_idx, more_power):
        """Fill the actions dictionary will schedules."""

        for src_id, schedule in srcs.items():
            entity_bus = self.config["der_mapping"][src_id]["bus"]
            if entity_bus != bus_idx:
                continue

            if self.config["der_mapping"][src_id]["type"] == "load":
                if more_power:
                    if schedule.loc[date]["target"] > 0.5:
                        setpoint = 0.5
                    elif schedule.loc[date]["target"] > 0.0:
                        setpoint = 0.0
                    else:
                        continue
                else:
                    if schedule.loc[date]["target"] < 0.5:
                        setpoint = 0.5
                    elif schedule.loc[date]["target"] < 1.0:
                        setpoint = 1.0
                    else:
                        continue

            elif self.config["der_mapping"][src_id]["type"] == "sgen":
                if more_power:
                    if schedule.loc[date]["target"] < 0.5:
                        setpoint = 0.5
                    elif schedule.loc[date]["target"] < 1.0:
                        setpoint = 1.0
                    else:
                        continue
                else:
                    if schedule.loc[date]["target"] > 0.5:
                        setpoint = 0.5
                    elif schedule.loc[date]["target"] > 0.0:
                        setpoint = 0.0
                    else:
                        continue
            else:
                continue
            self.actions.setdefault(src_id, dict())
            self.actions[src_id][date] = setpoint

    def _send_schedules(self):
        """Unpack the actions dictionary an create messages."""
        for dst_id, schedule in self.actions.items():
            self.outbox.send(
                {
                    "to": dst_id,
                    "topic": "schedule",
                    "msg": pd.DataFrame(
                        data=list(schedule.values()),
                        columns=["target"],
                        index=list(schedule.keys()),
                    ),
                }
            )

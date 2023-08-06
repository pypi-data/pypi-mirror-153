"""This module contains the coordinator for the subfunctions of
the grid operator.

"""
from datetime import datetime, timedelta

from midas.core.goa.model.grid_analyzer import GridAnalyzer
from midas.core.goa.model.grid_forecaster import GridForecaster
from midas.core.goa.model.grid_observer import GridObserver
from midas.core.goa.model.load_estimator import LoadEstimator
from midas.core.goa.model.messenger import Messenger
from midas.core.powergrid.model.static import PandapowerGrid


class Coordinator:
    """Coordinator for all the subfunctions of the grid operator."""

    def __init__(self, params):

        self.config = params

        self.ppg = PandapowerGrid()
        self.ppg.setup(self.config["gridfile"], 0)

        self.now_dt = datetime.strptime(
            self.config["start_date"], "%Y-%m-%d %H:%M:%S%z"
        )
        self.step_size = self.config.get("step_size", 900)

        self.messenger = Messenger(self.config, self.ppg.entity_map)
        self.observer = GridObserver(self.config, self.ppg)
        self.analyzer = GridAnalyzer(self.ppg, self.config)
        self.load_estimator = LoadEstimator(self.config, self.ppg.entity_map)
        self.forecaster = GridForecaster(
            self.ppg, self.config, self.load_estimator
        )
        self.forecaster.outbox = self.messenger

        self.error = None
        self.health = None
        self.min_undervoltage = None
        self.max_overvoltage = None
        self.num_voltage_violations = None

    def step(self):
        """Perform a simulation step."""

        # Read inbox and filter messages
        self.messenger.step()

        if not self.config["grid_load_sensor"]:
            # Run the load estimator
            self.load_estimator.now_dt = self.now_dt
            self.load_estimator.step()
            self.observer.estimations = self.load_estimator.setpoints

        # Pass setpoints to grid observer
        self.observer.setpoints = self.messenger.setpoints
        self.observer.step()

        # Run the analyzer
        self.analyzer.real_grid_data = self.messenger.real_grid_data
        self.analyzer.step()

        self.error = self.analyzer.stats["error"]
        self.health = self.analyzer.stats["health"]
        self.min_undervoltage = self.analyzer.stats["voltage_violations"][
            "min_undervoltage"
        ]
        self.max_overvoltage = self.analyzer.stats["voltage_violations"][
            "max_overvoltage"
        ]
        self.num_voltage_violations = self.analyzer.stats[
            "voltage_violations"
        ]["num_violations"]

        if self.config["run_forecast"]:
            # Forecast the next steps
            self.forecaster.forecasts = self.messenger.forecasts
            self.forecaster.now_dt = self.now_dt
            self.forecaster.step_size = self.step_size
            self.forecaster.step()

        self.now_dt += timedelta(seconds=self.step_size)

    def receive(self, msg):
        """Receive a message.

        The message is a dictionary containing three keys:
        'from': (id of the source, e.g. '<sid>.<eid>'),
        'topic': (context of the message, e.g., the attribute to set),
        'msg': (content of the message, e.g., value to set)

        """
        self.messenger.inbox.put(msg)

    @property
    def outbox(self):
        """The message outbox."""
        return self.messenger.outbox

    @property
    def grid(self):
        return self.ppg.to_json()

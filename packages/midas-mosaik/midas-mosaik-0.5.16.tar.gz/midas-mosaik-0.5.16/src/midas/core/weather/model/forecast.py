"""This module contains the forecast-weather model."""
import math
from datetime import timedelta

import numpy as np
import pandas as pd

from midas.core.weather.model.current import WeatherCurrent


class WeatherForecast(WeatherCurrent):
    """Weather forecast model.

    Uses the real data from future steps and applies a random error
    to the values.

    An internal start date is used and updated each step. This model
    provides weather information read from a weather time series.
    Additional functionality can be activated.

    Parameters
    ----------
    wdata : midas.core.weather.model.provider.WeatherData
        A reference to the class storing the actual data.
    start_date : datetime.datime
        The point of time in the year which should be started with.
    step_size : int, optional
        *step_size is an input and needs to be set in each step.*
        Used to step the internal datetime object. Does not reset
        after a step, so it can also be provided once during
        initialization.
    interpolate : bool, optional
        If set to *True*, data is interpolated if the internal datetime
        points to a time within two hours.
    seed : int, optional
        A seed for the random number generator.
    randomize : bool, optional
        If set to *True*, a normally distributed random noise is
        applied to the data.
    block_mode : bool, optional
        If set to *True*, the *select_block* function is used instead
        of the *select_hour* function. See the *WeatherData* to learn
        about the differences
    frame : int, optional
        If *block_mode* is True, this value is passed to the
        *select_block* function. Defaults to 1.
    forecast_horizon_hours : float, optional
        Specify for how many hours in the future a forecast should be
        generated.
    forecast_error : float, optional
        Specify how large the forecast error should be. Defaults to 0
        for a perfect forecast.

    Attributes
    ----------
    t_air_deg_celsius : float
        The current air temperature in degree celsius.
    day_avg_t_air_deg_celsius : float
        The current day's average air temperatur in degree celsius.
    bh_w_per_m2:
        Beam horizontal or direct solar radiation on the horizontal
        plane in Watt per square meter of the current step.
    dh_w_per_m2:
        Diffuse horizontal or diffuse solar radiation on the horizontal
        plane in Watt per square meter of the current step.

    """

    def __init__(
        self,
        wdata,
        start_date,
        step_size=None,
        forecast_horizon_hours=0.25,
        forecast_error=0,
        seed=None,
        interpolate=False,
        block_mode=False,
        randomize=False,
    ):

        super().__init__(
            wdata, start_date, step_size, randomize, interpolate, seed
        )

        self.forecast_horizon_hours = forecast_horizon_hours
        self.forecast_error = forecast_error
        self.forecast = None

        if block_mode:
            self.select_data = self.wdata.select_block
        else:
            self.select_data = self.wdata.select_hour

    def step(self):
        """Perform a simulation step."""

        pred_start = self.now_dt + timedelta(hours=self.step_size / 3_600)

        index = pd.date_range(
            pred_start,
            pred_start
            + timedelta(hours=self.forecast_horizon_hours)
            - timedelta(seconds=self.step_size),
            freq="{}S".format(self.step_size),
        )
        self.forecast = pd.DataFrame(
            columns=[
                "bh_w_per_m2",
                "dh_w_per_m2",
                "t_air_deg_celsius",
                "day_avg_t_air_deg_celsius",
            ],
            index=index,
        )
        horizon = int(math.ceil(self.forecast_horizon_hours)) + 2

        results = self.select_data(
            pred_start.replace(minute=0, second=0, microsecond=0), horizon
        )

        steps = int(self.forecast_horizon_hours * 3_600 / self.step_size)

        if self.interpolate:
            val_idx = np.arange(0, horizon * 3_600, 3_600)

            start_sec = pred_start.minute * 60 + pred_start.second
            sel_idxs = list()
            start_hour = pred_start.hour
            for _ in range(steps):
                sel_idxs.append(start_sec)
                start_sec += self.step_size

            self.t_air_deg_celsius = [
                np.interp(h, val_idx, results[0]) for h in sel_idxs
            ]
            self.day_avg_t_air_deg_celsius = [
                np.interp(h, val_idx, results[1]) for h in sel_idxs
            ]
            self.bh_w_per_m2 = [
                np.interp(h, val_idx, results[2]) for h in sel_idxs
            ]
            self.dh_w_per_m2 = [
                np.interp(h, val_idx, results[3]) for h in sel_idxs
            ]

        else:
            sel_idxs = list()

            start_hour = pred_start.hour
            for _ in range(steps):
                sel_idxs.append(pred_start.hour - start_hour)

                pred_start += timedelta(hours=self.step_size / 3_600)

                if pred_start.hour < start_hour:
                    start_hour = pred_start.hour - 1

            self.t_air_deg_celsius = [results[0][h] for h in sel_idxs]
            self.day_avg_t_air_deg_celsius = [results[1][h] for h in sel_idxs]
            self.bh_w_per_m2 = [results[2][h] for h in sel_idxs]
            self.dh_w_per_m2 = [results[3][h] for h in sel_idxs]

        if self.randomize:
            self.t_air_deg_celsius = [
                v * self.rng.normal(scale=self.forecast_error, loc=1.0)
                for v in self.t_air_deg_celsius
            ]
            self.day_avg_t_air_deg_celsius = [
                v * self.rng.normal(scale=self.forecast_error, loc=1.0)
                for v in self.day_avg_t_air_deg_celsius
            ]
            self.bh_w_per_m2 = [
                v * self.rng.normal(scale=self.forecast_error, loc=1.0)
                for v in self.bh_w_per_m2
            ]
            self.dh_w_per_m2 = [
                v * self.rng.normal(scale=self.forecast_error, loc=1.0)
                for v in self.dh_w_per_m2
            ]

        self.forecast["bh_w_per_m2"] = self.bh_w_per_m2
        self.forecast["dh_w_per_m2"] = self.dh_w_per_m2
        self.forecast["t_air_deg_celsius"] = self.t_air_deg_celsius
        self.forecast[
            "day_avg_t_air_deg_celsius"
        ] = self.day_avg_t_air_deg_celsius

        return results

    @property
    def forecast_bh_w_per_m2(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, ["bh_w_per_m2"]]

    @property
    def forecast_dh_w_per_m2(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, ["dh_w_per_m2"]]

    @property
    def forecast_t_air_deg_celsius(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, ["t_air_deg_celsius"]]

    @property
    def forecast_day_avg_t_air_deg_celsius(self):
        """Handle forecast_ - prefix."""
        return self.forecast.loc[:, ["day_avg_t_air_deg_celsius"]]

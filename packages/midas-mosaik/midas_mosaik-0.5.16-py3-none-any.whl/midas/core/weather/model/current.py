"""This module contains the current-weather model."""
from datetime import timedelta

import numpy as np


class WeatherCurrent:
    """This class provides weather information.

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
        randomize=False,
        interpolate=False,
        seed=None,
        block_mode=False,
        frame=1,
    ):

        # Config
        self.wdata = wdata
        self.now_dt = start_date
        self.interpolate = interpolate
        self.randomize = randomize

        # State
        self.t_air_deg_celsius = None
        self.day_avg_t_air_deg_celsius = None
        self.bh_w_per_m2 = None
        self.dh_w_per_m2 = None
        self.rng = np.random.RandomState(seed)

        # Input
        self.step_size = step_size
        self.block_mode = block_mode
        self.frame = frame

    def step(self):
        """Perform a simulation step."""

        select_dt = self.now_dt.replace(minute=0, second=0, microsecond=0)

        if self.block_mode:
            res = self.wdata.select_block(select_dt, 1, self.frame)
        else:
            res = self.wdata.select_hour(select_dt)
        if self.interpolate:
            select_dt = select_dt + timedelta(hours=1)
            if self.block_mode:
                res2 = self.wdata.select_block(select_dt, 1, self.frame)
            else:
                res2 = self.wdata.select_hour(select_dt)

            cur_sec = self.now_dt.minute * 60
            res = [
                [np.interp(cur_sec, [0, 3_600], [res[i][0], res2[i][0]])]
                for i in range(len(res))
            ]

        if self.randomize:
            res = [[r[0] * self.rng.normal(scale=0.05, loc=1.0)] for r in res]

        # Radiation can't be lower than 0
        res[2][0] = max(0, res[2][0])
        res[3][0] = max(0, res[3][0])

        # print(res)
        self.t_air_deg_celsius = res[0][0]
        self.day_avg_t_air_deg_celsius = res[1][0]
        self.bh_w_per_m2 = res[2][0]
        self.dh_w_per_m2 = res[3][0]

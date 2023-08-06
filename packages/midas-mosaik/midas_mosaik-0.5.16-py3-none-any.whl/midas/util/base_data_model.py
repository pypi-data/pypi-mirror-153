"""This module contains the model for data simulators."""

import math

import numpy as np
from midas.util.compute_q import compute_q


class DataModel:
    """A model for a single load or sgen time series.

    There are a few assumptions for the time series that are not
    checked. First, the time series ranges over a whole year and
    secondly, the time passed between two values is 15 minutes.
    Therefore, not less than 35040 value are expected to be in each
    time series (for *data_p* and for *data_q*).

    However, the *DataModel* could be extended to support other timely
    resolutions and make use of data of a second (third, fourth,...)
    year.

    Parameters
    ----------
    data_p : pandas.DataFrame
        Contains values (either load or sgen) for active power. The
        index columns are simple *int*.
    data_q : pandas.DataFrame
        Contains values (either load or sgen) for reactive power. The
        index columns are simple *int*. If *None* is provided for
        *data_q*, the cos phi is used in each step to calculate a value
        for *q*.
    data_step_size: int
        Timely resolution of the data in seconds.
    scaling : float
        An overall scaling for this model. This scaling is applied in
        each to step both of *p* and *q*.
    seed : int, optional
        A seed for the random number generator.
    interpolate : bool, optional
        If set to *True*, interpolation is applied when values between
        full 15-minute intervalls are requested.
    randomize_data : bool, optional
        If set to *True*, a normally distributed random noise is
        applied to all outputs.
    randomize_cos_phi : bool, optional
        If set to *True* and data_q is not provided, the cos phi for
        the calculation of *q* is randomized.
    date_index : bool, optional
        Set this to *True* if the has datetime as index instead of ints.
    noise_factor: float, optional
        Set this to increase or lower the noise if randomization is
        activated.

    Attributes
    ----------
    now_dt : datetime.datetime
        *now_dt is an input and needs to be provided in each step.*
        The current simulated time. Is used to calculate the index for
        the current value in the time series.
    cos_phi : float
        *cos_phi is an input and needs to be provided in each step.*
        The phase angle used to calculate reactive power if no reactive
        power time series is provided.
    p_mw : float
        *p_mw is an output.* The active power for the current step.
    q_mvar : float
        *q_mvar is an output.* The reactive power for the current step.

    """

    def __init__(self, data_p, data_q, data_step_size, scaling, **params):
        self.data_p = data_p
        self.data_q = data_q
        self.sps = data_step_size
        self.scaling = scaling
        self.date_index = params.get("date_index", False)

        # RNG
        self.seed = params.get("seed", None)
        self.rng = np.random.RandomState(self.seed)

        self.interpolate = params.get("interpolate", False)
        self.randomize_data = params.get("randomize_data", False)
        self.randomize_cos_phi = params.get("randomize_cos_phi", False)
        self.noise_factor = params.get("noise_factor", 0.2)
        self.p_std = self.data_p.std() * self.scaling
        self.p_mwh_per_a = self.data_p.sum() * self.scaling / self.sps * 3_600
        if self.data_q is not None:
            self.q_std = self.data_q.std() * self.scaling
        else:
            self.q_std = None

        # Inputs
        self.now_dt = None
        self.cos_phi = None

        # Outputs
        self.p_mw = None
        self.q_mvar = None

    def step(self):
        """Perform a simulation step."""

        self.p_mw = None
        self.q_mvar = None

        self._interpolation()
        self._randomization()

        self._random_cos_phi()

        if self.q_mvar is None:
            self.q_mvar = compute_q(self.p_mw, self.cos_phi)

        # Numpy multiply failes for int and float if *= is used
        self.p_mw = self.p_mw * self.scaling
        self.q_mvar = self.q_mvar * self.scaling

        tmp = self.p_mw**2 + self.q_mvar**2
        if tmp != 0:
            self.cos_phi = self.p_mw / math.sqrt(tmp)
        else:
            self.cos_phi = 0

    def _interpolation(self):
        # We assume that the dataset starts on the first of the year.
        dif = self.now_dt - self.now_dt.replace(
            month=1, day=1, hour=0, minute=0, second=0
        )
        dif_s = dif.total_seconds()

        tidx = int(dif_s // self.sps) % len(  # step size of the data
            self.data_p.index
        )

        # Apply interpolation
        if self.interpolate:
            self.p_mw = self._interpolate(tidx, self.data_p)
            if self.data_q is not None:
                self.q_mvar = self._interpolate(tidx, self.data_q)
        else:
            self.p_mw = self.data_p.values[tidx]
            if self.data_q is not None:
                self.q_mvar = self.data_q.values[tidx]

    def _interpolate(self, tidx, data):

        current_second = (
            self.now_dt.minute * 60 + self.now_dt.second
        ) % self.sps

        tidx_end = tidx + 2
        y_vals = data.values[tidx:tidx_end]

        if tidx_end > len(data.index):
            # Start from beginning
            y_vals = np.array([y_vals[0], data.values[0]])
        x_vals = np.array([0, self.sps])

        result = np.interp(current_second, x_vals, y_vals)

        return result

    def _randomization(self):

        if self.randomize_data:
            noise = self.rng.normal(
                scale=(self.p_std * self.noise_factor), loc=0.0
            )
            self.p_mw = max(0, self.p_mw + noise)

            if self.q_mvar is not None:
                noise = self.rng.normal(
                    scale=(self.q_std * self.noise_factor), loc=0.0
                )
                self.q_mvar = max(0, self.q_mvar + noise)

    def _random_cos_phi(self):
        if self.q_mvar is None and self.randomize_cos_phi:
            self.cos_phi = max(
                0, min(1.0, self.rng.normal(scale=0.02, loc=0.9))
            )

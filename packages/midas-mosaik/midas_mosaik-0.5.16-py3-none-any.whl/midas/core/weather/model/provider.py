"""This module contains the provider for weather data."""
from datetime import timedelta

import numpy as np
import pandas as pd


DATE = "Datetime"
T_AIR = "t_air_degree_celsius"
AVG_T_AIR = "day_avg_t_air_degree_celsius"
GHI = "gh_w_per_m2"
DI = "dh_w_per_m2"
WIND = "wind_v_m_per_s"
WINDDIR = "wind_dir_degree"


class WeatherData:
    """A simple weather data provider.

    This class provides weather data from a csv file. Either a concrete
    datetime can be selected or randomly from a time frame.

    The new weather time series now covers the years from 2009 to 2019,
    however, the former weather time series only covered the year 2018
    and, therefore, this class needs further modifications to
    dynamically support other years.

    Furthermore, although the wind data is already present, they will
    not be fetched.

    Parameters
    ----------
    filename : str
        Absolute path to the weather database.
    seed : int
        A seed for the randum number generatore. Random values are only
        used in the *select_block* method to pick randomly one value
        from the block. The values itself are unchanged.

    """

    def __init__(self, filename, seed=None):

        self.wdata = pd.read_hdf(filename, "weather")
        self.rng = np.random.RandomState(seed)

    def select_hour(self, now_dt, horizon=1):
        """
        Select weather data at given datetime *now_dt*.

        Returns
        -------
        list
            A *list* containing [[t_air], [avg_t_air], [GHI-DI], [DI]]

        """
        start = now_dt.replace(minute=0, second=0, microsecond=0).strftime(
            "%Y-%m-%d %H:%M:%S%z"
        )
        # Workaround since more data is available
        old_year_end = f"{now_dt.year}-12-31 23:00:00+0000"
        end_dt = now_dt + timedelta(hours=horizon)

        if end_dt.minute == 0:
            end_dt -= timedelta(hours=1)

        end = end_dt.replace(minute=0, second=0, microsecond=0).strftime(
            "%Y-%m-%d %H:%M:%S%z"
        )
        # Workaround since more data is available
        new_year_start = f"{end_dt.year}-01-01 00:00:00+0000"

        if end_dt.year > now_dt.year:
            data1 = self.wdata.loc[start:old_year_end]
            data2 = self.wdata.loc[new_year_start:end]

            return [
                (data1[T_AIR].values.tolist() + data2[T_AIR].values.tolist()),
                (
                    data1[AVG_T_AIR].values.tolist()
                    + data2[AVG_T_AIR].values.tolist()
                ),
                (
                    (data1[GHI].values - data1[DI].values).tolist()
                    + (data2[GHI].values - data2[DI].values).tolist()
                ),
                (data1[DI].values.tolist() + data2[DI].values.tolist()),
            ]

        else:

            data = self.wdata.loc[start:end]

            return [
                data[T_AIR].values.tolist(),
                data[AVG_T_AIR].values.tolist(),
                (data[GHI].values - data[DI].values).tolist(),
                data[DI].values.tolist(),
            ]

    def select_block(self, now_dt, horizon=1, frame=2):
        """Select weather data from a block related to *now_dt*.

        Gather the weather data from *frame* days in the past and in
        the future at exactly the same hour of the day and select
        randomly one of those values for each output. If self.horizon
        has a value > 1, then this is repeated for all hours in the
        horizon.

        Parameters
        ----------
        now_dt : datetime.datetime
            The time for which data is requested.
        horizon : int, optional
            Fetches data from the time steps following the provided
            time. Can be used to simulate weather forecast.
        frame : int, optional
            Specify the number of days which should be considered in
            each direction.

        """
        if frame < 1:
            return self.select_hour(now_dt, horizon)

        t_airs = []
        avg_t_airs = []
        ghis = []
        dis = []

        # Iterate over time horizon
        for hour in range(horizon):
            start = now_dt + timedelta(hours=hour)

            # Get days of the current time frame
            days_before = [
                (start - timedelta(days=day + 1)).strftime(
                    "%Y-%m-%d %H:%M:%S%z"
                )
                for day in range(frame)
            ]
            days_after = [
                (start + timedelta(days=day + 1)).strftime(
                    "%Y-%m-%d %H:%M:%S%z"
                )
                for day in range(frame)
            ]
            days = (
                days_before[::-1]
                + [start.strftime("%Y-%m-%d %H:%M:%S%z")]
                + days_after
            )

            # Get the data from dataframe
            data = self.wdata[self.wdata.index.isin(days)]

            # Select randomly from time frame
            t_airs.append(self.rng.choice(data[T_AIR].values.tolist()))
            avg_t_airs.append(self.rng.choice(data[AVG_T_AIR].values.tolist()))
            ghis.append(self.rng.choice(data[GHI].values.tolist()))
            dis.append(self.rng.choice(data[DI].values.tolist()))

        return [t_airs, avg_t_airs, ghis, dis]


if __name__ == "__main__":
    WeatherData("data/weather_bre2009-2020.hdf5")

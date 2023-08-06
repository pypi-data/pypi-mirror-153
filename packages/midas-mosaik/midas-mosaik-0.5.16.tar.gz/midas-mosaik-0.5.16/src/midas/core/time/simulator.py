import mosaik_api
import numpy as np
from .meta import META
from datetime import timezone, datetime, timedelta
from midas.util.dateformat import GER
import calendar

SECONDS_PER_DAY = 24 * 60 * 60
SECONDS_PER_WEEK = SECONDS_PER_DAY * 7
SECONDS_PER_YEAR = SECONDS_PER_DAY * 365
SECONDS_PER_LEAP_YEAR = SECONDS_PER_DAY * 366


class TimeSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)

        self.sid = None
        self.eid = None
        self._sin_time_day: float = None
        self._cos_time_day: float = None
        self._sin_time_week: float = None
        self._cos_time_week: float = None
        self._sin_time_year: float = None
        self._cos_time_year: float = None

        self._step_size: int = None
        self._utc_now_dt: datetime = None
        self._local_now_dt: datetime = None
        self._time_schedule: list = None
        self._current_schedule_idx: int = 0
        self._day_dif_td: timedelta = None
        self._week_dif_td: timedelta = None
        self._year_dif_td: timedelta = None

    def init(self, sid, **sim_params):
        self.sid = sid
        self._step_size = sim_params.get("step_size", 900)
        self._local_now_dt = datetime.strptime(
            sim_params.get("start_date", "2020-01-01 00:00:00+0100"), GER
        )
        self._utc_now_dt = self._local_now_dt.astimezone(timezone.utc)

        self._day_dif_td = self._local_now_dt - self._local_now_dt.replace(
            hour=0, minute=0, second=0
        )
        self._year_dif_td = self._local_now_dt - self._local_now_dt.replace(
            month=1, day=1, hour=0, minute=0, second=0
        )
        self._week_dif_td = timedelta(days=self._local_now_dt.weekday())

        self._time_schedule = sim_params.get("time_schedule", None)

        return self.meta

    def create(self, num, model, **model_params):
        errmsg = (
            "You should really not try to instantiate more than one ",
            "timegenerator.",
        )
        assert num == 1 and self.eid is None, errmsg

        self.eid = "Timegenerator-0"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance=0):
        if time > 0:
            if self._time_schedule is not None:
                self._local_now_dt = datetime.strptime(
                    self._time_schedule[self._current_schedule_idx], GER
                )
                self._utc_now_dt = self._local_now_dt.astimezone(timezone.utc)
                self._current_schedule_idx = (
                    self._current_schedule_idx + 1
                ) % len(self._time_schedule)
            else:
                # Setting the time for all simulators, so updating the time
                # ... but not in the first step.
                self._local_now_dt += timedelta(seconds=self._step_size)
                self._utc_now_dt += timedelta(seconds=self._step_size)

        if calendar.isleap(self._local_now_dt.year):
            seconds_per_year = SECONDS_PER_LEAP_YEAR
        else:
            seconds_per_year = SECONDS_PER_YEAR

        self.sin_time_day = np.sin(
            2
            * np.pi
            * (time + self._day_dif_td.total_seconds())
            / SECONDS_PER_DAY
        )
        self.sin_time_week = np.sin(
            2
            * np.pi
            * (time + self._week_dif_td.total_seconds())
            / SECONDS_PER_WEEK
        )
        self.sin_time_year = np.sin(
            2
            * np.pi
            * (time + self._year_dif_td.total_seconds())
            / seconds_per_year
        )
        self.cos_time_day = np.cos(
            2
            * np.pi
            * (time + self._day_dif_td.total_seconds())
            / SECONDS_PER_DAY
        )
        self.cos_time_week = np.cos(
            2
            * np.pi
            * (time + self._week_dif_td.total_seconds())
            / SECONDS_PER_WEEK
        )
        self.cos_time_year = np.cos(
            2
            * np.pi
            * (time + self._year_dif_td.total_seconds())
            / seconds_per_year
        )

        return time + self._step_size

    def get_data(self, outputs):
        data = dict()
        data[self.eid] = dict()
        data[self.eid]["sin_day_time"] = self.sin_time_day
        data[self.eid]["sin_week_time"] = self.sin_time_week
        data[self.eid]["sin_year_time"] = self.sin_time_year
        data[self.eid]["cos_day_time"] = self.cos_time_day
        data[self.eid]["cos_week_time"] = self.cos_time_week
        data[self.eid]["cos_year_time"] = self.cos_time_year
        data[self.eid]["utc_time"] = self._utc_now_dt.strftime(GER)
        data[self.eid]["local_time"] = self._local_now_dt.strftime(GER)

        return data

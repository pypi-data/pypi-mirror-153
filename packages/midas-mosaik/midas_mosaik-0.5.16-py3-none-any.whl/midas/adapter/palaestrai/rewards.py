import math
from typing import List

import numpy as np

from palaestrai.agent import (
    ActuatorInformation,
    RewardInformation,
    SensorInformation,
)
from palaestrai.types import Box, Discrete

from .reward import Reward


def gaus_norm(
    raw_value: float,
    mu: float = 1,
    sigma: float = 0.1,
    c: float = 0.5,
    a: float = -1,
):
    if not isinstance(raw_value, float):
        return 0
    gaus_reward = a * math.exp(-((raw_value - mu) ** 2) / (2 * sigma**2)) - c
    return gaus_reward


class NoExtGridHealthReward(Reward):
    def __init__(self, **params):
        super().__init__(**params)
        self.grid_health_sensor = params.get(
            "grid_health", "Powergrid-0.Grid-0.health"
        )
        self.ext_grid_sensor = params.get(
            "ext_grid", "Powergrid-0.0-ext_grid-0.p_mw"
        )

    def __call__(self, state, *args, **kwargs):

        rewards = []
        for sensor in state:
            if self.grid_health_sensor == sensor.sensor_id:
                system_health_reward = RewardInformation(
                    sensor.sensor_value, Discrete(2), "grid_health_reward"
                )
                rewards.append(system_health_reward)
            elif self.ext_grid_sensor in sensor.sensor_id:
                reward = abs(sensor.sensor_value)
                external_grid_penalty_reward = RewardInformation(
                    reward, Discrete(1000), "external_grid_penalty_reward"
                )
                rewards.append(external_grid_penalty_reward)
        return rewards


class GridHealthReward(Reward):
    def _line_load(self, value):
        if not isinstance(value, int):
            return 0
        if value <= 100:
            return 0
        if value > 100 and value <= 120:
            return value - 100
        if value > 120:
            return np.exp((value - 100) / 10)

    def __call__(
        self, state: List[SensorInformation], *arg, **kwargs
    ) -> List[ActuatorInformation]:

        reward = 0
        for sensor in state:
            if "vm_pu" in sensor.sensor_id:
                reward += (gaus_norm(sensor(), 1, 0.02, 1.0, 2)) * 50
            if "line-" in sensor.sensor_id:
                reward -= self._line_load(sensor())
        final_reward = RewardInformation(
            reward, Box(-np.inf, np.inf, shape=(1,)), "grid_health_reward"
        )
        return [final_reward]

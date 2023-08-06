""" This module contains the DLP simulator."""
import os
from datetime import datetime

import h5py
import mosaik_api
import numpy as np
from midas.core.dlp import LOG
from midas.core.dlp.model import DLPModel
from midas.util.base_data_simulator import BaseDataSimulator
from midas.util.dateformat import GER
from midas.util.runtime_config import RuntimeConfig

from .meta import META


class DLPSimulator(BaseDataSimulator):
    """The DLP simulator."""

    def __init__(self):
        super().__init__(META)
        self.sid = None
        self.models = dict()
        self.num_models = dict()
        self.data = dict()

    def init(self, sid, **sim_params):
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.

        Returns
        -------
        dict
            The meta dict (set by *mosaik_api.Simulator*).
        """
        super().init(sid, **sim_params)

        # We want to use the provided timezone
        self.now_dt = datetime.strptime(sim_params["start_date"], GER)

        data_path = sim_params.get(
            "data_path", RuntimeConfig().paths["data_path"]
        )
        file_path = os.path.join(
            data_path, sim_params.get("filename", "DefaultLoadProfiles.hdf5")
        )
        LOG.debug("Using db file at %s.", file_path)

        with h5py.File(file_path, "r") as h5f:
            for profile in h5f:
                self.data.setdefault(profile, dict())
                for season in h5f[profile]:
                    self.data[profile].setdefault(season, dict())
                    for day in h5f[profile][season]:
                        self.data[profile][season][day] = np.array(
                            list(h5f[profile][season][day])
                        )
        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity).

        Parameters
        ----------
        num : int
            The number of models to create.
        model : str
            The name of the models to create. Must be present inside
            the simulator's meta.

        Returns
        -------
        list
            A list with information on the created entity.
        """

        entities = list()
        self.num_models.setdefault(model, 0)
        for _ in range(num):
            eid = f"{model}-{self.num_models[model]}"
            profile = model[-2:]
            self.models[eid] = DLPModel(
                data=self.data[profile],
                p_mwh_per_a=model_params["p_mwh_per_a"],
                seed=self.rng.randint(self.seed_max),
                interpolate=model_params.get("interpolate", self.interpolate),
                randomize_data=model_params.get(
                    "randomize_data", self.randomize_data
                ),
                randomize_cos_phi=model_params.get(
                    "randomize_cos_phi", self.randomize_cos_phi
                ),
            )

            self.num_models[model] += 1
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance=0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation step (by convention in seconds since
            simulation start.
        inputs : dict
            A *dict* containing inputs for entities of this simulator.

        Returns
        -------
        int
            The next step this simulator wants to be stepped.

        """
        LOG.debug("At step %d received inputs %s", time, inputs)

        return super().step(time, inputs)

    def get_data(self, outputs):
        """Return the requested output (if feasible).

        Parameters
        ----------
        outputs : dict
            A *dict* containing requested outputs of each entity.

        Returns
        -------
        dict
            A *dict* containing the values of the requested outputs.

        """

        data = super().get_data(outputs)

        LOG.debug("Gathered outputs %s", data)

        return data

    def get_data_info(self):
        info = {
            key: {"p_mwh_per_a": model.p_mwh_per_a}
            for key, model in self.models.items()
        }
        for model in self.meta["models"]:
            info[f"num_{model.lower()}"] = self.num_models.get(model, 0)

        return info


if __name__ == "__main__":
    mosaik_api.start_simulation(DLPSimulator())

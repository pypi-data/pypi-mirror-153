""" This module contains the CommercialData simulator."""
from os.path import abspath, join

import mosaik_api
import pandas as pd
from midas.core.comdata import LOG
from midas.util.base_data_model import DataModel
from midas.util.base_data_simulator import BaseDataSimulator

from .meta import META


class CommercialDataSimulator(BaseDataSimulator):
    """The CommercialData simulator."""

    def __init__(self):
        super().__init__(META)

        self.load_p = None
        self.load_q = None

        self.num_models = dict()
        self.step_size = None

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

        # Load the data
        data_path = sim_params.get(
            "data_path",
            abspath(join(__file__, "..", "..", "..", "..", "..", "data")),
        )
        file_path = join(
            data_path, sim_params.get("filename", "CommercialsRefTMY3.hdf5")
        )
        self.load_p = pd.read_hdf(file_path, "load_pmw")
        try:
            self.load_q = pd.read_hdf(file_path, "load_qmvar")
        except Exception:
            LOG.debug("No q values for loads available. Skipping.")

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

            data_q = None
            if self.load_q is not None:
                data_q = self.load_q[model]

            self.models[eid] = DataModel(
                data_p=self.load_p[model],
                data_q=data_q,
                data_step_size=3600,
                scaling=model_params.get("scaling", 1.0),
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

    def get_data_info(self, eid=None):
        # TODO: Scale the value to the actual scaling of the model
        info = {
            key: {"p_mwh_per_a": model.p_mwh_per_a}
            for key, model in self.models.items()
        }
        return info


if __name__ == "__main__":
    mosaik_api.start_simulation(CommercialDataSimulator())

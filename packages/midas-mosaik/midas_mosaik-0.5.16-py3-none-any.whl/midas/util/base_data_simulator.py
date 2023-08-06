"""This module contains the base simulator class for certain data
simulators.

The models itself are simple data providers.
"""
import logging
from datetime import datetime, timedelta, timezone
from distutils.util import strtobool
import mosaik_api
import numpy as np

from .dateformat import GER

LOG = logging.getLogger("midas.basedatasim")


class BaseDataSimulator(mosaik_api.Simulator):
    """A base simulator for hdf5 data.

    Parameters
    ----------
    meta : dict
        The meta dict this simulator should pass to mosaik_api.

    """

    def __init__(self, meta):
        super().__init__(meta)
        self.sid = None
        self.models = dict()

        self.step_size = None
        self.now_dt = None
        self.seed = None
        self.seed_max = None
        self.rng = None
        self.interpolate = None
        self.randomize_data = None
        self.cos_phi = None
        self.randomize_cos_phi = None

    def init(self, sid, **sim_params):
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.
        now_dt : str
            An ISO datestring with Europe/Berlin timezone.
        interpolate : bool
            If *True*, interpolation is applied when step size is lower
            than the resolution of the data.
        randomize_data : bool
            If *True*, a small random noise is added to the data in
            each step.
        cos_phi : float
            A static cos phi used if no values for q are present in the
            data.
        randomize_cos_phi : bool
            If *True*, the cos phi is randomized. Applies only to data
            without values for q.
        seed : int
            A seed for the random number generator. Random numbers are
            only used, if one of the randomize flags is set.

        Returns
        -------
        dict
            The meta dict (set by mosaik_api.Simulator)

        """

        # General params
        self.sid = sid
        if "step_size" not in sim_params:
            LOG.debug(
                "Param *step_size* not provided. "
                "Using default step size of 900."
            )
        self.step_size = int(sim_params.get("step_size", 900))
        self.now_dt = datetime.strptime(
            sim_params["start_date"], GER
        ).astimezone(timezone.utc)
        self.interpolate = sim_params.get("interpolate", False)
        try:
            self.interpolate = bool(strtobool(self.interpolate))
        except AttributeError:
            pass

        self.randomize_data = sim_params.get("randomize_data", False)
        self.cos_phi = sim_params.get("cos_phi", 0.9)
        self.randomize_cos_phi = sim_params.get("randomize_cos_phi", False)

        # RNG
        self.seed = sim_params.get("seed", None)
        self.seed_max = sim_params.get("seed_max", 1_000_000)
        if self.seed is not None:
            self.rng = np.random.RandomState(self.seed)
        else:
            LOG.debug("No seed provided. Using random seed.")
            self.rng = np.random.RandomState()

        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity)

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
        raise NotImplementedError

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

        for model in self.models.values():
            model.cos_phi = self.cos_phi
            model.now_dt = self.now_dt

        for eid, attrs in inputs.items():
            for attr, src_ids in attrs.items():
                if attr == "cos_phi":
                    assert (
                        len(src_ids) == 1
                    ), "Only one provider for cos_phi allowed"
                    self.models[eid].cos_phi = list(src_ids.values())[0]
                else:
                    LOG.info("Detected not supported input %s.", attr)

        for eid, model in self.models.items():
            model.step()

        self.now_dt += timedelta(seconds=self.step_size)

        return time + self.step_size

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
        data = dict()
        for eid, attrs in outputs.items():
            model = eid.split("-")[0]
            data[eid] = dict()
            for attr in attrs:
                if attr == "outbox":
                    data[eid][attr] = {
                        "p_mw": getattr(self.models[eid], "p_mw"),
                        "q_mvar": getattr(self.models[eid], "q_mvar"),
                    }
                elif attr in self.meta["models"][model]["attrs"]:
                    data[eid][attr] = getattr(self.models[eid], attr)
                else:
                    LOG.info("Unknown output attribute %s.", attr)

        return data

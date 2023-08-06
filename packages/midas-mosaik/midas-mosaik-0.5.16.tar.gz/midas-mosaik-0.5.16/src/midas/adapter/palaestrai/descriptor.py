"""This module contains the :class:`.Descriptor`, which implements the
functions required by palaestAI-mosaik and, therefore, allows to use
MIDAS as environment in ARL.

"""
import midas

# from midas.adapter.palaestrai import LOG

# from midas.scenario.configurator import Configurator


class Descriptor:
    """Descriptor for MIDAS as environment."""

    def __init__(self):
        self.configurator = None
        self.scenario = None
        self.world = None
        self.sensors = None
        self.actuators = None

    def describe(self, params=None):
        """Describe the MIDAs scenario.

        Parameters
        ----------
        name : str, (optional)
            Name of the scenario to describe.
        params : dict, (optional)
            A dict containing initial parameters, e.g., parameters
            normally provided by the command line interface.
        custom_cfg : str, (optional)
            A string containing the path to a custom configuration
            file. This file will be added to the available scenario
            configurations. To use that specific configuration, make
            sure to set :attr:`name` accordingly.
        init_path : str, (optional)
            A string containing the path to the midas ini file. Default
            location is used if None is provided.

        Returns
        -------
        tuple
            A tuple containing a list of sensors and a list of
            actuators.

        """
        if params is None:
            params = dict()
            name = "midasmv_der"
        else:
            name = params["name"]

        custom_cfg = params.get("config", None)

        if self.scenario is None:
            self._configure(name, params, custom_cfg)

        return (self.sensors, self.actuators)

    def get_world(self, params=None):
        """Return the world object of the MIDAS scenario.

        See :meth:`describe` for a description of parameters.

        Returns
        -------
        :obj:`mosaik.scenario.World`
            A fully configured world object that has not started.

        """
        if params is None:
            params = dict()
            name = "midasmv_der"
        else:
            name = params["name"]

        custom_cfg = params.get("config", None)

        if self.scenario is None:
            self._configure(name, params, custom_cfg)

        return self.world

    def _configure(self, name, params, custom_cfg):
        params["arl"] = True
        self.scenario = midas.run(name, custom_cfg, params, no_run=True)

        # self.configurator = Configurator(inipath=ini_path, autocfg=True)
        # self.scenario = self.configurator.configure(name, params, custom_cfg)
        self.world = self.scenario["world"]
        self.sensors = self.scenario["sensors"]
        self.actuators = self.scenario["actuators"]

import os

import click
from midas.scenario.configurator import Configurator

from . import fnc_configure, fnc_download


def run(
    scenario_name="demo",
    config=None,
    params=None,
    no_run=False,
    no_script=False,
    no_yaml=False,
):
    """The main run method to start a MIDAS scenario.

    Parameters
    ----------
    scenario_name: str
        The name of the scenario to start. The name is the toplevel
        key in the scenario yaml file.
    config: Union[Tuple, str, None]
        One or more custom configs to load the scenario from.
    params: Union[Dict, None]
        Optional dictionary with scenario parameters that will be
        passed to the configurator.

    """

    # Just to be save: Configure runtime config and download datasets.
    fnc_configure.configure(autocfg=True)
    fnc_download.download()

    if scenario_name == "demo":
        scenario_name = "midasmv"

    if params is None:
        params = dict()

    params.setdefault("silent", False)

    if config is not None:
        if isinstance(config, str):
            config = (config,)
        config = [os.path.abspath(c) for c in config]

    configurator = Configurator()
    scenario = configurator.configure(
        scenario_name, params, config, no_script, no_yaml
    )
    if scenario:
        if no_run:
            return scenario
        else:
            configurator.run()
    else:
        click.echo(
            "Scenario configuration failed. See log files for more infos"
        )

    return dict()

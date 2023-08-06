"""This module contains the midas command line interface 2.0."""
import logging
import logging.config
import sys

import click
import midas
import pkg_resources
import setproctitle
from midas.util.runtime_config import RuntimeConfig

from . import fnc_analyze, fnc_configure, fnc_download, fnc_run, fnc_list


@click.group(invoke_without_command=True)
@click.option(
    "--config",
    "-c",
    type=click.Path(),
    help=(
        "Supply custom runtime configuration file. If used together with "
        "autocfg and no config is present at the given path, a new default "
        "config will be created. (Default search path: %s)"
        % midas.util.runtime_config.CONFIG_FILE_PATHS
    ),
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help=(
        "Increase program verbosity, can be given numerous times: "
        "-v prints also INFO messages, and -vv emits DEBUG output."
    ),
)
@click.version_option(pkg_resources.require("midas-mosaik")[0].version)
def cli(config=None, verbose=0):
    setproctitle.setproctitle(" ".join(sys.argv))

    if config:
        try:
            with open(config, "r") as fp:
                RuntimeConfig().load(fp)
        except OSError as err:
            click.echo(
                "ERROR: Could not load config from %s: %s." % (config, err)
            )
            exit(1)
    else:
        try:
            RuntimeConfig()
        except FileNotFoundError as err:
            click.echo(
                "Please create a runtime config. %s.\n"
                "Will continue with built-in defaults. " % err,
                file=sys.stderr,
            )
    init_logger(verbose)


@cli.command()
@click.option(
    "--autocfg",
    "-a",
    is_flag=True,
    help=(
        "Skip ini dialog and apply defaults or use inipath and datapath"
        " if provided with this command."
    ),
)
@click.option(
    "--config",
    "-c",
    type=click.Path(),
    help=(
        "Supply a path for the runtime configuration file to skip the "
        "corresponding prompt."
    ),
)
@click.option(
    "--data-path",
    "-d",
    "data_path",
    type=click.Path(),
    help=(
        "Specify the path to the datasets to skip the corresponding prompt."
    ),
)
@click.option(
    "--update",
    "-u",
    is_flag=True,
    help="Loading the newst DEFAULT_RUN_TIME_CONFIG",
)
def configure(**kwargs):
    fnc_configure.configure(**kwargs)


@cli.command()
@click.option(
    "-c",
    "--commercials",
    is_flag=True,
    help="Download only the commercial dataset.",
)
@click.option(
    "-dlp",
    "--default-load-profiles",
    "default_load_profiles",
    is_flag=True,
    help="Download only the default load profiles.",
)
@click.option(
    "-g",
    "--generator-ts",
    "gen_ts",
    is_flag=True,
    help="Download only generator timeseries.",
)
@click.option(
    "-sb",
    "--simbench",
    is_flag=True,
    help="Download only the Simbench datasets.",
)
@click.option(
    "-sn",
    "--smart-nord",
    "smartnord",
    is_flag=True,
    help="Download only the Smart Nord dataset.",
)
@click.option(
    "-w", "--weather", is_flag=True, help="Download only the weather datasets."
)
@click.option(
    "-k",
    "--keep-tmp",
    "keep_tmp",
    is_flag=True,
    help="Keep the temporarily downloaded files.",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Download the datasets and ignore existing ones.",
)
def download(**kwargs):
    click.echo("Start downloading...")
    fnc_download.download(**kwargs)
    click.echo("Download complete.")


@cli.command()
@click.argument("scenario_name")
@click.option(
    "--config",
    "-c",
    multiple=True,
    type=click.Path(
        exists=True,
        readable=True,
        dir_okay=True,
        file_okay=True,
        allow_dash=True,
    ),
    help=(
        "Provide a custom (scenario-)config file. Providing a scenario"
        " name is still required "
    ),
)
@click.option(
    "--db-file",
    "-df",
    "db_file",
    help=(
        "Specify a database file. Temporarily overwrites the scenario "
        "file settings. The -nd flag is ignored."
    ),
)
@click.option(
    "--end",
    "-e",
    default=None,
    type=int,
    help="Specify the number of simulation steps mosaik should perform.",
)
@click.option(
    "--no-db",
    "-nd",
    "no_db",
    is_flag=True,
    help=(
        "Disable the database. Default behavior is to use the settings"
        " of the scenario file."
    ),
)
@click.option(
    "--no-rng",
    "-nr",
    "no_rng",
    is_flag=True,
    help="Globally disable random number generator in the simulation.",
)
@click.option(
    "--port",
    "-p",
    default=5555,
    type=int,
    help="Specify the port for mosaik.",
)
@click.option(
    "--seed", "-s", type=int, help="Set a positive integer as random seed."
)
@click.option(
    "--silent",
    "-q",
    is_flag=True,
    help="Pass the silent flag to mosaik to suppress mosaik output",
)
def run(scenario_name, config=None, **kwargs):
    if not scenario_name:
        click.echo(
            "WARNING: No scenario name provided. Rerun the command with\n\n\t"
            "midasctl run demo\n\nto run the demo scenario or replace 'demo' "
            "with any other scenario you\n"
            "like (see 'Scenarios' in the docs)."
        )
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()
    # click.echo(kwargs)ss

    # Process additional cli options
    params = dict()

    db_file = kwargs.get("db_file", None)
    if db_file is not None:
        if not db_file.endswith(".hdf5"):
            db_file = f"{db_file}.hdf5"
        params["with_db"] = True
        params["mosaikdb_params"] = {"filename": db_file}
    else:
        params["with_db"] = not kwargs.get("no_db", False)

    # Mosaik options and port number
    port = kwargs.get("port", 5555)
    try:
        port = int(port)
    except ValueError:
        click.echo(f"Port {port} is not an integer. Using default port 5555.")
        port = 5555
    params["mosaik_params"] = {"addr": ("127.0.0.1", port)}
    params["silent"] = kwargs.get("silent", False)
    end = kwargs.get("end", None)
    if end is not None:
        params["end"] = end

    # Seeds and rng
    seed = kwargs.get("seed", None)
    if seed is not None:
        try:
            seed = abs(int(seed))
        except ValueError:
            click.echo(
                f"Seed {seed} is not an integer. Seed will be random, then!"
            )
            seed = "random"
        params["seed"] = seed
    params["deny_rng"] = kwargs.get("no_rng", False)

    fnc_run.run(scenario_name, config, params)


@cli.command()
@click.argument(
    "scenario_db_path",
    nargs=-1,
    type=click.Path(
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        allow_dash=True,
    ),
)
@click.option(
    "--output-folder",
    "-o",
    "output_folder",
    default="",
    help=(
        "Specify the folder where to store the analysis results. "
        "If not provided, the default output folder is used."
    ),
)
@click.option(
    "--db-style",
    "-ds",
    "db_style",
    default="midas",
    help=(
        "Set the database style. Default is mosaik, which assumes a "
        "database created with mosaikHDF5. The other option is midas, "
        "which uses the new midasHDF5 database created with pytables."
    ),
)
@click.option(
    "--from-step",
    "-s",
    "start",
    type=click.INT,
    default=0,
    help="Specify the first step to be included in the analysis.",
)
@click.option(
    "--to-step",
    "-e",
    "end",
    type=click.INT,
    default=-1,
    help="Specify the last step to be included in the analysis.",
)
@click.option(
    "--step-size",
    "-ss",
    "step_size",
    type=click.INT,
    default=900,
    help="Specify the step size used in the given database.",
)
@click.option(
    "--full", "-f", is_flag=True, help="Enable full report: More plot outputs."
)
def analyze(
    scenario_db_path, output_folder, db_style, start, end, step_size, full
):
    if start >= end and end != -1:
        click.echo(
            "Value for start must be lower than the value for end. "
            "Will use the default values."
        )
        start = 0
        end = -1
    fnc_analyze.analyze(
        scenario_db_path, output_folder, db_style, start, end, step_size, full
    )


@cli.command()
@click.option(
    "--config",
    "-c",
    multiple=True,
    type=click.Path(
        exists=True,
        readable=True,
        dir_okay=True,
        file_okay=True,
        allow_dash=True,
    ),
    help=(
        "Provide a custom (scenario-)config file. Providing a scenario"
        " name is still required "
    ),
)
def list_scenarios(config):
    fnc_list.list_scenarios(config)


def init_logger(verbose):
    """Init logger with config from either RuntimeConfig or a default."""
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = levels[verbose if verbose < len(levels) else len(levels) - 1]

    try:
        logging.config.dictConfig(RuntimeConfig().logging)
        logging.debug(
            "Initialized logging from RuntimeConfig(%s)", RuntimeConfig()
        )
    except (KeyError, ValueError) as err:
        logging.basicConfig(level=log_level)
        logging.warning(
            "Could not load logging config (%s), continuing with defaults.",
            err,
        )

    if verbose != 0:
        for name in logging.root.manager.loggerDict:
            logging.getLogger(name).setLevel(log_level)
            RuntimeConfig().logging["loggers"].update(
                {name: {"level": str(logging._levelToName[log_level])}}
            )


if __name__ == "__main__":
    cli(obj=dict())

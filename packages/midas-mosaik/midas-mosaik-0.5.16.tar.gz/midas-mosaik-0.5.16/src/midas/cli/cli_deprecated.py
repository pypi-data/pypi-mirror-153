"""This module contains the deprecated midas command line interface."""
import click

from . import cli


@click.command()
@click.option(
    "--config",
    "-c",
    help="Provide a custom config file. Providing a scenario name is "
    "still required.",
)
@click.option(
    "--with-db",
    "-d",
    "with_db",
    is_flag=True,
    help="Use a mosaikhdf5 database to log outputs.",
)
@click.option(
    "--db-file",
    "-df",
    "db_file",
    help="Specify a mosaikhdf5 database file. " "The -d flag is ignored.",
)
@click.option(
    "--scenario-name",
    "-n",
    "scenario_name",
    default="demo",
    help="The name of the scenario to run.",
)
@click.option(
    "--silent", "-q", is_flag=True, help="Suppress output from mosaik."
)
@click.option("--port", "-p", help="Specify the port for mosaik")
@click.option(
    "--log",
    "-l",
    default="WARNING",
    help="Set the log level (DEBUG|INFO|WARNING)",
)
@click.option(
    "--no-rng",
    "-r",
    "norng",
    is_flag=True,
    help="Globally disable random number generator in the simulation",
)
@click.option("--seed", "-s", help="Set a positive integer as random seed.")
def cli_deprecated(**kwargs):
    """Command line interface for midas."""
    main(**kwargs)


def main(**kwargs):
    """The main function of the midas CLI."""
    click.echo(
        "DEPRECATION WARNING: midascli is now deprecated. "
        "Use midasctl (--help) instead."
    )
    verbose = {"WARNING": "", "INFO": "-v", "DEBUG": "-vv"}[
        kwargs.get("log", "WARNING")
    ]
    options = list()
    if verbose != "":
        options.append(verbose)
    options.append("run")
    options.append(kwargs.get("scenario_name", "demo"))
    if kwargs.get("norng", False):
        options.append("--no-rng")
    if kwargs.get("port", None) is not None:
        options.append("--port")
        options.append(kwargs["port"])
    if kwargs.get("silent", False):
        options.append("--silent")
    db_file = kwargs.get("db_file", None)
    if db_file is not None:
        options.append("--db-file")
        options.append(db_file)
    elif not kwargs.get("with_db", True):
        options.append("--no-db")

    ccfg = kwargs.get("config", None)
    if ccfg is not None:
        options.append("--config")
        options.append(ccfg)

    click.echo(
        "Running the following command with midasctl (you should really"
        "use it by now)\n",
    )
    for idx, opt in enumerate(options):
        if idx == 0:
            print("\tmidasctl", end="")

        print(f" {opt}", end="")
    print("\n")
    cli.cli(options)


if __name__ == "__main__":
    main(scenario_name="midasmv_der", with_db=True)

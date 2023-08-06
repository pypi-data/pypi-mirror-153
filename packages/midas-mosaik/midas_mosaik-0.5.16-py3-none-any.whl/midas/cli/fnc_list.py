import click

from midas.util.config_util import get_config_files, load_configs


def list_scenarios(configs):

    files = get_config_files(configs)

    click.echo("Found the following scenarios:")

    for fil in files:
        configs = load_configs([fil])

        for key in configs:
            click.echo(f"* '{key}'  -->  {fil}")

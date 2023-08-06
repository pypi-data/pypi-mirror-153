import os

import click
from midas.tools import analysis
from midas.util.runtime_config import RuntimeConfig


def analyze(
    scenario_db_path,
    output_folder="",
    db_style="midas",
    start=0,
    end=-1,
    step_size=900,
    full=False,
):
    """The analyze function of midas CLI."""

    db_file = os.path.abspath(scenario_db_path[0])
    name = os.path.split(db_file)[-1][:-5]

    if output_folder == "":
        output_folder = RuntimeConfig().paths["output_path"]

    output_folder = os.path.abspath(output_folder)
    if not output_folder.endswith(name):
        output_folder = os.path.join(output_folder, name)

    if start > 0:
        output_folder += f"_from-{start}"
        if end < 0:
            output_folder += "_to-end"
        else:
            output_folder += f"_to-{end}"
    elif end > 0:
        output_folder += f"_from-start_to-{end}"

    click.echo(f'Reading database at "{db_file}".')
    click.echo(f'Saving results to "{output_folder}".')

    analysis.analyze(
        name, db_file, output_folder, db_style, start, end, step_size, full
    )

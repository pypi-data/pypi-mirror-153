import logging
import os
import shutil

import click
from midas.util.runtime_config import RuntimeConfig

from .download.download_commercials import download_commercials
from .download.download_dlp import download_dlp
from .download.download_gen import download_gen
from .download.download_simbench import download_simbench
from .download.download_smartnord import download_smart_nord
from .download.download_weather import download_weather

LOG = logging.getLogger("midas.cli")


def download(
    default_load_profiles=False,
    commercials=False,
    gen_ts=False,
    simbench=False,
    smartnord=False,
    weather=False,
    keep_tmp=False,
    force=False,
):
    """Download the required datasets.

    There are currently five categories of datasets:
        * Default load profiles from BDEW
        * Commercial dataset from openei.org
        * Simbench data from the simbench grids
        * Smart Nord dataset from the research project Smart Nord
        * Weather dataset from opendata.dwd.de

    The default behavior of this function is to download all missing
    datasets and, afterwards, remove the temporary directory created
    during this process.

    If at least one of the flags is set to *True*, only those datasets
    will be downloaded. If *force* is *True*, the datasets will be
    downloaded regardless of any existing dataset. If *keep_tmp* is
    *True*, the temporary downloaded files will not be removed
    afterwards.

    """
    # Check parameters
    if not any(
        [
            default_load_profiles,
            commercials,
            gen_ts,
            simbench,
            smartnord,
            weather,
        ]
    ):
        if_necessary = True
        default_load_profiles = (
            commercials
        ) = gen_ts = simbench = smartnord = weather = True
    else:
        if_necessary = False

    # Create paths
    data_path = RuntimeConfig().paths["data_path"]
    tmp_path = os.path.abspath(os.path.join(data_path, "tmp"))
    os.makedirs(tmp_path, exist_ok=True)

    if default_load_profiles:
        download_dlp(data_path, tmp_path, if_necessary, force)

    if commercials:
        download_commercials(data_path, tmp_path, if_necessary, force)

    if gen_ts:
        download_gen(data_path, tmp_path, if_necessary, force)

    if simbench:
        download_simbench(data_path, tmp_path, if_necessary, force)

    if smartnord:
        download_smart_nord(data_path, tmp_path, if_necessary, force)

    if weather:
        download_weather(data_path, tmp_path, if_necessary, force)

    # Clean up
    if not keep_tmp:
        try:
            shutil.rmtree(tmp_path)
        except Exception as err:
            click.echo(
                f"Failed to remove files '{tmp_path}'': {err}. "
                "You have to remove those files manually."
            )
            LOG.warning(
                "Could not remove temporary files at %s. You have to remove "
                "those files by hand. The error is: %s",
                tmp_path,
                err,
            )

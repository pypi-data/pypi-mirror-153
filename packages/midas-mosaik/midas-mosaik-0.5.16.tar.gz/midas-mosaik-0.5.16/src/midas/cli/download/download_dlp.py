import logging
import os
import platform
import shutil

import click
import h5py
import pandas as pd
import wget
from midas.util.runtime_config import RuntimeConfig

from .unzip import unzip

LOG = logging.getLogger("midas.cli")

if platform.system() == "Windows" or platform.system() == "Darwin":
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context


def download_dlp(data_path, tmp_path, if_necessary, force):
    """Download and convert default load profiles.

    The default load profiles can be downloaded from the BDEW (last
    visited on 2020-07-07):

    https://www.bdew.de/energie/standardlastprofile-strom/

    """

    LOG.info("Preparing default load profiles...")
    # Specify the paths, we only have one provider for those profiles.
    config = RuntimeConfig().data["default_load_profiles"][0]
    if if_necessary and not config.get("load_on_start", False):
        return

    output_path = os.path.abspath(os.path.join(data_path, config["name"]))

    if os.path.exists(output_path):
        LOG.debug("Found existing dataset at %s.", output_path)
        if not force:
            return

    # Download the file
    fname = config["base_url"].rsplit("/", 1)[-1]
    if not os.path.exists(os.path.join(tmp_path, fname)) or force:
        LOG.debug("Downloading '%s'...", config["base_url"])
        fname = wget.download(config["base_url"], out=tmp_path)
        click.echo()  # To get a new line after wget output
        LOG.debug("Download complete.")

    # Specify unzip target
    target = os.path.join(tmp_path, "dlp")
    if os.path.exists(target):
        LOG.debug("Removing existing files.")
        shutil.rmtree(target)

    # Extract the file

    LOG.debug("Extracting profiles...")
    unzip(tmp_path, fname, target)
    # with ZipFile(os.path.join(tmp_path, fname), "r") as zip_ref:
    #     zip_ref.extractall(os.path.join(tmp_path, target))
    LOG.debug("Extraction complete.")

    excel_path = os.path.join(target, config["filename"])

    # Load excel sheet
    data = pd.read_excel(
        io=excel_path,
        sheet_name=config["sheet_names"],
        header=[1, 2],
        skipfooter=1,
    )

    # Create a hdf5 datebase from the sheet
    LOG.debug("Creating hdf5 database...")
    h5f = h5py.File(output_path, "w")
    for name in config["sheet_names"]:
        grp = h5f.create_group(name)
        for season in config["seasons"]:
            subgrp = grp.create_group(season[1])
            for day in config["days"]:
                # Bring last value to front
                df = pd.DataFrame(
                    data={"series": data[name][(season[0], day[0])].values}
                )
                df["tmp"] = range(1, len(df) + 1)
                df.loc[df.index == len(df) - 1, "tmp"] = 0
                df = df.sort_values("tmp").drop("tmp", axis=1)
                df.index = range(len(df))
                subgrp.create_dataset(day[1], data=df["series"])
    h5f.attrs["hint"] = "Quarter-hourly power values for annual consumption."
    h5f.attrs["ref_value"] = "1000 kWh/a"
    h5f.close()
    LOG.info("Successfully created database for default load profiles.")

import logging
import os
import platform

import click
import pandas as pd
import wget
from midas.util.runtime_config import RuntimeConfig

LOG = logging.getLogger("midas.cli")

if platform.system() == "Windows" or platform.system() == "Darwin":
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context


def download_commercials(data_path, tmp_path, if_necessary, force):
    """Download and convert the commercial dataset.

    The datasets are downloaded from
    https://openei.org/datasets/files/961/pub

    """
    LOG.info("Preparing commercial datasets...")

    # We allow multiple datasets here (although not tested, yet)
    for config in RuntimeConfig().data["commercials"]:
        if if_necessary and not config.get("load_on_start", False):
            continue
        output_path = os.path.abspath(os.path.join(data_path, config["name"]))

        if os.path.exists(output_path):
            LOG.debug("Found existing dataset at %s.", output_path)
            if not force:
                continue

        # Construct the final download locations
        loc_url = config["base_url"] + config["loc_url"]
        files = [
            (loc_url + f + config["post_fix"]).rsplit("/", 1)[1]
            for f, _ in config["data_urls"]
        ]
        for idx in range(len(files)):
            file_path = os.path.join(tmp_path, files[idx])
            if not os.path.exists(file_path) or force:
                if os.path.exists(file_path):
                    os.remove(file_path)
                LOG.debug("Downloading '%s'...", files[idx])
                files[idx] = wget.download(
                    loc_url + config["data_urls"][idx][0] + config["post_fix"],
                    out=tmp_path,
                )
                click.echo()
            else:
                files[idx] = file_path
        LOG.debug("Download complete.")

        # Converting data
        date_range = pd.date_range(
            start="2004-01-01 00:00:00",
            end="2004-12-31 23:00:00",
            freq="H",
            tz="Europe/Berlin",
        )
        # Since 2004 is a leap year, we need to add an additional
        # day.
        dr_pt1 = pd.date_range(
            start="2004-01-01 00:00:00",
            end="2004-02-28 23:00:00",
            freq="H",
            tz="Europe/Berlin",
        )
        LOG.debug("Converting files...")
        # Now assemble the distinct files to one dataframe
        data = pd.DataFrame(index=date_range)
        for (src, tar), file_ in zip(config["data_urls"], files):
            fpath = os.path.join(tmp_path, file_)
            tsdat = pd.read_csv(fpath, sep=",")
            tsdat1 = tsdat.iloc[: len(dr_pt1)]
            tsdat1 = pd.concat([tsdat1, tsdat1.iloc[-24:]])
            tsdat2 = tsdat.iloc[len(dr_pt1) :]
            tsdat = pd.concat([tsdat1, tsdat2])
            tsdat.index = date_range
            data[tar] = tsdat[config["el_cols"]].sum(axis=1) * 1e-3
        LOG.debug("Conversion complete.")

        # Create hdf5 database
        data.to_hdf(output_path, "load_pmw", "w")
        LOG.info("Successfully created database for commercial dataset.")

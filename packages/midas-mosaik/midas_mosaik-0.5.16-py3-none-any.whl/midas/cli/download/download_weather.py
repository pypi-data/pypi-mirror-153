import logging
import os
import platform
from datetime import datetime

import click
import numpy as np
import pandas as pd
import wget
from midas.util.runtime_config import RuntimeConfig

from .unzip import unzip

LOG = logging.getLogger("midas.cli")

if platform.system() == "Windows" or platform.system() == "Darwin":
    import ssl

    ssl._create_default_https_context = ssl._create_unverified_context


def download_weather(data_path, tmp_path, if_necessary, force):
    """Download and convert the weather datasets.

    The weather data is downloaded from https://opendata.dwd.de,
    the selected weather station is located in Bremen.

    At the beginning of every new year, the data from the previous
    year is added to the dataset. Unfortunately, the download link
    changes at the same time, now including the latest year of data.

    To prevent a failure every year, the year value in the download
    link is increased, but that may break at anytime if DWD decides to
    change the download links in any other way.

    The year is included in the 'post_fix' key of the runtime config.

    """
    LOG.info("Preparing weather datasets...")

    # We allow multiple datasets here
    for config in RuntimeConfig().data["weather"]:
        if if_necessary and not config.get("load_on_start", False):
            continue

        output_path = os.path.abspath(os.path.join(data_path, config["name"]))

        if os.path.exists(output_path):
            LOG.debug("Found existing dataset at %s.", output_path)
            if not force:
                continue
            else:
                LOG.debug("Downloading weather data anyways...")
        else:
            LOG.debug("No dataset found. Start downloading weather data ...")

        base_url = config["base_url"]
        post_fix = config["post_fix"]
        year = int(post_fix[:4])
        for url in [
            "solar_url",
            "air_url",
            "cloud_url",
            "sun_url",
            "wind_url",
        ]:

            for idx in range(10):
                if url == "solar_url":
                    full_url = base_url + config[url]
                else:
                    # The other urls follow the same schema, including the
                    # latest year of data in the download link.
                    full_url = base_url + config[url] + f"{year}{post_fix[4:]}"

                fname = full_url.rsplit("/", 1)[-1]
                fpath = os.path.join(tmp_path, fname)
                if not os.path.exists(fpath):
                    try:
                        LOG.info("Start downloading '%s'...", full_url)
                        fpath = wget.download(full_url, out=tmp_path)
                        click.echo()
                        LOG.debug("Download complete.")
                        break
                    except Exception as err:
                        LOG.warning(
                            "Error during the download of file '%s': '%s'.\n"
                            "Probably the year has changed. Will try to fix "
                            "this automatically.",
                            full_url,
                            err,
                        )
                        fpath = None
                        if url != "solar_url":
                            year += 1
                        continue
                break

            if fpath is None:
                raise ValueError(
                    "Could not download weather data. Sorry for that. "
                    "This needs to be fixed manually :("
                )
            else:
                unzip(tmp_path, fpath, url.split("_")[0])

        LOG.debug("Creating database...")
        # We start at 2009 because the solar dataset has no data before
        # that year.
        start_date = str(config.get("start_date", "2009-01-01 00:00:00"))
        data = pd.DataFrame(
            index=pd.date_range(
                start=start_date,
                end=f"{year}-12-31 23:00:00",
                tz="Europe/Berlin",
                freq="H",
            )
        )

        data = load_data(tmp_path, "air", data, year, start_date)
        data = load_data(tmp_path, "solar", data, year, start_date)
        data = load_data(tmp_path, "wind", data, year, start_date)
        data = load_data(tmp_path, "cloud", data, year, start_date)
        data = load_data(tmp_path, "sun", data, year, start_date)

        data.to_hdf(output_path, "weather", "w")

        LOG.info("Successfully created database for weather data.")


# Horizontal solar radiation is provided as hourly sum in Joule/cm^2
# (i.e., correct would be Joule/s/cm^2 * 3600s), but we want Watt/m^2
# for our PV models. Since 1*W = 1*J/s we first need to get back to
# J/s by dividing by 3600. Next, we want to convert from cm^2 to m^2,
# which is by multiplying with 0.0001, however, since cm^2 is in the
# divisor, we need to divide by that value (or multiply with the
# reciprocal). So the calculation we need to apply is
# 1 / (3.6*1e^3) * 1 / 1e^-4 = 1e^4 / (3.6*1e^3) = 1e^1 / 3.6
# which is equal to:
JOULE_TO_WATT = 10 / 3.6
DATA_COLS = {
    "air": [("TT_TU", "t_air_degree_celsius", 1)],
    "solar": [
        ("FD_LBERG", "dh_w_per_m2", JOULE_TO_WATT),
        ("FG_LBERG", "gh_w_per_m2", JOULE_TO_WATT),
    ],
    "wind": [("   F", "wind_v_m_per_s", 1), ("   D", "wind_dir_degree", 1)],
    "cloud": [(" V_N", "cloud_percent", 12.5)],
    "sun": [("SD_SO", "sun_hours_min_per_h", 1)],
}


def load_data(path, target, data, year, start_date):
    """Load data from a csv file and add them to a dataframe.

    Parameters
    ----------
    path: str
        The path of the folder containing a folder with csv files.
    target: str
        The name of the folder which contains csv files.
    data: pd.DataFrame
        The dataframe to which the content of the csv file will be
        added.
    year: int
        Since the year may change over the years, we pass it here.

    """
    fname = os.path.join(path, target)
    files = os.listdir(fname)
    data_file = [f for f in files if f.startswith("produkt")][0]
    fname = os.path.join(fname, data_file)

    if target == "solar":
        # We need a different parser for the solar dataset
        def parser(date):
            return datetime.strptime(date.split(":")[0], "%Y%m%d%H")

    else:

        def parser(date):
            return datetime.strptime(date, "%Y%m%d%H")

    # Read and prepare the content of the csv file.
    csv = pd.read_csv(
        fname, sep=";", index_col=1, parse_dates=[1], date_parser=parser
    )
    # We want to start at 2009 and go to the latest year.
    end_date = f"{year}-12-31 23:00:00"
    csv = csv.loc[start_date:end_date]
    # Some values might be missing to we fill them with the nearest
    # observations.
    index = pd.date_range(start=start_date, end=end_date, freq="H")
    try:
        csv = csv.reindex(index, method="nearest")
    except ValueError:
        # Something went wrong with indexing
        if len(index) == len(csv.index):
            csv.index = index
        else:
            csv = csv[~csv.index.duplicated()]
            csv.index = index
    # Now we can copy the content of the csv to the dataframe
    for src_col, tar_col, fac in DATA_COLS[target]:
        data[tar_col] = csv[src_col].values * fac

        if target == "air":
            # We need the day average air temperature for some of our
            # models.
            tar_col2 = f"day_avg_{tar_col}"
            data[tar_col2] = (
                csv[src_col].values.reshape(-1, 24).mean(axis=1).repeat(24)
            )
        if target == "solar":
            # Missing values are negative. We need to fill those
            missing = data[data[tar_col] < 0]
            data.loc[missing.index, tar_col] = np.nan
            data = data.interpolate()

    return data

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


def download_gen(data_path, tmp_path, if_necessary, force):
    """Download and convert timeseries from 50hertz.

    Those are generator timeseries for PV and windpower.

    """

    LOG.info("Preparing generator timeseries...")
    config = RuntimeConfig().data["generator_timeseries"][0]
    if if_necessary and not config.get("load_on_start", False):
        return
    output_path = os.path.abspath(os.path.join(data_path, config["name"]))

    if os.path.exists(output_path):
        LOG.debug("Found existing dataset at '%s'.", output_path)
        if not force:
            return

    pv_data = _download_and_read(config, tmp_path, "pv")
    wind_data = _download_and_read(config, tmp_path, "wind")
    data = pd.concat([pv_data, wind_data], axis=1)
    data.columns = ["solar_p_mw", "onshore_p_mw", "offshore_p_mw"]

    data.to_hdf(output_path, "sgen_pmw", "w")

    LOG.info("Successfully created database for solar and wind power.")


def _download_and_read(config, tmp_path, plant):

    data = pd.DataFrame()
    base_url = config["base_url"] + config[f"{plant}_url"] + config["postfix"]
    if plant == "pv":
        usecols = [0, 1, 3]
    elif plant == "wind":
        usecols = [0, 1, 4, 5]
    years = list(
        range(int(config["first_year"]), int(config["last_year"]) + 1)
    )
    # years = [2015]
    for year in years:
        index = pd.date_range(
            start=f"{year}-01-01 00:00:00",
            end=f"{year}-12-31 23:45:00",
            freq="900S",
        )
        url = base_url + f"{year}.csv"

        LOG.debug("Downloading '%s'...", url)
        fname = wget.download(url, out=tmp_path)
        click.echo()
        LOG.debug("Download complete")

        try:
            ydata = pd.read_csv(
                fname,
                sep=";",
                skip_blank_lines=True,
                skiprows=3,
                encoding="utf-16-le",
                parse_dates=[[0, 1]],
                dayfirst=True,
                decimal=",",
                usecols=usecols,
            )
        except Exception:
            LOG.debug(
                "Decoding file with 'utf-16-le' failed. "
                "Now trying 'utf-16-be'."
            )
            ydata = pd.read_csv(
                fname,
                sep=";",
                skip_blank_lines=True,
                skiprows=3,
                encoding="utf-16-be",
                parse_dates=[[0, 1]],
                dayfirst=True,
                decimal=",",
                usecols=usecols,
            )
        ydata.index = ydata["Datum_Von"]
        try:
            ydata.index = ydata.index.tz_localize(
                "Europe/Berlin", ambiguous="infer"
            )
        except Exception as exc:
            LOG.debug(
                "Got exception '%s' while localizing dataset."
                "Will try a different strategy.",
                exc,
            )
            ydata.index = ydata.index.tz_localize(
                "Europe/Berlin", ambiguous=True
            )

        ydata.index = (
            ydata.index.tz_convert("UTC") + pd.Timedelta("1 hour")
        ).tz_localize(None)
        data = pd.concat([data, ydata.reindex(index, method="nearest")])

    return data.drop("Datum_Von", axis=1)

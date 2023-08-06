import logging
import os

import pandas as pd
from midas.util.runtime_config import RuntimeConfig

LOG = logging.getLogger("midas.cli")


def download_simbench(data_path, tmp_path, if_necessary, force):
    """Download and convert simbench datasets.

    Simbench datasets are actually not downloaded but stored in the
    python package simbench. The datasets are extracted from the grid.

    """
    import simbench as sb

    LOG.info("Preparing Simbench datasets...")

    # We allow multiple datasets here
    for config in RuntimeConfig().data["simbench"]:
        if if_necessary and not config.get("load_on_start", False):
            continue
        output_path = os.path.abspath(os.path.join(data_path, config["name"]))
        simbench_code = output_path.rsplit(os.sep, 1)[1].split(".")[0]

        if os.path.exists(output_path):
            LOG.debug("Found existing datasets at '%s'.", output_path)
            if not force:
                continue
            else:
                LOG.debug("Loading profiles anyways...")
        else:
            LOG.debug(
                "No dataset found. Start loading '%s' profiles...",
                simbench_code,
            )

        grid = sb.get_simbench_net(simbench_code)
        profiles = sb.get_absolute_values(grid, True)
        load_map = pd.DataFrame(columns=["idx", "bus", "name"])
        sgen_map = pd.DataFrame(columns=["idx", "bus", "name"])
        storage_map = pd.DataFrame(columns=["idx", "bus", "name"])

        LOG.debug("Loading loads...")
        for idx in range(len(grid.load)):
            load = grid.load.loc[idx]
            load_map = pd.concat(
                [
                    load_map,
                    pd.DataFrame(
                        {
                            "idx": idx,
                            "bus": int(load["bus"]),
                            "name": load["name"],
                        },
                        index=[idx],
                    ),
                ],
                ignore_index=True,
            )
        LOG.debug("Loading sgens...")
        for idx in range(len(grid.sgen)):
            sgen = grid.sgen.loc[idx]
            sgen_map = pd.concat(
                [
                    sgen_map,
                    pd.DataFrame(
                        {
                            "idx": idx,
                            "bus": int(sgen["bus"]),
                            "name": sgen["name"],
                        },
                        index=[idx],
                    ),
                ],
                ignore_index=True,
            )
        LOG.debug("Loading storages...")
        for idx in range(len(grid.storage)):
            storage = grid.storage.loc[idx]
            storage_map = pd.concat(
                [
                    storage_map,
                    pd.DataFrame(
                        {
                            "idx": idx,
                            "bus": int(storage["bus"]),
                            "name": storage["name"],
                        },
                        index=[idx],
                    ),
                ],
                ignore_index=True,
            )
        LOG.debug("Creating database...")
        profiles[("load", "p_mw")].to_hdf(output_path, "load_pmw", "w")
        profiles[("load", "q_mvar")].to_hdf(output_path, "load_qmvar")
        profiles[("sgen", "p_mw")].to_hdf(output_path, "sgen_pmw")
        profiles[("storage", "p_mw")].to_hdf(output_path, "storage_pmw")

        for df in (load_map, sgen_map, storage_map):
            df["idx"] = df["idx"].astype(int)
            df["bus"] = df["bus"].astype(int)
        load_map.to_hdf(output_path, "load_default_mapping")
        sgen_map.to_hdf(output_path, "sgen_default_mapping")
        storage_map.to_hdf(output_path, "storage_default_mapping")

        LOG.info(
            "Successfully created database for Simbench grid '%s'.",
            simbench_code,
        )

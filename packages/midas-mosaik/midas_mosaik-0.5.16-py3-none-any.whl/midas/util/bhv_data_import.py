"""
This module contains a function to extract the profiles from
bremerhaven grids.

"""
import csv
import os
import numpy as np
import pandas as pd
from midas.core.powergrid.custom.bhv import build_grid

# from midas.tools import LOG
from midas.util.runtime_config import RuntimeConfig
from midas.util import LOG


def import_bhv_grid_data():
    RuntimeConfig().load()
    data_path = RuntimeConfig().paths["data_path"]
    tmp_path = os.path.abspath(os.path.join(data_path, "tmp_bhv"))

    output_path = os.path.abspath(
        os.path.join(data_path, "BremerhavenData.hdf5")
    )
    os.makedirs(tmp_path, exist_ok=True)

    # if os.path.exists(output_path):
    #     LOG.debug("Found existing datasets at %s.", output_path)
    #     return True

    LOG.debug("No dataset found. Start loading profiles ...")

    grid = build_grid()
    profiles = {}

    # Loads
    load_path = os.path.join(tmp_path, "org_load_year.csv")
    with open(load_path, "r") as f:
        reader = csv.reader(f)
        i = np.array(next(reader)).astype(int)

    profiles[("load", "p_mw")] = pd.read_csv(load_path, names=i, skiprows=1)

    # Sgens
    sgen_path = os.path.join(tmp_path, "org_sgen_year.csv")
    with open(sgen_path, "r") as f:
        reader = csv.reader(f)
        i = np.array(next(reader)).astype(int)

    profiles[("sgen", "p_mw")] = pd.read_csv(sgen_path, names=i, skiprows=1)

    load_map = pd.DataFrame(columns=["idx", "bus", "name"])
    sgen_map = pd.DataFrame(columns=["idx", "bus", "name"])

    for idx in range(len(grid.load)):
        load = grid.load.loc[idx]
        load_map = load_map.append(
            {"idx": idx, "bus": int(load["bus"]), "name": load["name"]},
            ignore_index=True,
        )
    for idx in range(len(grid.sgen)):
        sgen = grid.sgen.loc[idx]
        sgen_map = sgen_map.append(
            {"idx": idx, "bus": int(sgen["bus"]), "name": sgen["name"]},
            ignore_index=True,
        )
    for idx in range(profiles[("load", "p_mw")].shape[1]):
        print(
            f"{load_map['bus'][idx]}: [[H0, "
            f"{profiles[('load', 'p_mw')][idx].sum()/4:.3f}]]"
        )

    profiles[("load", "p_mw")].to_hdf(output_path, "load_pmw", "w")
    # profiles[("load", "q_mvar")].to_hdf(output_path, "load_qmvar")
    profiles[("sgen", "p_mw")].to_hdf(output_path, "sgen_pmw")
    load_map.to_hdf(output_path, "load_default_mapping")
    sgen_map.to_hdf(output_path, "sgen_default_mapping")

    LOG.debug("Load complete.")


import_bhv_grid_data()

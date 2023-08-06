"""This module contains the mosaik meta for the Commercial
Load Simulator.

As additional info, load peaks, total energy and average
power are listed for each model.

"""

MODELS = [
    "FullServiceRestaurant",
    "Hospital",
    "LargeHotel",
    "LargeOffice",
    "MediumOffice",
    "MidriseApartment",
    "OutPatient",
    "PrimarySchool",
    "QuickServiceRestaurant",
    "SecondarySchool",
    "SmallHotel",
    "SmallOffice",
    "StandaloneRetail",
    "StripMall",
    "SuperMarket",
    "Warehouse",
]

CONFIG = {
    "public": True,
    "params": ["scaling"],
    "attrs": ["cos_phi", "p_mw", "q_mvar"],
}

INFO = {
    "FullServiceRestaurant": {
        "p_max_mw": 0.137,
        "p_mwh_per_a": 601.044,
        "p_mean_mw": 0.069,
    },
    "Hospital": {
        "p_max_mw": 2.805,
        "p_mwh_per_a": 18106.771,
        "p_mean_mw": 2.067,
    },
    "LargeHotel": {
        "p_max_mw": 0.876,
        "p_mwh_per_a": 4574.578,
        "p_mean_mw": 0.522,
    },
    "LargeOffice": {
        "p_max_mw": 3.482,
        "p_mwh_per_a": 12137.960,
        "p_mean_mw": 1.386,
    },
    "MediumOffice": {
        "p_max_mw": 0.588,
        "p_mwh_per_a": 1445.567,
        "p_mean_mw": 0.165,
    },
    "MidriseApartment": {
        "p_max_mw": 0.133,
        "p_mwh_per_a": 454.896,
        "p_mean_mw": 0.052,
    },
    "OutPatient": {
        "p_max_mw": 0.630,
        "p_mwh_per_a": 2643.197,
        "p_mean_mw": 0.302,
    },
    "PrimarySchool": {
        "p_max_mw": 0.713,
        "p_mwh_per_a": 1705.623,
        "p_mean_mw": 0.195,
    },
    "QuickServiceRestaurant": {
        "p_max_mw": 0.077,
        "p_mwh_per_a": 357.569,
        "p_mean_mw": 0.041,
    },
    "SecondarySchool": {
        "p_max_mw": 2.529,
        "p_mwh_per_a": 6396.515,
        "p_mean_mw": 0.730,
    },
    "SmallHotel": {
        "p_max_mw": 0.270,
        "p_mwh_per_a": 1147.850,
        "p_mean_mw": 0.131,
    },
    "SmallOffice": {
        "p_max_mw": 0.039,
        "p_mwh_per_a": 122.119,
        "p_mean_mw": 0.014,
    },
    "StandaloneRetail": {
        "p_max_mw": 0.219,
        "p_mwh_per_a": 615.892,
        "p_mean_mw": 0.070,
    },
    "StripMall": {
        "p_max_mw": 0.197,
        "p_mwh_per_a": 541.853,
        "p_mean_mw": 0.062,
    },
    "SuperMarket": {
        "p_max_mw": 0.568,
        "p_mwh_per_a": 2343.541,
        "p_mean_mw": 0.268,
    },
    "Warehouse": {
        "p_max_mw": 0.186,
        "p_mwh_per_a": 481.342,
        "p_mean_mw": 0.055,
    },
}

META = {
    "type": "time-based",
    "models": {model: CONFIG for model in MODELS},
    "extra_methods": ["get_data_info"],
}

"""This module contains the meta for the household data simulator.

Eight 'low voltage lands' are present in the data with different
number of households. They are distributed as following:
    #name   #num        #house ids      #annual con  #avg con   #peak con
    Land 0:  41 houses (hids   0 -  40)  (130 MWh/a)  (14.8 kW)  (39.9 kW)
    Land 1: 139 houses (hids  41 - 179)  (661 MWh/a)  (75.5 kW) (516.6 kW)
    Land 2:  67 houses (hids 180 - 246)  (323 MWh/a)  (36.9 kW) (148.2 kW)
    Land 3:  57 houses (hids 247 - 303)  (223 MWh/a)  (25.5 kW)  (70.9 kW)
    Land 4: 169 houses (hids 304 - 472)  (741 MWh/a)  (84.6 kW) (277.9 kW)
    Land 5: 299 houses (hids 473 - 771) (1377 MWh/a) (157.2 kW) (413.7 kW)
    Land 6:  66 houses (hids 772 - 837)  (309 MWh/a)  (35.3 kW)  (97.5 kW)
    Land 7: 103 houses (hids 838 - 940)  (421 MWh/a)  (48.1 kW) (146.4 kW)

Resulting in 941 households or 8 lands in total.

"""

INFO = {
    "Land0": {
        "num_houses": 41,
        "first_hid": 0,
        "last_hid": 40,
        "p_mwh_per_a": 130,
        "average_consumption": 0.0148,
        "peak_mw": 0.0399,
    },
    "Land1": {
        "num_houses": 139,
        "first_hid": 41,
        "last_hid": 179,
        "p_mwh_per_a": 661,
        "average_consumption": 0.5166,
        "peak_mw": 0.0755,
    },
    "Land2": {
        "num_houses": 67,
        "first_hid": 180,
        "last_hid": 246,
        "p_mwh_per_a": 323,
        "average_consumption": 0.0369,
        "peak_mw": 0.1482,
    },
    "Land3": {
        "num_houses": 57,
        "first_hid": 247,
        "last_hid": 303,
        "p_mwh_per_a": 223,
        "average_consumption": 0.0255,
        "peak_mw": 0.0709,
    },
    "Land4": {
        "num_houses": 169,
        "first_hid": 304,
        "last_hid": 472,
        "p_mwh_per_a": 741,
        "average_consumption": 0.0846,
        "peak_mw": 0.2279,
    },
    "Land5": {
        "num_houses": 299,
        "first_hid": 473,
        "last_hid": 771,
        "p_mwh_per_a": 1377,
        "average_consumption": 0.1572,
        "peak_mw": 0.4137,
    },
    "Land6": {
        "num_houses": 66,
        "first_hid": 772,
        "last_hid": 837,
        "p_mwh_per_a": 309,
        "average_consumption": 0.0353,
        "peak_mw": 0.0975,
    },
    "Land7": {
        "num_houses": 103,
        "first_hid": 838,
        "last_hid": 940,
        "p_mwh_per_a": 421,
        "average_consumption": 0.0481,
        "peak_mw": 0.1464,
    },
}

META = {
    "type": "time-based",
    "models": {
        "Household": {
            "public": True,
            "params": [
                "scaling",
                "eidx",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["cos_phi", "p_mw", "q_mvar"],
        },
        "Land": {
            "public": True,
            "params": [
                "scaling",
                "eidx",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["cos_phi", "p_mw", "q_mvar"],
        },
    },
    "extra_methods": ["get_data_info"],
}

META = {
    "type": "time-based",
    "models": {
        "PV": {
            "public": True,
            "params": [
                "p_peak_mw",
                "scaling",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
        "Wind": {
            "public": True,
            "params": [
                "p_peak_mw",
                "scaling",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
        "WindOffshore": {
            "public": True,
            "params": [
                "p_peak_mw",
                "scaling",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
    },
    "extra_methods": ["get_data_info"],
}

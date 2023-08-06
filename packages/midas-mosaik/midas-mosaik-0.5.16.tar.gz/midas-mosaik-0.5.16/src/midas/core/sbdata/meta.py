META = {
    "type": "time-based",
    "models": {
        "Load": {
            "public": True,
            "params": [
                "scaling",
                "eidx",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
        "Sgen": {
            "public": True,
            "params": [
                "scaling",
                "eidx",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
        "Storage": {
            "public": True,
            "params": [
                "scaling",
                "eidx",
                "interpolate",
                "randomize_data",
                "randomize_cos_phi",
            ],
            "attrs": ["p_mw", "q_mvar", "cos_phi"],
        },
    },
    "extra_methods": ["get_data_info"],
}

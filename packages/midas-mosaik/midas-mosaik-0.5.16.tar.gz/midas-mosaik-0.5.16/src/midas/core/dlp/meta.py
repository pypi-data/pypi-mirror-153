"""This module contains the meta for the default load profile
simulator.

All profiles are normalized to an annual consumption of 1000 kWh/a.

"""


MODELS = [
    "DefaultLoadH0",  # Households
    "DefaultLoadG0",  # Commercial (general)
    "DefaultLoadG1",  # Commercial (weekday 8-18)
    "DefaultLoadG2",  # Commercial (evening)
    "DefaultLoadG3",  # Commercial (continuous)
    "DefaultLoadG4",  # Commercial (Shop/Barber)
    "DefaultLoadG5",  # Commercial (Bakery)
    "DefaultLoadG6",  # Commercial (weekend)
    "DefaultLoadL0",  # Agriculture (general)
    "DefaultLoadL1",  # Acriculture (milk/animal breeding)
    "DefaultLoadL2",  # Agriculture (other)
]

CONFIG = {
    "public": True,
    "params": [
        "p_mwh_per_a",
        "interpolate",
        "randomize_data",
        "randomize_cos_phi",
    ],
    "attrs": ["p_mw", "q_mvar", "cos_phi"],
}

META = {
    "type": "time-based",
    "models": {model: CONFIG for model in MODELS},
    "extra_methods": ["get_data_info"],
}

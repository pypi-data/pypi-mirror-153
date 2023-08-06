"""This module contains the mosaik_api simulator meta for the
grid operator simulator.
"""


META = {
    "type": "time-based",
    "models": {
        "GOA": {
            "public": True,
            "params": ["params"],
            "any_inputs": True,
            "attrs": [
                "inbox",  # send messages to GOA
                "outbox",  # receive messages from GOA
                "health",  # Grid state
                "error",  # Miss-estimation of the GOA
                "max_overvoltage",
                "min_undervoltage",
                "num_voltage_violations",
                "grid",
            ],
        }
    },
}

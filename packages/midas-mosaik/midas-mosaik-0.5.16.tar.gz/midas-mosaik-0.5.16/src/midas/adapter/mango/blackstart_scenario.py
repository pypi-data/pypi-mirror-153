# scenario.py
"""
Simple example to test the connection of market and midas

"""
import sys
import logging

import mosaik
from midas.adapter.pysimmods.presets import get_presets

# Set Logging Config
# logging.basicConfig(stream=sys.stderr, level=logging.INFO)


# Sim config. and other parameters
SIM_CONFIG = {
    "Powergrid": {"python": "midas.core:PandapowerSimulator"},
    "Households": {"python": "midas.core:SmartNordDataSimulator"},
    "UnitMods": {"python": "pysimmods.mosaik:FlexibilitySimulator"},
    "Weather": {"python": "midas.core:WeatherDataSimulator"},
    "Operator": {"python": "midas.core:GridOperatorSimulator"},
    "Collector": {
        "python": "midas.util:Collector",
    },
    "MAS": {
        "python": "blackstart.blackstart_mas.mango_mosaik_api:MangoSimulator",
    },
}
END = 31 * 24 * 3600
START_DATE = "2017-05-01 12:00:00+0100"
STEP_SIZE = 15 * 60
SCHEDULE_LENGTH = 3

world = mosaik.World(SIM_CONFIG, mosaik_config={"addr": ("127.0.0.1", 5557)})

grid_params = {
    "sim_name": "Powergrid",
    "gridfile": "blackstartgrid",
    "static": True,
    "step_size": STEP_SIZE,
}

household_params = {
    "sim_name": "Households",
    "step_size": STEP_SIZE,
    "start_date": START_DATE,
    "cos_phi": 0.9,
    "interpolate": False,
    "randomize_data": False,
    "randomize_cos_phi": False,
    "seed": 0,
    "data_path": "C:\\Users\\sstark\\.midas\\midas_data",
    "household_mapping": {
        "Land-0": {"scaling": 0.15, "eidx": 0, "bus": 0},
        "Land-1": {"scaling": 0.65, "eidx": 3, "bus": 1},
    },
}

weather_params = {
    "sim_name": "Weather",
    "step_size": STEP_SIZE,
    "start_date": START_DATE,
    "seed": 1,
    "weather_mapping": {
        "Weather": [{"interpolate": True, "randomize": False}],
        "WeatherForecast": [
            {
                "interpolate": True,
                "randomize": False,
                "forecast_error": 0,
                "forecast_horizon_hours": SCHEDULE_LENGTH * 0.5,
            }
        ],
    },
    "data_path": "C:\\Users\\sstark\\.midas\\midas_data\\",
    "filename": "WeatherBre2009-2019.hdf5",
}

unitmods_params = {
    "sim_name": "UnitMods",
    "step_size": STEP_SIZE,
    "start_date": START_DATE,
    "provide_flexibilities": True,
    "flexibility_horizon_hours": SCHEDULE_LENGTH * 0.25,
    "num_schedules": 10,
    "unit": "mw",
    "pv_mapping": {
        "Photovoltaic-0": {
            "p_peak_mw": 0.051751,
            "q_control": "q_set",
            "bus": 1,
        },
        "Photovoltaic-1": {
            "p_peak_mw": 0.09195,
            "q_control": "q_set",
            "bus": 2,
        },
        "Photovoltaic-2": {"p_peak_mw": 0.014, "q_control": "q_set", "bus": 0},
        "Photovoltaic-3": {"p_peak_mw": 0.014, "q_control": "q_set", "bus": 0},
    },
}

goa_params = {
    "sim_name": "Operator",
    "step_size": STEP_SIZE,
    "goa_mapping": {
        "simple_four_bus_system": {
            "forecast_horizon": 0.25,
            "start_date": START_DATE,
            "grid_busload_sensor": False,
            "grid_busvm_sensor": True,
            "grid_load_sensor": True,
            "grid_sgen_sensor": False,
            "unit_load_sensor": False,
            "unit_load_forecast_sensor": False,
            "unit_sgen_sensor": True,
            "unit_sgen_forecast_sensor": True,
            "gridfile": "simple_four_bus_system",
            "run_forecast": True,
            "forecast_horizon_hours": 0.25,
            "house_mapping": dict(),
            "land_mapping": dict(),
            "overvoltage_pu": 1.04,
            "undervoltage_pu": 0.96,
            "der_mapping": {
                "Pysimmods-0.Photovoltaic-0": {
                    "bus": 2,
                    "p_mw": 0.05175,
                    "type": "sgen",
                },
                "Pysimmods-0.Photovoltaic-1": {
                    "bus": 2,
                    "p_mw": 0.014,
                    "type": "sgen",
                },
                "Pysimmods-0.Photovoltaic-2": {
                    "bus": 3,
                    "p_mw": 0.09195,
                    "type": "sgen",
                },
                "Pysimmods-0.Photovoltaic-3": {
                    "bus": 3,
                    "p_mw": 0.014,
                    "type": "sgen",
                },
            },
            "load_mapping": {
                2: [["land", 1659.8636152460517]],
                3: [["land", 2497.3919667577566]],
            },
        }
    },
}

mas_params = {
    "sim_name": "MAS",
    "step_size": STEP_SIZE,
    "host": "localhost",
    "port": 5556,
    "check_inbox_interval": 0.1,
    "holon_topology": {
        "agent8": [
            "BlackstartSwitchAgent-6",
            "BlackstartSwitchAgent-7",
            "BlackstartSwitchAgent-8",
        ],
        "agent3": ["BlackstartUnitAgent-2", "BlackstartUnitAgent-3"],
        "agent1": ["BlackstartUnitAgent-1", "BlackstartUnitAgent-5"],
        "agent2": ["BlackstartUnitAgent-0", "BlackstartUnitAgent-4"],
    },
    "der_mapping": {
        "BlackstartUnitAgent-0": "Pysimmods-0.Photovoltaic-0",
        "BlackstartUnitAgent-1": "Pysimmods-0.Photovoltaic-1",
        "BlackstartUnitAgent-2": "Pysimmods-0.Photovoltaic-2",
        "BlackstartUnitAgent-3": "Pysimmods-0.Photovoltaic-3",
    },
    "load_mapping": {"BlackstartUnitAgent-4": 0, "BlackstartUnitAgent-5": 1},
    "switch_mapping": {
        "BlackstartSwitchAgent-6": {
            "own_bus": 1,
            "adjacent_switches": {
                "switch-0": {"other_bus": 2, "access": True}
            },
            "assigned_speaker": "BlackstartUnitAgent-2",
        },
        "BlackstartSwitchAgent-7": {
            "own_bus": 2,
            "adjacent_switches": {
                "switch-0": {"other_bus": 1, "access": False},
                "switch-1": {"other_bus": 3, "access": True},
            },
            "assigned_speaker": "BlackstartUnitAgent-0",
        },
        "BlackstartSwitchAgent-8": {
            "own_bus": 3,
            "adjacent_switches": {
                "switch-1": {"other_bus": 2, "access": False}
            },
            "assigned_speaker": "BlackstartUnitAgent-1",
        },
    },
    "bc_agent_id": "BlackstartSwitchAgent-7",
    "schedule_length": SCHEDULE_LENGTH,
    "start_date": START_DATE,
}


# Start Simulators
grid_sim = world.start(**grid_params)
household_sim = world.start(**household_params)
weather_sim = world.start(**weather_params)
unit_sim = world.start(**unitmods_params)
# goa_sim = world.start(**goa_params)
mas = world.start(**mas_params)


# Start models
grid_model = grid_sim.Grid(gridfile=grid_params["gridfile"])
weather = weather_sim.WeatherCurrent(
    **weather_params["weather_mapping"]["Weather"][0]
)
weather_fc = weather_sim.WeatherForecast(
    **weather_params["weather_mapping"]["WeatherForecast"][0]
)
# goa = goa_sim.GOA(params=goa_params['goa_mapping']['simple_four_bus_system'])

load_models = []
for load, load_data in household_params["household_mapping"].items():
    load = household_sim.Land(
        scaling=load_data["scaling"], eidx=load_data["eidx"]
    )
    load_models.append(load)

pv_models = []
for pv_id, pv_data in unitmods_params["pv_mapping"].items():
    pv_params = get_presets(
        "PV", p_peak_mw=pv_data["p_peak_mw"], q_control=pv_data["q_control"]
    )
    pv = unit_sim.Photovoltaic(params=pv_params[0], inits=pv_params[1])
    pv_models.append(pv)

unit_agents = []
for unit_agent in mas_params["der_mapping"].keys():
    blackstart_unit_agent = mas.BlackstartUnitAgent(
        check_inbox_interval=mas_params["check_inbox_interval"]
    )
    unit_agents.append(blackstart_unit_agent)

load_agents = []
for unit_agent in mas_params["load_mapping"].keys():
    blackstart_unit_agent = mas.BlackstartUnitAgent(
        check_inbox_interval=mas_params["check_inbox_interval"]
    )
    load_agents.append(blackstart_unit_agent)

switch_agents = []
for switch_agent in mas_params["switch_mapping"].keys():
    blackstart_switch_agent = mas.BlackstartSwitchAgent(
        check_inbox_interval=mas_params["check_inbox_interval"]
    )
    switch_agents.append(blackstart_switch_agent)

# Connect models
loads = [e for e in grid_model.children if e.type == "Load"]
sgens = [e for e in grid_model.children if e.type == "Sgen"]
switches = [e for e in grid_model.children if e.type == "Switch"]
attrs = ["p_mw", "q_mvar"]
s_attrs = attrs + ["schedule"]
w_attrs = ["bh_w_per_m2", "dh_w_per_m2", "t_air_deg_celsius"]
wfc_attrs = ["forecast_{}".format(a) for a in w_attrs]

# Define connections for loads
for load in load_models:
    bus_number = household_params["household_mapping"][load.eid]["bus"]
    world.connect(load, loads[bus_number], *attrs)

# Define connections for pv models
for pv in pv_models:
    world.connect(weather, pv, *w_attrs)
    world.connect(weather_fc, pv, *wfc_attrs)
    bus_number = unitmods_params["pv_mapping"][pv.eid]["bus"]
    world.connect(pv, sgens[bus_number], *attrs)

# Define connections for unit agents
for pv, unit_agent in zip(pv_models, unit_agents):
    world.connect(pv, unit_agent, "flexibilities")
    world.connect(
        unit_agent,
        pv,
        "schedule",
        time_shifted=True,
        initial_data={"schedule": None},
    )

# Define connections for load agents
for load, load_agent in zip(load_models, load_agents):
    bus_number = household_params["household_mapping"][load.eid]["bus"]
    world.connect(loads[bus_number], load_agent, "p_mw")

# Define connections for switch agents
for switch_agent in switch_agents:
    for switch in mas_params["switch_mapping"][switch_agent.eid][
        "adjacent_switches"
    ].keys():
        switch_id_components = switch.split("-")
        switch_number = int(switch_id_components[1])
        world.connect(
            switches[switch_number], switch_agent, ("closed", "switch_state")
        )
        world.connect(
            switch_agent,
            switches[switch_number],
            ("switch_state", "closed"),
            time_shifted=True,
            initial_data={"switch_state": False},
        )

# Load and unit mods to goa
# world.connect(loads[0], goa, *attrs)
# world.connect(loads[1], goa, *attrs)
# world.connect(pv0, goa, *s_attrs)
# world.connect(pv1, goa, *s_attrs)
# world.connect(pv2, goa, *s_attrs)
# world.connect(pv3, goa, *s_attrs)


# Run simulation
world.run(until=END)

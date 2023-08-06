"""This module contains the mosaik meta for the weather simulator."""


META = {
    "type": "time-based",
    "models": {
        "WeatherCurrent": {
            "public": True,
            "params": [
                "data_path",
                "start_date",
                "interpolate",
                "randomize",
                "seed",
                "block_mode",
                "frame",
            ],
            "attrs": [
                "now",
                "bh_w_per_m2",
                "dh_w_per_m2",
                "t_air_deg_celsius",
                "day_avg_t_air_deg_celsius",
            ],
        },
        "WeatherForecast": {
            "public": True,
            "params": [
                "data_path",
                "start_date",
                "interpolate",
                "forecast_error",
                "seed",
                "randomize",
                "forecast_horizon_hours",
                "block_mode",
                "frame",
            ],
            "attrs": [
                "now",
                "forecast_horizon_hours",
                "forecast_bh_w_per_m2",
                "forecast_dh_w_per_m2",
                "forecast_t_air_deg_celsius",
                "forecast_day_avg_t_air_deg_celsius",
            ],
        },
    },
}

"""In this module, the midas mv grid is defined and configured."""
import pandapower as pp
import pandapower.networks as pn


def build_grid(**kwargs):
    """Create the default midas mv grid."""
    # DERs are added manually
    grid = pn.create_cigre_network_mv(with_der="all")
    grid.load = grid.load[0:0]
    grid.sgen = grid.sgen[0:0]
    grid.storage = grid.storage[0:0]

    load_res = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    load_com = [13, 14]
    sgen = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]
    storage = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]
    tap_changer = {
        0: {"min": -10, "max": 10, "mid": 0, "ts_size": 0.625},
        1: {"min": -10, "max": 10, "mid": 0, "ts_size": 0.625},
    }

    for bus_id in load_res:
        pp.create_load(
            grid,
            bus=bus_id,
            p_mw=0.0,
            q_mvar=0.0,
            name="LOAD_AGGRLV_{}".format(bus_id),
            scaling=1.0,
            in_service=True,
            controllable=False,
        )

    for bus_id in load_com:
        pp.create_load(
            grid,
            bus=bus_id,
            p_mw=0.0,
            q_mvar=0.0,
            name="LOAD_COMM_{}".format(bus_id),
            scaling=1.0,
            in_service=True,
            controllable=False,
        )

    for bus_id in sgen:
        pp.create_sgen(
            grid,
            bus=bus_id,
            p_mw=0.0,
            q_mvar=0.0,
            name="SGEN_{}".format(bus_id),
            scaling=1.0,
            type=None,
            in_service=True,
            controllable=False,
        )

    for bus_id in storage:
        pp.create_storage(
            grid,
            bus=bus_id,
            p_mw=0.0,
            max_e_mwh=1,
            q_mvar=0.0,
            name="STORAGE_{}".format(bus_id),
            scaling=1.0,
            type=None,
            in_service=True,
            controllable=False,
        )

    for trafo_id, trafo_config in tap_changer.items():
        grid.trafo.tap_side[trafo_id] = "lv"
        grid.trafo.tap_min[trafo_id] = trafo_config["min"]
        grid.trafo.tap_max[trafo_id] = trafo_config["max"]
        grid.trafo.tap_neutral[trafo_id] = trafo_config["mid"]
        grid.trafo.tap_step_percent[trafo_id] = trafo_config["ts_size"]

    return grid

import pandapower as pp
import pandapower.networks as pn


def build_grid():
    """Create the default midas mv grid."""
    # DERs are added manually

    grid = pn.simple_four_bus_system()
    pp.create_switch(grid, 1, 2, "b", type="CB", closed=False)
    pp.create_switch(grid, 2, 3, "b", type="CB", closed=False)

    grid.sgen = grid.sgen[0:0]

    sgen = [1, 2, 3]

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

    return grid

"""In this module, the midas lv grid is defined and configured."""
import pandapower as pp
import pandapower.networks as pn


def build_grid(**kwargs):

    grid = pn.create_cigre_network_lv()
    grid.load = grid.load[0:0]

    load_res = [2, 12, 16, 17, 18, 19]
    load_ind = [22]
    load_com = [24, 35, 36, 37, 40, 41, 42, 43]
    sgen = load_res + load_ind + load_com
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
            name="LOAD_RES_{}".format(bus_id),
            scaling=1.0,
            in_service=True,
            controllable=False,
        )

    for bus_id in load_ind:
        pp.create_load(
            grid,
            bus=bus_id,
            p_mw=0.0,
            q_mvar=0.0,
            name="LOAD_IND_{}".format(bus_id),
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
            name="LOAD_COM_{}".format(bus_id),
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

    for trafo_id, trafo_config in tap_changer.items():
        grid.trafo.tap_side[trafo_id] = "lv"
        grid.trafo.tap_min[trafo_id] = trafo_config["min"]
        grid.trafo.tap_max[trafo_id] = trafo_config["max"]
        grid.trafo.tap_neutral[trafo_id] = trafo_config["mid"]
        grid.trafo.tap_step_percent[trafo_id] = trafo_config["ts_size"]

    return grid

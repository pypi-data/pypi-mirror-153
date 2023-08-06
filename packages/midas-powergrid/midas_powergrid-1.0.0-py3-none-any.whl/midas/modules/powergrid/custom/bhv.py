"""Creates a pandapower network of the BHV power grid."""

import pandapower as pp
from midas.util.compute_q import compute_q


def build_grid(
    invert_geodata: bool = False, use_extension: bool = False
) -> pp.pandapowerNet:
    """Return a pandapower network of BHV based on FLOSM map data.

    Returns
    -------
    pp.pandapowerNet
        powergrid model of Bremerhaven.

    """
    grid = pp.create_empty_network()
    buses = dict()
    _create_line_types(grid)
    _create_buses_hv(grid, buses)
    _create_lines_hv(grid, buses)
    _create_overseas(grid, buses)
    _create_lehe(grid, buses)
    _create_windpark_speckenbuettel(grid, buses)
    _create_windpark_multibrid(grid, buses)
    _create_geestemuende(grid, buses)
    _create_city(grid, buses, use_extension)
    _create_windpark_lehe(grid, buses)
    _create_klinikum_reinkenheide(grid, buses)
    _create_schiffdorferdamm(grid, buses)
    _create_eisarena(grid, buses)
    _create_mitte(grid, buses)
    _create_leherheide(grid, buses)
    _create_wulsdorf(grid, buses)
    _create_abfall(grid, buses, use_extension)
    _create_surheide(grid, buses)
    _create_klinikum_buergerpark(grid, buses)
    _create_innenstadt(grid, buses)
    _create_zoo(grid, buses)
    _create_klinikum_mitte(grid, buses)
    _create_fischereihafen(grid, buses)
    _create_geestemuende_v2(grid, buses)
    _create_bremerhaven_sued(grid, buses)

    if invert_geodata:
        _invert_geodata(grid)

    return grid


def _create_line_types(grid):
    """Add line data based on CIGRE."""
    line_data = {
        "c_nf_per_km": 151.1749,
        "r_ohm_per_km": 0.501,
        "x_ohm_per_km": 0.716,
        "max_i_ka": 0.145,
        "type": "cs",
    }
    pp.create_std_type(grid, line_data, name="CABLE_CIGRE_MV", element="line")

    line_data = {
        "c_nf_per_km": 10.09679,
        "r_ohm_per_km": 0.510,
        "x_ohm_per_km": 0.366,
        "max_i_ka": 0.195,
        "type": "ol",
    }
    pp.create_std_type(grid, line_data, name="OHL_CIGRE_MV", element="line")

    line_data = {
        "c_nf_per_km": 0.0,
        "r_ohm_per_km": 0.162,
        "x_ohm_per_km": 0.0832,
        "max_i_ka": 1.0,
        "type": "cs",
    }
    pp.create_std_type(grid, line_data, name="UG1", element="line")


def _create_buses_hv(net, buses):
    """Instantiate 110 kV buses based on FLOSM geodata"""
    # Nordenham Blexen
    # https://www.openstreetmap.org/way/37932525
    buses["hv_bus_0"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Umspannwerk Blexen/hv_bus_0",
        type="b",
        geodata=(53.528571, 8.545029),
    )

    buses["ov_hv_0"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Überseehafen, Wurster Straße/ov_hv_0",
        type="b",
        geodata=(53.597675, 8.538051),
    )

    # https://www.openstreetmap.org/way/107058988
    buses["hv_bus_2"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Überseehafen, Grauwallring/hv_bus_2",
        type="b",
        geodata=(53.596534, 8.571337),
    )
    # Nord - Leherheide
    # https://www.openstreetmap.org/way/41831269
    buses["hv_bus_3"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Leherheide, Debstedter Weg/hv_bus_3",
        type="b",
        geodata=(53.602492, 8.621490),
    )
    # Mitte - Lehe
    # https://www.openstreetmap.org/way/111990696
    buses["hv_bus_4"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Lehe, Am Wischhacker/hv_bus_4",
        type="b",
        geodata=(53.560075, 8.601626),
    )
    # Mitte - Schiffdorferdamm
    # https://www.openstreetmap.org/node/1195969029
    buses["hv_bus_5"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Schiffdorferdamm, Johann-Wichels-Weg/hv_bus_5",
        type="b",
        geodata=(53.539539, 8.629766),
    )
    # Süd - Wulsdorf
    # https://www.openstreetmap.org/way/117216153
    buses["hv_bus_6"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Surheide, Midgardweg/hv_bus_6",
        type="b",
        geodata=(53.510913, 8.620990),
    )
    # https://www.openstreetmap.org/way/36903323
    buses["hv_bus_7"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Wulsdorf, Daimlerstraße/hv_bus_7",
        type="b",
        geodata=(53.515625, 8.603047),
    )
    # https://www.openstreetmap.org/way/370348954
    buses["hv_bus_8"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Wulsdorf, Hackfahrel/hv_bus_8",
        type="b",
        geodata=(53.500857, 8.595032),
    )
    # Mitte - Kaiserhafen Eins
    # https://www.openstreetmap.org/node/6470789771
    buses["hv_bus_9"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Kaiserhafen Eins, Lohmannstraße/hv_bus_9",
        type="b",
        geodata=(53.555433, 8.560829),
    )
    # Mitte - Mitte
    # https://www.openstreetmap.org/way/252421504
    buses["hv_bus_10"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Mitte, Barkhausenstraße/hv_bus_10",
        type="b",
        geodata=(53.548044, 8.572743),
    )
    # Mitte - Geestemünde-Nord
    # https://www.openstreetmap.org/node/2335975543
    buses["hv_bus_11"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Geestemünde-Nord, Mozartstraße/hv_bus_11",
        type="b",
        geodata=(53.543114, 8.593258),
    )
    # https://www.openstreetmap.org/way/292524887
    buses["hv_bus_12"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Handelshafen, Klußmannstraße/hv_bus_12",
        type="b",
        geodata=(53.532868, 8.583921),
    )


def _create_lines_hv(net, buses):
    """
    Connect buses based on FLOSM power pole geodata
    """
    pp.create_line(
        net,
        from_bus=buses["ov_hv_0"],
        to_bus=buses["hv_bus_3"],
        length_km=9.96,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            (53.597675, 8.538051),  # from_bus
            (53.598356, 8.538919),
            (53.598247, 8.540951),
            (53.598018, 8.544490),
            (53.598765, 8.548444),
            (53.599555, 8.552571),
            (53.600899, 8.555071),
            (53.602217, 8.557474),
            (53.601375, 8.561635),
            (53.600501, 8.565854),
            (53.599581, 8.570314),
            (53.598819, 8.573943),
            (53.600817, 8.577339),
            (53.602896, 8.580954),
            (53.604454, 8.583614),
            (53.606914, 8.584638),
            (53.609244, 8.585576),
            (53.611986, 8.586714),
            (53.614576, 8.587774),
            (53.617890, 8.589153),
            (53.620520, 8.592915),
            (53.623156, 8.596658),
            (53.623434, 8.601912),
            (53.623702, 8.606821),
            (53.622806, 8.611870),
            (53.622035, 8.616256),
            (53.621311, 8.620426),
            (53.620383, 8.625599),
            (53.617257, 8.628189),
            (53.614890, 8.628631),
            (53.611929, 8.629195),
            (53.609874, 8.627677),
            (53.607835, 8.626151),
            (53.605222, 8.624216),
            (53.602965, 8.622550),
            (53.602492, 8.621490),  # to_bus
        ],
    )
    buses["c_hv_0"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Langen Bremerhaven Nord/c_hv_0",
        type="b",
        geodata=(53.60537, 8.6241),
    )
    # hv bzs 5
    pp.create_line(
        net,
        from_bus=buses["hv_bus_5"],
        to_bus=buses["c_hv_0"],
        length_km=2,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            _bus_geo(net, buses["hv_bus_5"]),
            _bus_geo(net, buses["c_hv_0"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_3"],
        to_bus=buses["hv_bus_4"],
        length_km=10.08,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            (53.602492, 8.621490),  # from_bus
            (53.602718, 8.623000),
            (53.604402, 8.625998),
            (53.604395, 8.630796),
            (53.604373, 8.636187),
            (53.604380, 8.641501),
            (53.604358, 8.647265),
            (53.604344, 8.651771),
            (53.604326, 8.657091),
            (53.601005, 8.656239),
            (53.597519, 8.655461),
            (53.593976, 8.654641),
            (53.590606, 8.653878),
            (53.586869, 8.653052),
            (53.583463, 8.652269),
            (53.580202, 8.651513),
            (53.576792, 8.650749),
            (53.573688, 8.650031),
            (53.570436, 8.649304),
            (53.567128, 8.648553),
            (53.564986, 8.645384),
            (53.562641, 8.641858),
            (53.560282, 8.638338),
            (53.558868, 8.634269),
            (53.558998, 8.632271),
            (53.559300, 8.627266),
            (53.559599, 8.622411),
            (53.559884, 8.617658),
            (53.560164, 8.612923),
            (53.560471, 8.607664),
            (53.560258, 8.602617),
            (53.560075, 8.601626),  # to_bus
        ],
    )
    buses["c_hv_1"] = pp.create_bus(
        net,
        vn_kv=110,
        name="110 kV Lehe/c_hv_1",
        type="b",
        geodata=(53.563454, 8.601023),
    )

    pp.create_line(
        net,
        from_bus=buses["hv_bus_4"],
        to_bus=buses["c_hv_1"],
        length_km=2,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            _bus_geo(net, buses["hv_bus_4"]),
            _bus_geo(net, buses["c_hv_1"]),
        ],
    )

    pp.create_line(
        net,
        from_bus=buses["hv_bus_4"],
        to_bus=buses["hv_bus_6"],
        length_km=7.67,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            (53.560075, 8.601626),  # from_bus
            (53.559832, 8.603161),
            (53.560022, 8.607649),
            (53.559732, 8.612116),
            (53.559403, 8.617469),
            (53.559058, 8.622976),
            (53.558708, 8.628350),
            (53.558359, 8.633821),
            (53.555374, 8.635590),
            (53.552654, 8.634057),
            (53.549372, 8.632231),
            (53.546590, 8.630663),
            (53.543353, 8.628849),
            (53.540546, 8.627274),
            (53.537848, 8.625771),
            (53.535248, 8.624267),
            (53.532523, 8.622777),
            (53.530186, 8.621398),
            (53.527832, 8.620009),
            (53.524874, 8.618278),
            (53.521592, 8.620127),
            (53.518242, 8.619302),
            (53.515789, 8.618684),
            (53.513301, 8.618067),
            (53.512171, 8.619612),
            (53.510913, 8.620990),  # to_bus
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_7"],
        to_bus=buses["hv_bus_6"],
        length_km=1.27,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            (53.515625, 8.603047),  # from_bus
            (53.515551, 8.603400),
            (53.515384, 8.605437),
            (53.515142, 8.607763),
            (53.514873, 8.610541),
            (53.513592, 8.613797),
            (53.512418, 8.616813),
            (53.511601, 8.618849),
            (53.510913, 8.620990),  # to_bus
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_6"],
        to_bus=buses["hv_bus_8"],
        length_km=4.41,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            (53.510913, 8.620990),  # from_bus
            (53.509886, 8.621935),
            (53.507894, 8.626273),
            (53.505894, 8.627324),
            (53.503911, 8.624381),
            (53.501855, 8.621282),
            (53.499356, 8.617602),
            (53.497031, 8.614142),
            (53.494530, 8.610403),
            (53.492585, 8.607504),
            (53.490529, 8.603516),
            (53.491313, 8.599338),
            (53.493578, 8.597337),
            (53.496759, 8.596275),
            (53.499637, 8.595319),
            (53.500857, 8.595032),  # to_bus
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_3"],
        to_bus=buses["hv_bus_6"],
        length_km=13.55,
        std_type="243-AL1/39-ST1A 110.0",
        geodata=[
            (53.602492, 8.621490),  # from_bus
            (53.602762, 8.622957),
            (53.602762, 8.622957),
            (53.604383, 8.630787),
            (53.604381, 8.636158),
            (53.604368, 8.641503),
            (53.604368, 8.647260),
            (53.604337, 8.651789),
            (53.604326, 8.656977),
            (53.526075, 8.639376),
            (53.524229, 8.635588),
            (53.523043, 8.633121),
            (53.521484, 8.629963),
            (53.519890, 8.626781),
            (53.518433, 8.623689),
            (53.516985, 8.620731),
            (53.515793, 8.618661),
            (53.513261, 8.617566),
            (53.511989, 8.619317),
            (53.510913, 8.620990),  # to_bus
        ],
    )

    # Connect remaining HV buses with hypothetical underground lines
    pp.create_line(
        net,
        from_bus=buses["ov_hv_0"],
        to_bus=buses["hv_bus_2"],
        length_km=2.19,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["ov_hv_0"]),
            _bus_geo(net, buses["hv_bus_2"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_4"],
        to_bus=buses["hv_bus_5"],
        length_km=2.9,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_4"]),
            _bus_geo(net, buses["hv_bus_5"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["ov_hv_0"],
        to_bus=buses["hv_bus_9"],
        length_km=4.93,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["ov_hv_0"]),
            _bus_geo(net, buses["hv_bus_9"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_9"],
        to_bus=buses["hv_bus_10"],
        length_km=1.14,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_9"]),
            _bus_geo(net, buses["hv_bus_10"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_10"],
        to_bus=buses["hv_bus_11"],
        length_km=1.47,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_10"]),
            _bus_geo(net, buses["hv_bus_11"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_11"],
        to_bus=buses["hv_bus_12"],
        length_km=1.3,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_11"]),
            _bus_geo(net, buses["hv_bus_12"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_12"],
        to_bus=buses["hv_bus_8"],
        length_km=3.63,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_12"]),
            _bus_geo(net, buses["hv_bus_8"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_0"],
        to_bus=buses["hv_bus_12"],
        length_km=2.61,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_0"]),
            _bus_geo(net, buses["hv_bus_12"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_7"],
        to_bus=buses["hv_bus_8"],
        length_km=1.73,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_7"]),
            _bus_geo(net, buses["hv_bus_8"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_7"],
        to_bus=buses["hv_bus_12"],
        length_km=2.29,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_7"]),
            _bus_geo(net, buses["hv_bus_12"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_10"],
        to_bus=buses["hv_bus_12"],
        length_km=1.84,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_10"]),
            _bus_geo(net, buses["hv_bus_12"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_2"],
        to_bus=buses["hv_bus_3"],
        length_km=3.39,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_2"]),
            _bus_geo(net, buses["hv_bus_3"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_2"],
        to_bus=buses["hv_bus_4"],
        length_km=4.52,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_2"]),
            _bus_geo(net, buses["hv_bus_4"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_4"],
        to_bus=buses["hv_bus_11"],
        length_km=1.97,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_4"]),
            _bus_geo(net, buses["hv_bus_11"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_5"],
        to_bus=buses["hv_bus_11"],
        length_km=2.44,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_5"]),
            _bus_geo(net, buses["hv_bus_11"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_4"],
        to_bus=buses["hv_bus_9"],
        length_km=2.74,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_4"]),
            _bus_geo(net, buses["hv_bus_9"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_3"],
        to_bus=buses["hv_bus_4"],
        length_km=4.00,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_3"]),
            _bus_geo(net, buses["hv_bus_4"]),
        ],
    )
    pp.create_line(
        net,
        from_bus=buses["hv_bus_5"],
        to_bus=buses["hv_bus_7"],
        length_km=3.19,
        std_type="N2XS(FL)2Y 1x240 RM/35 64/110 kV",
        geodata=[
            _bus_geo(net, buses["hv_bus_5"]),
            _bus_geo(net, buses["hv_bus_7"]),
        ],
    )


def _create_overseas(net, buses):
    pp.create_ext_grid(net, bus=buses["ov_hv_0"], name="Überseehafen")
    # Nord - Überseehafen
    # https://www.openstreetmap.org/way/157422539

    buses["ov_load_0"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Weddewarden Industrielast/ov_load_0",
        type="n",
        geodata=(53.604462, 8.534789),
    )

    pp.create_load(
        net,
        bus=buses["ov_load_0"],
        p_mw=0.06,
        name="Weddewarden Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.06),
    )
    pp.create_transformer(
        net,
        buses["ov_hv_0"],
        buses["ov_load_0"],
        name="110kV/20kV transformer",
        std_type="25 MVA 110/20 kV",
    )

    buses["ov_sgen_0"] = pp.create_bus(
        net,
        vn_kv=20,
        name="20 kV Gen Bus Windpark Speckenbüttel 2/ov_sgen_0",
        type="n",
        geodata=(53.593788, 8.555553),
    )

    pp.create_sgen(
        net,
        bus=buses["ov_sgen_0"],
        p_mw=5.0,
        name="Windpark Speckenbüttel 2",
        type="WP",
        min_p_mw=0,
        max_p_mw=5.0,
        q_mvar=compute_q(cos_phi=0.9, p_w=5),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["ov_load_0"],
        to_bus=buses["ov_sgen_0"],
        length_km=1.815,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["ov_load_0"]),
            _bus_geo(net, buses["ov_sgen_0"]),
        ],
    )

    buses["ov_lv_0"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Weddewarden LV/ov_lv_0",
        type="n",
        geodata=(53.604462, 8.534789),
    )

    pp.create_load(
        net,
        bus=buses["ov_lv_0"],
        p_mw=0.237,
        name="Weddewarden Households",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.237),
    )
    pp.create_sgen(
        net,
        bus=buses["ov_lv_0"],
        p_mw=0.03,
        name="PV Weddewarden",
        min_p_mw=0,
        max_p_mw=0.29,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.03),
    )
    buses["ov_load_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Weddewarden MV/ov_load_1",
        type="n",
        geodata=(53.604469, 8.534780),
    )

    pp.create_transformer_from_parameters(
        net,
        buses["ov_load_1"],
        buses["ov_lv_0"],
        sn_mva=0.4,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo-OS",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["ov_sgen_0"],
        to_bus=buses["ov_load_1"],
        length_km=0.01,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["ov_sgen_0"]),
            _bus_geo(net, buses["ov_load_1"]),
        ],
    )


def _create_lehe(net, buses):
    # Lehe
    buses["c_load_2"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Lehe Industrielast/c_load_2",
        type="n",
        geodata=(53.571902, 8.596871),
    )
    pp.create_load(
        net,
        bus=buses["c_load_2"],
        p_mw=3.905,
        name="Lehe Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=3.905),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["ov_load_1"],
        to_bus=buses["c_load_2"],
        length_km=3.19,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["ov_load_1"]),
            _bus_geo(net, buses["c_load_2"]),
        ],
    )

    buses["c_lv_1_0"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Lehe LV - 0/c_lv_1_0",
        type="n",
        geodata=(53.574865, 8.598650),
    )

    pp.create_sgen(
        net,
        bus=buses["c_lv_1_0"],
        p_mw=0.41,
        name="PV Lehe - 0",
        min_p_mw=0,
        max_p_mw=0.41,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.41),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_1_0"],
        p_mw=3.3,
        name="Lehe Households - 0",
        q_mvar=compute_q(cos_phi=0.97, p_w=3.3),
    )

    buses["c_load_3_0"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Lehe MV - 0/c_load_3_0",
        type="n",
        geodata=(53.560578, 8.593889),
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_3_0"],
        buses["c_lv_1_0"],
        sn_mva=2.2,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 1 - 0",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_2"],
        to_bus=buses["c_load_3_0"],
        length_km=1.27,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_2"]),
            _bus_geo(net, buses["c_load_3_0"]),
        ],
    )


def _create_windpark_speckenbuettel(net, buses):
    buses["ov_sgen_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="20 kV Gen Bus Windpark Speckenbüttel 1/ov_sgen_1",
        type="n",
        geodata=(53.602913, 8.548237),
    )
    pp.create_sgen(
        net,
        bus=buses["ov_sgen_1"],
        p_mw=5.0,
        name="Windpark Speckenbüttel 1",
        type="WP",
        min_p_mw=0,
        max_p_mw=5.0,
        q_mvar=compute_q(cos_phi=0.9, p_w=5),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_3_0"],
        to_bus=buses["ov_sgen_1"],
        length_km=0.905,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_3_0"]),
            _bus_geo(net, buses["ov_sgen_1"]),
        ],
    )


def _create_windpark_multibrid(net, buses):
    # # Multibrid M5000, 5 MW
    # # https://www.openstreetmap.org/node/1342407392
    buses["ov_sgen_2"] = pp.create_bus(
        net,
        vn_kv=20,
        name="20 kV Gen Bus Windpark Multibrid/ov_sgen_2",
        type="n",
        geodata=(53.602913, 8.548237),
    )
    pp.create_sgen(
        net,
        bus=buses["ov_sgen_2"],
        p_mw=5.0,
        name="Windpark Multibrid",
        type="WP",
        min_p_mw=0,
        max_p_mw=5.0,
        q_mvar=compute_q(cos_phi=0.9, p_w=5),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_3_0"],
        to_bus=buses["ov_sgen_2"],
        length_km=0.905,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_3_0"]),
            _bus_geo(net, buses["ov_sgen_2"]),
        ],
    )

    buses["c_load_12"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Geestemünde Industrielast/c_load_12",
        type="n",
        geodata=(53.530963, 8.599030),
    )
    pp.create_load(
        net,
        bus=buses["c_load_12"],
        p_mw=3.44,
        name="Geestemünde Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=3.44),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["ov_sgen_2"],
        to_bus=buses["c_load_12"],
        length_km=0.17,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["ov_sgen_2"]),
            _bus_geo(net, buses["c_load_12"]),
        ],
    )


def _create_geestemuende(net, buses):
    # Geestemünde
    buses["c_lv_3"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Geestemünde LV - 0/c_lv_3",
        type="n",
        geodata=(53.531437, 8.599357),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_3"],
        p_mw=3.45,
        name="Geestemünde Households - 0",
        q_mvar=compute_q(cos_phi=0.97, p_w=3.45),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_3"],
        p_mw=0.83,
        name="PV Geestemünde - 0",
        min_p_mw=0,
        max_p_mw=0.83,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.83),
    )

    buses["c_load_11"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Geestemünde MV - 0/c_load_11",
        type="n",
        geodata=(53.532464, 8.598488),
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_11"],
        buses["c_lv_3"],
        sn_mva=2.2,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 3",
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_12"],
        to_bus=buses["c_load_11"],
        length_km=0.389,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_12"]),
            _bus_geo(net, buses["c_load_11"]),
        ],
    )
    # Siemens SWT-2.3-93, 2.3 MW
    # https://www.openstreetmap.org/node/1145946171
    # Siemens SWT-2.3-93, 2.3 MW
    # https://www.openstreetmap.org/node/1145946189
    # Siemens SWT-2.3-93, 2.3 MW
    # https://www.openstreetmap.org/node/272116702
    # REpower 3.XM, 3.3 MW
    # https://www.openstreetmap.org/node/1342407395
    # Enercon E-82, 2 MW
    # https://www.openstreetmap.org/node/1305577597
    # Senvion 3.4M104, 3.4 MW
    # https://www.openstreetmap.org/node/4767958198
    # Multibrid M5000, 5 MW
    # https://www.openstreetmap.org/node/1230878049
    # Enercon Unknown, 3 MW
    # https://www.openstreetmap.org/node/5394329003
    # Enercon E-101, 3.05 MW
    # https://www.openstreetmap.org/node/4767958197
    # Enercon E-115, 3 MW
    # https://www.openstreetmap.org/node/617575631
    # Enercon E-82, 3 MW
    # https://www.openstreetmap.org/node/1342407391
    # REpower 3.3M, 3.3 MW
    # https://www.openstreetmap.org/node/1342407393


def _create_city(net, buses, use_extension):
    # city
    # ext grid right corner
    buses["c_ext_grid"] = pp.create_bus(
        net,
        vn_kv=20,
        name="110 kV Langen Bremerhaven Nord/c_ext_grid",
        type="b",
        geodata=(53.60537, 8.6241),
    )

    pp.create_ext_grid(net, bus=buses["c_hv_0"], name="BHV Nord")

    pp.create_transformer_from_parameters(
        net,
        buses["c_hv_0"],
        buses["c_ext_grid"],
        sn_mva=25,
        vn_hv_kv=110,
        vn_lv_kv=20,
        vkr_percent=0.16,
        vk_percent=12.00107,
        pfe_kw=0,
        i0_percent=0,
        shift_degree=30.0,
        name="Trafo 0-1",
    )

    # line between rings
    line_1 = pp.create_line_from_parameters(
        net,
        from_bus=buses["c_ext_grid"],
        to_bus=buses["c_load_11"],
        length_km=0.906,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_ext_grid"]),
            _bus_geo(net, buses["c_load_11"]),
        ],
    )
    # switch 0
    pp.create_switch(
        net, buses["c_load_11"], line_1, et="l", closed=True, type="LBS"
    )
    pp.create_switch(
        net,
        buses["c_ext_grid"],
        line_1,
        et="l",
        closed=False,
        type="LBS",
        name="S0",
    )
    buses["c_lv_1_1"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Lehe LV - 1/c_lv_1_1",
        type="n",
        geodata=(53.574865, 8.598650),
    )

    pp.create_sgen(
        net,
        bus=buses["c_lv_1_1"],
        p_mw=0.44,
        name="PV Lehe - 1",
        min_p_mw=0,
        max_p_mw=0.44,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.44),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_1_1"],
        p_mw=3.03,
        name="Lehe Households - 1",
        q_mvar=compute_q(cos_phi=0.97, p_w=3),
    )

    buses["c_load_3_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Lehe MV - 1/c_load_3_1",
        type="n",
        geodata=(53.560578, 8.593889),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_ext_grid"],
        to_bus=buses["c_load_3_1"],
        length_km=1.27,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_ext_grid"]),
            _bus_geo(net, buses["c_load_3_1"]),
        ],
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_3_1"],
        buses["c_lv_1_1"],
        sn_mva=1.9,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 1 - 1",
    )
    buses["c_lv_1_2"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Lehe LV - 2/c_lv_1_2",
        type="n",
        geodata=(53.574865, 8.598650),
    )

    pp.create_sgen(
        net,
        bus=buses["c_lv_1_2"],
        p_mw=0.49,
        name="PV Lehe - 2",
        min_p_mw=0,
        max_p_mw=0.49,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.49),
    )

    pp.create_load(
        net,
        bus=buses["c_lv_1_2"],
        p_mw=3.3,
        name="Lehe Households - 2",
        q_mvar=compute_q(cos_phi=0.97, p_w=3.3),
    )

    buses["c_load_3_2"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Lehe MV - 2/c_load_3_2",
        type="n",
        geodata=(53.560578, 8.593889),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_3_1"],
        to_bus=buses["c_load_3_2"],
        length_km=1.27,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_3_1"]),
            _bus_geo(net, buses["c_load_3_2"]),
        ],
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_3_2"],
        buses["c_lv_1_2"],
        sn_mva=2.1,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 1 - 2",
    )
    if use_extension:
        _ex_create_pv_plant_for_city(net, buses)
    else:
        # ----- Erdgas -----
        # Kronos, 17,1 MW, 110/6 kV
        buses["c_sgen_0"] = pp.create_bus(
            net,
            vn_kv=20,
            name="110 kV Gen Bus Erdgas Kronos Titan GmbH/c_sgen_0",
            type="n",
            geodata=(53.528558, 8.547564),
        )
        pp.create_sgen(
            net,
            bus=buses["c_sgen_0"],
            p_mw=17.1,
            name="Erdgas Kronos Titan GmbH",
            type="GUD",
            min_p_mw=0,
            max_p_mw=17.1,
            q_mvar=compute_q(cos_phi=0.8, p_w=17.1),
        )
        # The gas and steam turbine power plant not only generates power,
        # it also draws some from the grid. Because we work with the
        # scaling and to avoid a negative scaling, we create a load at
        # the same bus with the values the gas and steam turbine power
        # plant draws from the grid while the sgen only considers the
        # generated power

        pp.create_load(
            net,
            bus=buses["c_sgen_0"],
            p_mw=0.04,
            name="Erdgas Kronos Titan GmbH",
            q_mvar=compute_q(cos_phi=0.97, p_w=0.04),
        )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_3_2"],
        to_bus=buses["c_sgen_0"],
        length_km=2.72,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_3_2"]),
            _bus_geo(net, buses["c_sgen_0"]),
        ],
    )
    # Geestemünde
    buses["c_lv_3"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Geestemünde LV - 1/c_lv_3",
        type="n",
        geodata=(53.531437, 8.599357),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_3"],
        p_mw=4.25,
        name="Geestemünde Households - 1",
        q_mvar=compute_q(cos_phi=0.97, p_w=4.25),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_3"],
        p_mw=0.83,
        name="PV Geestemünde - 1",
        min_p_mw=0,
        max_p_mw=0.83,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.83),
    )
    buses["c_load_11"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Geestemünde MV - 1/c_load_11",
        type="n",
        geodata=(53.532464, 8.598488),
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_11"],
        buses["c_lv_3"],
        sn_mva=2.9,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 3",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_sgen_0"],
        to_bus=buses["c_load_11"],
        length_km=0.389,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_sgen_0"]),
            _bus_geo(net, buses["c_load_11"]),
        ],
    )

    buses["c_lv_1_3"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Lehe LV - 3/c_lv_1_3",
        type="n",
        geodata=(53.574865, 8.598650),
    )

    pp.create_sgen(
        net,
        bus=buses["c_lv_1_3"],
        p_mw=0.45,
        name="PV Lehe - 3",
        min_p_mw=0,
        max_p_mw=0.45,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.45),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_1_3"],
        p_mw=3,
        name="Lehe Households - 3",
        q_mvar=compute_q(cos_phi=0.97, p_w=3),
    )

    buses["c_load_3_3"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Lehe MV - 3/c_load_3_3",
        type="n",
        geodata=(53.560578, 8.593889),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_11"],
        to_bus=buses["c_load_3_3"],
        length_km=1.27,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_11"]),
            _bus_geo(net, buses["c_load_3_3"]),
        ],
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_3_3"],
        buses["c_lv_1_3"],
        sn_mva=2,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 1 - 3",
    )

    buses["c_lv_1_4"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Lehe LV - 4/c_lv_1_4",
        type="n",
        geodata=(53.574865, 8.598650),
    )

    pp.create_sgen(
        net,
        bus=buses["c_lv_1_4"],
        p_mw=0.44,
        name="PV Lehe - 4",
        min_p_mw=0,
        max_p_mw=0.44,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.44),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_1_4"],
        p_mw=3,
        name="Lehe Households - 4",
        q_mvar=compute_q(cos_phi=0.97, p_w=3),
    )

    buses["c_load_3_4"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Lehe MV - 4/c_load_3_4",
        type="n",
        geodata=(53.560578, 8.593889),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_3_3"],
        to_bus=buses["c_load_3_4"],
        length_km=1.27,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_3_3"]),
            _bus_geo(net, buses["c_load_3_4"]),
        ],
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_3_4"],
        buses["c_lv_1_4"],
        sn_mva=2,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 1",
    )
    # REpower 5M, 5 MW
    # https://www.openstreetmap.org/node/691722623
    buses["ov_sgen_2"] = pp.create_bus(
        net,
        vn_kv=20,
        name="20 kV Gen Bus Windpark Repower/ov_sgen_2",
        type="n",
        geodata=(53.602913, 8.548237),
    )
    pp.create_sgen(
        net,
        bus=buses["ov_sgen_2"],
        p_mw=5.0,
        name="Windpark Repower",
        type="WP",
        min_p_mw=0,
        max_p_mw=5.0,
        q_mvar=compute_q(cos_phi=0.9, p_w=5),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_3_4"],
        to_bus=buses["ov_sgen_2"],
        length_km=0.905,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_3_4"]),
            _bus_geo(net, buses["ov_sgen_2"]),
        ],
    )

    buses["c_lv_0"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Leherheide LV - 0/c_lv_0",
        type="n",
        geodata=(53.594306, 8.607556),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_0"],
        p_mw=3.7,
        name="Leherheide Households - 0",
        q_mvar=compute_q(cos_phi=0.97, p_w=3.7),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_0"],
        p_mw=0.46,
        name="PV Leherheide - 0",
        min_p_mw=0,
        max_p_mw=0.46,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.46),
    )
    buses["c_load_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Leherheide MV - 0/c_load_1",
        type="n",
        geodata=(53.592671, 8.604457),
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_1"],
        buses["c_lv_0"],
        sn_mva=2.4,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 0 - 0",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_3_4"],
        to_bus=buses["c_load_1"],
        length_km=0.3,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_3_4"]),
            _bus_geo(net, buses["c_load_1"]),
        ],
    )
    # ext grid central
    buses["c_ext_grid_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="110 kV Lehe ExtGrid/c_ext_grid_1",
        type="b",
        geodata=(53.563454, 8.601023),
    )

    pp.create_ext_grid(net, bus=buses["c_hv_1"], name="Lehe")

    pp.create_transformer(
        net,
        buses["c_hv_1"],
        buses["c_ext_grid_1"],
        name="110kV/20kV transformer",
        std_type="25 MVA 110/20 kV",
    )


def _ex_create_pv_plant_for_city(net, buses):
    buses["c_sgen_0"] = pp.create_bus(
        net,
        vn_kv=20,
        name="8.5MW wind plant for gas plant/c_sgen_0",
        type="n",
        geodata=(53.528558, 8.547564),
    )
    buses["c1_sgen_0"] = pp.create_bus(
        net, vn_kv=20, name="3.1MW pv plant for gas plant/c1_sgen_0", type="b"
    )
    buses["c2_sgen_0"] = pp.create_bus(
        net, vn_kv=20, name="1MW pv plant for gas plant/c2_sgen_0", type="b"
    )
    buses["c3_sgen_0"] = pp.create_bus(
        net, vn_kv=20, name="3MW wind plant for gas plant/c3_sgen_0", type="b"
    )
    buses["c4_sgen_0"] = pp.create_bus(
        net, vn_kv=20, name="1MW pv plant for gas plant/c4_sgen_0", type="b"
    )
    pp.create_sgen(
        net,
        bus=buses["c_sgen_0"],
        p_mw=8.5,
        name="8.5MW wind c_sgen_0",
        min_p_mw=0,
        max_p_mw=8.5,
        q_mvar=compute_q(cos_phi=0.9, p_w=8.5),
        type="wp",
    )  # 3 wind turbine ( 2.5MW, 3MW and 3MW )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_sgen_0"],
        to_bus=buses["c1_sgen_0"],
        length_km=3,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )

    pp.create_sgen(
        net,
        bus=buses["c1_sgen_0"],
        p_mw=3.1,
        name="3.1MW pv c1_sgen_0",
        min_p_mw=0,
        max_p_mw=3.1,
        q_mvar=compute_q(cos_phi=0.92, p_w=3.1),
        type="pv",
    )
    pp.create_load(
        net,
        bus=buses["c1_sgen_0"],
        p_mw=0.3,
        name="load c1_sgen_0",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.3),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c1_sgen_0"],
        to_bus=buses["c2_sgen_0"],
        length_km=5,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )
    pp.create_sgen(
        net,
        bus=buses["c2_sgen_0"],
        p_mw=1.0,
        name="1MW pv c2_sgen_0",
        min_p_mw=0,
        max_p_mw=1,
        q_mvar=compute_q(cos_phi=0.93, p_w=1),
        type="biomass",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c2_sgen_0"],
        to_bus=buses["c3_sgen_0"],
        length_km=2.7,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )
    pp.create_sgen(
        net,
        bus=buses["c3_sgen_0"],
        p_mw=3.0,
        name="3MW wind c3_sgen_0",
        min_p_mw=0,
        max_p_mw=3,
        q_mvar=compute_q(cos_phi=0.95, p_w=3),
        type="wp",
    )
    pp.create_load(
        net,
        bus=buses["c3_sgen_0"],
        p_mw=0.7,
        name="load c3_sgen_0",
        q_mvar=compute_q(cos_phi=0.95, p_w=0.7),
    )


def _create_windpark_lehe(net, buses):
    # ----- Windenergie: Windpark Lehe, 10.0 MW HS/MS ------
    buses["c_sgen_2"] = pp.create_bus(
        net,
        vn_kv=20,
        name="20 kV Gen Bus Windpark Lehe/c_sgen_2",
        type="n",
        geodata=(53.561192, 8.622811),
    )
    pp.create_sgen(
        net,
        bus=buses["c_sgen_2"],
        p_mw=10.0,
        name="Windpark Lehe",
        type="WP",
        min_p_mw=0,
        max_p_mw=10.0,
        q_mvar=compute_q(cos_phi=0.9, p_w=10.0),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_ext_grid_1"],
        to_bus=buses["c_sgen_2"],
        length_km=1.462,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_ext_grid_1"]),
            _bus_geo(net, buses["c_sgen_2"]),
        ],
    )


def _create_klinikum_reinkenheide(net, buses):
    buses["c_load_20"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Klinikum Bremerhaven - Reinkenheide gGmbH/c_load_20",
        type="n",
        geodata=(53.537969, 8.636555),
    )

    pp.create_load(
        net,
        bus=buses["c_load_20"],
        p_mw=0.938,
        name="Klinikum Bremerhaven - Reinkenheide gGmbH",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.938),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_sgen_2"],
        to_bus=buses["c_load_20"],
        length_km=1.03,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.6,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_sgen_2"]),
            _bus_geo(net, buses["c_load_20"]),
        ],
    )


def _create_schiffdorferdamm(net, buses):
    # Schiffdorferdamm
    buses["c_lv_6"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Schiffdorferdamm LV/c_lv_6",
        type="n",
        geodata=(53.530717, 8.632589),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_6"],
        p_mw=0.13,
        name="PV Schiffdorferdamm",
        min_p_mw=0,
        max_p_mw=0.13,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.13),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_6"],
        p_mw=1.043,
        name="Schiffdorferdamm Households",
        q_mvar=compute_q(cos_phi=0.97, p_w=1.043),
    )
    buses["c_load_18"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Schiffdorferdamm MV/c_load_18",
        type="n",
        geodata=(53.530717, 8.632589),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_20"],
        to_bus=buses["c_load_18"],
        length_km=1.47,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_20"]),
            _bus_geo(net, buses["c_load_18"]),
        ],
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_18"],
        buses["c_lv_6"],
        sn_mva=0.7,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 6",
    )

    buses["c_load_19"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Schiffdorferdamm Industrielast/c_load_19",
        type="n",
        geodata=(53.529534, 8.630127),
    )
    pp.create_load(
        net,
        bus=buses["c_load_19"],
        p_mw=0.266,
        name="Schiffdorferdamm Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.266),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_18"],
        to_bus=buses["c_load_19"],
        length_km=0.209,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_18"]),
            _bus_geo(net, buses["c_load_19"]),
        ],
    )


def _create_eisarena(net, buses):
    # Eisarena
    buses["c_load_4"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Bremerhaven Eisarena, Stadthalle etc./c_load_4",
        type="n",
        geodata=(53.554570, 8.590115),
    )
    pp.create_load(
        net,
        bus=buses["c_load_4"],
        p_mw=0.54,
        name="Bremerhaven Eisarena, Stadthalle etc.",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.54),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_19"],
        to_bus=buses["c_load_4"],
        length_km=0.7,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_19"]),
            _bus_geo(net, buses["c_load_4"]),
        ],
    )

    buses["c_load_7"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Mitte Industrielast/c_load_7",
        type="n",
        geodata=(53.542821, 8.581104),
    )
    pp.create_load(
        net,
        bus=buses["c_load_7"],
        p_mw=1.296,
        name="Mitte Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=1.296),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_4"],
        to_bus=buses["c_load_7"],
        length_km=1.44,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_4"]),
            _bus_geo(net, buses["c_load_7"]),
        ],
    )


def _create_mitte(net, buses):
    # Mitte
    buses["c_lv_2"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Mitte LV - 0/c_lv_2",
        type="n",
        geodata=(53.547459, 8.580126),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_2"],
        p_mw=2.55,
        name="Mitte Households - 0",
        q_mvar=compute_q(cos_phi=0.97, p_w=2.55),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_2"],
        p_mw=0.33,
        name="PV Mitte - 0",
        min_p_mw=0,
        max_p_mw=0.33,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.33),
    )
    buses["c_load_6"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Mitte MV - 0/c_load_6",
        type="n",
        geodata=(53.546510, 8.579083),
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_6"],
        buses["c_lv_2"],
        sn_mva=1.7,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 2",
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_7"],
        to_bus=buses["c_load_6"],
        length_km=0.35,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_7"]),
            _bus_geo(net, buses["c_load_6"]),
        ],
    )


def _create_leherheide(net, buses):
    # Leherheide
    buses["c_load_0"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Leherheide Industrielast/c_load_0",
        type="n",
        geodata=(53.598963, 8.629993),
    )

    pp.create_load(
        net,
        bus=buses["c_load_0"],
        p_mw=1.701,
        name="Leherheide Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=1.701),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_6"],
        to_bus=buses["c_load_0"],
        length_km=6.7,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_6"]),
            _bus_geo(net, buses["c_load_0"]),
        ],
    )


def _create_wulsdorf(net, buses):
    # Wulsdorf
    buses["c_lv_4_1"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Wulsdorf LV - 0/c_lv_4_1",
        type="n",
        geodata=(53.503051, 8.605203),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_4_1"],
        p_mw=2.6,
        name="Wulsdorf Households - 0",
        q_mvar=compute_q(cos_phi=0.97, p_w=2.6),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_4_1"],
        p_mw=0.33,
        name="PV Wulsdorf - 0",
        min_p_mw=0,
        max_p_mw=0.33,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.33),
    )
    buses["c_load_13_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Wulsdorf MV - 0/c_load_13_1",
        type="n",
        geodata=(53.503051, 8.605203),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_0"],
        to_bus=buses["c_load_13_1"],
        length_km=10.7,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_0"]),
            _bus_geo(net, buses["c_load_13_1"]),
        ],
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_13_1"],
        buses["c_lv_4_1"],
        sn_mva=1.8,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 4",
    )


def _create_abfall(net, buses, use_extension):
    # # ----- Abfall -----
    # # BEG, 14.0 MW, 20 kV
    # # https://www.openstreetmap.org/way/105301541
    # # https://www.wikidata.org/wiki/Q59315437
    buses["c_sgen_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="20 kV Gen Bus Abfall BEG mbh/c_sgen_1",
        type="n",
        geodata=(53.547946, 8.617964),
    )
    if use_extension:
        _ex_create_pv_plant_for_abfall(net, buses)
    else:

        pp.create_sgen(
            net,
            bus=buses["c_sgen_1"],
            p_mw=14.0,
            name="Abfall BEG mbh",
            min_p_mw=0,
            max_p_mw=14.0,
            q_mvar=compute_q(cos_phi=0.8, p_w=14),
            type="CHP",
        )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_13_1"],
        to_bus=buses["c_sgen_1"],
        length_km=5,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.55,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_13_1"]),
            _bus_geo(net, buses["c_sgen_1"]),
        ],
    )

    buses["c_load_17"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Surheide Industrielast/c_load_17",
        type="n",
        geodata=(53.517510, 8.632251),
    )

    pp.create_load(
        net,
        bus=buses["c_load_17"],
        p_mw=0.311,
        name="Surheide Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.311),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_sgen_1"],
        to_bus=buses["c_load_17"],
        length_km=3.5,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_sgen_1"]),
            _bus_geo(net, buses["c_load_17"]),
        ],
    )


def _ex_create_pv_plant_for_abfall(net, buses):
    # ( Replacement of Waste fuel powerplant by RE # 14MW )
    # C1_sgen_1 ,C2_sgen_1, C3_sgen_1, C4_sgen_1 buses are created
    # All these buses are connected to the existing bus C_sgen_1 in a
    # radial format
    # No transformer and LV line are connected yet in the system
    buses["c1_sgen_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="3MW wind plant for waste plant/c1_sgen_1",
        type="b",
    )
    buses["c2_sgen_1"] = pp.create_bus(
        net, vn_kv=20, name="2MW pv plant for waste plant/c2_sgen_1", type="b"
    )
    buses["c3_sgen_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="1.5MW pv plant for waste plant/c3_sgen_1",
        type="b",
    )
    buses["c4_sgen_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="2.5MW wind plant for waste plant/c4_sgen_1",
        type="b",
    )

    pp.create_sgen(
        net,
        bus=buses["c_sgen_1"],
        p_mw=5.0,
        name="5MW wind c_sgen_1",
        min_p_mw=0,
        max_p_mw=5.0,
        q_mvar=compute_q(cos_phi=0.9, p_w=5),
        type="wp",
    )  # 2 wind turbine, 2.5MW each

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_sgen_1"],
        to_bus=buses["c1_sgen_1"],
        length_km=1.28,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )
    pp.create_sgen(
        net,
        bus=buses["c1_sgen_1"],
        p_mw=3.0,
        name="3MW wind c1_sgen_1",
        min_p_mw=0,
        max_p_mw=3.0,
        q_mvar=compute_q(cos_phi=0.95, p_w=3),
        type="wp",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c1_sgen_1"],
        to_bus=buses["c2_sgen_1"],
        length_km=2,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )

    pp.create_sgen(
        net,
        bus=buses["c2_sgen_1"],
        p_mw=2.0,
        name="2MW solar c2_sgen_1",
        min_p_mw=0,
        max_p_mw=2.0,
        q_mvar=compute_q(cos_phi=0.97, p_w=2),
        type="pv",
    )
    pp.create_load(
        net,
        bus=buses["c2_sgen_1"],
        p_mw=0.7,
        name="load c2_sgen_1",
        q_mvar=compute_q(cos_phi=0.96, p_w=0.7),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c2_sgen_1"],
        to_bus=buses["c3_sgen_1"],
        length_km=7,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )

    pp.create_sgen(
        net,
        bus=buses["c3_sgen_1"],
        p_mw=1.5,
        name="1.5MW solar c3_sgen_1",
        min_p_mw=0,
        max_p_mw=1.5,
        q_mvar=compute_q(cos_phi=0.95, p_w=1.5),
        type="pv",
    )

    pp.create_load(
        net,
        bus=buses["c3_sgen_1"],
        p_mw=0.63,
        name="load c3_sgen_1",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.63),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c3_sgen_1"],
        to_bus=buses["c4_sgen_1"],
        length_km=3,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )

    pp.create_sgen(
        net,
        bus=buses["c4_sgen_1"],
        p_mw=2.5,
        name="2.5MW wind c4_sgen_1",
        min_p_mw=0,
        max_p_mw=2.5,
        q_mvar=compute_q(cos_phi=0.96, p_w=2.5),
        type="biomass",
    )

    pp.create_load(
        net,
        bus=buses["c4_sgen_1"],
        p_mw=0.2,
        name="load1 c4_sgen_1",
        q_mvar=compute_q(cos_phi=0.95, p_w=0.2),
    )
    pp.create_load(
        net,
        bus=buses["c4_sgen_1"],
        p_mw=1.1,
        name="load2 c4_sgen_1",
        q_mvar=compute_q(cos_phi=0.93, p_w=1.1),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c4_sgen_1"],
        to_bus=buses["c_sgen_1"],
        length_km=5,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
    )


def _create_surheide(net, buses):
    # # Surheide
    buses["c_lv_5"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Surheide LV/c_lv_5",
        type="n",
        geodata=(53.519094, 8.637143),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_5"],
        p_mw=1.22,
        name="Surheide Households",
        q_mvar=compute_q(cos_phi=0.97, p_w=1.22),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_5"],
        p_mw=0.16,
        name="PV Surheide",
        min_p_mw=0,
        max_p_mw=0.16,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.16),
    )
    buses["c_load_16"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Surheide MV/c_load_16",
        type="n",
        geodata=(53.519094, 8.637143),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_17"],
        to_bus=buses["c_load_16"],
        length_km=0.37,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_17"]),
            _bus_geo(net, buses["c_load_16"]),
        ],
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_16"],
        buses["c_lv_5"],
        sn_mva=0.8,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 5",
    )


def _create_klinikum_buergerpark(net, buses):
    # Klinikum Bürgerpark
    buses["c_load_10"] = pp.create_bus(
        net,
        vn_kv=20,
        name="AMEOS Klinikum Am Bürgerpark Bremerhaven/c_load_10",
        type="n",
        geodata=(53.532376, 8.604369),
    )
    pp.create_load(
        net,
        bus=buses["c_load_10"],
        p_mw=0.28,
        name="AMEOS Klinikum Am Bürgerpark Bremerhaven",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.28),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_16"],
        to_bus=buses["c_load_10"],
        length_km=2.6,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_16"]),
            _bus_geo(net, buses["c_load_10"]),
        ],
    )


def _create_innenstadt(net, buses):
    # # Innenstadt
    buses["c_load_9"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Bremerhaven Innenstadt/c_load_9",
        type="n",
        geodata=(53.542787, 8.581111),
    )
    pp.create_load(
        net,
        bus=buses["c_load_9"],
        p_mw=0.355,
        name="Bremerhaven Innenstadt",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.355),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_10"],
        to_bus=buses["c_load_9"],
        length_km=1.9,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_10"]),
            _bus_geo(net, buses["c_load_9"]),
        ],
    )


def _create_zoo(net, buses):
    # Zoo
    buses["c_load_8"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Zoo/c_load_8",
        type="n",
        geodata=(53.544990, 8.570957),
    )
    pp.create_load(
        net,
        bus=buses["c_load_8"],
        p_mw=0.27,
        name="Zoo",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.27),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_9"],
        to_bus=buses["c_load_8"],
        length_km=0.713,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_9"]),
            _bus_geo(net, buses["c_load_8"]),
        ],
    )


def _create_klinikum_mitte(net, buses):
    # Klinikum Mitte
    buses["c_load_5"] = pp.create_bus(
        net,
        vn_kv=20,
        name="AMEOS Klinikum Mitte Bremerhaven/c_load_5",
        type="n",
        geodata=(53.552685, 8.575043),
    )
    pp.create_load(
        net,
        bus=buses["c_load_5"],
        p_mw=0.236,
        name="AMEOS Klinikum Mitte Bremerhaven",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.236),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_8"],
        to_bus=buses["c_load_5"],
        length_km=0.89,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_8"]),
            _bus_geo(net, buses["c_load_5"]),
        ],
    )

    buses["c_lv_2"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Mitte LV - 1/c_lv_2",
        type="n",
        geodata=(53.547459, 8.580126),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_2"],
        p_mw=2.55,
        name="Mitte Households - 1",
        q_mvar=compute_q(cos_phi=0.97, p_w=2.55),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_2"],
        p_mw=0.32,
        name="PV Mitte - 1",
        min_p_mw=0,
        max_p_mw=0.32,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.32),
    )
    buses["c_load_6"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Mitte MV/c_load_6",
        type="n",
        geodata=(53.546510, 8.579083),
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_6"],
        buses["c_lv_2"],
        sn_mva=1.8,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 2",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_5"],
        to_bus=buses["c_load_6"],
        length_km=0.74,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_5"]),
            _bus_geo(net, buses["c_load_6"]),
        ],
    )

    buses["c_lv_0_1"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Leherheide LV - 1/c_lv_0_1",
        type="n",
        geodata=(53.594306, 8.607559),
    )

    pp.create_load(
        net,
        bus=buses["c_lv_0_1"],
        p_mw=2.2,
        name="Leherheide Households - 1",
        q_mvar=compute_q(cos_phi=0.97, p_w=2.2),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_0_1"],
        p_mw=0.28,
        name="PV Leherheide - 1",
        min_p_mw=0,
        max_p_mw=0.28,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.28),
    )
    buses["c_load_1_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Leherheide MV - 1/c_load_1_1",
        type="n",
        geodata=(53.592671, 8.604461),
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_1_1"],
        buses["c_lv_0_1"],
        sn_mva=1.6,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 0 - 1",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_6"],
        to_bus=buses["c_load_1_1"],
        length_km=5.4,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_6"]),
            _bus_geo(net, buses["c_load_1_1"]),
        ],
    )

    buses["c_lv_4"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Wulsdorf LV - 1/c_lv_4",
        type="n",
        geodata=(53.503051, 8.605203),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_4"],
        p_mw=2,
        name="Wulsdorf Households - 1",
        q_mvar=compute_q(cos_phi=0.97, p_w=2),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_4"],
        p_mw=0.25,
        name="PV Wulsdorf - 1",
        min_p_mw=0,
        max_p_mw=0.25,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.25),
    )
    buses["c_load_13"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Wulsdorf MV - 1/c_load_13",
        type="n",
        geodata=(53.503051, 8.605203),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_1_1"],
        to_bus=buses["c_load_13"],
        length_km=9.13,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.5,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_1_1"]),
            _bus_geo(net, buses["c_load_13"]),
        ],
    )

    pp.create_transformer_from_parameters(
        net,
        buses["c_load_13"],
        buses["c_lv_4"],
        sn_mva=1.4,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 4",
    )

    # Multibrid M5000, 5 MW
    # https://www.openstreetmap.org/node/691695235
    # Multibrid M5000, 5 MW
    # https://www.openstreetmap.org/node/2432566699
    # Senvion 3.4M104 - 3.4 MW
    # https://www.openstreetmap.org/node/1476500908
    # Senvion 3.4M104 - 3.4 MW
    # https://www.openstreetmap.org/node/2917846569
    # Senvion 3.4M114 - 3.4 MW
    # https://www.openstreetmap.org/node/2509552694
    # REpower 3.0M122, 3 MW
    # https://www.openstreetmap.org/node/2097192036


def _create_fischereihafen(net, buses):
    # fishing port ring
    # line between rings
    buses["fp_load_6"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Fischereihafen Industrielast/fp_load_6",
        type="n",
        geodata=(53.509672, 8.584799),
    )
    line_0 = pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_6"],
        to_bus=buses["c_load_13"],
        length_km=1.54,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_6"]),
            _bus_geo(net, buses["c_load_13"]),
        ],
    )

    # switch 1
    pp.create_switch(
        net, buses["c_load_13"], line_0, et="l", closed=True, type="LBS"
    )
    pp.create_switch(
        net,
        buses["fp_load_6"],
        line_0,
        et="l",
        closed=False,
        type="LBS",
        name="S1",
    )

    pp.create_load(
        net,
        bus=buses["fp_load_6"],
        p_mw=0.02,
        name="Fischereihafen Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.02),
    )

    buses["c_load_14"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Wulsdorf Industrielast/c_load_14",
        type="n",
        geodata=(53.499859, 8.606736),
    )

    pp.create_load(
        net,
        bus=buses["c_load_14"],
        p_mw=1.176,
        name="Wulsdorf Industrielast",
        q_mvar=compute_q(cos_phi=0.97, p_w=1.176),
    )
    pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_6"],
        to_bus=buses["c_load_14"],
        length_km=1.8,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_6"]),
            _bus_geo(net, buses["c_load_14"]),
        ],
    )


def _create_geestemuende_v2(net, buses):
    # Geestemünde
    buses["c_lv_3"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Geestemünde LV - 2/c_lv_3",
        type="n",
        geodata=(53.531437, 8.599357),
    )
    pp.create_load(
        net,
        bus=buses["c_lv_3"],
        p_mw=2.9,
        name="Geestemünde Households - 2",
        q_mvar=compute_q(cos_phi=0.97, p_w=2.9),
    )
    pp.create_sgen(
        net,
        bus=buses["c_lv_3"],
        p_mw=0.83,
        name="PV Geestemünde - 2",
        min_p_mw=0,
        max_p_mw=0.83,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.83),
    )
    buses["c_load_11"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Geestemünde MV - 2/c_load_11",
        type="n",
        geodata=(53.532464, 8.598488),
    )
    pp.create_transformer_from_parameters(
        net,
        buses["c_load_11"],
        buses["c_lv_3"],
        sn_mva=1.8,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo C - 3",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_14"],
        to_bus=buses["c_load_11"],
        length_km=3.69,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_14"]),
            _bus_geo(net, buses["c_load_11"]),
        ],
    )


def _create_bremerhaven_sued(net, buses):
    # Bremerhaven Süd
    buses["c_load_15"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Bremerhaven Süd/c_load_15",
        type="n",
        geodata=(53.489738, 8.602587),
    )
    pp.create_load(
        net,
        bus=buses["c_load_15"],
        p_mw=0.533,
        name="Bremerhaven Süd",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.533),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_11"],
        to_bus=buses["c_load_15"],
        length_km=5.7,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_11"]),
            _bus_geo(net, buses["c_load_15"]),
        ],
    )

    buses["fp_load_5"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Fischereihafen - 4/fp_load_5",
        type="n",
        geodata=(53.525959, 8.582308),
    )

    pp.create_load(
        net,
        bus=buses["fp_load_5"],
        p_mw=0.25,
        name="Fischereihafen - 4",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.25),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["c_load_15"],
        to_bus=buses["fp_load_5"],
        length_km=4.24,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["c_load_15"]),
            _bus_geo(net, buses["fp_load_5"]),
        ],
    )
    buses["fp_load_4"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Fischereihafen - 3/fp_load_4",
        type="n",
        geodata=(53.507744, 8.588815),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_5"],
        to_bus=buses["fp_load_4"],
        length_km=2.072,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_5"]),
            _bus_geo(net, buses["fp_load_4"]),
        ],
    )

    pp.create_load(
        net,
        bus=buses["fp_load_4"],
        p_mw=0.25,
        name="Fischereihafen - 3",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.25),
    )

    buses["fp_load_3"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Fischereihafen - 2/fp_load_3",
        type="n",
        geodata=(53.498069, 8.589991),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_4"],
        to_bus=buses["fp_load_3"],
        length_km=1.08,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_4"]),
            _bus_geo(net, buses["fp_load_3"]),
        ],
    )

    pp.create_load(
        net,
        bus=buses["fp_load_3"],
        p_mw=0.25,
        name="Fischereihafen - 2",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.25),
    )

    buses["fp_load_2"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Fischereihafen - 1/fp_load_2",
        type="n",
        geodata=(53.516097, 8.573791),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_3"],
        to_bus=buses["fp_load_2"],
        length_km=2.275,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_3"]),
            _bus_geo(net, buses["fp_load_2"]),
        ],
    )

    pp.create_load(
        net,
        bus=buses["fp_load_2"],
        p_mw=0.25,
        name="Fischereihafen - 1",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.25),
    )

    buses["fp_load_1"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Fischereihafen - 0/fp_load_1",
        type="n",
        geodata=(53.515457, 8.585792),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_2"],
        to_bus=buses["fp_load_1"],
        length_km=0.798,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_2"]),
            _bus_geo(net, buses["fp_load_1"]),
        ],
    )
    pp.create_load(
        net,
        bus=buses["fp_load_1"],
        p_mw=0.25,
        name="Fischereihafen - 0",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.25),
    )

    buses["fp_load_0"] = pp.create_bus(
        net,
        vn_kv=20,
        name="Fischereihafen MV/fp_load_0",
        type="n",
        geodata=(53.509672, 8.584799),
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_1"],
        to_bus=buses["fp_load_0"],
        length_km=0.647,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_1"]),
            _bus_geo(net, buses["fp_load_0"]),
        ],
    )
    buses["fp_lv__0"] = pp.create_bus(
        net,
        vn_kv=0.4,
        name="Fischereihafen LV/fp_lv__0",
        type="n",
        geodata=(53.509672, 8.584799),
    )
    pp.create_sgen(
        net,
        bus=buses["fp_lv__0"],
        p_mw=0.01,
        name="PV Fischereihafen",
        min_p_mw=0,
        max_p_mw=0.01,
        type="PV",
        q_mvar=compute_q(cos_phi=0.9, p_w=0.01),
    )
    pp.create_load(
        net,
        bus=buses["fp_lv__0"],
        p_mw=0.078,
        name="Fischereihafen Households",
        q_mvar=compute_q(cos_phi=0.97, p_w=0.078),
    )

    pp.create_transformer_from_parameters(
        net,
        buses["fp_load_0"],
        buses["fp_lv__0"],
        sn_mva=0.4,
        vn_hv_kv=20,
        vn_lv_kv=0.4,
        vkr_percent=1.325,
        vk_percent=4,
        pfe_kw=0.95,
        i0_percent=0.2375,
        tap_side="hv",
        tap_neutral=0,
        tap_min=-2,
        tap_max=2,
        tap_step_percent=2.5,
        tp_pos=0,
        shift_degree=150,
        name="MV-LV-Trafo FP",
    )

    buses["fp_ext_grid"] = pp.create_bus(
        net,
        vn_kv=20,
        name="110 kV Ext Grid Fischereihafen MV/fp_ext_grid",
        type="b",
        geodata=(53.515996, 8.606491),
    )

    pp.create_ext_grid(
        net, bus=buses["hv_bus_8"], name="Ext Grid Fischereihafen"
    )

    pp.create_transformer(
        net,
        buses["hv_bus_8"],
        buses["fp_ext_grid"],
        name="110kV/20kV transformer",
        std_type="25 MVA 110/20 kV",
    )

    pp.create_line_from_parameters(
        net,
        from_bus=buses["fp_load_0"],
        to_bus=buses["fp_ext_grid"],
        length_km=1.59,
        type="cs",
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.05,
        max_i_ka=0.4,
        c_nf_per_km=10,
        geodata=[
            _bus_geo(net, buses["fp_load_0"]),
            _bus_geo(net, buses["fp_ext_grid"]),
        ],
    )


def _invert_geodata(net):
    for idx, row in net.bus_geodata.iterrows():
        row["x"], row["y"] = row["y"], row["x"]
        net.bus_geodata.loc[idx] = row
        for idx, row in net.line_geodata.iterrows():
            reversed_coords = []
            for coord in row["coords"]:
                reversed_coords.append(tuple(reversed(coord)))
            row["coords"] = reversed_coords
            net.line_geodata.loc[idx] = row


def _bus_geo(net, bus):
    x = net["bus_geodata"].loc[bus, "x"]
    y = net["bus_geodata"].loc[bus, "y"]
    return x, y


# grid = build_grid()

# pp.runpp(grid, numba=True)
# plt.simple_plot(grid, plot_line_switches=True)

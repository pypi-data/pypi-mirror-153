"""This module contains the mosaik meta definition for the
pandapower simulator.

"""

META = {
    "type": "time-based",
    "models": {
        "Grid": {
            "public": True,
            "params": [
                "gridfile",  # Name of the grid topology
                "grid_params",
                "plotting",  # Flag to activate plotting
                "use_constraints",  # Flag to activate constraints
                "constraints",  # A list of constraints to activate
            ],
            "attrs": ["health", "grid_json"],
        },
        "Ext_grid": {
            "public": False,
            "params": [],
            "attrs": [
                "p_mw",  # load active power [MW]
                "q_mvar",  # load reactive power [MVAr]
            ],
        },
        "Bus": {
            "public": False,
            "params": [],
            "attrs": [
                "p_mw",  # load Active power [MW]
                "q_mvar",  # Reactive power [MVAr]
                "vn_kv",  # Nominal bus voltage [KV]
                "vm_pu",  # Voltage magnitude [p.u]
                "va_degree",  # Voltage angle [deg]
            ],
        },
        "Load": {
            "public": False,
            "params": [],
            "attrs": [
                "p_mw",  # load Active power [MW]
                "q_mvar",  # Reactive power [MVAr]
                "in_service",  # specifies if the load is in service.
                "controllable",  # States if load is controllable or not.
            ],
        },
        "Sgen": {
            "public": False,
            "params": [],
            "attrs": [
                "p_mw",  # load Active power [MW]
                "q_mvar",  # Reactive power [MVAr]
                "in_service",  # specifies if the load is in service.
                "controllable",  # States if load is controllable or not.
                "va_degree",  # Voltage angle [deg]
            ],
        },
        "Trafo": {
            "public": False,
            "params": [],
            "attrs": [
                "p_hv_mw",  # Active power at "from" side [MW]
                "q_hv_mvar",  # Reactive power at "from" side [MVAr]
                "p_lv_mw",  # Active power at "to" side [MW]
                "q_lv_mvar",  # Reactive power at "to" side [MVAr]
                "sn_mva",  # Rated apparent power [MVA]
                "max_loading_percent",  # Maximum Loading
                "vn_hv_kv",  # Nominal primary voltage [kV]
                "vn_lv_kv",  # Nominal secondary voltage [kV]
                "pl_mw",  # Active power loss [MW]
                "ql_mvar",  # reactive power consumption of the
                # transformer [Mvar]
                # 'pfe_kw',       #  iron losses in kW [kW]
                # 'i0_percent',       #  iron losses in kW [kW]
                "loading_percent",  # load utilization relative to rated
                # power [%]
                "i_hv_ka",  # current at the high voltage side of the
                # transformer [kA]
                "i_lv_ka",  # current at the low voltage side of the
                # transformer [kA]
                "tap_max",  # maximum possible  tap turns
                "tap_min",  # minimum possible tap turns
                "tap_pos",  # Currently active tap turn
            ],
        },
        "Line": {
            "public": False,
            "params": [],
            "attrs": [
                "p_from_mw",  # Active power at "from" side [MW]
                "q_from_mvar",  # Reactive power at "from" side [MVAr]
                "p_to_mw",  # Active power at "to" side [MW]
                "q_to_mvar",  # Reactive power at "to" side [MVAr]
                "max_i_ka",  # Maximum current [KA]
                "length_km",  # Line length [km]
                "pl_mw",  # active power losses of the line [MW]
                "ql_mvar",  # reactive power consumption of the line [MVar]
                "i_from_ka",  # Current at from bus [kA]
                "i_to_ka",  # Current at to bus [kA]
                "loading_percent",  # line loading [%]
                "r_ohm_per_km",  # Resistance per unit length [Ω/km]
                "x_ohm_per_km",  # Reactance per unit length [Ω/km]
                "c_nf_per_km",  # Capactity per unit length [nF/km]
                "in_service",  # Boolean flag (True|False)
            ],
        },
        "Switch": {
            "public": False,
            "params": [],
            "attrs": [
                "et",
                "type",
                "closed",
            ],
        },
        "Storage": {
            "public": False,
            "params": [],
            "attrs": [
                "p_mw",  # load Active power [MW]
                "q_mvar",  # Reactive power [MVAr]
                "max_e_mwh"  # maximum charge level
                "in_service",  # specifies if the load is in service.
                "controllable",  # States if load is controllable or not.
            ],
        },
    },
}

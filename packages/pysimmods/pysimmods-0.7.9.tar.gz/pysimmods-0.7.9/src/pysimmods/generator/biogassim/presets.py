"""This module contains multiple configuration examples for the
biogas plant.

"""

import sys

ALL_PRESETS = [
    (40, 1),
    (80, 1),
    (320, 1),
    (550, 1),
    (373, 1),
    (1250, 1),
    (55, 2),
    (110, 2),
    (220, 2),
    (300, 2),
    (320, 2),
    (2050, 2),
    (555, 3),
    (1500, 3),
]


def biogas_presets(pn_max_kw, **kwargs):
    """Return the parameter configuration for a biogas model from the
    pysimmods package.

    """
    thismodule = sys.modules[__name__]
    num_gens = kwargs.get("num_gens", None)

    possible_p = [val for val in ALL_PRESETS if val[0] == pn_max_kw]

    if num_gens is not None:
        possible_p = [val for val in possible_p if val[1] == num_gens]

    method_params = f"params_{possible_p[0][1]}g_{possible_p[0][0]}kw"
    method_inits = f"inits_{possible_p[0][1]}g_{possible_p[0][0]}kw"

    params = getattr(thismodule, method_params)()
    params["sign_convention"] = "active"

    return params, getattr(thismodule, method_inits)()


def params_1g_40kw():
    """Params for a Biogas plant with 40 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_m3_per_day": 550,
        "cap_gas_m3": 250,
        "gas_fill_min_percent": 2.5,
        "gas_fill_max_percent": 97.5,
        "ch4_concentration_percent": 51.9,
        "num_chps": 1,
        "chp0": {
            "pn_stages_kw": [20, 40],
            "eta_stages_percent": [28.0, 30.0],
            "eta_th_stages_percent": [31.4, 32.0],
            "restarts_per_day": 0,
            "active_min_s": 0,
            "active_max_s_per_day": 18 * 3_600,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_1g_40kw():
    """Init vals for a Biogas plant with 40 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_fill_percent": 50.0,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 20,
        },
    }


def params_1g_80kw():
    """Params for a Biogas plant with 80 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_m3_per_day": 750,
        "cap_gas_m3": 375,
        "gas_fill_min_percent": 2.5,
        "gas_fill_max_percent": 97.5,
        "ch4_concentration_percent": 52.9,
        "num_chps": 1,
        "chp0": {
            "pn_stages_kw": [40, 80],
            "eta_stages_percent": [37.0, 36.7],
            "eta_th_stages_percent": [32.4, 32.0],
            "restarts_per_day": 5,
            "active_min_s": 0,
            "active_max_s_per_day": 18 * 3_600,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_1g_80kw():
    """Init vals for a Biogas plant with 80 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_fill_percent": 50.0,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 40,
        },
    }


def params_1g_320kw():
    """Params for a Biogas plant with 320 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_m3_per_day": 2100,
        "cap_gas_m3": 2000,
        "gas_fill_min_percent": 5.0,
        "gas_fill_max_percent": 95.0,
        "ch4_concentration_percent": 55.3,
        "num_chps": 1,
        "chp0": {
            "pn_stages_kw": [160, 240, 320],
            "eta_stages_percent": [36.6, 37.0, 37.5],
            "eta_th_stages_percent": [31.0, 31.5, 31.9],
            "restarts_per_day": 0,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_1g_320kw():
    """Init vals for a Biogas plant with 320 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_fill_percent": 50.0,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 160,
        },
    }


def params_1g_550kw():
    """Params for a Biogas plant with 550 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_m3_per_day": 5450,
        "cap_gas_m3": 1578,
        "gas_fill_min_percent": 2.0,
        "gas_fill_max_percent": 98.0,
        "ch4_concentration_percent": 55.4,
        "num_chps": 1,
        "chp0": {
            "pn_stages_kw": [275, 330, 440, 550],
            "eta_stages_percent": [31.6, 31.8, 32.0, 32.2],
            "eta_th_stages_percent": [41.0, 42.1, 43.2, 44.2],
            "restarts_per_day": 0,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_1g_550kw():
    """Init vals for a Biogas plant with 550 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_fill_percent": 50.0,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 275,
        },
    }


def params_1g_373kw():
    """Params for a Biogas plant with 375 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_m3_per_day": 2550,
        "cap_gas_m3": 2500,
        "gas_fill_min_percent": 5.0,
        "gas_fill_max_percent": 95.0,
        "ch4_concentration_percent": 58.5,
        "num_chps": 1,
        "chp0": {
            "pn_stages_kw": [121, 252, 373],
            "eta_stages_percent": [33.7, 36.2, 37.9],
            "eta_th_stages_percent": [45.0, 46.0, 47.8],
            "restarts_per_day": 6,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_1g_373kw():
    """Init vals for a Biogas plant with 373 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_fill_percent": 50.0,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 750,
        },
    }


def params_1g_1250kw():
    """Params for a Biogas plant with 1250 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_m3_per_day": 9_750,
        "cap_gas_m3": 9_250,
        "gas_fill_min_percent": 2.5,
        "gas_fill_max_percent": 97.5,
        "ch4_concentration_percent": 50.0,
        "num_chps": 1,
        "chp0": {
            "pn_stages_kw": [750, 1250],
            "eta_stages_percent": [37.0, 41.25],
            "eta_th_stages_percent": [48.0, 44.0],
            "restarts_per_day": 4,
            "active_min_s": 0,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_1g_1250kw():
    """Init vals for a Biogas plant with 1250 kw nominal power and
    one CHP CNG.
    """
    return {
        "gas_fill_percent": 50.0,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 750,
        },
    }


def params_2g_55kw():
    """Params for a Biogas plant with 55 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_m3_per_day": 255,
        "cap_gas_m3": 390,
        "gas_fill_min_percent": 5.0,
        "gas_fill_max_percent": 95.0,
        "ch4_concentration_percent": 50.2,
        "has_heat_storage": False,
        "num_chps": 2,
        "chp0": {
            "pn_stages_kw": [9.0, 18.0],
            "eta_stages_percent": [29.3, 28.7],
            "eta_th_stages_percent": [35.4, 36.1],
            "restarts_per_day": 0,
            "active_min_s": 1 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [18.5, 37.0],
            "eta_stages_percent": [31.4, 32.5],
            "eta_th_stages_percent": [36.1, 36.8],
            "restarts_per_day": 0,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_2g_55kw():
    """Init vals for a Biogas plant with 55 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 27.5,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 18.3,
        },
    }


def params_2g_110kw():
    """Params for a Biogas plant with 110 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_m3_per_day": 950,
        "cap_gas_m3": 1000,
        "gas_fill_min_percent": 2.5,
        "gas_fill_max_percent": 97.5,
        "ch4_concentration_percent": 56.8,
        "has_heat_storage": False,
        "num_chps": 2,
        "chp0": {
            "pn_stages_kw": [27.5, 55.0],
            "eta_stages_percent": [29.7, 31.9],
            "eta_th_stages_percent": [36.4, 37.0],
            "restarts_per_day": 6,
            "active_min_s": 1 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [18.3, 36.6, 55.0],
            "eta_stages_percent": [30.8, 32.2, 33.9],
            "eta_th_stages_percent": [36.1, 36.8, 38.0],
            "restarts_per_day": 6,
            "active_min_s": 1 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_2g_110kw():
    """Init vals for a Biogas plant with 110 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 27.5,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 18.3,
        },
    }


def params_2g_220kw():
    """Params for a Biogas plant with 220 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_m3_per_day": 2000,
        "cap_gas_m3": 1150,
        "gas_fill_min_percent": 2.5,
        "gas_fill_max_percent": 97.5,
        "ch4_concentration_percent": 55.7,
        "has_heat_storage": False,
        "num_chps": 2,
        "chp0": {
            "pn_stages_kw": [55.0, 110.0],
            "eta_stages_percent": [35.4, 34.7],
            "eta_th_stages_percent": [31.4, 31.0],
            "restarts_per_day": 6,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [55.0, 110.0],
            "eta_stages_percent": [35.5, 36.1],
            "eta_th_stages_percent": [38.0, 42.4],
            "restarts_per_day": 6,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_2g_220kw():
    """Init vals for a Biogas plant with 220 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 55.0,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 55.0,
        },
    }


def params_2g_300kw():
    """Params for a Biogas plant with 300 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_m3_per_day": 3030,
        "cap_gas_m3": 1530,
        "gas_fill_min_percent": 2.0,
        "gas_fill_max_percent": 98.0,
        "ch4_concentration_percent": 54.4,
        "has_heat_storage": False,
        "num_chps": 2,
        "chp0": {
            "pn_stages_kw": [75.0, 150.0],
            "eta_stages_percent": [31.1, 32.4],
            "eta_th_stages_percent": [30.8, 31.2],
            "restarts_per_day": 6,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 2 * 3_600,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [75.0, 150.0],
            "eta_stages_percent": [33.0, 33.2],
            "eta_th_stages_percent": [30.0, 30.5],
            "restarts_per_day": 6,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 2 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_2g_300kw():
    """Init vals for a Biogas plant with 300 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 75.0,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 75.0,
        },
    }


def params_2g_320kw():
    """Params for a Biogas plant with 320 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_m3_per_day": 2050,
        "cap_gas_m3": 855,
        "gas_fill_min_percent": 2.0,
        "gas_fill_max_percent": 98.0,
        "ch4_concentration_percent": 63.9,
        "has_heat_storage": False,
        "num_chps": 2,
        "chp0": {
            "pn_stages_kw": [40.0, 80.0, 120.0, 160.0],
            "eta_stages_percent": [31.1, 32.2, 33.3, 34.4],
            "eta_th_stages_percent": [30.8, 31.2, 32.3, 32.3],
            "restarts_per_day": 6,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [85.0, 110.0, 135.0, 160.0],
            "eta_stages_percent": [32.2, 33.0, 33.8, 34.6],
            "eta_th_stages_percent": [30.0, 30.5, 31.0, 31.5],
            "restarts_per_day": 6,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_2g_320kw():
    """Init vals for a Biogas plant with 320 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 80.0,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 85.0,
        },
    }


def params_2g_2050kw():
    """Params for a Biogas plant with 2050 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_m3_per_day": 14_500,
        "cap_gas_m3": 13_000,
        "gas_fill_min_percent": 5,
        "gas_fill_max_percent": 95,
        "ch4_concentration_percent": 50.0,
        "has_heat_storage": False,
        "num_chps": 2,
        "chp0": {
            "pn_stages_kw": [700, 1150],
            "eta_stages_percent": [37.0, 44.0],
            "eta_th_stages_percent": [40.0, 44.0],
            "restarts_per_day": 4,
            "active_min_s": 0,
            "active_max_s_per_day": 16 * 3_600,
            "inactive_min_s": 2 * 3_600,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [600, 900],
            "eta_stages_percent": [37, 40.0],
            "eta_th_stages_percent": [42.0, 43.0],
            "restarts_per_day": 4,
            "active_min_s": 0,
            "active_max_s_per_day": 16 * 3_600,
            "inactive_min_s": 2 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_2g_2050kw():
    """Init vals for a Biogas plant with 2050 kw nominal power and
    two CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 700,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 600,
        },
    }


def params_3g_555kw():
    """Params for a Biogas plant with 555 kw nominal power and
    three CHP CNGs.
    """
    return {
        "gas_m3_per_day": 6000,
        "cap_gas_m3": 2500,
        "gas_fill_min_percent": 5,
        "gas_fill_max_percent": 95,
        "ch4_concentration_percent": 51.6,
        "has_heat_storage": False,
        "num_chps": 3,
        "chp0": {
            "pn_stages_kw": [125, 250],
            "eta_stages_percent": [31.2, 34.7],
            "eta_th_stages_percent": [42.0, 45.9],
            "restarts_per_day": 0,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 18 * 3_600,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [125, 250],
            "eta_stages_percent": [34.3, 36.1],
            "eta_th_stages_percent": [41.9, 43],
            "restarts_per_day": 0,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 18 * 3_600,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
        "chp2": {
            "pn_stages_kw": [27.5, 55],
            "eta_stages_percent": [28.6, 30],
            "eta_th_stages_percent": [35.1, 36.1],
            "restarts_per_day": 0,
            "active_min_s": 2 * 3_600,
            "active_max_s_per_day": 18 * 3_600,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_3g_555kw():
    """Init vals for a Biogas plant with 555 kw nominal power and
    three CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 250,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 125,
        },
        "chp2": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 55,
        },
    }


def params_3g_1500kw():
    """Params for a Biogas plant with 1500 kw nominal power and
    three CHP CNGs.
    """
    return {
        "gas_m3_per_day": 16_040,
        "cap_gas_m3": 25_200,
        "gas_fill_min_percent": 5,
        "gas_fill_max_percent": 95,
        "ch4_concentration_percent": 53.9,
        "has_heat_storage": False,
        "num_chps": 3,
        "chp0": {
            "pn_stages_kw": [
                125.0,
                250.0,
                375.0,
                500.0,
                625.0,
                750.0,
            ],
            "eta_stages_percent": [
                26.1,
                27.0,
                27.3,
                28.0,
                27.7,
                27.5,
            ],
            "eta_th_stages_percent": [
                50.0,
                50.2,
                50.5,
                50.9,
                51.0,
                52.1,
            ],
            "restarts_per_day": 0,
            "active_min_s": 3 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
        "chp1": {
            "pn_stages_kw": [330.0, 440.0, 550],
            "eta_stages_percent": [27.9, 28.5, 29.1],
            "eta_th_stages_percent": [45.9, 47.3, 51.0],
            "restarts_per_day": 0,
            "active_min_s": 1 * 3_600,
            "active_max_s_per_day": 0,
            "inactive_min_s": 0,
            "inactive_max_s_per_day": 0,
        },
        "chp2": {
            "pn_stages_kw": [100, 200],
            "eta_stages_percent": [28.8, 29.9],
            "eta_th_stages_percent": [29.7, 30.1],
            "restarts_per_day": 0,
            "active_min_s": 0,
            "active_max_s_per_day": 0,
            "inactive_min_s": 1 * 3_600,
            "inactive_max_s_per_day": 0,
        },
    }


def inits_3g_1500kw():
    """Init vals for a Biogas plant with 1500 kw nominal power and
    three CHP CNGs.
    """
    return {
        "gas_fill_percent": 50,
        "chp0": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 125.0,
        },
        "chp1": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 330,
        },
        "chp2": {
            "active_s": 0,
            "active_s_per_day": 0,
            "inactive_s": 0,
            "inactive_s_per_day": 0,
            "restarts": 0,
            "p_kw": 100,
        },
    }

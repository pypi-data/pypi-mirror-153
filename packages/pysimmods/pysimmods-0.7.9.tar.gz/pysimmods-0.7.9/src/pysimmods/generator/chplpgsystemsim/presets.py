"""This module contains configurations for chp models.

Example:

    from pysimmods.chpsystemsim import CHPSystem
    chp = CHPSystem(chp_params(7), chp_init(7))

"""
import sys


def chp_presets(p_kw, start_date="2017-01-01 00:00:00+0100", **kwargs):
    """Return the parameter configuration for a chp model
    from the pysimmods package.

    """
    thismodule = sys.modules[__name__]

    if p_kw in (7, 14, 200, 400):
        pmethod = f"_chp_{int(p_kw)}kw_params"
        imethod = f"_chp_{int(p_kw)}kw_init"
    else:
        raise ValueError("Not supported model size {} p_kw".format(p_kw))

    params = getattr(thismodule, pmethod)()
    params["sign_convention"] = "active"
    inits = {
        "chp": getattr(thismodule, imethod)(),
        "household": {
            "start_date": start_date,
            "t_last_3": 2.1,
            "t_last_2": 1.7,
            "t_last_1": 4.2,
        },
    }
    return params, inits


def _chp_7kw_params():
    params = {
        "chp": {
            "p_max_kw": 7.0,
            "p_min_kw": 3.5,
            "p_2_p_th_percent": 257.0,
            "eta_max_percent": 86.1,
            "eta_min_percent": 80.5,
            "own_consumption_kw": 0.55,
            "active_min_s": 0.0,
            "inactive_min_s": 0.0,
            "lubricant_max_l": 10.0,
            "lubricant_ml_per_h": 10.0,
            "storage_cap_l": 1050.0,
            "storage_consumption_kwh_per_day": 0.75,
            "storage_t_min_c": 40.0,
            "storage_t_max_c": 85.0,
        }
    }
    return params


def _chp_7kw_init():
    init_vals = {
        "lubricant_l": 9,
        "active_s": 1800,
        "inactive_s": 0,
        "is_active": True,
        "storage_t_c": 50,
    }
    return init_vals


def _chp_14kw_params():
    params = {
        "chp": {
            "p_max_kw": 14.0,
            "p_min_kw": 7,
            "p_2_p_th_percent": 248.0,
            "eta_max_percent": 87.2,
            "eta_min_percent": 78.4,
            "own_consumption_kw": 0.588,
            "active_min_s": 0.0,
            "inactive_min_s": 0.0,
            "lubricant_max_l": 14.0,
            "lubricant_ml_per_h": 12.5,
            "storage_cap_l": 2100.0,
            "storage_consumption_kwh_per_day": 0.77,
            "storage_t_min_c": 40.0,
            "storage_t_max_c": 85.0,
        }
    }
    return params


def _chp_14kw_init():
    init_vals = {
        "lubricant_l": 9,
        "active_s": 1800,
        "inactive_s": 0,
        "is_active": True,
        "storage_t_c": 50,
    }
    return init_vals


def _chp_200kw_params():
    params = {
        "chp": {
            "p_max_kw": 198,
            "p_min_kw": 99,
            "p_2_p_th_percent": 148.0,
            "eta_max_percent": 88.8,
            "eta_min_percent": 87.1,
            "own_consumption_kw": 2.9,
            "active_min_s": 0.0,
            "inactive_min_s": 0.0,
            "lubricant_max_l": 95.0,
            "lubricant_ml_per_h": 80.0,
            "storage_cap_l": 30_000.0,
            "storage_consumption_kwh_per_day": 1.63,
            "storage_t_min_c": 40.0,
            "storage_t_max_c": 85.0,
        }
    }
    return params


def _chp_200kw_init():
    init_vals = {
        "lubricant_l": 90,
        "active_s": 1800,
        "inactive_s": 0,
        "is_active": True,
        "storage_t_c": 50,
    }
    return init_vals


def _chp_400kw_params():
    params = {
        "chp": {
            "p_max_kw": 400,
            "p_min_kw": 200,
            "p_2_p_th_percent": 128.0,
            "eta_max_percent": 88.7,
            "eta_min_percent": 87.4,
            "own_consumption_kw": 5.3,
            "active_min_s": 0.0,
            "inactive_min_s": 0.0,
            "lubricant_max_l": 155.0,
            "lubricant_ml_per_h": 130.0,
            "storage_cap_l": 60_000.0,
            "storage_consumption_kwh_per_day": 2.13,
            "storage_t_min_c": 40.0,
            "storage_t_max_c": 85.0,
        }
    }
    return params


def _chp_400kw_init():
    init_vals = {
        "lubricant_l": 154,
        "active_s": 1800,
        "inactive_s": 0,
        "is_active": True,
        "storage_t_c": 50,
    }
    return init_vals

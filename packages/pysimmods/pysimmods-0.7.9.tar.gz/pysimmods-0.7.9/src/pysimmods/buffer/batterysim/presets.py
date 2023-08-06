"""Presets for the battery model."""

import sys


def battery_presets(pn_max_kw, **kwargs):

    params = _get_dict(pn_max_kw, cap_kwh=kwargs.get("cap_kwh", pn_max_kw * 5))
    inits = {"soc_percent": 50}

    return params, inits


def _get_dict(pn_max_kw, cap_kwh):
    params = {
        "cap_kwh": cap_kwh,
        "soc_min_percent": 15,
        "p_charge_max_kw": pn_max_kw,
        "p_discharge_max_kw": pn_max_kw,
        "eta_pc": [-2.109566, 0.403556, 97.110770],
    }
    return params

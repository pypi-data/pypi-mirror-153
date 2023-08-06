def diesel_presets(p_max_kw):
    params = _get_dict(p_max_kw)
    inits = {"p_kw": 0, "q_kvar": 0}

    params["sign_convention"] = "active"

    return params, inits


def _get_dict(p_max_kw):
    params = {
        "p_max_kw": p_max_kw,
        "p_min_kw": 0,
        "q_max_kvar": 0,
        "q_min_kvar": 0,
    }
    return params

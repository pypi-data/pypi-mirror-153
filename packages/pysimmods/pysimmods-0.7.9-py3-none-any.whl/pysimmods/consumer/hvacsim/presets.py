"""Configuration of "TK-Anlagen" based on
https://www.tis-gdv.de/tis/tagungen/svt/svt10/weilhart/inhalt-htm/

"""

import sys


def hvac_preset(pn_max_kw, **kwargs):

    params = _get_dict(pn_max_kw, "params")
    inits = _get_dict(pn_max_kw, "init")

    return params, inits


def _get_dict(p_kw, dicttype):

    thismodule = sys.modules[__name__]

    if p_kw in (0.08,):
        method = "hvac_{}w_{}".format(int(p_kw * 1000), dicttype)
    elif p_kw in (2, 60, 100, 230, 343, 1279):
        method = "hvac_{}kw_{}".format(int(p_kw), dicttype)
    else:
        # TODO: find
        raise ValueError(f"Not supported model size {p_kw} p_kw")

    return getattr(thismodule, method)()


def hvac_80w_params():
    """The classic fridge from practical training
    energy informatics.
    """
    params = {
        "p_max_kw": 0.08,
        "eta_percent": 200.0,
        "length": 0.5,
        "width": 0.5,
        "height": 0.5,
        "d_m": 0.02,
        "lambda_w_per_m_k": 0.019,
        "t_min_deg_celsius": 3.0,
        "t_max_deg_celsius": 7.0,
    }
    return params


def hvac_80w_init():
    """The classic fridge from practical training
    energy informatics.
    """
    inits = {
        "mass_kg": 5.0,  # eggs
        "c_j_per_kg_k": 3.18 * 1e3,  # eggs not frozen
        "theta_t_deg_celsius": 4.0,
        "cooling": True,
        "mode": "auto",
    }
    return inits


def hvac_2kw_params():
    """The classic air conditioning from practical
    training energy informatics."""
    params = {
        "p_max_kw": 2.0,
        "eta_percent": 200.0,
        "length": 4.0,
        "width": 5.0,
        "height": 2.5,
        "d_m": 0.25,
        "lambda_w_per_m_k": 0.5,
        "t_min_deg_celsius": 17.0,
        "t_max_deg_celsius": 23.0,
    }
    return params


def hvac_2kw_init():
    """The classic air conditioning from practical
    training energy informatics."""
    inits = {
        "mass_kg": 500.0,
        "c_j_per_kg_k": 2390.0,
        "theta_t_deg_celsius": 21.0,
        "cooling": True,
        "mode": "auto",
    }
    return inits


def hvac_60kw_params():
    """Following the information from the link in the module
    header, this cooling room has an energetic value of approx.
    210 kWh/(m^3*Year) and a storage volume of 800 m^3.

    (All calculations use rounded values)

    This results in a total of 168000 kWh/Year and 460 kWh/Day.

    Assuming a workload of 33%, this cooling house could consume
    up to 1380 kWh/Day maximum, and therefore 57.5 kWh/h.

    The thaw and cool factor allow a bit control over the cooling and
    thawing process. They are set to match the characteristics above.
    """
    params = {
        "p_max_kw": 60,
        "eta_percent": 10.25,
        "length": 20.0,
        "width": 8.0,
        "height": 5.0,
        "d_m": 0.2,
        "lambda_w_per_m_k": 0.12,
        "t_min_deg_celsius": -30.0,
        "t_max_deg_celsius": -18.0,
        "thaw_factor": 5,
        "cool_factor": 1.0,
    }
    return params


def hvac_60kw_init():
    """We calculate the the mass of content in relation to the
    classic air conditioning, which assumes 500kg of oak with a
    specific heat capacity of 2390 J/(kg*K). This goes into the
    equation as 500 kg * 2390 J/(kg*K) = 1195000 J/K.

    However, the cooling house does not store oak, but food.
    Non-froozen food, e.g. apples, have a specific heat capacity
    of 3890 J/(kg*K). To get a similar relation, we calculate
    1195000 J/K / 3890 J/(kg*K) = 311kg, and, subsequently,
    apply the relation of the cooling volumen, which is 50m^3
    for the air conditioning and 800m^3 for the cooling house,
    i.e.: 311 kg * 800 m^3 / 50 m^3 = 4966 kg of food content.
    """
    inits = {
        "mass_kg": 5000.0,
        "c_j_per_kg_k": 3850.0,
        "theta_t_deg_celsius": -22,
        "cooling": True,
        "mode": "auto",
    }
    return inits


def hvac_100kw_params():
    """See explanation of hvac_60kw_params.

    Energetic value: 160 kWh/(m^3*Year)
    Volume: 1800 m^3
    Workload: 33 %
    """
    params = {
        "p_max_kw": 100,
        "eta_percent": 45.0,
        "length": 30.0,
        "width": 10.0,
        "height": 6.0,
        "d_m": 0.2,
        "lambda_w_per_m_k": 0.12,
        "t_min_deg_celsius": -30.0,
        "t_max_deg_celsius": -18.0,
        "thaw_factor": 10,
        "cool_factor": 0.1375,
    }
    return params


def hvac_100kw_init():
    """See explanation of hvac_60kw_init."""
    inits = {
        "mass_kg": 11_200.0,
        "c_j_per_kg_k": 3850.0,
        "theta_t_deg_celsius": -29,
        "cooling": True,
        "mode": "auto",
    }
    return inits


def hvac_230kw_params():
    """See explanation of hvac_60kw_params.

    Energetic value: 140 kWh/(m^3*Year)
    Volume: 4800 m^3
    Workload: 33 %
    """
    params = {
        "p_max_kw": 230,
        "eta_percent": 45.0,
        "length": 40.0,
        "width": 15.0,
        "height": 8.0,
        "d_m": 0.2,
        "lambda_w_per_m_k": 0.14,
        "t_min_deg_celsius": -30.0,
        "t_max_deg_celsius": -18.0,
        "thaw_factor": 13,
        "cool_factor": 0.07,
    }
    return params


def hvac_230kw_init():
    """See explanation of hvac_60kw_init."""
    inits = {
        "mass_kg": 29_856.0,
        "c_j_per_kg_k": 3850.0,
        "theta_t_deg_celsius": -19,
        "cooling": True,
        "mode": "auto",
    }
    return inits


def hvac_343kw_params():
    """See explanation of hvac_60kw_params.

    Energetic value: 120 kWh/(m^3*Year)
    Volume: 10000 m^3
    Workload: 40 %
    """
    params = {
        "p_max_kw": 343,
        "eta_percent": 45.0,
        "length": 50.0,
        "width": 25.0,
        "height": 8.0,
        "d_m": 0.2,
        "lambda_w_per_m_k": 0.15,
        "t_min_deg_celsius": -30.0,
        "t_max_deg_celsius": -18.0,
        "thaw_factor": 15.0,
        "cool_factor": 0.041,
    }
    return params


def hvac_343kw_init():
    """See explanation of hvac_60kw_init."""
    inits = {
        "mass_kg": 62_200.0,
        "c_j_per_kg_k": 3850.0,
        "theta_t_deg_celsius": -26,
        "cooling": True,
        "mode": "auto",
    }
    return inits


def hvac_1279kw_params():
    """See explanation of hvac_60kw_params.

    Energetic value: 70 kWh/(m^3*Year)
    Volume: 72000 m^3
    Workload: 45 %

    * 5040000 kWh/Year
    * 13808 kWh/Day (45%)
    * 30684 kWh/Day (100%)
    * 1279 kWh/h (100%)

    The efficiency is experimentally determined to match the values
    above (see the test file not_a_test_hvac).

    """
    params = {
        "p_max_kw": 1279,
        "eta_percent": 45.0,
        "length": 100.0,
        "width": 60.0,
        "height": 12.0,
        "d_m": 0.2,
        "lambda_w_per_m_k": 0.15,
        "t_min_deg_celsius": -30.0,
        "t_max_deg_celsius": -18.0,
        "thaw_factor": 50.0,  # 0.00235,
        "cool_factor": 0.011,
    }
    return params


def hvac_1279kw_init():
    """See explanation of hvac_60kw_init."""
    inits = {
        "mass_kg": 448_000.0,
        "c_j_per_kg_k": 3850.0,
        "theta_t_deg_celsius": -20,
        "cooling": True,
        "mode": "auto",
    }
    return inits

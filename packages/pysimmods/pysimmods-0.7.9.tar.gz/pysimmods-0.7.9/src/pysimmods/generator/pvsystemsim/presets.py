"""This module containts functions to create configurations for the
:class:`.PVPlantSystem` model.

"""


def pv_preset(
    p_peak_kw,
    eta=0.25,
    cos_phi=0.9,
    q_control="p_set",
    inverter_mode="inductive",
):
    """Return a preset configuration for a PV plant.

    Creates configuration for parameters and initialization values.

    Parameters
    ----------
    p_peak_kw : float
        The targeted peak power of the PV plant.
    eta : float, optional
        The efficiency of the module. Default is 0.25 (25 %).
    cos_phi : float, optional
        The cosinus of the phase angle for apparent power calculation.
        Default is 0.9.
    q_control : str, optional
        Define how reactive power is controlled by the inverter. See
        :class:`.Inverter` for more information. Default is *"p_set"*.
    inverter_mode : str, optional
        Define the inverter mode. Can be *"inductive"* or
        *"capactive"*. Default is *"inductive"*.

    Returns
    -------
    tuple
        A *tuple* of two *dicts* with all necessary parameters and
        initialization values for a :class:`.PVPlantSystem`.

    """
    params = {
        "pv": {"a_m2": p_peak_kw / eta, "eta_percent": eta * 100},
        "inverter": {
            "sn_kva": p_peak_kw / cos_phi,
            "q_control": q_control,
            "cos_phi": cos_phi,
            "inverter_mode": inverter_mode,
        },
        "sign_convention": "active",
    }
    inits = {"pv": {"t_module_deg_celsius": 5.0}, "inverter": None}

    return params, inits

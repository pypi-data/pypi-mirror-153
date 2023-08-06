"""This module contains the input model for the PV system."""
from pysimmods.model.inputs import ModelInputs


class PVSystemInputs(ModelInputs):
    """Input variables for the PV plant system.

    Attributes
    ----------
    cos_phi_set : float
        See :attr:`~.InverterInputs.cos_phi_set`.
    inverter_inductive:: bool
        See _attr:`~.InverterInputs.inverter_inductive`.
    bh_w_per_m2 : float
        See :attr:`~.PVInputs.bh_w_per_m2`.
    dh_w_per_m2 : float
        See :attr:`~.PVInputs.dh_w_per_m2`.
    s_module_w_per_m2 : float
        See :attr:`~.PVInputs.s_module_w_per_m2`.
    t_air_deg_celsius : float
        See :attr:`~.PVInputs.t_air_deg_celsius`.


    """

    def __init__(self):
        super().__init__()

        self.cos_phi_set = None
        self.inverter_inductive = None
        self.bh_w_per_m2 = None
        self.dh_w_per_m2 = None
        self.s_module_w_per_m2 = None
        self.t_air_deg_celsius = None

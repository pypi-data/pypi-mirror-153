"""This module contains the state model for pv."""
from pysimmods.model.state import ModelState


class PVState(ModelState):
    """State parameters of pv model.

    See :class:`pysimmods.model.state.ModelState` for additional
    information.

    Parameters
    ----------
    inits : dict
        Contains the initial configuration of this PV plant. See
        attributes section for specific to the PV plant.

    Attributes
    ----------
    t_module_deg_celsius : float
        Temperature of the module in [°C].

    """

    def __init__(self, inits):
        super().__init__(inits)
        self.t_module_deg_celsius = inits["t_module_deg_celsius"]

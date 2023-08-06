"""This module contains the state model of the chp system."""
from pysimmods.model.state import ModelState


class CHPLPGSystemState(ModelState):
    """captures the state of the chp system

    The references are updated during each step.
    """

    def __init__(self, init_vals):
        super().__init__(init_vals)

        self.p_th_kw = None
        """Current thermal power of the chp in [kW]."""

        self.storage_t_c = None
        """Current temperature of the heat storage in [°C]."""

        self.lubricant_l = None
        """Among of lubricant remaining in [l]."""

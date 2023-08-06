"""This module contains the state model of the chp."""

from pysimmods.model.state import ModelState


class CHPCNGState(ModelState):
    """A CHP CNG state information class."""

    def __init__(self, init_vals):
        super().__init__(init_vals)

        self.active_s = init_vals["active_s"]
        """Time since unit switched to current power level in [s]."""
        self.active_s_per_day = init_vals["active_s_per_day"]
        """Time the unit is active on the current day in [s]."""
        self.inactive_s = init_vals["inactive_s"]
        """Time since unit is switched off in [s]."""
        self.inactive_s_per_day = init_vals["inactive_s_per_day"]
        """Time the unit is inactive on the current day in [s]."""

        self.restarts = init_vals["restarts"]
        """Number of restarts on the current day."""

        self.p_th_kw = None
        """Thermal power generated in [kW]."""
        self.gas_cons_m3 = None
        """Gas consumed in the last step in [m^3]."""

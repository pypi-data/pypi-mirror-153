"""This module contains the state model of the chp."""
from pysimmods.model.state import ModelState


class CHPLPGState(ModelState):
    """A CHP LGP state information class

    This class captures the state of the chp model. States normally
    change during the step-method of this model.

    Parameters
    ----------
    inits : dict
        A *dict* containing initialization parameters for the model.

    Attributes
    ----------
    active_s : int
        Time since unit was switched on in [s].
    inactive_s : int
        Time since unit was switch off in [s].
    is_active : bool
        True if the unit is operating.
    storage_t_c : float
        Stores the current temperature of the heat storage in [°C].
    lubricant_l : float, optional
        Current amount of lubricant in [l]. Defaults to 10.

    """

    def __init__(self, inits):
        super().__init__(inits)

        self.active_s = inits["active_s"]
        self.inactive_s = inits["inactive_s"]
        self.is_active = inits["is_active"]
        self.storage_t_c = inits["storage_t_c"]
        self.lubricant_l = inits.get("lubricant_l", 10)

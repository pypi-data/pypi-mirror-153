"""This module contains the input model for the chp."""
from pysimmods.model.inputs import ModelInputs


class CHPLPGInputs(ModelInputs):
    """A CHP input class

    This class captures the inputs for the chp model. The values need to be
    provided in before calling the step method. However, once an input is set
    it will be reused as long as it is not changed.

    Attributes
    ----------
    e_th_demand_set_kwh : float
        The setpoint for thermal energy demand in [kWh].
    """

    def __init__(self):
        super().__init__()

        self.e_th_demand_set_kwh = None

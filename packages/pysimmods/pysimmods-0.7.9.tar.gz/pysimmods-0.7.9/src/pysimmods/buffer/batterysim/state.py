"""This module contains the state model of the battery."""
from pysimmods.model.state import ModelState


class BatteryState(ModelState):
    """Captures the state variables of the battery model

    State variables normally change during the simulation process. They are
    updated in the step-method of the battery model.

    There is two types of state variables. State variables like *soc_percent*
    which are used in the recalculation of the state variables in the
    step-method of the battery model and such state variables like *p_kw*
    whose current value doesn't affect the update of state variables in the
    step-method.

    The former require the assignment of intial values. Therefore a dictionary
    with intial values for this kind of state variables has to be passed to the
    constructor of the State class. State variables which are not needed as an
    input for calculating the next state in the step-method are initialized
    with None by default.

    Attributes
    ----------
    soc_percent : float
        Current state of charge of battery in percent of capacity.
    eta_percent : float
        Current efficiency of battery in percent.
    _energy_kwh : float
        Current energy of the battery, calculated during the step in
        [kWh].

    """

    def __init__(self, inits):
        super().__init__(inits)

        self.soc_percent = inits["soc_percent"]
        self.eta_percent = None
        self._energy_kwh = None

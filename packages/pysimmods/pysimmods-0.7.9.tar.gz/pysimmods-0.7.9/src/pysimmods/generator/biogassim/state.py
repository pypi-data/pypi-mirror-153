"""This module contains the state model of the Biogas plant."""
from pysimmods.model.state import ModelState


class BiogasState(ModelState):
    """State parameters of the biogas plant model.

    This class captures the state of the biogas model. States normally
    change during the step-method of this model.

    Parameters
    ----------
    inits: dict
        A dictionary containing initialization parameters for the
        biogas model. The :attr:`gas_fill_percent` is the only
        model-specific key that ist required.

    Attributes
    ----------
    gas_fill_percent: float
        Current level of the gas storage in [%].
    gas_prod_m3: float
        Amount of gas produced in current step in [m^3].
    gas_cons_m3: float
        Amount of gas consumed in the current step in [m^3].
    p_th_kw: float
        Thermal power output in [kW].
    gas_critical: bool, optional
        Is true, when storage boundaries are exceeded.
    burn_gas: bool, optional
        Is true, when the upper storage boundary is exceeded.
        Resets to False, when gas_fill_percent gets below 60 %.
    pool_gas: bool, optional
        Is true, when the lower storage boundary is exceeded.
        Resets to False, when gas_fill_percent gets above 40 %.

    """

    def __init__(self, inits):
        super().__init__(inits)
        self.gas_fill_percent = inits["gas_fill_percent"]
        self.gas_prod_m3 = inits.get("gas_prod_m3", None)
        self.gas_cons_m3 = inits.get("gas_cons_m3", None)
        self.p_th_kw = inits.get("p_th_kw", None)
        self.gas_critical = inits.get("gas_critical", False)
        self.burn_gas = inits.get("burn_gas", False)
        self.pool_gas = inits.get("pool_gas", False)

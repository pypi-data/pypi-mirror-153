"""This module contains the state model for HVAC."""
from pysimmods.model.state import ModelState


class HVACState(ModelState):
    """State parameters of the HVAC model.

    See :class:`.ModelState` for additional information.

    Parameters
    ----------
    inits : dict
        Contains the initial configuration of this HVAC model. See
        the attributes section for specific information of the HVAC
        model.

    Attributes
    ----------
    mass_kg : float
        Mass of the content in [kg].
    c_j_per_kg_k : float
        Mean specific heat capacity of refer cargo in [Jkg^-K^-1].
    theta_t_deg_celsius : float
        Time dependent temperature of the model in [°C].
    cooling : bool
        If set to True, the model is cooling, i.e., consuming power.
    mode : str
        The operation mode of this model.

    """

    def __init__(self, inits):
        super().__init__(inits)

        self.mass_kg = inits.get("mass_kg", 500)
        self.c_j_per_kg_k = inits.get("c_j_per_kg_k", 2390)
        self.theta_t_deg_celsius = inits.get("theta_t_deg_celsius", 21)
        self.cooling = inits.get("cooling", True)
        try:
            if self.cooling.lower() in (0, "f", "false"):
                self.cooling = False
        except AttributeError:
            # cooling is already a bool
            pass

        self.mode = inits.get("mode", "auto")

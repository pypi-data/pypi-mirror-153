"""This module contains the input model for the HVAC model."""
from pysimmods.model.inputs import ModelInputs


class HVACInputs(ModelInputs):
    """Input variables of the HVAC model.

    See :class:`.ModelInputs` for additional information. This class
    has no inputs itself. Instead, each of the values is to be
    provided before each step.

    Attributes
    ----------
    t_air_deg_celsius : float
        Temperature of the environment in [°C].

    """

    def __init__(self):
        super().__init__()

        self.t_air_deg_celsius = None

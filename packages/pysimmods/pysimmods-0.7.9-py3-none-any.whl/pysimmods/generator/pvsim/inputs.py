"""This module contains the input model for PV plant."""
from pysimmods.model.inputs import ModelInputs


class PVInputs(ModelInputs):
    """Input variables of PV plant model.

    See :class:`pysimmods.model.inputs.ModelInputs` for additional
    information. This class has no inputs itself. Instead, each
    of the values is to be provided before each step.

    Attributes
    ----------
    bh_w_per_m2 : float
        Beam horizontal (direct solar radiation on horizontal plane)
        in [W/m²].
    dh_w_per_m2 : float
        Diffuse horizontal (diffuse solar radiation on horizontal
        plane) in [W/m²].
    s_module_w_per_m2 : float
        Solar irradiance on module surface in [W/m²]. Must be set
        as input instead of :attr:`bh_w_per_m2` and
        :attr:`dh_w_per_m2`, if
        :attr:`~.PVConfig.has_external_irradiance_model` is set to
        True. Otherwise, this attribute is ignored.
    t_air_deg_celsius:
        Air temperature in [°C].
    """

    def __init__(self):
        super().__init__()
        self.bh_w_per_m2 = None
        self.dh_w_per_m2 = None
        self.s_module_w_per_m2 = None
        self.t_air_deg_celsius = None

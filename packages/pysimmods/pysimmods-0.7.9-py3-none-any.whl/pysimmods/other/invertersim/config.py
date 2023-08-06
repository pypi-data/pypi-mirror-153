"""This module contains the config model for the inverter."""
from pysimmods.model.config import ModelConfig
from pysimmods.model.qgenerator import QControl


class InverterConfig(ModelConfig):
    """Inverter config

    Parameter
    ---------
    params : dict
        Contains configuration parameters of the inverter. See
        *attributes* section for more information.

    Attributes
    ----------
    sn_kva : float
        Nominal apparent power of the inverter in [kVA].
    q_control : str, optional
        Set the mode for the inverter. Can be one of *'p_set'*,
        *'q_set'*, *'cos_phi_set'*, *'pq_set'*, and *'qpset.'* Default
        is *'p_set'*. See :class:`~.Inverter` for more information
        about the different modes.
    cos_phi : float, optional
        Cosinus of the phase angle for *q_control* modes with constant
        *cos_phi*. Default is 0.9.
    inverter_mode : str, optional
        Specifies whether the inverter is *'capacitive'* or
        *'inductive'*. Default is *'capacitive'*.

    """

    def __init__(self, params):
        super().__init__(params)

        self.s_max_kva = params["sn_kva"]
        self._controls = [
            "p_set",
            "q_set",
            "cos_phi_set",
            "pq_set",
            "qp_set",
        ]
        self.q_control = QControl[params.get("q_control", "p_set").upper()]
        self.cos_phi = params.get("cos_phi", 0.9)
        self.inverter_mode = params.get("inverter_mode", "capacitive")

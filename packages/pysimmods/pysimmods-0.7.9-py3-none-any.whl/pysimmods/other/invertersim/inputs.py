"""This module contains the input model for the inverter."""


from distutils.util import strtobool


class InverterInputs:
    """Inverter inputs.

    This model does not inherit from the :class:`~.ModelInputs`,
    because those inputs are not required for the inverter.

    Attributes
    ----------
    p_in_kw : float
        Incoming (available) active power in [kW]
    p_set_kw : float
        Target active power in [kW]. Only used in the *'p_set'*,
        *'pq_set'*, and *'qp_set'* modes of the inverter.
    q_set_kw : float
        Target reactive power in [kVAr]. Only used in the *'q_set'*,
        *'pq_set'*, and *'qp_set'* modes of the inverter.
    cos_phi_set : float
        Target cos phi between 0 and 1. Only used in the
        *'cos_phi_set'* mode of the inverter.
    inverter_inductive: bool
        If True, the inductive inverter mode will used for the next
        step. Otherwise, capacitive mode is used. If not set, the
        inverter mode from the config is used.
    """

    def __init__(self):
        self.p_in_kw = None
        self.p_set_kw = None
        self.q_set_kvar = None
        self.cos_phi_set = None
        self._inductive = None

    def reset(self):
        self.p_in_kw = None
        self.p_set_kw = None
        self.q_set_kvar = None
        self.cos_phi_set = None
        self._inductive = None

    @property
    def inductive(self):
        if self._inductive:
            return 1
        else:
            return 0

    @inductive.setter
    def inductive(self, val):
        if val is None or isinstance(val, bool):
            self._inductive = val
        elif isinstance(val, str):
            self._inductive = strtobool(val)
        elif val != 0:
            self._inductive = True
        else:
            self._inductive = False

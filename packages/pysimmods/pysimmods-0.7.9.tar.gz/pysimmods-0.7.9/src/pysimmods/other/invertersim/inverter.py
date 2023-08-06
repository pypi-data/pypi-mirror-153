"""This module contains an inverter model"""

import math
from copy import copy

from pysimmods.other.invertersim.config import InverterConfig
from pysimmods.other.invertersim.inputs import InverterInputs
from pysimmods.other.invertersim.state import InverterState
from pysimmods.model.qgenerator import QGenerator, QControl


class Inverter(QGenerator):
    """Inverter model

    Supports five different modes:

    - *p_set*: p_set_kw is provided, cos phi remains constant and
      q_kvar is calculated with sqrt(s^2-p^2).
    - *q_set*: q_set_kvar is provided, cos phi remains constant and
      p_kw is calculated with sqrt(s^2-q^2)
    - *cos_phi_set*: cos phi is provided, p_kw is calculated from
      p_in_kw and q_kvar is calculated accordingly.
    - *pq_set*: p_set_kw and q_set_kvar are provided, with p being
      prioritized, i.e., q is limited by sqrt(s^2-p^2), and cos phi is
    calculated with p/s.
    - *qp_set*: q_set_kvar and p_set_kw are provided, with q being
      prioritized, i.e., p is limited by sqrt(s^2-q^2), and cos phi is
      calculated with p/s

    Parameters
    ----------
    params : dict
        A *dict* containing configuration parameters.
    inits : dict, optional
        A *dict* containing initialization parameters.

    Attributes
    ----------
    config : :class:`~.InverterConfig`
        Configuration parameters of the inverter.
    state : :class:`~.InverterState`
        Initialization parameters of the inverter.
    inputs : :class:`~.InverterInputs`
        Input parameters of the inverter.

    """

    def __init__(self, params, inits=None):
        if inits is None:
            inits = dict()
        self.config = InverterConfig(params)
        self.state = InverterState(inits)
        self.inputs = InverterInputs()

    def step(self):
        """Perform simulation step"""
        next_state = copy(self.state)

        self._check_inputs()

        next_state._inductive = self.inputs._inductive

        if self.config.q_control == QControl.P_SET:
            self._calc_p_set(next_state)

        elif self.config.q_control == QControl.Q_SET:
            self._calc_q_set(next_state)

        elif self.config.q_control == QControl.COS_PHI_SET:
            self._calc_cos_phi_set(next_state)

        elif self.config.q_control == QControl.PQ_SET:
            self._calc_pq_set(next_state)

        elif self.config.q_control == QControl.QP_SET:
            self._calc_qp_set(next_state)

        if next_state.inductive:
            next_state.q_kvar *= -1

        self.state = next_state
        self.inputs.reset()

    def _check_inputs(self):
        if self.inputs.p_set_kw is None:
            self.inputs.p_set_kw = self.inputs.p_in_kw

        if self.inputs.q_set_kvar is None:
            self.inputs.q_set_kvar = self.config.s_max_kva

        if self.inputs.cos_phi_set is None:
            self.inputs.cos_phi_set = self.config.cos_phi

        if self.inputs._inductive is None:
            self.inputs._inductive = self.config.inverter_mode == "inductive"

    def _calc_p_set(self, next_state):

        # Current active power
        p_kw = min(abs(self.inputs.p_in_kw), abs(self.inputs.p_set_kw))

        # Check constraints for apparent power
        s_kva = p_kw / self.config.cos_phi
        s_kva = min(s_kva, self.config.s_max_kva)

        # Check constraints for active power
        p_max_kw = s_kva * self.config.cos_phi
        p_kw = min(p_kw, p_max_kw)

        # Current reactive power
        q_kvar = (s_kva**2 - p_kw**2) ** 0.5
        q_max_kvar = (self.config.s_max_kva**2 - p_kw**2) ** 0.5
        q_kvar = min(q_max_kvar, q_kvar)

        # Update state
        next_state.p_kw = p_kw
        next_state.q_kvar = q_kvar
        next_state.cos_phi = self.config.cos_phi

    def _calc_q_set(self, next_state):

        # Check constraints for reactive power
        phi = math.acos(self.config.cos_phi)
        q_max_kvar = self.config.s_max_kva * math.sin(phi)
        q_kvar = min(abs(self.inputs.q_set_kvar), q_max_kvar)

        # Check constraints for active power
        p_max_kw = (self.config.s_max_kva**2 - q_kvar**2) ** 0.5
        p_kw = min(abs(self.inputs.p_in_kw), p_max_kw)

        # Update state
        next_state.q_kvar = q_kvar
        next_state.p_kw = p_kw
        next_state.cos_phi = self.config.cos_phi

    def _calc_cos_phi_set(self, next_state):

        # Check cos phi input

        # Check constraints for apparent power
        s_kva = abs(self.inputs.p_in_kw) / self.inputs.cos_phi_set
        s_kva = min(s_kva, self.config.s_max_kva)

        # Check constraints for active power
        p_max_kw = s_kva * self.inputs.cos_phi_set
        p_kw = min(abs(self.inputs.p_in_kw), p_max_kw)

        # Calculate reactive power
        q_kvar = (s_kva**2 - p_kw**2) ** 0.5

        # Update state
        next_state.p_kw = p_kw
        next_state.q_kvar = q_kvar
        next_state.cos_phi = self.inputs.cos_phi_set

    def _calc_pq_set(self, next_state):

        # Calculate active power
        p_kw = min(abs(self.inputs.p_in_kw), abs(self.inputs.p_set_kw))

        # Check constraints for reactive power
        q_max_kvar = (self.config.s_max_kva**2 - p_kw**2) ** 0.5
        q_kvar = min(q_max_kvar, abs(self.inputs.q_set_kvar))

        # Calculate cos phi
        cos_phi = p_kw / self.config.s_max_kva

        # Update state
        next_state.p_kw = p_kw
        next_state.q_kvar = q_kvar
        next_state.cos_phi = cos_phi

    def _calc_qp_set(self, next_state):

        # Calculate reactive power
        q_kvar = abs(self.inputs.q_set_kvar)
        q_kvar = min(q_kvar, self.config.s_max_kva)

        # Calculate active power
        p_kw = min(abs(self.inputs.p_in_kw), abs(self.inputs.p_set_kw))

        # Check constraints for active power
        p_max_kw = (
            self.config.s_max_kva**2 - self.inputs.q_set_kvar**2
        ) ** 0.5
        p_kw = min(p_max_kw, p_kw)

        # Calculate cos phi
        cos_phi = p_kw / self.config.s_max_kva

        # Update state
        next_state.p_kw = p_kw
        next_state.q_kvar = q_kvar
        next_state.cos_phi = cos_phi

    def set_q_kvar(self, q_kvar: float) -> None:
        q_min = self.get_qn_min_kvar()
        q_max = self.get_qn_max_kvar()
        if self.config.inverter_mode == "capacitive":
            q_kvar *= -1

        if q_kvar * self.config.gsign > 0:
            # Consider capacitive and inductive
            q_kvar = abs(q_kvar)
            if q_kvar < q_min:
                self.inputs.q_set_kvar = 0
            else:
                self.inputs.q_set_kvar = min(q_max, q_kvar)
        else:
            self.inputs.q_set_kvar = 0

from .generator import Generator
from enum import Enum
import math


class QControl(Enum):
    P_SET = 0
    PQ_SET = 1
    Q_SET = 2
    QP_SET = 3
    COS_PHI_SET = 4


P_DOMINATED = [QControl.P_SET, QControl.PQ_SET]
Q_DOMINATED = [QControl.Q_SET, QControl.QP_SET]
COS_PHI_DOMINATED = [QControl.COS_PHI_SET]


class QGenerator(Generator):
    """A generator subtype model with reactive power support.

    The set_percent and get_percent_in functions behave differently
    depending on the q_control attribute of the model.
    """

    def set_q_kvar(self, q_kvar: float) -> None:
        q_min = self.get_qn_min_kvar()
        q_max = self.get_qn_max_kvar()

        if q_kvar * self.config.gsign > 0:
            # Consider capacitive and inductive
            q_kvar = abs(q_kvar)
            if q_kvar < q_min:
                self.inputs.q_set_kvar = 0
            else:
                self.inputs.q_set_kvar = min(q_max, q_kvar)
        else:
            self.inputs.q_set_kvar = 0

    def get_q_kvar(self) -> float:
        return self.state.q_kvar * self.config.gsign

    def set_cos_phi(self, cos_phi) -> None:
        self.inputs.cos_phi = max(0, min(1, cos_phi))

    def get_cos_phi(self) -> float:
        return self.state.cos_phi

    def get_percent_in(self):

        if self.config.q_control in P_DOMINATED:
            p_kw = self.inputs.p_set_kw
            if p_kw is None:
                return None
            if p_kw > 0:
                val = abs(p_kw)
                val_min = self.get_pn_min_kw()
                val_max = self.get_pn_max_kw()
            else:
                return 0
        if self.config.q_control in Q_DOMINATED:
            q_kvar = self.inputs.q_set_kvar
            if q_kvar is None:
                return None
            if q_kvar > 0:
                val = abs(q_kvar)
                val_min = self.get_qn_min_kvar()
                val_max = self.get_qn_max_kvar()
            else:
                return 0
        if self.config.q_control in COS_PHI_DOMINATED:
            val = self.inputs.cos_phi
            if val is None:
                return None
            return val if self.config.use_decimal_percent else val * 100

        decimal = (val - val_min) / (val_max - val_min)
        if decimal < 0:
            return 0
        decimal = max(0.0001, decimal)

        if self.config.use_decimal_percent:
            return decimal
        else:
            return decimal * 100

    def set_percent(self, percentage):

        self.inputs.cos_phi = self.config.cos_phi
        if self.config.q_control == QControl.P_SET:
            if percentage <= 0:
                self.inputs.p_set_kw = 0
                return
            self._set_percent_p(percentage)

        elif self.config.q_control == QControl.Q_SET:
            if percentage <= 0:
                self.inputs.q_set_kvar = 0
                return
            self._set_percent_q(percentage)

        elif self.config.q_control == QControl.PQ_SET:
            self.inputs.cos_phi = None
            if percentage <= 0:
                self.inputs.p_set_kw = 0
                self.inputs.q_set_kvar = 0
                return
            self._set_percent_p(percentage)
            self.inputs.q_set_kvar = math.sqrt(
                self.config.s_max_kva**2 - self.inputs.p_set_kw**2
            )

        elif self.config.q_control == QControl.QP_SET:
            self.inputs.cos_phi = None
            if percentage <= 0:
                self.inputs.p_set_kw = 0
                self.inputs.q_set_kvar = 0
                return
            self._set_percent_q(percentage)
            p_set_kw = math.sqrt(
                self.config.s_max_kva**2 - self.inputs.q_set_kvar**2
            )
            if p_set_kw < self.get_pn_min_kw():
                self.inputs.p_set_kw = 0
            else:
                self.inputs.p_set_kw = min(self.get_pn_max_kw(), p_set_kw)

        elif self.config.q_control == QControl.COS_PHI_SET:
            if self.config.use_decimal_percent:
                decimal = max(min(percentage, 1.0), 0.0)
            else:
                # Internally, decimal percentage is used.
                decimal = max(min(percentage, 100.0), 0.0) / 100.0

            self.inputs.cos_phi = decimal

    def get_qn_min_kvar(self) -> float:
        return 0

    def get_qn_max_kvar(self) -> float:
        return self.config.s_max_kva

    def _set_percent_p(self, percentage):

        if self.config.use_decimal_percent:
            decimal = max(min(abs(percentage), 1.0), 0.0)
        else:
            # Internally, decimal percentage is used.
            decimal = max(min(abs(percentage), 100.0), 0.0) / 100.0

        if decimal == 0:
            self.inputs.p_set_kw = 0
        if decimal <= 0.0001:
            # Map values lower than 0.01 % to minimum power
            decimal = 0

        p_max_kw = self.get_pn_max_kw()
        p_min_kw = self.get_pn_min_kw()
        self.inputs.p_set_kw = p_min_kw + decimal * (p_max_kw - p_min_kw)

    def _set_percent_q(self, percentage):
        if percentage <= 0:
            self.inputs.q_set_kvar = 0
            return
        if self.config.use_decimal_percent:
            decimal = max(min(abs(percentage), 1.0), 0.0)
        else:
            # Internally, decimal percentage is used.
            decimal = max(min(abs(percentage), 100.0), 0.0) / 100.0

        if decimal == 0:
            self.inputs.q_set_kvar = 0

        q_min = self.get_qn_min_kvar()
        q_max = self.get_qn_max_kvar()
        self.inputs.q_set_kvar = q_min + decimal * (q_max - q_min)

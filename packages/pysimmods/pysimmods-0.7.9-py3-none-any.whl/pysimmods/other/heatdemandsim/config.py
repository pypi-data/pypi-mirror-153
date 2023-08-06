"""This module contains the config information for the heat demand
model.

"""


class HeatDemandConfig:
    """Captures the configuration variables of the heat demand model."""

    def __init__(self, params):
        self.const_a = params.get("A")
        self.const_b = params.get("B")
        self.const_c = params.get("C")
        self.const_d = params.get("D")
        self.const_v_0 = params.get("V_0")
        self.const_m_h = params.get("M_H")
        self.const_b_h = params.get("B_H")
        self.const_m_w = params.get("M_W")
        self.const_b_w = params.get("B_W")

        self.load_profile = params.get("load_profile")
        self.consumer_const = params.get("consumer_constant")
        self.weekday_const = params.get("weekday_constants")

        self.degree_of_efficiency = 0.93

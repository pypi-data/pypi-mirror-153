"""This module contains the config model for the chp system."""
from pysimmods.model.config import ModelConfig

from pysimmods.generator.chplpgsim.config import CHPLPGConfig
from pysimmods.other.heatdemandsim.config import HeatDemandConfig


class CHPLPGSystemConfig(ModelConfig):
    """captures the configs for the chp system's components"""

    def __init__(self, params):
        super().__init__(params)

        self.house = HeatDemandConfig(params["household"])
        self.chp = CHPLPGConfig(params["chp"])

        self.default_schedule = self.chp.default_schedule

    @property
    def p_min_kw(self):

        return self.chp.p_min_kw

    @property
    def p_max_kw(self):
        return self.chp.p_max_kw

    @property
    def q_min_kvar(self):
        return self.chp.q_min_kvar

    @property
    def q_max_kvar(self):
        return self.chp.q_max_kvar

"""This module contains the input model for the chp system."""
from pysimmods.model.inputs import ModelInputs
from pysimmods.generator.chplpgsim.inputs import CHPLPGInputs
from pysimmods.other.heatdemandsim.inputs import HeatDemandInputs


class CHPLPGSystemInputs(ModelInputs):
    """captures the inputs of the chp system"""

    def __init__(self):
        super().__init__()

        self.day_avg_t_air_deg_celsius = None
        """Average temperature of the current day in [°C]."""

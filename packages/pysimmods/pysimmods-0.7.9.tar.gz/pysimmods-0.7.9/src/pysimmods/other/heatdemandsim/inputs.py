"""This module contains the input information of the heat demand
model.
"""


class HeatDemandInputs:
    """Captures the inputs of the heat demand model"""

    def __init__(self):
        self.step_size = None
        self.day_avg_t_air_deg_celsius = None

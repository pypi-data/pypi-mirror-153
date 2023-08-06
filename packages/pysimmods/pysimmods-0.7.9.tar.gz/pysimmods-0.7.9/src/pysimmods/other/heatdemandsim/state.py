"""This module contains the state information of the heat demand model.
"""

from datetime import datetime
from pysimmods.util.date_util import GER


class HeatDemandState:
    """Captures the state of the heat demand model"""

    def __init__(self, inits):

        start_date = inits["start_date"]
        if isinstance(start_date, str):
            self.now_dt = datetime.strptime(start_date, GER)
        else:
            self.now_dt = start_date

        self.t_last_3_deg_celsius = inits.get("t_last_3_deg_celsius", 10.3)
        self.t_last_2_deg_celsius = inits.get("t_last_2_deg_celsius", 10.3)
        self.t_last_1_deg_celsius = inits.get("t_last_1_deg_celsius", 10.3)

        self.e_th_kwh = None

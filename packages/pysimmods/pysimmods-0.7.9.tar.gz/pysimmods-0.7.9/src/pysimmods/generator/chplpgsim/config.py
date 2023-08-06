"""This module contains the config model for the CHP LPG."""
from pysimmods.model.config import ModelConfig


class CHPLPGConfig(ModelConfig):
    """Config parameters of the CHP LPG.

    This class capturs the configuration parameters of the chp model.

    Parameters
    ----------
    params : dict
        A dictionary containing the configuration parameters.

    Attributes
    ----------
    pn_min_kw : float
        Minimal nominal electrical power output in [kW].
    pn_max_kw : float
        Maximal nominal electrical power output in [kW].
    p_2_p_th_percent : float
        Ratio to compute thermal output from electrical power in [%].
    eta_min_percent : float
        Minimal total efficiency regarding electrical and thermal power
        in [%].
    eta_max_percent : float
        Maximal total efficiency regarding electrical and thermal power
        in [%].
    own_consumption_kw : float
        Own electrical power consumption of the unit [kW].
    active_min_s : int
        Minimal active time of the unit in [s].
    inactive_min_s : int
        Minimal inactive time of the unit in [s].
    lubricant_max_l : float
        Capacity of the lubricant storage in [l].
    lubricant_ml_per_h : float
        Consumption of lubricant per hour in [ml/h].

    """

    def __init__(self, params):
        super().__init__(params)

        self.p_min_kw = abs(params["p_min_kw"])
        self.p_max_kw = abs(params["p_max_kw"])

        self.p_2_p_th_percent = params["p_2_p_th_percent"]
        self.eta_min_percent = params["eta_min_percent"]
        self.eta_max_percent = params["eta_max_percent"]
        self.own_consumption_kw = params["own_consumption_kw"]
        self.active_min_s = params["active_min_s"]
        self.inactive_min_s = params["inactive_min_s"]

        self.lubricant_max_l = params["lubricant_max_l"]
        self.lubricant_ml_per_h = params["lubricant_ml_per_h"]

        self.default_schedule = [
            50,
            50,
            50,
            50,
            50,
            100,
            100,
            100,
            100,
            50,
            50,
            50,
            100,
            100,
            50,
            50,
            50,
            100,
            100,
            100,
            100,
            50,
            50,
            50,
        ]

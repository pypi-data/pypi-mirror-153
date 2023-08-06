"""This module contains the contains the config model for HVAC."""

from pysimmods.model.config import ModelConfig


class HVACConfig(ModelConfig):
    """Config parameters of the HVAC model.

    Parameters
    ----------
    params : dict
        Contains the configuration for the HVAC model. See attribute
        section for more information about the parameters, attributes
        marked with *(Input)* can or must be provided.

    Attributes
    ----------
    pn_min_kw : float
        (Input) Nominal minimal power output in [kW].
    pn_max_kw : float
        (Input) Nominal power output in [kW].
    eta_percent : float
        (Input) Efficiency of the model in [%].
    l_m : float
        (Input) The length of the room to be cooled in [m].
    w_m : float
        (Input) The width of the room to be cooled in [m].
    h_m : float
        (Input) The height of the room to be cooled in [m].
    v_m3 : float
        The volume of the room to be cooled in [m³]. Is calculated
        from l_m, w_m, and h_m.
    a_m2 : float
        Surface of the room to be cooled in [m²]. Is calculated from
        l_m, w_m, and h_m.
    d_m : float
        Thickness of isolation in [m].
    lambda_w_per_m_k : float
        (Input) Thermal conductivity of isolation in [W*m^-1*K^-1].
    alpha : float
        Calculated from lambda_w_per_m_k, a_m2, and d_m.
    t_min_deg_celsius : float
        (Input) When this temperature is reached, the HVAC starts
        cooling, in [°C].
    t_max_deg_celsius : float
        (Input) When this temperature is reached, the HVAC stops
        cooling, in [°C].
    thaw_factor : float, optional
        Extra factor to control the speed of the thawing process.
        Defaults to 1.0.
    cool_factor : float, optional
        Extra factor control the speed of the cooling process.
        Defaults to 1.0.

    """

    def __init__(self, params):
        super().__init__(params)

        self.p_min_kw = 0
        self.p_max_kw = params.get("p_max_kw", 2)
        self.eta_percent = params.get("eta_percent", 200.0)
        self.l_m = params.get("l_m", 4)
        self.w_m = params.get("w_m", 5)
        self.h_m = params.get("h_m", 2.5)
        self.d_m = params.get("d_m", 0.25)
        self.lambda_w_per_m_k = params.get("lambda_w_per_m_k", 0.5)
        self.t_min_deg_celsius = params.get("t_min_deg_celsius", 17)
        self.t_max_deg_celsius = params.get("t_max_deg_celsius", 23)

        self.a_m2 = (
            self.l_m * self.w_m + self.l_m * self.h_m + self.w_m * self.h_m
        ) * 2
        self.v_m3 = self.l_m * self.w_m * self.h_m
        self.alpha = self.lambda_w_per_m_k * self.a_m2 / self.d_m

        self.thaw_factor = params.get("thaw_factor", 1.0)
        self.cool_factor = params.get("cool_factor", 1.0)

        # Model follows cooling demand;
        # Use ScheduleModel to set schedules
        self.default_schedule = None

        # self.default_schedule = list()
        # for _ in range(8):
        #     self.default_schedule.extend([80, 10, 10])

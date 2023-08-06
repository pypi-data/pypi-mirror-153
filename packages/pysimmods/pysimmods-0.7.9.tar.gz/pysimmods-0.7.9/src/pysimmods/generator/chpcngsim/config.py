"""This module contains the config model for the chp."""
from pysimmods.model.config import ModelConfig


class CHPCNGConfig(ModelConfig):
    """A CHP CNG configuration parameter class."""

    def __init__(self, params):
        super().__init__(params)

        self.pn_stages_kw = params["pn_stages_kw"]
        self.pn_stages_kw = [abs(stage) for stage in self.pn_stages_kw]
        """Possible electrial power stages in [kW].
        The power level 0 (unit off) should not be included.
        """
        self.p_max_kw = max(self.pn_stages_kw)
        self.p_min_kw = min(self.pn_stages_kw)

        self.eta_stages_percent = params["eta_stages_percent"]
        """Electrical efficiency at each power stage in [%]."""
        self.eta_th_stages_percent = params["eta_th_stages_percent"]
        """Thermal efficiency at each power state in [%]."""

        self.restarts_per_day = params["restarts_per_day"]
        """Allowed restarts per day."""
        self.active_min_s = params["active_min_s"]
        """Minimal active time of the unit in [s]."""
        self.active_max_s_per_day = params["active_max_s_per_day"]
        """Maximal cumulated active time per day in [s]."""
        self.inactive_min_s = params["inactive_min_s"]
        """Minimal time to be inactive in [s]."""
        self.inactive_max_s_per_day = params["inactive_max_s_per_day"]
        """Maximal cumulated inactive time per day in [s]."""

        self.e_ch4_kwh = 9.94
        """Energy of methane cas in [kWh]."""
        self.ch4_concentration_percent = params.get(
            "ch4_concentration_percent", 50.302
        )
        """Concentration of methane gas in [%]."""

        self.default_schedule = [50] * 24

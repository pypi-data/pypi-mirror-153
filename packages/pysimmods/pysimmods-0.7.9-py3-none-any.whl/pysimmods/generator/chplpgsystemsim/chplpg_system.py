"""
This module contains a model of a chp system with a chp and a
household. The household has a heat demand which allows the chp
to run for at least 5000 hours in a year.

"""
from pysimmods.generator.chplpgsim import CHPLPG
from pysimmods.model.generator import Generator
from pysimmods.other.heatdemandsim.heatdemand import create_heatdemand

from .config import CHPLPGSystemConfig
from .inputs import CHPLPGSystemInputs
from .state import CHPLPGSystemState


class CHPLPGSystem(Generator):
    """CHP system with CHP and household"""

    def __init__(self, params, inits):

        # First, create the chp
        params["chp"]["sign_convention"] = params.get(
            "sign_convention", "passive"
        )
        self.chp = CHPLPG(params["chp"], inits["chp"])

        # Get the thermal capabilities of the chp
        p_th_min_kw = (
            self.chp.config.p_min_kw * self.chp.config.p_2_p_th_percent * 0.01
        )

        params.setdefault("household", dict())
        params["household"]["chp_p_th_prod_kw"] = p_th_min_kw

        # Second, create an appropriate household
        self.heatdemand = create_heatdemand(
            params["household"], inits["household"]
        )

        self.config = CHPLPGSystemConfig(params)
        self.state = CHPLPGSystemState(inits)
        self.inputs = CHPLPGSystemInputs()

    def step(self):
        """Perform a simulation step"""

        # First step the household
        self.heatdemand.inputs.step_size = self.inputs.step_size
        self.heatdemand.inputs.day_avg_t_air_deg_celsius = (
            self.inputs.day_avg_t_air_deg_celsius
        )
        self.heatdemand.step()

        # Second step the chp
        p_set_kw = self._check_setpoint()
        self.chp.set_now_dt(self.inputs.now_dt)
        self.chp.inputs.e_th_demand_set_kwh = self.heatdemand.state.e_th_kwh
        self.chp.set_step_size(self.inputs.step_size)
        self.chp.set_p_kw(p_set_kw * self.config.gsign)
        self.chp.step()

        # Update the references
        self.state.p_kw = self.chp.state.p_kw
        self.state.q_kvar = self.chp.state.q_kvar
        self.state.p_th_kw = self.chp.state.p_th_kw
        self.state.storage_t_c = self.chp.state.storage_t_c
        self.state.lubricant_l = self.chp.state.lubricant_l

        self.inputs.reset()

    def _check_setpoint(self):
        setpoint = self.inputs.p_set_kw
        if setpoint is not None:
            return abs(setpoint)
        hour = self.inputs.now_dt.hour
        default = self.config.default_schedule[hour]
        setpoint = self.config.p_max_kw * default / 100

        return abs(setpoint)

    def get_state(self):
        """Get state"""
        state_dict = {
            "household": self.heatdemand.get_state(),
            "chp": self.chp.get_state(),
        }
        return state_dict

    def set_state(self, state_dict):
        """Set state"""
        self.heatdemand.set_state(state_dict["household"])
        self.chp.set_state(state_dict["chp"])

        self.state.p_kw = self.chp.state.p_kw
        self.state.q_kvar = self.chp.state.q_kvar
        self.state.p_th_kw = self.chp.state.p_th_kw
        self.state.storage_t_c = self.chp.state.storage_t_c
        self.state.lubricant_l = self.chp.state.lubricant_l

    # @property
    # def set_percent(self):
    #     return self.chp.set_percent

    # @set_percent.setter
    # def set_percent(self, value):
    #     self.chp.set_percent = value
    #     self.inputs.p_set_kw = self.chp.inputs.p_set_kw

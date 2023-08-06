"""This module contains a model of a pv system with pv modules and an
inverter"""
from pysimmods.generator.pvsim.pvp import PhotovoltaicPowerPlant
from pysimmods.generator.pvsystemsim.config import PVSystemConfig
from pysimmods.generator.pvsystemsim.inputs import PVSystemInputs
from pysimmods.generator.pvsystemsim.state import PVSystemState
from pysimmods.model.qgenerator import QGenerator
from pysimmods.other.invertersim.inverter import Inverter


class PVPlantSystem(QGenerator):
    """Pv system with pv modules and inverter"""

    def __init__(self, params, inits):
        self.config = PVSystemConfig(params)
        self.inputs = PVSystemInputs()
        self.state = PVSystemState(inits)
        self.pv = PhotovoltaicPowerPlant(params["pv"], inits["pv"])
        self.inverter = Inverter(params["inverter"])

    def step(self):
        """Perform simulation step"""

        # Step the pv plant
        self.pv.inputs.bh_w_per_m2 = self.inputs.bh_w_per_m2
        self.pv.inputs.dh_w_per_m2 = self.inputs.dh_w_per_m2
        self.pv.inputs.s_module_w_per_m2 = self.inputs.s_module_w_per_m2
        self.pv.inputs.t_air_deg_celsius = self.inputs.t_air_deg_celsius
        self.pv.inputs.step_size = self.inputs.step_size
        self.pv.inputs.now_dt = self.inputs.now_dt

        self.pv.step()

        # Step the inverter
        self.inverter.inputs.p_in_kw = self.pv.state.p_kw
        self.inverter.inputs.p_set_kw = self.inputs.p_set_kw
        self.inverter.inputs.q_set_kvar = self.inputs.q_set_kvar
        self.inverter.inputs.cos_phi_set = self.inputs.cos_phi_set
        self.inverter.inputs.inductive = self.inputs.inverter_inductive

        self.inverter.step()

        # Update state
        self.state.t_module_deg_celsius = self.pv.state.t_module_deg_celsius
        self.state.p_kw = self.inverter.state.p_kw
        self.state.q_kvar = self.inverter.state.q_kvar
        self.state.cos_phi = self.inverter.state.cos_phi
        self.state.inverter_inductive = self.inverter.state.inductive

        self.inputs.reset()

    def get_state(self):
        """Get state"""
        state_dict = {
            "pv": self.pv.get_state(),
            "inverter": self.inverter.get_state(),
        }
        return state_dict

    def set_state(self, state_dict):
        """Set state"""
        self.pv.set_state(state_dict["pv"])
        self.inverter.set_state(state_dict["inverter"])

        self.state.t_module_deg_celsius = self.pv.state.t_module_deg_celsius
        self.state.p_kw = self.inverter.state.p_kw
        self.state.q_kvar = self.inverter.state.q_kvar

    def set_q_kvar(self, q_kvar: float) -> None:
        return self.inverter.set_q_kvar(q_kvar)

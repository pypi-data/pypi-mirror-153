"""This module contains the python port of a CHP model developed in the
student's project group POWDER.
"""
from copy import copy

from pysimmods.generator.chplpgsim.config import CHPLPGConfig
from pysimmods.generator.chplpgsim.inputs import CHPLPGInputs
from pysimmods.generator.chplpgsim.state import CHPLPGState
from pysimmods.model.generator import Generator
from pysimmods.other.heatstoragesim.heatstorage import HeatStorage


class CHPLPG(Generator):
    """A Combined Heat and Power unit model.

    The CHP is fueled with Liquefied Petroleum Gas (LPG).

    Attributes
    ----------
    config : CHPLPGConfig
    state : CHPLPGState
    inputs : CHPLPGInputs

    """

    def __init__(self, params, inits):
        self.config = CHPLPGConfig(params)
        self.state = CHPLPGState(inits)
        self.inputs = CHPLPGInputs()

        self._storage = HeatStorage(params, inits)

    def step(self):
        """Perform a simulation step."""
        next_state = copy(self.state)
        next_state.p_kw = self._get_setpoint()

        # Operating state constraint is checked first to prevent
        # invalid user inputs. However, this has least priority and
        # changes due to other constraints are possible.
        self._check_operating_state(next_state)

        self._check_performance_limit(next_state)
        self._check_lubricant(next_state)
        self._check_storage_temperature(next_state)

        # Change operating state
        if next_state.p_kw != 0:
            next_state.is_active = True
            next_state.active_s += self.inputs.step_size
            next_state.inactive_s = 0
        else:
            next_state.is_active = False
            next_state.active_s = 0
            next_state.inactive_s += self.inputs.step_size
            # Auto refill of lubricant
            next_state.lubricant_l = self.config.lubricant_max_l

        next_state.q_kvar = 0

        self.state = next_state
        self.inputs.reset()

    def _get_setpoint(self):
        setpoint = self.inputs.p_set_kw

        if setpoint is not None:
            return abs(setpoint)

        hour = self.inputs.now_dt.hour
        default = self.config.default_schedule[hour]
        setpoint = self.config.p_max_kw * default / 100

        return abs(setpoint)

    def _check_operating_state(self, next_state):
        """Check if operating state constraints are satisfied.

        If the inut is not allowed to switch on, it will stay off.
        On the other hand, if the unit is not allowed to switch off,
        the minimal power is used as set value.

        """

        if next_state.p_kw != 0:
            if (
                not self.state.is_active
                and self.state.inactive_s < self.config.inactive_min_s
            ):
                next_state.p_kw = 0
        else:
            if (
                self.state.is_active
                and self.state.active_s < self.config.active_min_s
            ):
                next_state.p_kw = self.config.p_min_kw

    def _check_performance_limit(self, next_state):
        """Check if minimal performance is reached.

        If this is not the case, the set value is adapted to minimal
        power.

        """
        if next_state.p_kw != 0:
            next_state.p_kw = max(
                min(next_state.p_kw, self.config.p_max_kw),
                self.config.p_min_kw,
            )

    def _check_lubricant(self, next_state):
        """Check if lubricant constraint is satisfied.

        If no lubricant is available, the unit will switch off.

        """
        if next_state.p_kw != 0:
            lubricant_delta_l = (
                self.config.lubricant_ml_per_h
                * (self.inputs.step_size / 3_600)
                / 1_000
            )
            if self.state.lubricant_l < lubricant_delta_l:
                # not enough lubricant, switch off
                next_state.p_kw = 0
            else:
                next_state.lubricant_l -= lubricant_delta_l

    def _check_storage_temperature(self, next_state):
        """Check if the storage temperature is not to high

        Also calculates the new storage temperature and if the
        temperature is too high, a lower set value for power is
        calculated.

        """
        # Thermal energy production
        e_th_prod_kwh = (
            next_state.p_kw
            * self.config.p_2_p_th_percent
            / 100
            * self.inputs.step_size
            / 3_600
        )

        # Get maximal energy the storage can absorb
        e_th_in_max_kwh = self._storage.get_absorbable_energy()

        if e_th_prod_kwh < e_th_in_max_kwh:
            next_state.p_kw = (
                e_th_in_max_kwh
                * (100 / self.config.p_2_p_th_percent)
                * (3_600 / self.inputs.step_size)
            )
            e_th_prod_kwh = e_th_in_max_kwh

        self._storage.absorb_energy(
            e_th_prod_kwh, self.inputs.e_th_demand_set_kwh
        )

        next_state.storage_t_c = self._storage.t_c
        next_state.p_th_kw = (
            next_state.p_kw * self.config.p_2_p_th_percent / 100
        )

    def set_state(self, state_dict):
        """Set the state."""
        super().set_state(state_dict)
        self._storage.t_c = self.state.storage_t_c

    # @property
    # def set_percent(self):
    #     p_kw = self.inputs.p_set_kw
    #     if p_kw is None:
    #         p_kw = self.state.p_kw

    #     p_kw = (p_kw - self.config.pn_min_kw) / (
    #         self.config.pn_max_kw - self.config.pn_min_kw
    #     )
    #     return abs(p_kw) * 100

    # @set_percent.setter
    # def set_percent(self, value):
    #     value = max(min(abs(value), 100.0), 0.0)

    #     if value == 0:
    #         p_set_kw = 0
    #     else:
    #         p_range = self.config.pn_max_kw - self.config.pn_min_kw
    #         p_set_kw = self.config.pn_min_kw + value / 100 * p_range

    #     self.inputs.p_set_kw = p_set_kw

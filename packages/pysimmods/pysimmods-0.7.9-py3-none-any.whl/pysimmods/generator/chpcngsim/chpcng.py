"""This module contains a CHP model that is used by the biogas plant.

"""
from copy import deepcopy
from datetime import timedelta

import numpy as np
from pysimmods.generator.chpcngsim.config import CHPCNGConfig
from pysimmods.generator.chpcngsim.inputs import CHPCNGInputs
from pysimmods.generator.chpcngsim.state import CHPCNGState
from pysimmods.model.generator import Generator


class CHPCNG(Generator):
    """A combined heat and power unit model.

    The CHP is fueled with Compressed Natural Gas (CNG).
    The main purpose for this model is to be used by the biogas plant.

    Attributes
    ----------
    config : CHPLPGConfig
    state : CHPLPGState
    inputs : CHPLPGInputs

    """

    def __init__(self, params, inits):
        self.config = CHPCNGConfig(params)
        self.state = CHPCNGState(inits)
        self.inputs = CHPCNGInputs()

    def step(self, pretend=False):
        """Perform a simulation step."""
        next_state = deepcopy(self.state)
        next_state.p_kw = self._get_setpoint()

        self._check_constraints(next_state)

        if next_state.p_kw != 0:
            # Unit is / switches on
            next_state.active_s_per_day += self.inputs.step_size
            next_state.inactive_s = 0
            if self.state.p_kw != 0:
                # Unit was on in the last step
                if self.state.p_kw != next_state.p_kw:
                    # Power level changed
                    next_state.active_s = self.inputs.step_size
                else:
                    next_state.active_s += self.inputs.step_size
            else:
                next_state.restarts += 1
        else:
            # Unit is / switches off
            next_state.inactive_s += self.inputs.step_size
            next_state.inactive_s_per_day += (
                self.inputs.step_size % 86_400
            )  # Works correctly?

        next_state.p_th_kw = self._gas2thermal_power(
            next_state.p_kw, next_state.gas_cons_m3
        )

        # Update the time
        # TODO: Handle odd step sizes.
        next_dt = self.inputs.now_dt + timedelta(seconds=self.inputs.step_size)
        if next_dt.day != self.inputs.now_dt.day:
            # Start a new day
            next_state.restarts = 0
            next_state.active_s_per_day = 0
            next_state.inactive_s_per_day = 0

        if not pretend:
            self.state = next_state
            self.inputs.reset()

        return next_state

    def _get_setpoint(self):
        setpoint = self.inputs.p_set_kw

        if setpoint is None:
            hour = self.inputs.now_dt.hour
            default = self.config.default_schedule[hour]
            setpoint = self.config.p_min_kw + (
                (self.config.p_max_kw - self.config.p_min_kw) * default / 100
            )

        return abs(setpoint)

    def _check_constraints(self, next_state):

        if not self.inputs.gas_critical:
            self._check_daily_incative_time(next_state)
            self._check_restarts(next_state)
            self._check_daily_active_time(next_state)

        self._check_gas_demand(next_state)

    def _check_daily_incative_time(self, next_state):
        # Only check if this a constraint
        if self.config.inactive_max_s_per_day > 0:
            # Unit should be switched off in the next state
            if next_state.p_kw == 0:
                # Total inactive time after this step
                inactive_next = (
                    next_state.inactive_s_per_day + self.inputs.step_size
                )

                # No more inactivity allowed for today
                if inactive_next > self.config.inactive_max_s_per_day:
                    next_state.p_kw = self.config.pn_min_kw

    def _check_restarts(self, next_state):
        # Only check if this is a constraint
        if self.config.restarts_per_day > 0:
            # Unit was off and should switch on
            if self.state.p_kw == 0 and next_state.p_kw != 0:
                # Another restart is invalid
                if next_state.restarts >= self.config.restarts_per_day:
                    next_state.p_kw = 0

    def _check_daily_active_time(self, next_state):
        # Only check if this is a constraint
        if self.config.active_max_s_per_day > 0:
            # Unit should switch/stay on in the next step
            if next_state.p_kw != 0:
                # Total active time after this step
                active_next = (
                    next_state.active_s_per_day + self.inputs.step_size
                )
                # Unit cannot stay switched on
                if active_next > self.config.active_max_s_per_day:
                    next_state.p_kw = 0

    def _check_gas_demand(self, next_state):
        # Unit should operate on next step
        if next_state.p_kw != 0:
            gas_cons = self._gas_demand(next_state.p_kw)

            # Enough gas for a whole step
            if gas_cons < self.inputs.gas_in_m3:
                next_state.gas_cons_m3 = gas_cons
            else:
                # Do not consider running for half a step
                next_state.p_kw = 0
                next_state.gas_cons_m3 = 0
        else:
            next_state.gas_cons_m3 = 0

    def _gas_demand(self, p_kw):
        e_kwh = abs(p_kw) * self.inputs.step_size / 3_600

        # Get best matching power level
        idx = np.argmin(abs(np.array(self.config.pn_stages_kw) - p_kw))
        # Get eta for p_kw
        eta = self.config.eta_stages_percent[idx] / 100

        gas = e_kwh / (
            eta
            * self.config.e_ch4_kwh
            * self.config.ch4_concentration_percent
            / 100
        )
        return gas

    def _gas2thermal_power(self, p_kw, gas):
        idx = np.argmin(abs(np.array(self.config.pn_stages_kw) - p_kw))
        eta = self.config.eta_th_stages_percent[idx] / 100
        v_methane = (
            self.config.e_ch4_kwh
            * self.config.ch4_concentration_percent
            * gas
            / 100
        )
        p_th_kw = eta * v_methane * 3_600 / self.inputs.step_size

        return p_th_kw

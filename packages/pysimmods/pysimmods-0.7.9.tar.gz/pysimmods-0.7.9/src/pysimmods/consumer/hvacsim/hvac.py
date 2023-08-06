"""This module contains the HVAC model."""
from copy import copy, deepcopy

import numpy as np
from pysimmods.consumer.hvacsim.config import HVACConfig
from pysimmods.consumer.hvacsim.inputs import HVACInputs
from pysimmods.consumer.hvacsim.state import HVACState
from pysimmods.model.consumer import Consumer


class HVAC(Consumer):
    """Simulation model of a heating, ventilation and air conditioning.

    This model is based on a port from the AC model from pratical
    training *energy informatics* of the University of Oldenburg.

    Parameters
    ----------
    params : dict
        Configuration parameters. See :class:`.HVACConfig` for all
        parameters.
    inits : dict
        Initialization parameters. See :class:`.HVACState` for all
        parameters.

    Attributes
    ----------
    config : :class:`.HVACConfig`
        Stores the configuration parameters of the HVAC model.
    state : :class:`.HVACState`
        Stores the initialization parameters of the HVAC model.
    inputs : :class:`.HVACInputs`
        Stores the input parameters for each step of the HVAC model.

    """

    def __init__(self, params, inits):
        self.config = HVACConfig(params)
        self.state = HVACState(inits)
        self.inputs = HVACInputs()

    def step(self):
        """Perform a simulation step."""

        next_state = copy(self.state)
        next_state.p_kw = self.inputs.p_set_kw

        self._check_constraints(next_state)

        self._calculate_t(next_state)

        next_state.q_kvar = 0

        self.state = next_state
        self.inputs.reset()

    def _check_constraints(self, next_state):
        if next_state.p_kw is None:
            self._check_internal_temperature(next_state)
        else:
            self._check_schedule(next_state)

    def _check_internal_temperature(self, next_state):
        """Check the temperature constraint

        If internal temperature reaches on the boundaries, cooling is
        activated respectively deactivated, depending on the boundary.

        A cooling HVAC consumes the maximum possible power, a
        non-cooling HVAC consume the minimum possible power (mostly 0).

        """
        if self.state.theta_t_deg_celsius <= self.config.t_min_deg_celsius:
            next_state.cooling = False
        if self.state.theta_t_deg_celsius >= self.config.t_max_deg_celsius:
            next_state.cooling = True

        if next_state.cooling:
            next_state.p_kw = self.config.p_max_kw
        else:
            next_state.p_kw = self.config.p_min_kw

    def _check_schedule(self, next_state):
        """Check if a scheduled operation is possible

        Currently, if p_set_kw was set as input, it will considered
        as one time schedule. If no boundaries are exceeded, the
        model follows the schedule.

        """

        if self.state.theta_t_deg_celsius <= self.config.t_min_deg_celsius:
            next_state.p_kw = self.config.p_min_kw

        elif self.state.theta_t_deg_celsius >= self.config.t_max_deg_celsius:
            next_state.p_kw = self.config.p_max_kw

        else:
            next_state.p_kw = abs(next_state.p_kw)

    def _calculate_t(self, next_state):
        """Calculate the temperature for the next step."""

        minuend = self.config.alpha * (
            self.inputs.t_air_deg_celsius - self.state.theta_t_deg_celsius
        )
        # eta_percent / 100 -> eta decimal
        # p_set_kw * 1000 -> p_set_w
        # -> 1e1
        subtrahend = (
            self.config.eta_percent
            * next_state.p_kw
            * 1e1
            * self.config.cool_factor
        )

        dividend = minuend - subtrahend
        divisor = self.state.mass_kg * self.state.c_j_per_kg_k

        quotient = dividend / divisor
        next_state.theta_t_deg_celsius = self.state.theta_t_deg_celsius + (
            self.inputs.step_size * quotient * self.config.thaw_factor
        )

    def set_percent(self, percentage: float) -> None:
        if percentage is not None and ~np.isnan(percentage):
            return super().set_percent(percentage)

    def get_default_setpoint(self, hour: int) -> float:

        test_state = deepcopy(self.state)
        self._check_constraints(test_state)
        return self._get_percent(
            test_state.p_kw,
            self.get_pn_min_kw(),
            self.get_pn_max_kw(),
        )

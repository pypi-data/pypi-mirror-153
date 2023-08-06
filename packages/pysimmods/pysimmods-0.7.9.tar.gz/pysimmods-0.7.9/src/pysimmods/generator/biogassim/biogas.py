import copy
import itertools
from copy import deepcopy

import numpy as np
from pysimmods.generator.biogassim.config import BiogasConfig
from pysimmods.generator.biogassim.inputs import BiogasInputs
from pysimmods.generator.biogassim.state import BiogasState
from pysimmods.generator.chpcngsim import CHPCNG
from pysimmods.model.generator import Generator


class BiogasPlant(Generator):
    """A biogas plant simulation model.

    A biogas plant consists basically of four main components:
    gas production, gas storage, one or more generator units, and
    a control unit. Additionally, a heat storage can be attached.

    These components are more or less integrated in the main model
    defined in this file. The generator units are out-sourced to
    pysimmods.chpngsim. A heat storage will be integrated in the
    future.

    An example parameter configuration for two generators could
    look like this::

        params = {
            'gas_m3_per_day': 3030,
            'cap_gas_m3': 1530,
            'gas_fill_min_percent': 2.0,
            'gas_fill_max_percent': 98.0,
            'ch4_concentration_percent': 54.4,
            'num_chps': 2,
            'chp0': {
                'pn_stages_kw': [75.0, 150.0],
                'eta_stages_percent': [31.1, 32.4],
                'eta_th_stages_percent': [30.8, 31.2],
                'restarts_per_day': 6,
                'active_min_s': 3 * 3_600,
                'active_max_s_per_day': 0,
                'inactive_min_s': 2 * 3_600,
                'inactive_max_s_per_day': 0,
            },
            'chp1': {
                'pn_stages_kw': [75.0, 150.0],
                'eta_stages_percent': [33.0, 33.2],
                'eta_th_stages_percent': [30.0, 30.5],
                'restarts_per_day': 6,
                'active_min_s': 3 * 3_600,
                'active_max_s_per_day': 0,
                'inactive_min_s': 2 * 3_600,
                'inactive_max_s_per_day': 0,
            }
        }

        inits = {
            'gas_fill_percent': 50,
            'chp0': {
                'active_s': 0,
                'active_s_per_day': 0,
                'inactive_s': 0,
                'inactive_s_per_day': 0,
                'restarts': 0,
                'p_kw': 75.0,
            },
            'chp1': {
                'active_s': 0,
                'active_s_per_day': 0,
                'inactive_s': 0,
                'inactive_s_per_day': 0,
                'restarts': 0,
                'p_kw': 75.0,
            },
        }

    More example configurations can be found in the presets.py

    Attributes
    ----------
    config: :class:`.BiogasConfig`
        The configuration parameters of the biogas model.
    state: :class:`.BiogasState`
        The initialization parameters of the biogas model.
    inputs: :class:`.BiogasInputs`
        The input parameters of the biogas model.
    chps: List[:class:`.CHPCNG`]
        A list containing the CHP objects of this biogas model.

    """

    def __init__(self, params, inits):
        self.config = BiogasConfig(params)
        self.state = BiogasState(inits)
        self.inputs = BiogasInputs()

        self.chps = list()
        for idx in range(self.config.num_chps):
            params[f"chp{idx}"].setdefault(
                "ch4_concentration_percent",
                self.config.ch4_concentration_percent,
            )
            params[f"chp{idx}"].setdefault(
                "sign_convention", self.config.sign_convention
            )
            self.chps.append(CHPCNG(params[f"chp{idx}"], inits[f"chp{idx}"]))

    def step(self):
        """Perform a simulation step."""
        next_state = deepcopy(self.state)
        self._check_inputs(next_state)
        self._check_gas_priority(next_state)
        self._check_gas_storage(next_state)

        self._step_chps(next_state)

        self._update_references(next_state)

        self.state = next_state
        self.inputs.reset()

    def _check_inputs(self, nstate):
        if self.inputs.p_set_kw is None:
            if self.inputs.now_dt is not None:
                default_val = self.config.default_schedule[
                    self.inputs.now_dt.hour
                ]
                if self.config.use_decimal_percent:
                    default_val *= 0.01
                self.set_percent(default_val)
                nstate.p_kw = self.inputs.p_set_kw
            else:
                nstate.p_w = 0
        else:
            nstate.p_kw = self.inputs.p_set_kw

    def _check_gas_priority(self, next_state):
        """Reset critical flags of the gas storage if feasible."""
        if 40 < self.state.gas_fill_percent < 60:
            next_state.burn_gas = False
            next_state.pool_gas = False

        if (
            self.config.gas_fill_min_percent
            < self.state.gas_fill_percent
            < self.config.gas_fill_max_percent
        ):
            next_state.gas_critical = False

    def _check_gas_storage(self, next_state):
        """Update the production part of the gas storage."""
        # Let's produce natural gas
        gas_per_s = self.config.gas_m3_per_day / 86_400
        next_state.gas_prod_m3 = gas_per_s * self.inputs.step_size

        # Now fill the gas storage
        gas_level = self.state.gas_fill_percent * 0.01 * self.config.cap_gas_m3
        gas_level += next_state.gas_prod_m3
        next_state.gas_fill_percent = gas_level / self.config.cap_gas_m3 * 100

    def _step_chps(self, next_state):
        """Find a suitable combination to step the CHPs to reach
        target electrical power (next_state.p_kw).
        """

        # Generate all combinations
        p_combis = list(
            itertools.product(
                *[[0] + chp.config.pn_stages_kw for chp in self.chps]
            )
        )

        # Try every combination and drop infeasible ones
        feasibles = self._generate_feasible_combis(next_state, p_combis)

        if not feasibles:
            # TODO: add logger warning
            feasibles[p_combis[0]] = 0

        # Determine the best combination
        best_score = np.Infinity
        best_combi = None
        for combi, score in feasibles.items():
            if score <= best_score:
                best_combi = combi
                best_score = score

        # Perform the steps with the best combination
        for chp, p_set_kw in zip(self.chps, best_combi):
            self._set_chp_inputs(next_state)
            # TODO: Adapt available gas
            chp.inputs.p_set_kw = p_set_kw
            chp.step()

    def _generate_feasible_combis(self, next_state, p_combis):

        feasibles = dict()
        for combi in p_combis:
            states = list()
            for chp, p_set_kw in zip(self.chps, combi):
                self._set_chp_inputs(next_state)
                chp.inputs.p_set_kw = p_set_kw
                states.append(chp.step(pretend=True))

            p_kws = list()
            gas_cons = list()
            for state in states:
                p_kws.append(state.p_kw)
                gas_cons.append(state.gas_cons_m3)

            diff = abs(sum(p_kws) - next_state.p_kw)

            new_gas_level = (
                min(100.0, next_state.gas_fill_percent)
                * 0.01
                * self.config.cap_gas_m3
            )
            new_gas_level -= sum(gas_cons)
            new_gas_percent = new_gas_level / self.config.cap_gas_m3 * 100

            if new_gas_percent < self.config.gas_fill_min_percent:
                if new_gas_percent < next_state.gas_fill_percent:
                    continue
            if new_gas_percent > self.config.gas_fill_max_percent:
                if new_gas_percent > next_state.gas_fill_percent:
                    continue

            feasibles[combi] = diff

        return feasibles

    def _set_chp_inputs(self, next_state):
        # Update inputs of the CHPs
        gas_level = next_state.gas_fill_percent * 0.01 * self.config.cap_gas_m3
        for chp in self.chps:
            chp.set_step_size(self.inputs.step_size)
            chp.set_now_dt(self.inputs.now_dt)
            chp.inputs.gas_critical = (
                next_state.burn_gas or next_state.pool_gas
            )
            chp.inputs.gas_in_m3 = gas_level / len(self.chps)

    def _update_references(self, next_state):
        next_state.p_kw = sum([chp.state.p_kw for chp in self.chps])
        next_state.p_th_kw = sum([chp.state.p_th_kw for chp in self.chps])

        next_state.gas_cons_m3 = sum(
            [chp.state.gas_cons_m3 for chp in self.chps]
        )
        next_state.gas_fill_percent -= (
            next_state.gas_cons_m3 / self.config.cap_gas_m3 * 100
        )
        next_state.gas_fill_percent = min(
            100, max(0, next_state.gas_fill_percent)
        )

        if next_state.gas_fill_percent < self.config.gas_fill_min_percent:
            next_state.pool_gas = True
            next_state.gas_critical = True

        if next_state.gas_fill_percent > self.config.gas_fill_max_percent:
            next_state.burn_gas = True
            next_state.gas_critical = True

    def get_state(self):

        state = {"state": copy.deepcopy(self.state.__dict__)}
        for idx, chp in enumerate(self.chps):
            state[f"chp-{idx}"] = chp.get_state()
        return state

    def set_state(self, state):
        for attr, value in state["state"].items():
            setattr(self.state, attr, value)
        # self.state = state["state"]
        for idx, chp in enumerate(self.chps):
            chp.set_state(state[f"chp-{idx}"])

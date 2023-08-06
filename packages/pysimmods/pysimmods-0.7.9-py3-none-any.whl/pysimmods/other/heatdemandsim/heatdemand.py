"""
This module contains a household class that simulates thermal power demand
for the chp.

"""
import math
import random
from copy import deepcopy
from datetime import timedelta

from pysimmods.other.heatdemandsim import (
    HeatDemandConfig,
    HeatDemandInputs,
    HeatDemandState,
    hprofiles,
)

DEMAND_PROFILES = dict()


class HeatDemand:
    """A simple model for thermal power demand.

    :constant CHP_AVERAGE_RUNTIME:
        source: 'IHK Projekte Hannover, Blockheizkraftwerke,
        Seite 5 IHK Projekte Durschnittliche Betriebsstunden
        eines BHKWs'
    :constant CHP_MIN_TH_CONS_COEF:
        source: 'IHK Projekte Hannover, Blockheizkraftwerke,
        Seite 5 Prozentzahl für die untere minimale thermische
        Leistung des Jahresverbrauchs eines Householdtypes'
    :constant CHP_MAX_TH_CONS_COEF:
        source: 'IHK Projekte Hannover, Blockheizkraftwerke,
        Seite 5 Prozentzahl für die obere maximale thermische
        Leistung des Jahresverbrauchs eines Householdtypes'
    :constant DEGREE_OF_EFFIENCY:
        source: 'Niedertemperatur- und Brennwertkessel.
        Wissenswertes über moderne Zentralheizungsanlagen.
        Hessisches Ministerium für Umwelt, Energie,
        Landwirtschaft und Verbraucherschutz. 2011'

    """

    CHP_AVERAGE_RUNTIME = 5_000.0
    CHP_MIN_TH_CONS_COEF = 1.0
    CHP_MAX_TH_CONS_COEF = 1.5
    # DEGREE_OF_EFFIENCY = 0.93

    def __init__(self, config, state):
        self.config = HeatDemandConfig(config)
        self.state = HeatDemandState(state)
        self.inputs = HeatDemandInputs()

    def step(self):
        """perform a simulation step"""

        next_state = deepcopy(self.state)

        # calculate allocation temperature for the current day
        # (weighted mean temperature of the current and the last
        # three days)
        t_alloc = (
            1.0 * self.inputs.day_avg_t_air_deg_celsius
            + 0.5 * self.state.t_last_1_deg_celsius
            + 0.25 * self.state.t_last_2_deg_celsius
            + 0.125 * self.state.t_last_3_deg_celsius
        ) / (1 + 0.5 + 0.25 + 0.125)

        # profile function 'SigLinDe': calculate daily consumption
        # depending on the allocation temperature. Has both a sigmoid
        # and a linear part
        tmp = math.pow(
            self.config.const_b / (t_alloc - self.config.const_v_0),
            self.config.const_c,
        )
        sigmoid = self.config.const_a / (1.0 + tmp) + self.config.const_d
        linear = max(
            self.config.const_m_h * t_alloc + self.config.const_b_h,
            self.config.const_m_w * t_alloc + self.config.const_b_w,
        )

        daily_cons = (
            self.config.consumer_const
            * (sigmoid + linear)
            * self.config.weekday_const[self.state.now_dt.weekday()]
        )

        next_state.e_th_kwh = (
            daily_cons
            * self.config.degree_of_efficiency
            * self.config.load_profile[self.state.now_dt.hour]
            * self.inputs.step_size
            / 3_600
        )

        next_state.now_dt += timedelta(seconds=self.inputs.step_size)
        if next_state.now_dt.day > self.state.now_dt.day:
            # we reached a new day
            next_state.t_last_3_deg_celsius = next_state.t_last_2_deg_celsius
            next_state.t_last_2_deg_celsius = next_state.t_last_1_deg_celsius
            next_state.t_last_1_deg_celsius = (
                self.inputs.day_avg_t_air_deg_celsius
            )

        self.state = next_state

    @property
    def e_th_kwh(self):
        """Returns the current thermal power demand"""
        return self.state.e_th_kwh

    def get_state(self) -> dict:
        """Return the current state of the model.

        Returns
        -------
        dict
            The current state of the model in form of a dictionary
            containing entries for all state variables. Returned dict
            can be assigned to the *inits* argument when creating a new
            model instance.

        """

        try:
            return {
                attr: getattr(self.state, attr)
                for attr in self.state.__slots__
            }
        except AttributeError:
            return deepcopy(self.state.__dict__)

    def set_state(self, state: dict) -> None:
        """Set the current state of the model.

        Parameters
        ----------
        state : dict
            A *dict* containing entries for all state variables.

        """
        for attr, value in state.items():
            setattr(self.state, attr, value)


def create_heatdemand(config, state):
    """Creates a household object"""

    if not DEMAND_PROFILES:
        load_demand_profiles()

    p_th_prod = -config.get("chp_p_th_prod_kw", -400)
    profile = find_demand_profile(p_th_prod)

    # adapt consumer constant of the household, so that power and
    # consumption better fit to each other
    profile["consumer_constant"] = p_th_prod * 24 * 2 / 3

    heatdemand_obj = HeatDemand(profile, state)

    return heatdemand_obj


def load_demand_profiles():
    """Write me"""
    global DEMAND_PROFILES
    DEMAND_PROFILES = dict()
    for name, func in hprofiles.__dict__.items():
        if "__" not in name:
            DEMAND_PROFILES[name] = func()


def find_demand_profile(chp_p_th_kw):
    """Write me"""
    min_consumption = dict()
    max_consumption = dict()

    for key, val in DEMAND_PROFILES.items():
        # average annual consumption per average operating
        # hours of the chp
        consumption = (
            val["consumer_constant"] * 365 / HeatDemand.CHP_AVERAGE_RUNTIME
        )
        # calculate lower power boundary
        min_consumption[key] = consumption * HeatDemand.CHP_MIN_TH_CONS_COEF
        # calculate upper power boundary
        max_consumption[key] = consumption * HeatDemand.CHP_MAX_TH_CONS_COEF

    possible_profiles = list()
    distances = dict()

    # Look for fitting households
    for key, val in DEMAND_PROFILES.items():
        if abs(chp_p_th_kw >= min_consumption[key]) and abs(
            chp_p_th_kw <= max_consumption[key]
        ):
            # Profile fits optimally
            possible_profiles.append(key)
            distances[key] = 0.0
        else:
            # Profile does not fit, calculate difference
            lower = abs(abs(chp_p_th_kw) - min_consumption[key])
            upper = abs(abs(chp_p_th_kw) - max_consumption[key])
            distances[key] = lower if lower < upper else upper

    if len(possible_profiles) == 1:
        # Exactly one matching profile
        demand_profile = DEMAND_PROFILES[possible_profiles[0]].copy()
    elif len(possible_profiles) > 1:
        # More than one matching profile, select randomly
        demand_profile = DEMAND_PROFILES[
            random.choice(possible_profiles)
        ].copy()
    else:
        # No matching profile, select the nearest one

        min_type = "one_family"
        min_val = float("Inf")

        for key, val in distances.items():
            if val < min_val:
                min_val = val
                min_type = key

        demand_profile = DEMAND_PROFILES[min_type].copy()
    return demand_profile

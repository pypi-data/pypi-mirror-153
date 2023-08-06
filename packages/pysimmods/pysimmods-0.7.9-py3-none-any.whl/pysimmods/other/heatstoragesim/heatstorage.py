"""This module contains the heat storage model that is used by the
CHP LPG.
"""
import math


C_WATER = 4.18
"""Specific heat capacity of water in [kJ/(kg*K)]"""


class HeatStorage:
    """Model of a heat storage.

    Parameters
    ----------
    params : dict
        A *dict* containing values for all attributes. The keys all
        have the prefix "storage_".
    inits : dict
        A *dict* containing state variables for the storage. The keys
        all have the prefix "storage_".

    Attributes
    ----------
    cap_l : float
        Capacity of the buffer storage in [l].
    consumption_kwh_per_day : float
        Average loss of energy in [kWh/day].
    t_min_c : float
        Minimal water temperature of the buffer storage in [°C].
    t_max_c : float
        Maximal water temperature of the buffer storage in [°C].
    t_c : float
        Current water temperature of the buffer storage in [°C].
    env_t_c : float, optional
        Current temperature of the environment in [°C]. The storage
        is assumed to be placed indoor and, therefore, defaults to
        19.0 °C.

    """

    def __init__(self, params, inits):

        # Config
        self.cap_l = params["storage_cap_l"]
        self.consumption_kwh_per_day = params[
            "storage_consumption_kwh_per_day"
        ]
        self.t_min_c = params["storage_t_min_c"]
        self.t_max_c = params["storage_t_max_c"]
        self.env_t_c = params.get("storage_env_t_c", 19.0)

        # State
        self.t_c = inits["storage_t_c"]
        self._t_chilled = None

    def _calculate_chilled_t(self):
        """Calculate the chilled temperature.

        This function requires that the :attr:`.env_t_c` is set.

        Returns
        -------
        float
            The chilled temperature

        """

        chill = (
            self.consumption_kwh_per_day
            * 3_600_00
            / (C_WATER * 1_000 * self.cap_l * 24)
        )
        t_next = self.t_c - chill

        # Prevent math domain/division by zero errors
        dif_t_next_env = max(t_next - self.env_t_c, 1e-3)
        dif_t_init_env = max(self.t_c - self.env_t_c, 1e-3)
        div_t = max(dif_t_next_env / dif_t_init_env, 1e-3)

        chill_coef = math.log(div_t) / t_next
        t_chilled = (self.t_c - self.env_t_c) * math.pow(
            math.e, chill_coef
        ) + self.env_t_c

        return t_chilled

    def get_absorbable_energy(self):
        """Return the amount of energy the storage can absorb."""
        e_th_in_max_kwh = (
            -1 * C_WATER * self.cap_l * (self.t_max_c - self.t_c) / 3_600
        )

        return e_th_in_max_kwh

    def absorb_energy(self, e_th_prod, e_th_demand):

        # 1 kWh = 3600 kJ
        e_th_delta_kj = (e_th_prod + e_th_demand) * 3_600

        t_chilled = self._calculate_chilled_t()
        t_new = -e_th_delta_kj / (C_WATER * self.cap_l) + t_chilled

        self.t_c = max(t_new, self.t_min_c)

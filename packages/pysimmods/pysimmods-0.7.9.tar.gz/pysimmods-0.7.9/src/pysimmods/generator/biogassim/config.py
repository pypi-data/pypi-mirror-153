"""This module contains the config model for the Biogas plant."""

from pysimmods.model.config import ModelConfig
import itertools


class BiogasConfig(ModelConfig):
    """Config parameters of the biogas plant model.

    This class captures the configuration parameters for the biogas
    model.

    Parameters
    ----------
    params: dict
        A dictionary containing the configuration parameters. See
        attributes section. The key for each attribute is the same as
        the attribute name, e.g.,::

             {'gas_m3_per_day': 100}

        to set the attribute 'gas_m3_per_day.

    Attributes
    ----------
    gas_m3_per_day: float
        Gas production per day in [m^3].
    cap_gas_m3: float
        Capacity of the gas storage in [m^3].
    gas_fill_min_percent: float
        Lower boundary for the gas storage in [%].
    gas_fill_max_percent: float
        Upper boundary for the gas storage in [%].
    ch4_concentration_percent: float, optional
        Concentration of methane gas in [%]. Defaults to 50.302% and
        should usually not be changed.
    num_chps: int
        Specifies the number of CHP units in this biogas plant.
    pn_stages_kw: list
        All possible combinations of setpoints for the chps, sorted in
        ascending order without duplicates. This attribute is
        calculated automatically and can not be provided.

    """

    def __init__(self, params):
        super().__init__(params)

        self.gas_m3_per_day = params["gas_m3_per_day"]
        self.cap_gas_m3 = params["cap_gas_m3"]
        self.gas_fill_min_percent = params["gas_fill_min_percent"]
        self.gas_fill_max_percent = params["gas_fill_max_percent"]
        self.ch4_concentration_percent = params.get(
            "ch4_concentration", 50.302
        )

        self.num_chps = params["num_chps"]
        stages = [
            params[f"chp{idx}"]["pn_stages_kw"] for idx in range(self.num_chps)
        ]
        self.pn_stages_kw = sorted(
            list(
                set(
                    [abs(sum(tup)) for tup in list(itertools.product(*stages))]
                )
            )
        )
        self.p_max_kw = max(self.pn_stages_kw)
        self.p_min_kw = min(self.pn_stages_kw)

        self.default_schedule = [
            50,
            50,
            50,
            50,
            50,
            100,
            100,
            100,
            100,
            50,
            50,
            50,
            100,
            100,
            50,
            50,
            50,
            100,
            100,
            100,
            100,
            50,
            50,
            50,
        ]

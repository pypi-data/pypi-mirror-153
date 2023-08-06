"""This module contains the base config for each model."""


class ModelConfig:
    """The base config for all models.

    Parameters
    ----------
    params: dict
        A *dict* containing configuration parameters. See *Attributes*
        for detailed information

    Attributes
    ----------
    sign_convention: str
        Should be defined in *params* and can have the values
        *'passive'* or *'active'*. Passive sign convention aka load
        reference arrow system is normally used and leads to positive
        consumption and negative generation power flows.
    psc: bool
        Will be automatically set to *True* if passive sign convention
        is used.
    asc: bool
        Will be automatically set to *True* if active sign convention is
        used.
    gsign: int
        The generator sign depending on the sign convention. Will be
        set to *-1* if passive sign convention is used and to *1*
        otherwise.
    lsign: int
        The load sign depending on the sign convention. Will be set to
        *1* is passive sign convention is used and to *-1* otherwise.
    use_decimal_percent: bool
        If *True* decimal percentage [0, 1.0] is used, otherwise normal
        percentage [0, 100] ist used.
    default_schedule: List[float]
        A *list* containing a default schedule with percentage
        power for each hour of the day (i.e., len(default_schedule) ==
        24). This is used if no other *p* or *q* input is provided.
    p_min_kw: float
        The minimum nominal active power output of the model.
    p_max_kw: float
        The maximum nominal active power output of the model.
    q_min_kvar: float
        The minimum nominal reactive power output of the model.
    q_max_kvar: float
        The maximum nominal reactive power output of the model.
    s_min_kva: float
        The minimal nominal apparent power output of the model.
    s_max_kva: float
        The maximal nominal apparent power output of the model.

    """

    def __init__(self, params: dict) -> None:

        self.sign_convention = params.get("sign_convention", "passive")
        assert self.sign_convention in ["active", "passive"]

        self.psc = self.sign_convention == "passive"
        self.asc = self.sign_convention == "active"

        if self.sign_convention == "active":
            self.gsign = 1
            self.lsign = -1
        else:
            self.gsign = -1
            self.lsign = 1

        self.use_decimal_percent = params.get("use_decimal_percent", False)
        self.default_schedule = params.get("default_schedule", [50] * 24)

        self.p_min_kw: float
        self.p_max_kw: float
        self.q_min_kvar: float
        self.q_max_kvar: float
        self.s_min_kva: float
        self.s_max_kva: float

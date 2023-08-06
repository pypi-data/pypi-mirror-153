"""This module contains the base class for all model states."""
from datetime import datetime
from typing import Optional


class ModelState:
    """Base class for model states.

    Parameters
    ----------
    inits : dict
        A *dict* containing the state variables.

    Attributes
    ----------
    p_kw: float
        Current (or last) electrical active power P in [kW].
    q_kvar: float
        Current (or last) electrical reactive power Q in [kVAr].
    s_kva: float
        Current (or last) electrical apparent power S in [kVA].
    now_dt: datetime, optional
        Current (or last) date and time. Marks the time where the last
        step started.
    delta_s: int, optional
        Duration of the current (or last) step in [s].
    """

    def __init__(self, inits: dict) -> None:
        self.p_kw: float = inits.get("p_kw", 0)
        self.q_kvar: float = inits.get("q_kvar", 0)
        self.s_kva: float = inits.get("s_kva", 0)
        self.now_dt: Optional[datetime] = inits.get("now_dt", None)
        self.delta_s: Optional[int] = inits.get("delta_s", None)

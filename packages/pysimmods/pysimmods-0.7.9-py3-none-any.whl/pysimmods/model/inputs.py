"""This module contains the base class for all model inputs."""
from datetime import datetime
from typing import Optional, Union

from pysimmods.util.date_util import convert_dt


class ModelInputs:
    """Base class for model inputs.

    Attributes
    ----------
    p_set_kw : float
        Target electrical activate power in [kW].
    q_set_kvar : float
        Target electrical reactive power in [kVAr].
    step_size : int
        Step size for the net step in [s].

    """

    def __init__(self) -> None:
        self.p_set_kw: Optional[float] = None
        self.q_set_kvar: Optional[float] = None
        self.step_size: Optional[float] = None
        self._now_dt: Optional[float] = None

    def reset(self) -> None:
        """To be called at the end of each step."""
        for attr in self.__dict__.keys():
            setattr(self, attr, None)

    @property
    def now_dt(self) -> datetime:
        """The current date and time of the model"""
        return self._now_dt

    @now_dt.setter
    def now_dt(self, now: Union[datetime, str, int]) -> None:
        self._now_dt = convert_dt(now)

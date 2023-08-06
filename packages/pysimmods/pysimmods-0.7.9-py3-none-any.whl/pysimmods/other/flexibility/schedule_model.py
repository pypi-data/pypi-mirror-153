from datetime import datetime
from typing import Optional

import numpy as np
from pysimmods.model.model import Model
from pysimmods.other.flexibility.schedule import Schedule


class ScheduleModel:
    """A wrapper for pysimmods, which allows models to use schedules.

    Parameters
    ----------
    model: :class:`.Model`

    """

    def __init__(
        self,
        model: Model,
        unit: str = "kw",
        priorize_setpoint: bool = False,
        use_absolute_schedule: bool = False,
    ):

        self._model = model
        self._priorize_setpoint = priorize_setpoint

        if unit == "mw":
            self._unit_factor = 1e-3
            self._pname = "p_mw"
            self._qname = "q_mvar"
        elif unit == "w":
            self._unit_factor = 1e3
            self._pname = "p_w"
            self._qname = "q_var"
        else:
            self._unit_factor = 1
            self._pname = "p_kw"
            self._qname = "q_kvar"

        self.schedule: Optional[Schedule] = None
        self._step_size: Optional[float] = None
        self._now_dt: Optional[datetime] = None
        self._percent_factor: float

        if self._model.config.use_decimal_percent:
            self._percent_factor = 0.01
        else:
            self._percent_factor = 1.0

    def update_schedule(self, schedule):
        if self.schedule is None:
            self._check_inputs()
        self.schedule.update(schedule)

    def step(self):
        """Perform a simulation step of the underlying model."""

        self._check_inputs()
        setpoint = self._get_setpoint()

        self._model.set_percent(setpoint)

        self._model.step()

        self.schedule.update_row(
            self._now_dt,
            setpoint,
            self._model.get_p_kw() * self._unit_factor,
            self._model.get_q_kvar() * self._unit_factor,
        )
        self.schedule.now_dt = self._now_dt
        self.schedule.prune()

    def _check_inputs(self) -> None:
        if self._model.inputs.step_size is not None:
            self._step_size = self._model.inputs.step_size
        if self._model.inputs.now_dt is not None:
            self._now_dt = self._model.inputs.now_dt
        if self.schedule is None:
            self.schedule = Schedule(
                self._pname,
                self._qname,
                self._now_dt,
                self._step_size,
            )
            self.schedule.init()
        if self.schedule.step_size is None:
            self.schedule.step_size = self._step_size

        if self._model.config.use_decimal_percent:
            self._percent_factor = 0.01
        else:
            self._percent_factor = 1.0

    def _get_setpoint(self) -> float:
        try:
            schedule_set = self.schedule.get(self._now_dt, "target")
        except TypeError:
            schedule_set = None

        try:
            model_set = self._model.get_percent_in()
        except TypeError:
            model_set = None

        try:
            default_set = (
                self._model.get_default_setpoint(self._now_dt.hour)
                * self._percent_factor
            )
        except TypeError:
            default_set = None

        priority = [schedule_set, model_set]
        if self._priorize_setpoint:
            priority = priority[::-1]
        priority.append(default_set)

        setpoint = None
        for setval in priority:
            if setval is not None and ~np.isnan(setval):
                setpoint = setval
                break
        # else:
        #     raise ValueError("Setpoint for model %s not set.", self._model)

        return setpoint

    def set_step_size(self, step_size):
        self._model.set_step_size(step_size)

    def set_now_dt(self, now_dt):
        self._model.set_now_dt(now_dt)

    def set_p_kw(self, p_kw):
        self._model.set_p_kw(p_kw)

    def set_q_kvar(self, q_kvar):
        self._model.set_q_kvar(q_kvar)

    def set_percent(self, percentage):
        self._model.set_percent(percentage)

    def get_now_dt(self):
        return self._model.get_now_dt()

    def get_p_kw(self):
        return self._model.get_p_kw()

    def get_q_kvar(self):
        return self._model.get_q_kvar()

    @property
    def inputs(self):
        return self._model.inputs

    @property
    def config(self):
        return self._model.config

    @property
    def state(self):
        return self._model.state

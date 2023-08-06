"""This module contains the :class:`ForecastModel`."""
from datetime import timedelta

import numpy as np
import pandas as pd
from pysimmods.model.model import Model

# from pysimmods.other.flexibility.schedule import Schedule
from pysimmods.other.flexibility.schedule_model import ScheduleModel

from . import LOG

# from pysimmods.util.date_util import GER


class ForecastModel(ScheduleModel):
    """The forecast model for all pysimmods.

    Parameters
    ----------
    model: :class:`.Model`
        An instance of a subclass of the base model class (e.g.,
        :class:`.Battery` model).
    start_date: str or datetime
        An ISO datetime string or a datetime object defining the start
        date.
    step_size: int, optional
        The step size of the model in seconds. Will be used as fallback
        if no step size is provided to the model. Defaults to 900.
    forecast_horizon_hours: float, optional
        The number of hours the model should create a forecast for.
        If the model needs a weather forecast, this weather forecast
        needs to be large enough.

    Attributes
    ----------
    model: :class:`.Model`
        A reference to the model.
    now_dt: :class:`.datetime.datetime`
        The current local time.
    step_size: int
        The step size of the model.
    forecasts: :class:`pandas.DataFrame`
        A dictionary containing forecasts for the inputs of the
        underlying model.
    flexibilities: dict
        A dictionary containing the current flexibilities of the
        underlying model.
    schedule: :class:`.Schedule`
        Contains the current schedule of the model.

    """

    def __init__(
        self,
        model: Model,
        unit="kw",
        priorize_setpoint: bool = False,
        forecast_horizon_hours=1,
    ):
        super().__init__(model, unit, priorize_setpoint)

        self._forecasts = None
        self._fch_hours = forecast_horizon_hours

    def step(self):
        """Perform a simulation step of the underlying model.

        Also updates the internal state of the flexibility model.

        """
        super().step()

        self._check_schedule()

    def update_forecasts(self, forecasts):
        if self._forecasts is None:
            self._forecasts = forecasts
        else:
            for col in forecasts.columns:
                if col not in self._forecasts.columns:
                    self._forecasts[col] = np.nan
            for index, _ in forecasts.iterrows():
                if index not in self._forecasts.index:
                    break

            # Update existing entries
            self._forecasts.update(forecasts.loc[:index])
            # Add missing entries
            self._forecasts = pd.concat(
                [self._forecasts, forecasts.loc[index:]]
            )
            # Remove duplicates
            self._forecasts = self._forecasts[
                ~self._forecasts.index.duplicated()
            ]

    def _check_schedule(self):

        if self.schedule.reschedule_required():
            self._create_default_schedule()
            self.schedule.prune()

    def _create_default_schedule(self):
        state_backup = self._model.get_state()

        now = self._now_dt + timedelta(seconds=self._step_size)
        periods = int(self._fch_hours * 3_600 / self._step_size)

        for _ in range(periods):
            self._prepare_step(now)
            self._perform_step(now)

            now += timedelta(seconds=self._step_size)

        self._model.set_state(state_backup)

    def _prepare_step(self, now):
        if not self.schedule.has_index(now):
            self.schedule.update_row(now, np.nan, np.nan, np.nan)

        default_setpoint = (
            self._model.get_default_setpoint(now.hour) * self._percent_factor
        )

        if np.isnan(self.schedule.get(now, "target")):
            self.schedule.update_entry(now, "target", default_setpoint)

    def _perform_step(self, now):
        try:
            self._calculate_step(now, self.schedule.get(now, "target"))

            self.schedule.update_entry(
                now,
                self._pname,
                self._model.get_p_kw() * self._unit_factor,
            )
            self.schedule.update_entry(
                now,
                self._qname,
                self._model.get_q_kvar() * self._unit_factor,
            )

        except KeyError:
            # Forecast is missing
            LOG.info(
                "No forecast provided at %s for model %s.",
                now,
                self._model,
            )
            self.schedule.update_row(now, np.nan, np.nan, np.nan)

    def _calculate_step(self, index, set_percent):
        self._model.set_percent(set_percent / self._percent_factor)

        if self._forecasts is not None:
            for col in self._forecasts.columns:
                if hasattr(self._model.inputs, col):
                    setattr(
                        self._model.inputs,
                        col,
                        self._forecasts.loc[index, col],
                    )

        self._model.set_now_dt(index)
        self._model.set_step_size(self._step_size)
        self._model.step()

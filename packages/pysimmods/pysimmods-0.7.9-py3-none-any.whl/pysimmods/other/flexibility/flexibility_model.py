"""This module contains the flexibility model."""
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from pysimmods.util.date_util import GER, TZ

from . import LOG
from .forecast_model import ForecastModel


class FlexibilityModel(ForecastModel):
    """The flexibility model for all pysimmods."""

    def __init__(
        self,
        model,
        unit="kw",
        priorize_setpoint=False,
        forecast_horizon_hours=1,
        seed=None,
    ):
        super().__init__(
            model, unit, priorize_setpoint, forecast_horizon_hours
        )

        if seed is not None:
            self._rng = np.random.RandomState(seed)
        else:
            self._rng = np.random.RandomState()

    def generate_schedules(
        self, start, flexibility_horizon_hours, num_schedules
    ):
        """Perform sampling and generate a set of schedules for the
        specified time interval.

        Args:
            start (str): Is the start of the planning horizon for which
                the sampling is done. It has to be provided as ISO 8601
                timezone string such as '2020-06-22 12:00:00+0000'

            forecast_horizon_hours (int): The planning horizon is divided into.

        """
        state_backup = self._model.get_state()
        step_size = self._step_size

        now_dt = self._now_dt
        start_dt = datetime.strptime(start, GER)
        end_dt = (
            start_dt
            + timedelta(hours=flexibility_horizon_hours)
            - timedelta(seconds=step_size)
        )
        periods = flexibility_horizon_hours * 3_600 / step_size

        # Fast forward to the planning interval
        while start_dt > now_dt:
            try:
                self._calculate_step(
                    now_dt,
                    self.schedule.get(now_dt, "target") / self._percent_factor,
                )
                now_dt += timedelta(seconds=step_size)
            except KeyError as err:
                # raise err
                LOG.info("Could not create flexibilities: %s", err)
                return dict()

        index = pd.date_range(start_dt, end_dt, periods=periods)

        self.flexibilities = dict()

        for schedule_id in range(num_schedules):
            schedule = self._generate_schedule(
                pd.DataFrame(
                    columns=["target", self._pname, self._qname],
                    index=index,
                )
            )

            self.flexibilities[schedule_id] = schedule.tz_convert(tz=TZ)

        self._model.set_state(state_backup)
        return self.flexibilities

    def _generate_schedule(self, dataframe):
        num_steps = len(dataframe.index)
        dataframe["target"] = self._rng.uniform(size=num_steps) / (
            0.01 / self._percent_factor
        )

        state_backup = self._model.get_state()
        for index, row in dataframe.iterrows():
            try:
                self._calculate_step(index, row["target"])
                dataframe.loc[index, self._pname] = (
                    self._model.get_p_kw() * self._unit_factor
                )
                dataframe.loc[index, self._qname] = (
                    self._model.get_q_kvar() * self._unit_factor
                )

            except KeyError:
                # Forecast is missing
                dataframe.loc[index, self._pname] = np.nan
                dataframe.loc[index, self._qname] = np.nan
                dataframe.loc[index, "target"] = np.nan
        self._model.set_state(state_backup)

        return dataframe

"""This module contains a :class:`mosaik_api.Simulator` for the
flexiblity model, which is a wrapper for all models of the
pysimmods package.

"""
import distutils
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Union

from midas.util.logging import set_and_init_logger
from midas.util.runtime_config import RuntimeConfig
import mosaik_api
import numpy as np
import pandas as pd
from pysimmods.mosaik import LOG
from pysimmods.other.flexibility.flexibility_model import (
    FlexibilityModel,
)
from pysimmods.other.flexibility.forecast_model import ForecastModel
from pysimmods.other.flexibility.schedule_model import ScheduleModel
from pysimmods.util.date_util import GER

from .meta import META, MODELS


class FlexibilitySimulator(mosaik_api.Simulator):
    """The generic flexiblity mosaik simulator for all pysimmods."""

    def __init__(self):
        super().__init__(META)
        self.sid = None
        self.models = dict()
        self.num_models = dict()

        self.step_size = None
        self.now_dt = None

        self.planning_horizon = None
        self.num_schedules = 0

        self._key_value_logs: bool = RuntimeConfig().misc.get(
            "key_value_logs", False
        )

    def init(self, sid, **sim_params):
        """Called exactly ones after the simulator has been started.

        Parameters
        ----------
        sid : str
            Simulator ID for this simulator.
        start_date : str
            The start date as UTC ISO 8601 date string.
        step_size : int, optional
            Step size for this simulator. Defaults to 900.

        Returns
        -------
        dict
            The meta dict (set by *mosaik_api.Simulator*).

        """
        self.sid = sid
        if "step_size" not in sim_params:
            LOG.debug(
                "Param *step_size* not provided. "
                "Using default step size of 900."
            )
        self.step_size = sim_params.get("step_size", 900)
        self.now_dt = datetime.strptime(
            sim_params["start_date"], GER
        ).astimezone(timezone.utc)

        self.unit = sim_params.get("unit", "kw")
        self.use_decimal_percent = sim_params.get("use_decimal_percent", False)
        if not isinstance(self.use_decimal_percent, bool):
            try:
                self.use_decimal_percent = bool(
                    distutils.util.strtobool(self.use_decimal_percent)
                )
            except AttributeError:
                self.use_decimal_percent = False

        self.priorize_setpoint = sim_params.get("priorize_setpoint", False)
        self.provide_forecasts = sim_params.get("provide_forecasts", False)
        self.forecast_horizon_hours = sim_params.get(
            "forecast_horizon_hours", self.step_size / 3_600
        )

        self.provide_flexibilities = sim_params.get(
            "provide_flexibilities", False
        )
        self.flexibility_horizon_hours = sim_params.get(
            "flexibility_horizon_hours", 2
        )
        self.num_schedules = sim_params.get("num_schedules", 10)
        self.rng = np.random.RandomState(sim_params.get("seed", None))

        self._update_meta()

        return self.meta

    def create(self, num, model, **model_params):
        """Initialize the simulation model instance (entity).

        Parameters
        ----------
        num : int
            The number of models to create.
        model : str
            The name of the models to create. Must be present inside
            the simulator's meta.

        Returns
        -------
        list
            A list with information on the created entity.

        """
        entities = []
        params = model_params["params"]
        params.setdefault("use_decimal_percent", self.use_decimal_percent)
        inits = model_params["inits"]
        self.num_models.setdefault(model, 0)

        for _ in range(num):
            eid = f"{model}-{self.num_models[model]}"
            if self.provide_flexibilities:
                self.models[eid] = FlexibilityModel(
                    MODELS[model](params, inits),
                    self.now_dt,
                    step_size=self.step_size,
                    forecast_horizon_hours=self.forecast_horizon_hours,
                    flexibility_horizon_hours=self.flexibility_horizon_hours,
                    num_schedules=self.num_schedules,
                    seed=self.rng.randint(1_000_000),
                    unit=self.unit,
                    use_decimal_percent=self.use_decimal_percent,
                    priorize_schedule=self.priorize_setpoint,
                )
            elif self.provide_forecasts:
                self.models[eid] = ForecastModel(
                    MODELS[model](params, inits),
                    unit=self.unit,
                    priorize_setpoint=self.priorize_setpoint,
                    forecast_horizon_hours=self.forecast_horizon_hours,
                )
            else:
                self.models[eid] = ScheduleModel(
                    MODELS[model](params, inits),
                    unit=self.unit,
                    priorize_setpoint=self.priorize_setpoint,
                )
            self.num_models[model] += 1
            entities.append({"eid": eid, "type": model})
        return entities

    def step(self, time, inputs, max_advance=0):
        """Perform a simulation step.

        Parameters
        ----------
        time : int
            The current simulation step (by convention in seconds since
            simulation start.
        inputs : dict
            A *dict* containing inputs for entities of this simulator.

        Returns
        -------
        int
            The next step this simulator wants to be stepped.

        """
        LOG.debug("At step %d: Received inputs: %s.", time, inputs)

        self._default_inputs()
        self._mosaik_inputs(inputs)

        for eid, model in self.models.items():
            model.step()

        self.now_dt += timedelta(seconds=self.step_size)
        self._generate_flexibilities()

        return time + self.step_size

    def get_data(self, outputs):
        """Returns the requested outputs (if feasible)"""

        data = dict()
        for eid, attrs in outputs.items():
            data[eid] = dict()
            # model = eid.split("-")[0]
            log_msg = {
                "id": f"{self.sid}_{eid}",
                "name": eid,
                "type": "modelname",
            }
            for attr in attrs:

                if attr == "flexibilities":
                    value = self.models[eid].flexibilities
                elif attr == "schedule":
                    value = (
                        self.models[eid]
                        .schedule._data.loc[
                            self.now_dt : self.now_dt
                            + timedelta(hours=self.forecast_horizon_hours)
                            - timedelta(seconds=self.step_size)
                        ]
                        .to_json()
                    )
                    log_msg[attr] = value
                elif attr == "target":
                    value = self.models[eid].schedule._data.loc[
                        self.now_dt - timedelta(seconds=self.step_size)
                    ]["target"]

                else:
                    # Apply correction of the attr if necessary
                    if attr in ("p_mw", "p_th_mw", "q_mvar"):
                        true_attr = attr.replace("m", "k")
                    else:
                        true_attr = attr

                    if true_attr == "p_kw":
                        value = self.models[eid].get_p_kw()
                    elif true_attr == "q_kvar":
                        value = self.models[eid].get_q_kvar()
                    else:
                        value = getattr(self.models[eid].state, true_attr)

                    # Apply correction of the value if necessary
                    if attr in ("p_mw", "p_th_mw", "q_mvar"):
                        value *= 1e-3

                    log_msg[attr] = value

                data.setdefault(eid, dict())[attr] = value

            if self._key_value_logs:
                LOG.info(log_msg)

        LOG.debug("Gathered outputs: %s.", data)
        return data

    def _update_meta(self):
        for model in self.meta["models"].keys():
            self.meta["models"][model]["attrs"].append("flexibilities")
            self.meta["models"][model]["attrs"].append("schedule")
            self.meta["models"][model]["attrs"].append("target")

        self.meta["models"]["Photovoltaic"]["attrs"] += [
            "forecast_t_air_deg_celsius",
            "forecast_bh_w_per_m2",
            "forecast_dh_w_per_m2",
        ]
        self.meta["models"]["CHP"]["attrs"] += [
            "forecast_day_avg_t_air_deg_celsius"
        ]
        self.meta["models"]["HVAC"]["attrs"] += ["forecast_t_air_deg_celsius"]

    def _default_inputs(self):
        for eid, model in self.models.items():
            model.set_step_size(self.step_size)
            model.set_now_dt(self.now_dt)

    def _mosaik_inputs(self, inputs):

        for eid, attrs in inputs.items():
            for attr, src_ids in attrs.items():

                if "forecast" in attr:
                    for forecast in src_ids.values():
                        if not isinstance(forecast, pd.DataFrame):
                            forecast = pd.read_json(forecast).tz_localize(
                                "UTC"
                            )
                        self.models[eid].update_forecasts(forecast)
                    continue
                elif attr == "schedule":
                    for schedule in src_ids.values():
                        if schedule is not None:
                            schedule = deserialize_schedule(schedule)

                            if not schedule.empty:
                                self.models[eid].update_schedule(schedule)
                    continue

                elif attr == "local_time":
                    # Use time information from time generator
                    for val in src_ids.values():
                        self.models[eid].set_now_dt(val)
                        self.now_dt = datetime.strptime(val, GER).astimezone(
                            timezone.utc
                        )
                        break
                    continue

                # Aggregate inputs from different sources
                attr_sum = 0
                for src_id, val in src_ids.items():
                    if val is None:
                        continue
                    if isinstance(val, np.ndarray):
                        val = val[0]
                    attr_sum += val
                attr_sum /= len(src_ids)

                # Apply corrections
                if attr in ("p_set_mw", "p_th_set_mw", "q_set_mvar"):
                    attr = attr.replace("m", "k")
                    attr_sum *= 1e3

                # Set the inputs
                if attr == "set_percent":
                    self.models[eid].set_percent(
                        attr_sum / self.models[eid]._percent_factor
                    )
                elif attr == "p_set_kw":
                    self.models[eid].set_p_kw(attr_sum)
                elif attr == "q_set_kvar":
                    self.models[eid].set_q_kvar(attr_sum)
                else:
                    setattr(self.models[eid].inputs, attr, attr_sum)

    def _generate_flexibilities(self):
        if self.provide_flexibilities:
            for eid, model in self.models.items():
                model.generate_schedules(
                    self.now_dt.strftime(GER),
                    self.flexibility_horizon_hours,
                    self.num_schedules,
                )


def deserialize_schedule(
    schedule: Union[pd.DataFrame, Dict[str, Any], str]
) -> pd.DataFrame:
    """Convert the schedule provided by mosaik to DataFrame"""

    if isinstance(schedule, pd.DataFrame):
        return schedule

    if isinstance(schedule, dict):
        # The schedule might be nested into the schedule because of an
        # ICT simulator
        return deserialize_schedule(list(schedule.values())[0])

    if isinstance(schedule, str):
        return pd.read_json(schedule).tz_localize("UTC")

    raise ValueError(
        f"Unsupported schedule format {type(schedule)}: {schedule}"
    )


if __name__ == "__main__":
    set_and_init_logger(
        0, "pysimmods-logfile", "pysimmods-flex.log", replace=True
    )
    LOG.info("Starting mosaik simulation...")
    mosaik_api.start_simulation(FlexibilitySimulator())

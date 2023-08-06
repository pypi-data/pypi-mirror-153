"""This module contains a :class:`mosaik_api.Simulator` for all models
of the pysimmods package.

"""
import pprint
from datetime import datetime, timedelta, timezone
from multiprocessing.sharedctypes import Value

import mosaik_api
import numpy as np
from midas.util.dict_util import strtobool
from midas.util.logging import set_and_init_logger
from pysimmods.mosaik import LOG
from pysimmods.util.date_util import GER

from .meta import META, MODELS


class PysimmodsSimulator(mosaik_api.Simulator):
    """The Pysimmods simulator."""

    def __init__(self):
        super().__init__(META)
        self.sid = None
        self.models = dict()
        self.num_models = dict()

        self.step_size = None
        self.now_dt = None
        self.percent_factor = 1.0

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

        use_decimal_percent = sim_params.get("use_decimal_percent", False)
        if not isinstance(use_decimal_percent, bool):
            try:
                use_decimal_percent = strtobool(use_decimal_percent)
            except ValueError:
                use_decimal_percent = False

        if use_decimal_percent:
            self.percent_factor = 0.01
        else:
            self.percent_factor = 1.0

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
        entities = list()
        params = model_params["params"]
        inits = model_params["inits"]
        self.num_models.setdefault(model, 0)

        for _ in range(num):

            eid = f"{model}-{self.num_models[model]}"
            self.models[eid] = MODELS[model](params, inits)
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
        LOG.debug(
            "At step %d: Received inputs: %s.",
            time,
            pprint.pformat(inputs),
        )
        # Set default inputs
        for eid, model in self.models.items():
            model.set_step_size(self.step_size)
            model.set_now_dt(self.now_dt)

        # Set inputs from other simulators
        for eid, attrs in inputs.items():
            for attr, src_ids in attrs.items():

                # Use time information from time generator
                if attr == "local_time":
                    for val in src_ids.values():
                        self.models[eid].set_now_dt(val)
                        break
                    continue

                # Aggregate inputs from different sources
                attr_sum = 0
                for val in src_ids.values():
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
                        attr_sum / self.percent_factor
                    )
                elif attr == "p_set_kw":
                    self.models[eid].set_p_kw(attr_sum)
                elif attr == "q_set_kvar":
                    self.models[eid].set_q_kvar(attr_sum)
                else:
                    setattr(self.models[eid].inputs, attr, attr_sum)

        # Step the models
        for model in self.models.values():
            model.step()
            p = model.state.p_kw

        # Update time for the next step
        self.now_dt += timedelta(seconds=self.step_size)

        return time + self.step_size

    def get_data(self, outputs):
        """Return the requested output (if feasible).

        Parameters
        ----------
        outputs : dict
            A *dict* containing requested outputs of each entity.

        Returns
        -------
        dict
            A *dict* containing the values of the requested outputs.

        """

        data = dict()
        for eid, attrs in outputs.items():
            for attr in attrs:
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

                data.setdefault(eid, dict())[attr] = value

        LOG.debug("Gathered outputs: %s.", pprint.pformat(data))
        return data


if __name__ == "__main__":
    set_and_init_logger(
        0, "pysimmods-logfile", "pysimmods-mosaik.log", replace=True
    )
    LOG.info("Starting mosaik simulation...")
    mosaik_api.start_simulation(PysimmodsSimulator())

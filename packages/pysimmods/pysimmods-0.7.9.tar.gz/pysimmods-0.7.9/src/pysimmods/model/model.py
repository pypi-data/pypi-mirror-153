"""This module contains the base class for all pysimmods models."""
import copy
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Union

from .config import ModelConfig
from .inputs import ModelInputs
from .state import ModelState


class Model(ABC):
    """Base class for pysimmods models.

    Normally, other models should not directly derive from this class;
    there are interface classes for consumers, buffers, and generators,
    as well.

    The *Model* class provides an interface for all models within this
    package. It takes two dictionaries at construction time, one for
    configuration parameters of the model and one to provide an initial
    state for the model. Those can be accessed via different attributes.

    Methods for accessing the most important attributes are provided as
    well as generic get/set state methods.

    All interface methods have in common that they consider the sign
    convention, i.e, in the (default) passive sign convention, power
    consumption is denoted with a positive sign while generation has a
    negative sign. Internally, all models use positive signs. The only
    exception mark the buffer models, which can both consume and
    generate power.

    Parameters
    ----------
    params : dict
        A *dict* containing configuration parameters.
    inits : dict
        A *dict* containing the state variables.

    Attributes
    ----------
    config: :class:`.ModelConfig`
        A config object holding all the configuration parameters of
        this model. These do not change during simulation.
    state: :class:`.ModelState`
        A state object holding all variable parameters of this model.
        These values normally change during each step.
    inputs: :class:`.ModelInputs`
        An inputs object defining the inputs for this model. In each
        step, all the inputs need to be provided.

    """

    def __init__(self, params: dict, inits: dict) -> None:
        self.config: ModelConfig
        self.state: ModelState
        self.inputs: ModelInputs

    @abstractmethod
    def step(self) -> None:
        """Perform a simulation step.

        All required input variables need to be set beforehand. In
        *step*, inputs will be interpreted and calculation results of
        the model will be stored in the state of the model.
        """

    def get_state(self) -> dict:
        """Return the current state of the model.

        Returns
        -------
        dict
            The current state of the model in form of a dictionary
            containing entries for all state variables. Returned dict
            can be assigned to the *inits* argument when creating a new
            model instance.

        """

        try:
            return {
                attr: getattr(self.state, attr)
                for attr in self.state.__slots__
            }
        except AttributeError:
            return copy.deepcopy(self.state.__dict__)

    def set_state(self, state: dict) -> None:
        """Set the current state of the model.

        Parameters
        ----------
        state : dict
            A *dict* containing entries for all state variables.

        """
        for attr, value in state.items():
            setattr(self.state, attr, value)

    @abstractmethod
    def set_p_kw(self, p_kw: float) -> None:
        """Set the target value for active power for the model's next
        step.

        The value will be checked against the boundaries p_min_kw and
        p_max_kw.

        """

    @abstractmethod
    def get_p_kw(self) -> float:
        """Return the current active power output of the model."""

    def get_pn_max_kw(self) -> float:
        """Maximum nominal active power output of the model.

        The output depends on the used sign convention. The base
        implementation is done in the consumer/generator/buffer
        subclasses.

        """
        return self.config.p_max_kw

    def get_pn_min_kw(self) -> float:
        """Minimum nominal active power output of the model.

        The output depends on the used sign convention. The minimum
        output is always the minimal output **while the model is
        active**. In contrast, the models can be turned off, which is
        indicated by an output of 0.

        """
        return self.config.p_min_kw

    def set_percent(self, percentage: float) -> None:
        """Convenience function to set the desired output of the model.

        *percentage* is expected to be a value between 0 and 100 (unless
        the :attr:`_use_decimal_percentage` is set to True; in that case
        the value is expected to be within [0, 1.0]).

        A value of exactly 0 will indicate the model to turn off. For
        any other value, percentage is some valid value between the
        model's p_min_kw and p_max_kw (exception here, if the model is
        able to output reactive power, see (insert link)).

        Parameters
        ----------
        percentage: float
            Percentage setpoint value for the model between 0 and 100.
        """
        if percentage <= 0:
            self.inputs.p_set_kw = 0
            return

        if self.config.use_decimal_percent:
            decimal = max(min(abs(percentage), 1.0), 0.0)
        else:
            # Internally, decimal percentage is used.
            decimal = max(min(abs(percentage), 100.0), 0.0) / 100.0

        if decimal <= 0.0001:
            # Map values lower than 0.01 % to minimum power
            decimal = 0
        if decimal > 1.0:
            # Map values higher than 1 to maximum power
            decimal = 1.0

        p_max_kw = self.get_pn_max_kw()
        p_min_kw = self.get_pn_min_kw()

        self.inputs.p_set_kw = p_min_kw + decimal * (p_max_kw - p_min_kw)

    def get_percent_in(self) -> float:
        """Return the percentage setpoint."""
        p_kw = self.inputs.p_set_kw
        if p_kw is None:
            return None

        return self._get_percent(
            p_kw, self.get_pn_min_kw(), self.get_pn_max_kw()
        )

    def get_percent_out(self) -> float:
        """Return the percentage output power."""
        p_kw = self.state.p_set_kw
        if p_kw is None:
            return None

        return self._get_percent(
            p_kw, self.get_pn_min_kw(), self.get_pn_max_kw()
        )

    def set_step_size(self, step_size: int):
        step_size = int(step_size)
        assert step_size > 0, "step_size must be greater than zero"

        self.inputs.step_size = step_size

    def set_now_dt(self, now: Union[datetime, str, int]) -> None:
        """Set the current date and time of the model.

        The parameter *now* can be either a datetime object, an UTC ISO
        8601 time string or a unit timestamp (in seconds, as int). The
        value will be converted and stored as datetime in UTC time
        internally.

        Parameters
        ----------
        now: Union[datetime, str, int]
            The current date and time to set.

        """

        self.inputs.now_dt = now

    def get_now_dt(self) -> datetime:
        """Return the current date and time of the model.

        TODO: Return the value from inputs or from state?

        """
        raise NotImplementedError()

    def set_q_kvar(self, q_kvar) -> None:
        """Set the target value for reactive power for the model's next
        step.

        The value will be checked against the boundaries q_min_kvar and
        q_max_kvar.

        """
        raise NotImplementedError()

    def get_q_kvar(self) -> float:
        """Return the current reactive power output of the model."""
        return 0

    def get_qn_max_kvar(self) -> float:
        """Maximum nominal reactive power output of the model.

        The output depends on the used sign convention. The base
        implementation is done in the consumer/generator/buffer
        subclasses.

        """
        raise NotImplementedError()

    def get_qn_min_kvar(self) -> float:
        """Minimum nominal reactive power output of the model.

        The output depends on the used sign convention and the model's
        capability to output reactive power. The minimum output is
        always the minimal output **while the model is active**.

        In contrast, the models can be turned off, which is
        indicated by an output of 0 as well as if the model cannot
        output reactive power.

        """
        raise NotImplementedError()

    def get_default_schedule(self) -> List[float]:
        """Return the default schedule.

        Returns
        -------
        list
            A *list* containing a default schedule with percentage
            power for each hour of the day (i.e.,
            len(default_schedule) == 24). This is used if no other *p*
            or *q* input is provided.

        """
        return self.config.default_schedule

    def _get_percent(self, val, val_min, val_max):
        if val > 0:
            # Following the primary purpose
            decimal = (val - val_min) / (val_max - val_min)
            if decimal < 0:
                # val is too low, turn off
                return 0

            # We don't allow 0 if the unit is turned on
            decimal = max(0.0001, decimal)

            if self.config.use_decimal_percent:
                return decimal
            else:
                return decimal * 100
        else:
            # Unit is off or does not follow primary purpose
            return 0

    def get_default_setpoint(self, hour: int) -> float:
        """Return the value of the default schedule at *hour*"""
        hour = max(0, min(23, hour))
        return self.config.default_schedule[hour]

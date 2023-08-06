from copy import copy

from pysimmods.generator.dieselsim.config import DieselGenConfig
from pysimmods.generator.dieselsim.inputs import DieselGenInputs
from pysimmods.generator.dieselsim.state import DieselGenState
from pysimmods.model.generator import Generator


class DieselGenerator(Generator):
    def __init__(self, params, inits):
        super().__init__(params, inits)
        self.config = DieselGenConfig(params)
        self.state = DieselGenState(inits)
        self.inputs = DieselGenInputs()

    def step(self):
        nstate = copy(self.state)

        self._check_inputs(nstate)

        self.state = nstate

    def _check_inputs(self, nstate):
        """Check constraints for active power."""
        if self.inputs.p_set_kw is None:
            hour = self.inputs.now_dt.hour
            default = self.config.default_schedule[hour]
            if default == 0:
                nstate.p_kw = 0
            else:
                nstate.p_kw = self.config.p_min_kw + (
                    (self.config.p_max_kw - self.config.p_min_kw)
                    * default
                    / 100
                )
        else:
            if self.inputs.p_set_kw != 0:
                nstate.p_kw = max(
                    min(
                        abs(self.inputs.p_set_kw),
                        self.config.p_max_kw,
                    ),
                    self.config.p_min_kw,
                )
            else:
                nstate.p_kw = 0

    # @property
    # def set_percent(self):
    #     p_kw = self.inputs.p_set_kw
    #     if p_kw is None:
    #         p_kw = self.state.p_kw

    #     p_kw = (p_kw - self.config._p_min_kw) / (
    #         self.config._p_max_kw - self.config._p_min_kw
    #     )
    #     return abs(p_kw) * 100

    # @set_percent.setter
    # def set_percent(self, value):
    #     value = max(min(abs(value), 100.0), 0.0)

    #     if value == 0:
    #         p_set_kw = 0
    #     else:
    #         p_range = self.config._p_max_kw - self.config._p_min_kw
    #         p_set_kw = self.config._p_min_kw + value / 100 * p_range

    #     self.inputs.p_set_kw = p_set_kw

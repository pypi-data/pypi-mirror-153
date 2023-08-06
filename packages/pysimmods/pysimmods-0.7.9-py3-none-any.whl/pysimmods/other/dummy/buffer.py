from pysimmods.model.buffer import Buffer
from pysimmods.model.config import ModelConfig
from pysimmods.model.inputs import ModelInputs
from pysimmods.model.state import ModelState


class DummyBufferConfig(ModelConfig):
    def __init__(self, params):
        params.setdefault("default_schedule", [10] * 24)
        super().__init__(params)

        self.p_max_kw = params.get("p_max_kw", 500)
        self.p_min_kw = params.get("p_min_kw", 250)
        self.q_max_kvar = params.get("q_max_kvar", 100)
        self.q_min_kvar = params.get("q_min_kvar", 25)

        if "p_charge_max_kw" in params:
            self.p_charge_max_kw = params["p_charge_max_kw"]
        if "p_charge_min_kw" in params:
            self.p_charge_min_kw = params["p_charge_min_kw"]
        if "p_discharge_max_kw" in params:
            self.p_discharge_max_kw = params["p_discharge_max_kw"]
        if "p_discharge_min_kw" in params:
            self.p_discharge_min_kw = params["p_discharge_min_kw"]


class DummyBufferState(ModelState):
    pass


class DummyBufferInputs(ModelInputs):
    pass


class DummyBuffer(Buffer):
    """The dummy buffer model."""

    def __init__(self, params, inits):
        self.config = DummyBufferConfig(params)
        self.state = DummyBufferState(inits)
        self.inputs = DummyBufferInputs()

    def step(self):
        self.state.p_kw = self.inputs.p_set_kw

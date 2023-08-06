from pysimmods.model.config import ModelConfig
from pysimmods.model.consumer import Consumer
from pysimmods.model.inputs import ModelInputs
from pysimmods.model.state import ModelState


class DummyConsumerConfig(ModelConfig):
    def __init__(self, params):
        params.setdefault("default_schedule", [10] * 24)
        super().__init__(params)

        self.p_max_kw = params.get("p_max_kw", 500)
        self.p_min_kw = params.get("p_min_kw", 250)
        self.q_max_kvar = params.get("q_max_kvar", 100)
        self.q_min_kvar = params.get("q_min_kvar", 25)


class DummyConsumerState(ModelState):
    pass


class DummyConsumerInputs(ModelInputs):
    pass


class DummyConsumer(Consumer):
    """The dummy buffer model."""

    def __init__(self, params, inits):
        self.config = DummyConsumerConfig(params)
        self.state = DummyConsumerState(inits)
        self.inputs = DummyConsumerInputs()

    def step(self):
        self.state.p_kw = self.inputs.p_set_kw

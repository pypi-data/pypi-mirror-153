from pysimmods.model.config import ModelConfig
from pysimmods.model.generator import Generator
from pysimmods.model.inputs import ModelInputs
from pysimmods.model.state import ModelState


class DummyGeneratorConfig(ModelConfig):
    def __init__(self, params):
        params.setdefault("default_schedule", [10] * 24)
        super().__init__(params)

        self.p_max_kw = params.get("p_max_kw", 500)
        self.p_min_kw = params.get("p_min_kw", 250)


class DummyGeneratorState(ModelState):
    pass


class DummyGeneratorInputs(ModelInputs):
    pass


class DummyGenerator(Generator):
    """The dummy buffer model."""

    def __init__(self, params, inits):
        self.config = DummyGeneratorConfig(params)
        self.state = DummyGeneratorState(inits)
        self.inputs = DummyGeneratorInputs()

    def step(self):
        self.state.p_kw = self.inputs.p_set_kw

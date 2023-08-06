from pysimmods.model.config import ModelConfig
from pysimmods.model.qgenerator import QControl, QGenerator
from pysimmods.model.inputs import ModelInputs
from pysimmods.model.state import ModelState


class DummyGeneratorConfig(ModelConfig):
    def __init__(self, params):
        super().__init__(params)

        self.p_max_kw = params.get("p_max_kw", 500)
        self.p_min_kw = params.get("p_min_kw", 250)
        self.s_max_kva = params.get("s_max_kva", self.p_max_kw * 1.2)
        self.q_control = params.get("q_control", QControl.P_SET)
        self.cos_phi = params.get("cos_phi", 0.9)


class DummyGeneratorState(ModelState):
    pass


class DummyGeneratorInputs(ModelInputs):
    def __init__(self):
        super().__init__()

        self.cos_phi = None


class DummyQGenerator(QGenerator):
    """The dummy buffer model."""

    def __init__(self, params, inits):
        self.config = DummyGeneratorConfig(params)
        self.state = DummyGeneratorState(inits)
        self.inputs = DummyGeneratorInputs()

    def step(self):
        self.state.p_kw = self.inputs.p_set_kw
        self.state.q_kvar = self.inputs.q_set_kvar

from pysimmods.model.inputs import ModelInputs


class DieselGenInputs(ModelInputs):
    """Captures the input variables of the diesel generator model

    Input variables can be modified from outside the diesel generator
    model before calling the step-method. They are used as an input for
    the calculation of new values for the state variables in the
    step-method.

    """

from pysimmods.model.inputs import ModelInputs


class BatteryInputs(ModelInputs):
    """Captures the input variables of the battery model

    Input variables can be modified from outside the battery model before
    calling the step-method. They are used as an input for the calculation of
    new values for the state variables in the step-method.

    """

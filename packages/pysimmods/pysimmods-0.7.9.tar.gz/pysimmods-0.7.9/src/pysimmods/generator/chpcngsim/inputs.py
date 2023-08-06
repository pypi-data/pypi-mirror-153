"""This module contains the input model for the chp."""
from pysimmods.model.inputs import ModelInputs


class CHPCNGInputs(ModelInputs):
    """A CHP CNG input class."""

    def __init__(self):
        super().__init__()

        self.gas_in_m3 = None
        """Available gas (e.g from a gas storage) in [m^3]."""

        self.gas_critical = False
        """If set to True, this unit will reduce generation."""

        self.heat_critical = False
        """If set to True, this unit will increase generation.
        Has lower priority than gas_critical.
        """

    def reset(self):
        """To be called at the end of each step."""
        for attr in self.__dict__.keys():
            setattr(self, attr, None)

        self.gas_critical = False
        self.heat_critical = False

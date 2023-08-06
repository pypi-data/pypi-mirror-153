"""
This module contains a reimplementation of the MATLAB battery model
provided by the TU Munich in context of the research project iHEM
(intelligent Home Energy Management).

"""
from copy import copy

from pysimmods.buffer.batterysim import LOG
from pysimmods.buffer.batterysim.config import BatteryConfig
from pysimmods.buffer.batterysim.inputs import BatteryInputs
from pysimmods.buffer.batterysim.state import BatteryState
from pysimmods.model.buffer import Buffer


class Battery(Buffer):
    """Simple battery simulation model

    Self-discharge and aging are not considered. Effect of charging power on
    efficiency eta is modelled by fitting a polynomial model to data measured
    by TU Munich.

    You have to provide the two dictionaries *params* and *inits*.
    *params* provides the configuration parameters for the battery model and
    might look like this::

        {
            'cap_kwh': 5,
            'p_charge_max_kw': 1,
            'p_discharge_max_kw': 1,
            'soc_min_percent': 15,
            'eta_pc': [-2.109566, 0.403556, 97.110770],
        }

    Here *cap_kwh* is the electric capacity of the battery in kWh. *p_min_kw*
    and *p_max_kw* specify the minimum and maximum power of the battery in kW.
    Negative values indicate charging (battery is a consumer).  Positive values
    indicate discharging (battery is a producer). *soc_min_percent* indicates
    the minimum state of charge in percent below which discharging is stopped.
    The entry *eta_pc* is a list and contains the coefficients a, b, c of a
    quadratic polynomial function, which is used to model power dependency of
    efficiency.

    The dict *inits* provides initial values for state variables. The
    battery model has only one state variable that must be specified when the
    model is initialized. It is *soc_percent*, which indicates the initial
    state of charge in percent of battery capacity. The model has two more
    state variables *p_kw* and *eta_percent*. They indicate the current power
    and efficiency of the battery. But as they are flow quantities and their
    current value has no effect in the next simulation step, they are just set
    to None during initialization of the model::

        {
            'soc_percent': 50
        }

    Attributes
    ----------
    config : :class:`~.BatteryConfig`
        Stores the configuration parameters of the battery model.
    state : :class:`~.BatteryState`
        Stores the initialization parameters of the battery model.
    inputs : :class:`~.BatteryInputs`
        Stores the input parameters for each step of the battery
        model.

    """

    def __init__(self, params, inits):
        self.config = BatteryConfig(params)
        self.state = BatteryState(inits)
        self.inputs = BatteryInputs()

    def step(self):
        """Perform a simulation step."""

        nstate = copy(self.state)

        self._check_inputs(nstate)

        self._calculate_efficiency(nstate)

        if nstate.p_kw * self.config.gsign > 0:
            self._discharge(nstate)
        else:
            self._charge(nstate)

        nstate.soc_percent = nstate._energy_kwh / self.config.cap_kwh * 100

        self.state = nstate
        self.inputs.reset()

    def _check_inputs(self, nstate):
        """Check constraints for active power."""
        if self.inputs.p_set_kw is None:
            if self.inputs.now_dt is not None:
                default_val = self.config.default_schedule[
                    self.inputs.now_dt.hour
                ]
                if self.config.use_decimal_percent:
                    default_val *= 0.01

                self.set_percent(default_val)
                nstate.p_kw = self.inputs.p_set_kw
            else:
                nstate.p_kw = 0
        else:
            nstate.p_kw = self.inputs.p_set_kw

    def _calculate_efficiency(self, nstate):
        """Calculate efficiency using a second degree polynomial."""

        nstate._energy_kwh = self.config.cap_kwh * self.state.soc_percent / 100
        p_set_norm = nstate.p_kw / self.config.cap_kwh

        nstate.eta_percent = (
            self.config.eta_pc[0] * p_set_norm**2
            + self.config.eta_pc[1] * p_set_norm
            + self.config.eta_pc[2]
        )

    def _discharge(self, nstate):
        LOG.debug("Battery is discharging.")

        delta_energy_kwh = (
            nstate.p_kw
            / (nstate.eta_percent / 100)
            * (self.inputs.step_size / 3600)
        )

        theoretical_energy_kwh = (
            nstate._energy_kwh
            - self.config.cap_kwh * self.config.soc_min_percent / 100
        )

        if theoretical_energy_kwh > abs(delta_energy_kwh):
            # Won't be fully discharged in this step
            nstate._energy_kwh += delta_energy_kwh
        else:
            # Will be fully discharged in this step
            nstate.p_kw = theoretical_energy_kwh / (
                self.inputs.step_size / 3600
            )
            nstate._energy_kwh = (
                self.config.soc_min_percent / 100 * self.config.cap_kwh
            )
            nstate.p_kw *= nstate.eta_percent / -100

    def _charge(self, nstate):
        delta_energy_kwh = (
            nstate.p_kw
            * (nstate.eta_percent / 100)
            * (self.inputs.step_size / 3600)
        )

        if (self.config.cap_kwh - nstate._energy_kwh) > delta_energy_kwh:
            # Won't be fully charged in this step
            nstate._energy_kwh += delta_energy_kwh
        else:
            # Will be fully charged in this step
            nstate.p_kw = (self.config.cap_kwh - nstate._energy_kwh) / (
                self.inputs.step_size / 3600
            )
            nstate._energy_kwh = self.config.cap_kwh
            nstate.p_kw /= nstate.eta_percent * 100

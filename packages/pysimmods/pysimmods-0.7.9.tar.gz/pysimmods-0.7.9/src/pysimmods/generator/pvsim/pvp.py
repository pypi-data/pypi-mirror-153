"""This module contains a simulation model of a PV plant. The model was
developed within the scope of the research project iHEM (intelligent
Home Energy Management).

"""
from pysimmods.generator.pvsim.config import PVConfig
from pysimmods.generator.pvsim.inputs import PVInputs
from pysimmods.generator.pvsim.state import PVState
from pysimmods.model.generator import Generator
from pysimmods.util import irradiance, solargeometry


class PhotovoltaicPowerPlant(Generator):
    """Simulation model of a photovoltaic plant.

    A PV plant consists of one or more modules, but the model treats
    all modules as one big module. Impact of the temperature of the PV
    module on efficiency is considered. Therefore the temperature of
    the PV plant is explicitly modelled. The PV modules are considered
    to be homogeneous bodies, which are specified by their mass per
    unit area and heat capacity. To model the temperature of the PV
    modules heat flows between the PV modules and environment are
    calculated in each simulation step. The PV modules are heated by
    the share of sun radiation, which is not reflected by the surface
    of the PV modules and which is not converted into electric energy.
    At the same time, the PV plant releases heat to the ambient air.
    This heat flow is considered to be proportional to the temperature
    gradient between air temperature and module temperature. The
    corresponding proportionality factor is the heat transmission
    coefficient between air and module. Wind speed dependency of this
    coefficient is not taken into account.

    You have to provide the two dictionaries *params* and *inits*.
    The dict *params* provides the parameters for the PV plant model
    and should at least look like this::

        {
            'a_m2': 15.0,
            'eta_percent': 25,
        }

    The parameter *a_m2* specifies the overall area of the PV modules
    in square meter. Additional parameters can be provided, see
    :class:`~.config.PVConfig`.
    The parameter *eta_percent* is optional and specifies the
    efficiency of the PV plant.
    The peak power of the PV plant depends directly on the size of the
    Surface and the efficiency and is defined as::

        p_peak_kw = eta_percent/100 * a_m2

    The dict *inits* provides the initial values for the state variables.
    The PV plant model has one state variable that must be specified when
    the model is initialized. It is *t_module_deg_celsius* (indicates the
    temperature of the PV modules in °C)::

            {
                't_module_deg_celsius': 25
            }

    Parameters
    ----------
    params : dict
        Configuration parameters as described above. See
        :class:`~.PVConfig` for all parameters.
    inits : dict
        Initialization parameters as described above. See
        :class:`~.PVState` for all parameters.

    Attributes
    ----------
    config : :class:`~.PVConfig`
        Stores the configuration parameters of the PV plant model.
    state : :class:`~.PVState`
        Stores the initialization parameters of the PV plant model.
    inputs : :class:`~.PVInputs`
        Stores the input parameters for each step of the PV plant
        model.

    """

    def __init__(self, params, inits):
        self.config = PVConfig(params)
        self.state = PVState(inits)
        self.inputs = PVInputs()

    def step(self):
        """perform simulation step

        Irradiance on plant depends on current solar position and
        orientation and tilt of the PV modules. To calculate the total
        irradiance on the tilted PV modules, functions
        :func:`~.tilted_surface` and :func:`~.compute_sun_position` are
        applied.

        """
        self._check_inputs()

        if self.config.has_external_irradiance_model:
            irradiance_w_per_m2 = self.inputs.s_module_w_per_m2
        else:
            if self.inputs.bh_w_per_m2 > 2 or self.inputs.dh_w_per_m2 > 2:
                sun_pos = solargeometry.compute_sun_position(
                    self.inputs.now_dt.timestamp(),
                    self.config.lat_deg,
                    self.config.lon_deg,
                )
                args = [
                    self.inputs.bh_w_per_m2,
                    self.inputs.dh_w_per_m2,
                    self.config.tilt_deg,
                    self.config.orient_deg,
                    sun_pos["elevation"],
                    sun_pos["azimuth"],
                ]
                irradiance_w_per_m2 = irradiance.tilted_surface(*args)
            else:
                irradiance_w_per_m2 = 0

        # calculate heat balance, irradiance induced heat flow
        # (Watt/m2, pos. sign indicates heat uptake of plant)
        if not self.config.is_static_t_module:
            t_module_change = self._calculate_module_temperature(
                irradiance_w_per_m2
            )

            self.state.t_module_deg_celsius += t_module_change

        # temperature for which eta_percent was measured
        t_ref_deg_celsius = 25  # °C

        # calculate alternating current power output of plant
        k_temp = (
            1
            - self.config.beta_percent_per_kelvin
            * max(self.state.t_module_deg_celsius - t_ref_deg_celsius, 0)
            / 100
        )
        # factor for temperature dependency of module efficiency

        eff_rel_max = (self.config.k_m_w_per_m2 + 1e3) / 1e3
        k_irradicance = (
            eff_rel_max
            * irradiance_w_per_m2
            / (self.config.k_m_w_per_m2 + irradiance_w_per_m2)
        )
        # factor for irradiance dependency of module efficiency
        # k_irr is modeled by a saturation curve whose function value is 0.5 if
        # the total irradiance equals K_m and 1.0 if the total
        # irradiance equals the irradiance at standard conditions
        # (1000 Watt/m2)

        self.state.p_kw = (
            irradiance_w_per_m2
            * self.config.eta_percent
            / 100
            * k_temp
            * k_irradicance
            * self.config.a_m2
            / 1e3
        )

    def _check_inputs(self):
        error = self.inputs.step_size is None
        error = error or self.inputs.t_air_deg_celsius is None
        if not self.config.has_external_irradiance_model:
            error = error or self.inputs.bh_w_per_m2 is None
            error = error or self.inputs.dh_w_per_m2 is None
            error = error or self.inputs.now_dt is None

        if error:
            raise KeyError("At least one input is not set")

    def _calculate_module_temperature(self, irradiance_w_per_m2):
        if self.inputs.step_size > self.config.max_step_size:
            steps = self.inputs.step_size // self.config.max_step_size
            step_sizes = [self.config.max_step_size] * steps
            remainder = self.inputs.step_size % self.config.max_step_size
            if remainder > 0:
                step_sizes.append(remainder)

        else:
            step_sizes = [self.inputs.step_size]

        t_module = self.state.t_module_deg_celsius

        for step_size in step_sizes:
            q_dot_irradiance = irradiance_w_per_m2 * (
                1
                - self.config.eta_percent / 100
                - self.config.reflex_percent / 100
            )
            # heat flow induced by temperature gradient between module and air
            q_dot_temp_grad = self.config.alpha_w_per_m2_kelvin * (
                self.inputs.t_air_deg_celsius - t_module
            )
            # heat transfer in current time step [J/m2]
            e_j_per_m2 = (q_dot_irradiance + q_dot_temp_grad) * step_size
            # calculate new temperature of module
            t_module += e_j_per_m2 / (
                self.config.rho_kg_per_m2 * self.config.c_j_per_kg_kelvin
            )
        return t_module - self.state.t_module_deg_celsius

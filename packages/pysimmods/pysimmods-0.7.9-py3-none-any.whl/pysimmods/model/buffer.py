from pysimmods.model.model import Model


class Buffer(Model):
    """A buffer subtype model.

    This class provides pre-implemented all required functions so that
    derived models only need to provide the step-function. However,
    those functions can be overwritten if needed.

    This class also provides unified access to set_percent for all
    buffer models. With passive sign convention, the buffer returns
    negative power for generation and positive power for consumption.
    With active sign convention, it is the other way around.

    *set_percent* hides the sign convention. In contrast to generator
    and load, the battery is idle with a set_percent of 50.

    """

    def get_percent_out(self) -> float:
        # TODO:
        return 0.5 if self.config.use_decimal_percent else 50

    def get_percent_in(self):
        """Return the percentage value that was set as input.

        50 % indicates no operation. Lower values represent discharging
        and higher values represent charging in passive sign convention.

        Depending on the previous definition, there are some spots that
        will be remapped. Values between 50 and 50.01 will be mapped to
        50.005 and values between 49.995 and 50 will be mapped to
        49.995.

        Returns values between 0 and 100 unless the use_decimal_percent
        flag is set in the model config.

        """
        p_kw = self.inputs.p_set_kw
        if p_kw is None:
            return None

        if p_kw * self.config.gsign > 0:
            # Generating energy
            p_max_kw = self.get_pn_discharge_max_kw()
            p_min_kw = self.get_pn_discharge_min_kw()
            sign = self.config.gsign

        elif p_kw * self.config.lsign > 0:
            # Consuming energy
            p_max_kw = self.get_pn_charge_max_kw()
            p_min_kw = self.get_pn_charge_min_kw()
            sign = self.config.lsign

        else:
            return 0.5 if self.config.use_decimal_percent else 50

        decimal = (p_kw - p_min_kw) / (p_max_kw - p_min_kw)
        if decimal < 0:
            # p_kw too low, turn off
            decimal = 0.5
        else:
            decimal = max(0.0001, decimal)
            decimal = 0.5 + (decimal * 0.5 * sign)

        return decimal if self.config.use_decimal_percent else decimal * 100

    def set_percent(self, percentage):
        """Set the percentage power.

        The definitions from get_percent_in are valid here as well.

        """
        if self.config.use_decimal_percent:
            decimal = max(min(abs(percentage), 1.0), 0.0)
        else:
            # Internally, decimal percentage is used.
            decimal = max(min(abs(percentage), 100.0), 0.0) / 100.0

        if decimal == 0.5:
            self.inputs.p_set_kw = 0
        else:
            if decimal < 0.5:
                decimal = min(0.49995, decimal)
            elif decimal > 0.5:
                decimal = max(0.50005, decimal)
            psc = self.config.psc

            if psc and decimal < 0.5 or not psc and decimal > 0.5:
                # Generating energy in psc
                p_max_kw = self.get_pn_discharge_max_kw()
                p_min_kw = self.get_pn_discharge_min_kw()
            else:
                # Consuming energy in psc
                p_max_kw = self.get_pn_charge_max_kw()
                p_min_kw = self.get_pn_charge_min_kw()

            decimal = abs((0.5 - decimal) * 2)
            self.inputs.p_set_kw = p_min_kw + decimal * (p_max_kw - p_min_kw)

    def get_pn_charge_max_kw(self):
        if hasattr(self.config, "p_charge_max_kw"):
            return self.config.p_charge_max_kw * self.config.lsign
        else:
            return self.config.p_max_kw * self.config.lsign

    def get_pn_charge_min_kw(self):
        if hasattr(self.config, "p_charge_min_kw"):
            return self.config.p_charge_min_kw * self.config.lsign
        else:
            return self.config.p_min_kw * self.config.lsign

    def get_pn_discharge_max_kw(self):
        if hasattr(self.config, "p_discharge_max_kw"):
            return self.config.p_discharge_max_kw * self.config.gsign
        else:
            return self.config.p_max_kw * self.config.gsign

    def get_pn_discharge_min_kw(self):
        if hasattr(self.config, "p_discharge_min_kw"):
            return self.config.p_discharge_min_kw * self.config.gsign
        else:
            return self.config.p_min_kw * self.config.gsign

    def get_pn_min_kw(self):
        """Minimum power of battery in kW.

        The minimum power is the maximum discharging power in passive
        sign convention.

        """
        if self.config.psc:
            return self.get_pn_discharge_max_kw()
        else:
            return self.get_pn_charge_max_kw()

    def get_pn_max_kw(self):
        """Maximum power of battery in kW.

        The maximum power is the maximum charging power in passive sign
        convention.

        """
        if self.config.psc:
            return self.get_pn_charge_max_kw()
        else:
            return self.get_pn_discharge_max_kw()

    def set_p_kw(self, p_kw: float) -> None:
        """Set the target active power value.

        With passive sign convention, positive values indicate charging
        and *p_kw* needs to be between pn_charge_min_kw and
        pn_charge_max_kw. Negative values indicate discharging and
        *p_kw* needs to be between pn_discharge_min_kw and
        pn_discharge_max_kw.

        If *p_kw* is lower than the respective min value, it will be set
        to zero. If it is higher than the respective max value, it will
        be set to the max value.

        """
        if self.config.psc and p_kw < 0 or self.config.asc and p_kw > 0:
            # Discharging
            if p_kw < 0:
                p_max = self.get_pn_discharge_min_kw()
                p_min = self.get_pn_discharge_max_kw()
            else:
                p_min = self.get_pn_discharge_min_kw()
                p_max = self.get_pn_discharge_max_kw()
        elif self.config.psc and p_kw > 0 or self.config.asc and p_kw < 0:
            # Charging
            if p_kw < 0:
                p_max = self.get_pn_charge_min_kw()
                p_min = self.get_pn_charge_max_kw()
            else:
                p_min = self.get_pn_charge_min_kw()
                p_max = self.get_pn_charge_max_kw()
        else:
            self.inputs.p_set_kw = 0
            return

        if abs(p_kw) < abs(p_min) and abs(p_kw) < abs(p_max):
            self.inputs.p_set_kw = 0
        else:
            self.inputs.p_set_kw = max(p_min, min(p_max, p_kw))

    def set_q_kvar(self, q_kvar) -> None:
        self.inputs.q_set_kvar = q_kvar

    def get_p_kw(self) -> float:
        return self.state.p_kw * self.config.lsign

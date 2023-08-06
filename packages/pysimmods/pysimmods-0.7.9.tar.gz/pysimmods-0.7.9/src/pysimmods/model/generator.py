from .model import Model


class Generator(Model):
    """A generator subtype model.

    This class provides unified access to set_percent for all
    generators. A generator returns negative power values in the
    consumer reference arrow system (passive sign convention), which
    is hided if one uses *set_percent*, i.e. calling set_percent
    with, e.g., a value of 50 will always set the power of the
    generator to 50 percent, independently of the reference system
    used.

    """

    def set_p_kw(self, p_kw: float) -> None:
        p_min = self.get_pn_min_kw()
        p_max = self.get_pn_max_kw()

        if p_kw * self.config.gsign > 0:
            # Generating power
            p_kw = abs(p_kw)
            if p_kw < p_min:
                # Better turn off than to generate too much power
                self.inputs.p_set_kw = 0
            else:
                self.inputs.p_set_kw = min(p_max, p_kw)
        else:
            # Can't consume power
            self.inputs.p_set_kw = 0

    def get_p_kw(self) -> float:
        return self.state.p_kw * self.config.gsign

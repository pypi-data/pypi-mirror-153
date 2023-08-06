"""This module contains a function :func:`tilted_surface` to calculate
irradiance on tilted surfaces.

"""
from math import cos, radians, sin, tan
import logging

LOG = logging.getLogger(__name__)


def tilted_surface(
    direct_radiation,
    diffuse_radiation,
    surface_tilt,
    surface_azimuth,
    sun_elevation,
    sun_azimuth,
    albedo=0.2,
    model="klucher",
):
    """Compute radiation on tilted surface.

    Parameters
    ----------
    direct_radiation : float
        Direct solar radiation on horizontal surface in Watt/m2.
    diffuse_radiation : float
        Diffuse solar radiation on horizontal surface in Watt/m2.
    surface_tilt : float
        Tilt of the surface in degree (between 0° and 90°).
    surface_azimuth : float
        Orientation of the surface in degree (North 0°, East 90°,
        West 270°).
    sun_elevation : float
        Elevation of the sun in degree.
    sun_azimuth : float
        Solar azimuth angle in degree (Noth 0°, East 90°, West 270°).
    albedo: float
        Ratio of reflected radiation from surrounding surface to
        incident radiation on it.
    model : str
        Model which is used to compute solar radiation on tilted
        surface. Default is an advanced Klucher model [#]_.

    Returns
    -------
    float
        Total solar radiation on tilted surface in Watt/m2.

    Raises
    ------
    ValueError
        If either *direct_radiation* or *diffuse_radiation* is < 0.

    .. [#] Behrens, Tanja. Bestimmung der spektralen Solarstrahlung am Erdboden
           aus Satellitendaten zur Bewertung des Leistugnsverhaltens von
           Dünnschicht-Solarzellen. Von der Fakultät für Mathematik
           und Naturwissenschaften der Universität Oldenburg angenommene
           Disseratation zur Erlangung des Grades und Titels einer Doktorin der
           Naturwissenschaften, 2011, S. 36 f.

    """
    if direct_radiation < 0:
        LOG.warning("Direct radiation must be greater than zero")
        direct_radiation = 0
    if diffuse_radiation < 0:
        LOG.warning("Diffuse radiation must be greater than zero")
        diffuse_radiation = 0
    global_radiation = direct_radiation + diffuse_radiation
    if global_radiation <= 0:
        return 0

    # calculate ratio of titled and horizontal beam irradiance
    sun_zenith = min(90, 90 - sun_elevation)

    cos_incident = max(
        0,
        cos(radians(surface_tilt)) * cos(radians(sun_zenith))
        + sin(radians(surface_tilt))
        * sin(radians(sun_zenith))
        * cos(radians(sun_azimuth - surface_azimuth)),
    )
    # dot product of surface normal and solar angle

    ratio = min(10, cos_incident / cos(radians(sun_zenith)))
    # avoid unfavorable angles of incident which especially appear in winter

    # calculate total radiation on tilted surface using Klucher's 1979 model

    if model == "klucher":
        F = 1 - (diffuse_radiation / global_radiation) ** 2
        # anisotropy parameter

        a = ratio + (1 - cos(radians(surface_tilt))) * albedo / 2

        b = -ratio + (
            (1 + F * sin(radians(surface_tilt / 2)) ** 3)
            * (1 + F * cos_incident**2 * sin(radians(sun_zenith)) ** 3)
            * (1 + cos(radians(surface_tilt)))
            / 2
        )

        radiation_tilt = a * global_radiation + b * diffuse_radiation

    return radiation_tilt

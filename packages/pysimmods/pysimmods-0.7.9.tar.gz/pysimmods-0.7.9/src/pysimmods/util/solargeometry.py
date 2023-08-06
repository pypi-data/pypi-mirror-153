"""This module contains a function :func:`compute_sun_position` to 
calculate the sun position for a given time and location.

"""
from math import asin, atan, cos, degrees, radians, sin, tan


def compute_sun_position(time, lat, lon):
    """Compute the sun position.

    Computes the sun position for a given time and geographical location.
    Detailed calculation is explained in Wikipedia article Sonnenstand_.
    For calculation of right ascension alpha and declination delta the article
    refers to [#]_. For calculation of eclipitc longitude lambda the aricle
    refers to [#]_.

    Parameters
    ----------
    time : int
        Time as unix timestamp.
    lat : float
        Geographical latitude in degree (+North, -South).
    lon : float
        Geographical longitude in degree (+East, -West).

    Returns
    -------
    dict
        *dict* with keys *'azimuth'* and *'elevation'*.

        - *'azimuth'* - Solar azimuth angle in degree (Noth 0°, East 90°,
          West 270°)
        - *'elevation'* - Elevation of the sun in degree

    .. _Sonnenstand: https://de.wikipedia.org/wiki/Sonnenstand

    .. [#] The Astronomical Almanac For The Year 2006, The Stationary Office,
           London 2004

    .. [#] Astronomical Algorithms, Billmann-Bell, Richmond 2000 (2nd ed.,
           2nd printing)

    """

    JD_1970 = 2440587.5  # julian day of epoch 1970-01-01 00:00
    JD_time = time / 86400.0 + JD_1970
    # print(JD_time)
    JD_2000 = 2451545.0  # Greenich noon 2000-01-01 12:00
    n = JD_time - JD_2000  # days since Greenich noon 2000-01-01

    # Calculate the mean longitude of the Sun, corrected for the aberration of
    # light
    L = (280.460 + 0.9856474 * n) % 360  # degree

    # Calculate the mean anomaly of the sun
    g = (357.528 + 0.9856003 * n) % 360  # degree

    # Calculate the ecliptic longitude of the sun
    Lambda = L + 1.915 * sin(radians(g)) + 0.01997 * sin(radians(2 * g))

    # Calculate obliquity of the ecliptic
    epsilon = 23.439 - 4e-7 * n

    # Calculate right ascension
    denominator = cos(radians(Lambda))
    alpha = degrees(
        atan(cos(radians(epsilon)) * sin(radians(Lambda)) / denominator)
    )

    # Bring angle to apropriate quadrant
    # print(denominator)
    if denominator < 0:
        alpha = alpha + 180

    # Calculate declination
    delta = degrees(asin(sin(radians(epsilon)) * sin(radians(Lambda))))
    # print(alpha, delta)

    # Calculate Greenwich hour angle in several steps

    # First calculate julian day of time 00:00 UTC
    JD_0 = time // 86400 + JD_1970

    # Calculate julian centuries since UTC 2000-01-01 00:00
    T_0 = (JD_0 - JD_2000) / 36525
    # print("T_0: %s" % T_0)

    # Calculate hour of day, for example 17:45 -> 17.75
    T = (time % 86400) / 3600

    # Calculate Greenwich mean sidereal time
    teta_G_h = (6.697376 + 2400.05134 * T_0 + 1.002738 * T) % 24
    # First term describes Greenwich sidereal time at 2000-01-01 00:00.
    # Second term describes the daily advancement of sidereal time for about 4
    # minutes per day.
    # The third term adds the fraction of the day meassured in sidereal time

    # Convert from hours to degree (1h = 15°)
    teta_G = teta_G_h * 15

    # Consider geographical longitude (count eastern direction positive)
    teta = teta_G + lon
    # print("teta_G: %s" % teta_G)

    # Calculate hour angle for this place by subtracting right ascension
    tau = teta - alpha

    # Calculate azimuth
    denominator = cos(radians(tau)) * sin(radians(lat)) - tan(
        radians(delta)
    ) * cos(radians(lat))
    azimuth = degrees(atan(sin(radians(tau)) / denominator))

    # Bring azimuth to appropriate quadrant
    if denominator < 0:
        azimuth = azimuth + 180

    # Count azimuth from north
    azimuth = (azimuth + 180) % 360

    # Calculate elevation angle of sun
    h = degrees(
        asin(
            cos(radians(delta)) * cos(radians(tau)) * cos(radians(lat))
            + sin(radians(delta)) * sin(radians(lat))
        )
    )
    # print("Azimuth: %s, h: %s" % (azimuth, h))

    # Coorect elevation because of atmospheric refraction
    R = 1.02 / tan(radians(h + 10.3 / (h + 5.11)))
    h_R = h + R / 60
    # Keep in mind that refraction depends on detailed state of atmosphere.
    # The given formula assumes air pressure 1010 mbar and temperatur 10°C

    return {"azimuth": azimuth, "elevation": h_R}

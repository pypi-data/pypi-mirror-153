"""Mueller matrices of base optical components."""
import numpy as np


def elliptical_retarder_matrix(t_ret, d_h, d_45, d_r) -> np.ndarray:
    """Compute the Mueller matrix of an elliptical retarder."""
    # See either "Mueller matrix of DKIST calibration unit retarders" or
    #  "DKIST Polarization Calibration: Modeling of Calibration Unit elements"
    # both April 2018 by C. Beck.

    d = np.sqrt(d_h**2 + d_45**2 + d_r**2)
    cosd = np.cos(d)
    sind = np.sin(d)

    m22 = (d_h**2 + cosd * (d_45**2 + d_r**2)) / d**2
    m23 = ((1 - cosd) * d_45 * d_h) / d**2 + sind * d_r / d
    m24 = ((1 - cosd) * d_h * d_r) / d**2 - sind * d_45 / d
    m32 = ((1 - cosd) * d_45 * d_h) / d**2 - sind * d_r / d
    m33 = (d_45**2 + cosd * (d_h**2 + d_r**2)) / d**2
    m34 = ((1 - cosd) * d_45 * d_r) / d**2 + sind * d_h / d
    m42 = ((1 - cosd) * d_h * d_r) / d**2 + sind * d_45 / d
    m43 = ((1 - cosd) * d_45 * d_r) / d**2 - sind * d_h / d
    m44 = (d_r**2 + cosd * (d_45**2 + d_h**2)) / d**2

    # fmt: off
    return t_ret * np.array(
        [
            [1,   0,   0,   0],
            [0, m22, m23, m24],
            [0, m32, m33, m34],
            [0, m42, m43, m44]
        ],
        dtype=np.float64
    )
    # fmt: on


def polarizer_matrix(t_pol, py, px=1) -> np.ndarray:
    """Compute the Mueller matrix of a linear polarizer."""
    # See "DKIST Polarization Calibration: Modeling of Calibration Unit elements" by C. Beck, April 2018
    p_factor = px**2 + py**2
    p_ratio = (px**2 - py**2) / p_factor
    UV_factor = 2 * px * py / p_factor

    # fmt: off
    return (0.5 * t_pol * p_factor
            * np.array(
            [
                [1,       p_ratio,   0,         0],
                [p_ratio, 1,         0,         0],
                [0,       0, UV_factor,         0],
                [0,       0,         0, UV_factor]
            ],
            dtype=np.float64,
        )
    )
    # fmt: on


def rotation_matrix(theta) -> np.ndarray:
    """Compute a *polarimetric* rotation matrix."""
    # fmt: off
    return np.array(
        [
            [1,                  0,                 0, 0],
            [0,  np.cos(2 * theta), np.sin(2 * theta), 0],
            [0, -np.sin(2 * theta), np.cos(2 * theta), 0],
            [0,                  0,                 0, 1],
        ],
        dtype=np.float64,
    )
    # fmt: on


def mirror_matrix(x, tau) -> np.ndarray:
    """Compute the Mueller matrix of a single, flat mirror."""
    # See "Mueller matrix of a mirror or mirror group", C. Beck March 2018

    # fmt: off
    mirror = np.array(
        [
            [1 + x**2, 1 - x**2,                    0,                   0],
            [1 - x**2, 1 + x**2,                    0,                   0],
            [0,               0,  2 * x * np.cos(tau), 2 * x * np.sin(tau)],
            [0,               0, -2 * x * np.sin(tau), 2 * x * np.cos(tau)],
        ],
        dtype=np.float64,
    )
    # fmt: on
    return mirror / (1 + x**2)

import numpy as np
import numba

from typing import Tuple

EPSILON = np.finfo(float).eps



@numba.njit(cache=True)
def spherical_to_cartesian(r, theta, phi) -> Tuple[float, float, float]:
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    return x, y, z


@numba.njit(cache=True)
def cartesian_to_spherical(x, y, z) -> Tuple[float, float, float]:
    r = (x**2 + y**2 + z**2)**0.5
    theta = np.arctan(y / (x + EPSILON))
    if x < 0:
        theta += np.pi
    phi = np.arccos(z / (r + EPSILON))
    return r, theta, phi
    
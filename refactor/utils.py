import math

from refactor.constants import EPS


def deg_to_rad(theta):
    return (theta / 360) * 2 * math.pi


def clamp(x, x_min, x_max):
    if x < x_min:
        x = x_min
    elif x > x_max:
        x = x_max

    return x


def approx_equal(a, b):
    return abs(a - b) < EPS
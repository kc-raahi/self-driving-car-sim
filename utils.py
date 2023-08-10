import math
import random

from constants import EPS


def deg_to_rad(theta):
    return (theta / 360) * 2 * math.pi


def clamp(x, x_min, x_max):
    # tops or bottoms out a given value if necessary
    if x < x_min:
        x = x_min
    elif x > x_max:
        x = x_max

    return x


def approx_equal(a, b):
    return abs(a - b) < EPS


def mutate_value(val, max_perturb, min_val=-1, max_val=1):
    """
    Returns a value in the range of val +- any fraction of the max perturbation value.
    """
    sign = random.choice([-1, 1])
    min_allowed = val - (val - min_val) * max_perturb
    max_allowed = val + (max_val - val) * max_perturb
    if sign == -1:
        return random.uniform(min_allowed, val)
    else:
        return random.uniform(val, max_allowed)

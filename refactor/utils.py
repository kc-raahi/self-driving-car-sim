from refactor.constants import CAR_POS_ONSCREEN


def lerp(a, b, t):
    """
    Linear interpolation - computes the value that is a fraction t away from a
    :param a: start of the interval
    :param b: end of the interval
    :param t: between 0 and 1
    :return:
    """
    return a + (b - a) * t


def to_screen_y(y, viewport_top_y):
    return viewport_top_y - y


def clamp(v, min_v, max_v):
    if v > max_v:
        return max_v
    if v < min_v:
        return min_v

    return v

def top_of_screen_from_car_y(car_y):
    return car_y + CAR_POS_ONSCREEN



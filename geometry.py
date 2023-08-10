import math

from constants import EPS
from utils import deg_to_rad, approx_equal


class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def is_identical(self, other):
        return approx_equal(self.x, other.x) and approx_equal(self.y, other.y)

    def as_tuple(self):
        return self.x, self.y


def transpose(p, dx, dy):
    return Pt(p.x + dx, p.y + dy)


def transpose_line(line, dx, dy):
    p1, p2 = line
    tp1 = transpose(p1, dx, dy)
    tp2 = transpose(p2, dx, dy)
    return tp1, tp2


def rotate_about_origin(pt, angle_deg):
    theta = math.atan(pt.y / pt.x) if pt.x > EPS or pt.x < -EPS else math.pi / 2 if pt.y > 0 else -math.pi / 2
    if pt.x < 0:
        theta += math.pi
    alpha = deg_to_rad(angle_deg)
    d = dist(Pt(0, 0), pt)
    x = d * math.cos(theta + alpha)
    y = d * math.sin(theta + alpha)
    return Pt(x, y)


def rotate_line_about_origin(line, angle_deg):
    p1 = rotate_about_origin(line[0], angle_deg)
    p2 = rotate_about_origin(line[1], angle_deg)

    return p1, p2


def dist(pt1, pt2):
    return math.sqrt((pt2.x - pt1.x) ** 2 + (pt2.y - pt1.y) ** 2)


def x_y_flip_point(p):
    return Pt(p.y, p.x)


def x_y_flip_line(line):
    p1, p2 = line
    return x_y_flip_point(p1), x_y_flip_point(p2)


def slope_intercept(line):
    left_pt, right_pt = line
    if left_pt.x > right_pt.x:
        tmp_pt = left_pt
        left_pt = right_pt
        right_pt = tmp_pt

    rise = right_pt.y - left_pt.y
    run = right_pt.x - left_pt.x
    m = rise / run if not approx_equal(run, 0) else math.inf
    c = left_pt.y - m * left_pt.x if not math.isinf(m) else None

    return m, c


def horizontal_line_intersection(line, h_line):
    p1, p2 = h_line
    min_x = min(p1.x, p2.x)
    max_x = max(p1.x, p2.x)
    h_y = p1.y
    q1, q2 = line
    min_y = min(q1.y, q2.y)
    max_y = max(q1.y, q2.y)
    m, c = slope_intercept(line)
    if m == 0:
        return None
    x = (h_y - c) / m if not math.isinf(m) else q1.x

    if min_x <= x <= max_x and min_y <= h_y <= max_y:
        return Pt(x, h_y)
    else:
        return None


def vertical_line_intersection(line, v_line):
    p = horizontal_line_intersection(x_y_flip_line(line), x_y_flip_line(v_line))
    return x_y_flip_point(p) if p is not None else None


def line_segment_intersection(line, h_or_v_line):
    # Check if h_or_v_line is horizontal or vertical. Use helper methods to proceed.
    p1, p2 = h_or_v_line
    if approx_equal(p1.y, p2.y):
        # is horizontal
        return horizontal_line_intersection(line, h_or_v_line)
    elif approx_equal(p1.x, p2.x):
        # is vertical
        return vertical_line_intersection(line, h_or_v_line)
    else:
        raise Exception("h_or_v_line is neither horizontal nor vertical", h_or_v_line)




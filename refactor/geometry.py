import math

from refactor.constants import EPS
from refactor.utils import deg_to_rad, approx_equal


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



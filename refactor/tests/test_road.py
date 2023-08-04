import pytest

from refactor.constants import MARKER_LENGTH, NUM_LANES
from refactor.geometry import Pt
from refactor.road import Road


def test_get_lines():
    road = Road()
    line = road.get_lines()[0]
    print(line)
    road.left_x = MARKER_LENGTH * 3
    print(road.left_x)
    line = road.get_lines()[0]
    p1, p2 = line
    print(line)
    assert p1.is_identical(Pt(40, 67.5))

def test_get_lane_center():
    road = Road()
    mid_index = int(NUM_LANES / 2)
    print(mid_index)
    y = road.get_lane_center(mid_index)
    print(y)



import pytest

from refactor.utils import lerp, to_screen_y, clamp


@pytest.mark.parametrize("a, b, t, o", [(0, 1, 0.5, 0.5), (0, 2, 1, 2), (1, 2, 0.5, 1.5)])
def test_lerp(a, b, t, o):
    assert lerp(a, b, t) == o


@pytest.mark.parametrize("y, vty, o", [(-450, 0, 450), (0, 10, 10)])
def test_to_screen_y(y, vty, o):
    assert to_screen_y(y, vty) == o


@pytest.mark.parametrize("v, min_v, max_v, o", [(0.5, 0, 1, 0.5), (2, 0, 1, 1), (-1, 0, 1, 0)])
def test_clamp(v, min_v, max_v, o):
    c = clamp(v, min_v, max_v)
    assert c >= min_v
    assert c <= max_v

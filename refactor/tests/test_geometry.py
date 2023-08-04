import pytest

from refactor.geometry import transpose, Pt, transpose_line, rotate_about_origin


def test_transpose():
    pt = Pt(0, 0)
    pt2 = transpose(pt, 5, 10)
    print(pt2)

def test_transpose_line():
    pt1 = Pt(0, 0)
    pt2 = Pt(5, 10)
    l = (pt1, pt2)
    l2 = transpose_line(l, 5, 10)
    print(l2)


@pytest.mark.parametrize("p_c, e_c",[
    ((0, 1),(-1, 0)),
    ((-1, 0), (0, -1)),
    ((0, -1), (1, 0)),
    ((1, 0), (0, 1))
])
def test_rotate(p_c, e_c):
    p = Pt(*p_c)
    e = Pt(*e_c)
    p2 = rotate_about_origin(p, 90)
    print(p2)
    assert p2.is_identical(e)
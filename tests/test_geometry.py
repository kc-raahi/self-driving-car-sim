import pytest

from geometry import transpose, Pt, transpose_line, rotate_about_origin, line_segment_intersection


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


H_LINE = (Pt(-1, 0), Pt(1, 0))
V_LINE = (Pt(0, -1), Pt(0, 1))

ORIGIN = Pt(0, 0)
@pytest.mark.parametrize("l1, l2, e", [
    (V_LINE, H_LINE, ORIGIN),
    (H_LINE, V_LINE, ORIGIN),
    ((Pt(-1, -1), Pt(1, 1)), H_LINE, ORIGIN),
    ((Pt(1, 1), Pt(-1, -1)), H_LINE, ORIGIN),
    ((Pt(-1, 1), Pt(1, -1)), H_LINE, ORIGIN),
    ((Pt(1, 3), Pt(3, 1)), H_LINE, None)
]
                         )
def test_line_intersection(l1, l2, e):
    r = line_segment_intersection(l1, l2)
    assert r is None or r.is_identical(e)


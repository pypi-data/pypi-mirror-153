from pytest import mark
import pytest
from pyece import Corners


@mark.parametrize(
    "shape",
    [(1, 2), (1, 2, 3), (1, 2, 3, 4)],
)
def test_corners_product(shape):
    cs = Corners.product(shape).value
    assert cs.shape[0] == 2 ** len(shape)
    assert cs.mean() == sum(shape) / len(shape) / 2
    assert (cs[0] == [0]*len(shape)).all()
    assert (cs[-1] == shape).all()
    assert set(cs.flatten()) == {0, *shape}


def test_corners():
    assert Corners([[]]).value.shape == (1, 0)
    with pytest.raises(ValueError):
        Corners([[1]]).value
    with pytest.raises(ValueError):
        Corners([[0, 0]]*3).value
    assert Corners([[0, 0]]*4).value.shape == (4,2)
    with pytest.raises(ValueError):
        Corners([[0, 0]]*8).value
    assert Corners([[0]*3]*8).value.shape == (8, 3)
    assert Corners([[0]*4]*16).value.shape == (16, 4)

import numpy as np
from pyece.core.math.rotate import rotate


def test_rotate_2d():
    assert np.allclose(
        rotate((1, 1), (1, 11), (np.pi / 2,)),
        np.array((-9,  1)),
        atol=1e-06
    )
    assert np.allclose(
        rotate((1, 1), (1, 11), (-np.pi / 2,)),
        np.array((11,  1)),
        atol=1e-06
    )
    assert np.allclose(
        rotate((1, 1), (1, 11), (np.pi,)),
        np.array((1,  -9)),
        atol=1e-06
    )
    assert np.allclose(
        rotate((1, 1), (1, 11), (np.pi / 6,)),
        np.array((1 - 10 / 2,  1 + 10 * np.sqrt(3) / 2)),
        atol=1e-06
    )


def test_rotate_3d():
    assert np.allclose(
        rotate((1, 1, 2), (1, 11, 2), (0, 0, np.pi / 2)),
        np.array((-9, 1, 2)),
        atol=1e-06
    )
    assert np.allclose(
        rotate((1, 2, 1), (11, 2, 1), (0, np.pi / 2, 0)),
        np.array((1, 2, -9)),
        atol=1e-06
    )
    assert np.allclose(
        rotate((2, 1, 1), (2, 1, 11), (np.pi / 2, 0, 0)),
        np.array((2, -9, 1)),
        atol=1e-06
    )

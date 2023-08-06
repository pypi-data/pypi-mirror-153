__all__ = ("rotate",)

from typing import Tuple, Union

import numpy as np


def rotate(
    pivot: np.ndarray,
    turning: np.ndarray,
    angle: Union[Tuple[float], Tuple[float, float, float]],
) -> np.ndarray:
    pivot = np.asarray(pivot)
    turning = np.asarray(turning)
    assert pivot.shape == turning.shape
    matrix = get_rotate_matrix(angle)
    return matrix @ (turning - pivot) + pivot


def get_rotate_matrix(
    angle: Union[Tuple[float], Tuple[float, float, float]]
) -> np.ndarray:
    if len(angle) == 1:
        return rotate_matrix_2d(angle[0])
    elif len(angle) == 3:
        return rotate_matrix_3d(angle)
    else:
        raise ValueError(f"ndim should be 2 or 3")


def rotate_matrix_2d(angle: float) -> np.ndarray:
    return np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])


def rotate_matrix_3d(angle: Tuple[float, float, float]) -> np.ndarray:
    rotate_matrix_x = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle[0]), -np.sin(angle[0])],
            [0, np.sin(angle[0]), np.cos(angle[0])],
        ]
    )
    rotate_matrix_y = np.array(
        [
            [np.cos(angle[1]), 0, np.sin(angle[1])],
            [0, 1, 0],
            [-np.sin(angle[1]), 0, np.cos(angle[1])],
        ]
    )
    rotate_matrix_z = np.array(
        [
            [np.cos(angle[2]), -np.sin(angle[2]), 0],
            [np.sin(angle[2]), np.cos(angle[2]), 0],
            [0, 0, 1],
        ]
    )
    return rotate_matrix_x @ rotate_matrix_y @ rotate_matrix_z

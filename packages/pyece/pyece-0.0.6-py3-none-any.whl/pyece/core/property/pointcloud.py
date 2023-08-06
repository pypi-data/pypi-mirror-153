__all__ = (
    "PointCloud",
    "Corners",
)

from itertools import product
from typing import Sequence, Tuple, Union

import numpy as np

from .base import Operation, Property
from .point import (
    LikePoint,
    Point,
    PointInflation,
    PointOperation,
    PointRotate,
    as_point,
)


class PointCloud(Point):
    def __init__(self, points: Sequence[LikePoint]):
        super().__init__([as_point(p) for p in points])

    def transform(self, operation: Operation, **kwargs) -> Property:
        if isinstance(operation, PointOperation):
            points = self.value
            if isinstance(operation, (PointRotate, PointInflation)):
                if operation._pivot is None:
                    kwargs["pivot"] = points.mean(0)
            fn = operation(**kwargs)
            return PointCloud(tuple(map(fn, points)))
        return super().transform(operation, **kwargs)


LikePointCloud = Union[PointCloud, Sequence[LikePoint]]


def as_pointcloud(value: LikePointCloud) -> PointCloud:
    if isinstance(value, PointCloud):
        return value
    return PointCloud(value)


class Corners(PointCloud):
    def get(self) -> np.ndarray:
        corners = super().get()
        n, p = corners.shape
        if 2 ** p != n:
            msg = ""
            raise ValueError(msg)
        return corners

    @staticmethod
    def product(shape: Tuple) -> "Corners":
        masks = list(product((False, True), repeat=len(shape)))
        corners = [[s if c else 0 for c, s in zip(mask, shape)] for mask in masks]
        return Corners(corners)

__all__ = (
    "Point",
    "PointOperation",
    "PointShift",
    "PointRotate",
    "PointInflation",
)

from abc import abstractmethod
from typing import Callable, Union

import numpy as np

from ..math.rotate import rotate
from .base import LikeProperty, Operation, Property, PropertySequence, as_property


class Point(Property):
    def __init__(self, point: PropertySequence):
        self._point = [as_property(p) for p in point]

    def get(self) -> np.ndarray:
        return np.asarray([p.value for p in self._point])


LikePoint = Union[Point, PropertySequence, np.ndarray]


def as_point(value: LikePoint) -> Point:
    if isinstance(value, Point):
        return value
    return Point(value)


class PointOperation(Operation):
    def __call__(self, **params) -> Callable[[LikePoint], Point]:
        def inner(point: LikePoint):
            point = as_point(point).value
            value = self.operation(point, **params)
            return Point(value)

        return inner

    @abstractmethod
    def operation(self, obj: np.ndarray, **params) -> np.ndarray:
        return NotImplemented


class PointShift(PointOperation):
    def __init__(self, shift: LikePoint):
        self._shift = as_point(shift)

    def __call__(self) -> Callable[[LikePoint], Point]:
        shift = self._shift.value
        return super().__call__(shift=shift)

    def operation(self, obj: np.ndarray, shift: np.ndarray) -> np.ndarray:
        return obj + shift


class PointRotate(PointOperation):
    def __init__(self, angle: LikeProperty, pivot: LikePoint = None):
        self._angle = as_property(angle)
        self._pivot = None if pivot is None else as_point(pivot)

    def __call__(self, pivot: LikePoint = None) -> Callable[[LikePoint], Point]:
        angle = np.asarray(self._angle.value).reshape(-1) % (2 * np.pi)
        if pivot is not None:
            pivot = as_point(pivot).value
        elif self._pivot is not None:
            pivot = self._pivot.value
        else:
            raise RuntimeError
        return super().__call__(pivot=pivot, angle=angle)

    def operation(
        self, obj: np.ndarray, pivot: np.ndarray, angle: np.ndarray
    ) -> np.ndarray:
        return rotate(pivot, obj, angle)


class PointInflation(PointOperation):
    def __init__(self, factor: LikeProperty, pivot: LikePoint = None):
        self._factor = as_property(factor)
        self._pivot = None if pivot is None else as_point(pivot)

    def __call__(self, pivot: LikePoint = None) -> Callable[[LikePoint], Point]:
        factor = self._factor.value
        if pivot is not None:
            pivot = as_point(pivot).value
        elif self._pivot is not None:
            pivot = self._pivot.value
        else:
            raise RuntimeError
        return super().__call__(pivot=pivot, factor=factor)

    def operation(
        self, obj: np.ndarray, pivot: np.ndarray, factor: np.ndarray
    ) -> np.ndarray:
        return pivot + (obj - pivot) * factor

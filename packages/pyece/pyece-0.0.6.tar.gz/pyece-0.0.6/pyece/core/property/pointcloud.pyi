import numpy as np
from .base import Operation, Property
from .point import LikePoint, Point
from typing import Sequence, Tuple, Union

class PointCloud(Point):
    def __init__(self, points: Sequence[LikePoint]) -> None: ...
    def transform(self, operation: Operation, **kwargs) -> Property: ...
LikePointCloud = Union[PointCloud, Sequence[LikePoint]]

class Corners(PointCloud):
    def get(self) -> np.ndarray: ...
    @staticmethod
    def product(shape: Tuple) -> Corners: ...

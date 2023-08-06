__all__ = [
    'Point',
    'Size',
    'Box',
    'area_union',
    'area_intersection',
]

from collections.abc import Iterable
from typing import Dict, List, Tuple, Union

import numpy as np

Number = (int, float, complex)
AnyPoint = Union[Tuple[Union[int, float, complex], ...], 'Point']
AnySize = Union[Tuple[Union[int, float, complex], ...], 'Size']

def _as_numpy(fn):
    def wrapper(self, other):
        return Point(fn(self.numpy(), Point(other).numpy()))
    return wrapper


class Point:
    def __init__(self, *coords: AnyPoint):
        if len(coords) == 1:
            coords = coords[0]
            if np.isscalar(coords):
                coords = [coords]
            elif isinstance(coords, Point):
                coords = coords
            elif isinstance(coords, Iterable):
                coords = Point(*coords)
            else:
                raise NotImplementedError
        self.coords = coords

    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, coords):
        if isinstance(coords, Point):
            self._coords = coords.coords
        self._coords = [
            p if np.isscalar(p) else Point(p)
            for p in coords
        ]

    def numpy(self) -> np.ndarray:
        return np.asarray(self.coords, dtype=float)

    def __len__(self):
        return len(self._coords)

    def __getitem__(self, i) -> 'Point':
        return self._coords[i]

    def __setitem__(self, i, v) -> None:
        if all([np.isscalar(v) for v in self]):
            self._coords[i]=v
            return
        raise NotImplementedError

    def __iter__(self):
        for s in self.coords:
            yield s

    def __repr__(self) -> str:
        return 'Point[{}]'.format(', '.join([*map(repr, self.coords)]))

    def __eq__(self, other: 'Point') -> bool:
        return hash(self) == hash(Point(other))

    def __hash__(self):
        return hash(self.numpy().data.tobytes())

    @_as_numpy
    def __add__(self, other):
        return self + other

    @_as_numpy
    def __sub__(self, other):
        return self - other

    @_as_numpy
    def __mul__(self, other):
        return self * other

    @_as_numpy
    def __truediv__(self, other):
        return self / other

    @_as_numpy
    def __radd__(self, other):
        return self + other

    @_as_numpy
    def __rsub__(self, other):
        return self - other

    @_as_numpy
    def __rmul__(self, other):
        return self * other

    @_as_numpy
    def __rtruediv__(self, other):
        return self / other

class Size:
    def __init__(self, *sides: AnySize):
        if len(sides) == 1:
            sides = sides[0]
            if np.isscalar(sides):
                sides = [sides]
            elif isinstance(sides, Size):
                sides = sides
            elif isinstance(sides, Iterable):
                sides = Size(*sides)
            else:
                raise NotImplementedError
        self.sides = sides

    @property
    def sides(self):
        return self._sides

    @sides.setter
    def sides(self, other):
        if all([np.isscalar(s) for s in other]):
            self._sides = [s for s in other]
        else:
            raise NotImplementedError

    def numpy(self) -> np.ndarray:
        return np.asarray(self.sides, dtype=float)

    def __len__(self):
        return len(self._sides)

    def __getitem__(self, i) -> 'Size':
        return self._sides[i]

    def __setitem__(self, i, v) -> None:
        if all([np.isscalar(v) for v in self]):
            self._sides[i] = v
            return
        raise NotImplementedError

    def __iter__(self):
        for s in self.sides:
            yield s

    def __eq__(self, other):
        return hash(self) == hash(Size(other))

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Size[{}]'.format(', '.join([*map(repr, self.sides)]))

    def __hash__(self):
        return hash(self.numpy().data.tobytes())


class Box:
    def __init__(self, anchor: Point, sides: Size, canvas: Size):
        self._dim = None
        self.canvas = canvas
        self.anchor = anchor
        self.sides = sides

    def __len__(self):
        return self._dim

    @property
    def anchor(self) -> Point:
        return Point(self._a) * self.canvas

    @anchor.setter
    def anchor(self, other):
        anchor = Point(other) / self.canvas
        assert len(anchor) == len(self)
        self._a = anchor

    @property
    def sides(self) -> Size:
        return Size(Point(self._s) * self.canvas)

    @sides.setter
    def sides(self, other) -> None:
        sides = Point(other)
        assert len(sides) == len(self)
        for dim, s in enumerate(sides):
            if s < 0:
                a = self.anchor
                a[dim] += s
                sides[dim] = -1 * s
                self.anchor = a
        sides = Size(sides / self.canvas)
        self._s = sides

    @property
    def distant(self) -> Point:
        return self.anchor + self.sides

    @property
    def centre(self) -> Point:
        return (self.anchor + self.distant) / 2

    @property
    def canvas(self) -> Size:
        return self._c

    @canvas.setter
    def canvas(self, other) -> None:
        canvas = Size(other)
        if self._dim is None:
            self._dim = len(canvas)
        else:
            assert len(canvas) == len(self)
        self._c = canvas

    def __repr__(self):
        return 'Box[{}+>{}]'.format(repr(self.anchor.coords), repr(self.sides.sides))

    def __hash__(self):
        return hash(
            self._a.numpy().data.tobytes() +
            self._s.numpy().data.tobytes()
        )

    def __contains__(self, point: Point):
        point = Point(point)
        p1 = self.anchor
        p2 = p1 + self.sides
        return all([p1[dim] < point[dim] < p2[dim] for dim in range(len(self))])

    def __eq__(self, other: 'Box') -> bool:
        if isinstance(other, Box):
            return hash(self) == hash(other)
        raise NotImplementedError

    def __ne__(self, other: 'Box') -> bool:
        return not self == other

    @property
    def area(self) -> float:
        return np.prod(Point(self.sides))

    def split(self, *points: Point) -> List['Box']:
        ps = [Point(p) for p in points]
        assert all([len(p) == len(self) for p in ps])
        p1 = self.anchor
        p2 = p1 + self.sides
        ax = [
            [p[dim] for p in ps if p1[dim] < p[dim] < p2[dim]] + [p1[dim]] + [p2[dim]]
            for dim in range(len(self))
        ]
        for dim, a in enumerate(ax):
            a.sort()
            ax[dim] = [p for p in zip(a[:-1], a[1:])]
        idxs = np.meshgrid(*[range(len(a)) for a in ax], indexing='ij')
        idxs = np.asarray([idx.flatten() for idx in idxs]).transpose()
        result = list()
        canvas = self.canvas
        for idx in idxs:
            p1 = Point([ax[dim][i][0] for dim, i in enumerate(idx)])
            p2 = Point([ax[dim][i][1] for dim, i in enumerate(idx)])
            box = Box(p1, p2-p1, canvas)
            result.append(box)
        return result

def area_union(*boxes: Box) -> float:
    assert len(set(box.canvas for box in boxes)) == 1
    split_points = set(
        [box.anchor for box in boxes] +
        [box.distant for box in boxes]
    )
    unique_boxs = set()
    for box in boxes:
        unique_boxs.update(box.split(*split_points))
    return np.sum([box.area for box in unique_boxs])

def map_box_groups(*box_groups: List[Box]) -> Dict[int, List[Box]]:
    groups = {i: list() for i in range(len(box_groups))}
    for i, group in enumerate(box_groups):
        if isinstance(group, Iterable):
            for box in group:
                assert isinstance(box, Box)
                groups[i].append(box)
        elif isinstance(group, Box):
            groups[i].append(group)
        else:
            raise NotImplementedError
    assert len(set(box.canvas for group in groups.values() for box in group))
    return groups

def area_intersection(*box_groups: List[Box]) -> float:
    groups = map_box_groups(*box_groups)
    corners = {
        p for group in groups.values()
        for box in group
        for p in [box.anchor, box.distant]}
    groups = {i: {b for box in group for b in box.split(*corners)} for i, group in groups.items()}
    intersection = set.intersection(*list(groups.values()))
    return np.sum([box.area for box in intersection])

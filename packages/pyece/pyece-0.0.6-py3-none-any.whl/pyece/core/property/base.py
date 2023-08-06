__all__ = (
    "Operation",
    "Property",
    "Constant",
    "Source",
    "Convert",
    "Iter",
    "RandomUniform",
    "RandomChoice",
    "Transformer",
)

from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable, Sequence, Union

import numpy as np

LikeProperty = Union["Property", float, int, str]
PropertySequence = Union[Sequence[LikeProperty], np.ndarray]


class Operation(ABC):
    def __call__(self, **params) -> Callable:
        def inner(obj):
            self.operation(obj, **params)

        return inner

    @abstractmethod
    def operation(self, obj, **params) -> Any:
        return NotImplemented


class Property(ABC):
    @abstractmethod
    def get(self) -> Any:
        return NotImplemented

    @property
    def value(self) -> Any:
        return self.get()

    def transform(self, operation: Operation, **kwargs) -> "Property":
        assert isinstance(operation, Operation)
        return operation(**kwargs)(self)


class Constant(Property):
    def __init__(self, value):
        self._value = value

    def get(self) -> Any:
        return self._value


def as_property(value: LikeProperty) -> Property:
    if isinstance(value, Property):
        return value
    return Constant(value)


class Source(Property):
    def __init__(self, fn: Callable, *args, **kwargs):
        assert callable(fn)
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def get(self) -> Any:
        return self._fn(*self._args, **self._kwargs)


class Convert(Source):
    def __init__(self, p: LikeProperty, fn: Callable, *args, **kwargs):
        self._original = as_property(p)
        super().__init__(fn, *args, **kwargs)

    def get(self) -> Any:
        return self._fn(self._original.value, *self._args, **self._kwargs)


class Iter(Property):
    def __init__(self, seq: Iterable):
        self._source = seq
        self._iter = iter(self._source)

    def _next(self):
        try:
            return next(self._iter)
        except StopIteration:
            self._iter = iter(self._source)
            return next(self._iter)

    def get(self) -> Any:
        return self._next()


# TODO: random state
class RandomUniform(Property):
    def __init__(self, low=0.0, high=1.0):
        self._low = low
        self._high = high

    def get(self):
        return np.random.uniform(self._low, self._high)


# TODO: random state
class RandomChoice(Property):
    def __init__(self, items):
        self._items = list(items)

    def get(self):
        return np.random.choice(self._items)


class Transformer:
    def __init__(self, *operations: Operation):
        assert all([isinstance(op, Operation) for op in operations])
        self._operations = operations

    def __call__(self, instance: Property) -> Property:
        for op in self._operations:
            instance = instance.transform(op)
        return instance

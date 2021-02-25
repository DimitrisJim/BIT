"""Tests for `bit` package. Will use a plain list holding values
in order to test against. This will most likely make things run
quite slow here due to many O(N) ops.
"""
from collections.abc import MutableSequence
from random import randint
from operator import add, sub
from bit import BIT


# quick toggle for test intensity.
intensities = {
    'quick': {
        randint(1, 10),
        randint(10, 100),
        randint(100, 1000)
    },
    'thorough': {
        randint(1000, 10000),
        randint(10000, 100000),
    },
    # you'll probably wait, a while.
    'overkill': {
        randint(100000, 1000000)
    }
}
# timeouts used with pytest-timeout
timeouts = {
    # 5m tops
    'quick': 300,
    # 15m tops
    'thorough': 900,
    # None.
    'overkill': 0
}


class DummyPS(MutableSequence):
    """ The dumb version to find prefix sums. Wraps and
    delegates to a list. """

    def __init__(self, iterable=None, op=add, inv=sub):
        self.binop = op
        self.inverse = sub
        self.storage = list(iterable) or []

    def __getitem__(self, index):
        """ O(N) prefix sum. """
        index = index + len(self) if index < 0 else index
        op = self.binop
        sum_ = self.storage[0]
        for i in range(1, index+1):
            sum_ = op(sum_, self.storage[i])
        return sum_

    def __repr__(self):
        return repr(self.storage)

    def __setitem__(self, index, value):
        self.storage[index] = value

    def update(self, index, value):
        self.storage[index] += value

    def __delitem__(self, index):
        del self.storage[index]

    def __len__(self):
        return len(self.storage)

    def extend(self, iterable):
        if isinstance(iterable, type(self)):
            iterable = list(iterable.storage)
        for v in iterable:
            self.append(v)

    def append(self, value):
        self.storage.append(value)

    def insert(self, index, value):
        self.storage.insert(index, value)

    def pop(self, index=-1):
        return self.storage.pop(index)

    def index(self, value):
        return self.storage.index(value)

    def range_sum(self, i, j):
        """ Sum from i to j. """
        return self.inverse(self[j], self[i])


def rand_int_list(length, start=0, end=1_000_000):
    """ Use random numbers from 0, 1_000_000. """
    return [randint(start, end) for _ in range(length)]


def bit_dummy(lst, binop=add, inverse=sub):
    return BIT(lst, binop, inverse), DummyPS(lst, binop)

def bit_dummy_set(lst, binop=set.union, inverse=set.intersection):
    return BIT(lst, binop, inverse), DummyPS(lst, binop, inverse)

__all__ = ['intensities', 'DummyPS', 'rand_int_list', 'bit_dummy']

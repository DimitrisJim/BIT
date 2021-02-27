"""Tests for `bit` package. Will use a plain list holding values
in order to test against. This will most likely make things run
quite slow here due to many O(N) ops.
"""
from collections.abc import MutableSequence
from collections import Counter
from random import randint
from decimal import Decimal as Dec
from operator import (
    add, sub, and_, or_, xor, mul, truediv
)
from bit import BIT


# quick toggle for test intensity.
intensities = {
    'quick': {
        randint(1, 10),
        randint(10, 100),
        randint(100, 500)
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
        self.inverse = inv
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
        old_value = self.storage[index]
        self.storage[index] = self.binop(old_value, value)

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


# Ints.
def rand_int_list(length, start=0, end=1_000_000):
    """ Use random numbers from 0, 1_000_000. """
    return [randint(start, end) for _ in range(length)]


int_add = add
int_sub = sub
int_and = and_
int_or = or_
int_xor = xor
int_mul = mul


# Decimal.
def rand_decimal_list(length, start=0, end=1_000_000):
    return [Dec(randint(start, end)) for _ in range(length)]


dec_add = add
dec_sub = sub


# Sets.
def rand_set_list(length):
    lst = rand_int_list(length)
    return [{i} for i in lst]


set_union = set.union
set_intersection = set.intersection
set_symmetric_difference = set.symmetric_difference


# Multisets.
def rand_multiset_list(length, start=0, end=1_000_000):
    # transform number to str.
    return [Counter(str(randint(start, end))) for _ in range(length)]


multiset_add = Counter.__add__
multiset_sub = Counter.__sub__


def bit_dummy(lst, binop, inverse):
    """ Create instances of BIT and dummy version with given list,
    binary op and inverse binary op.
    """
    return BIT(lst, binop, inverse), DummyPS(lst, binop, inverse)


__all__ = [
    'intensities', 'DummyPS', 'rand_int_list', 'bit_dummy',
    'rand_set_list',
]

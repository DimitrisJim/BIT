#!/usr/bin/env python
# pylint: disable=C0321, W0613, R0201, C0111
"""Tests for `bit` package. Will use a plain list holding values
in order to test against. This will most likely make things run
quite slow here due to many O(N) ops.
"""
from random import randint
import pytest
from bit import BIT


# quick toggle for test intensity.
INTENSITY = 'quick'
intensities = {
    'quick': {
        randint(10, 20),
        randint(100, 200),
        randint(1000, 2000)
    },
    'overkill': {
        randint(100, 10000),
        randint(10000, 100000),
        randint(100000, 1000000)
    }
}


class DummyPS:
    """ The dumb version to find prefix sums. Wraps a list. """

    def __init__(self, iterable=None, op=lambda x, y: x + y):
        self.binop = op
        self.storage = list(iterable) or []

    def __getitem__(self, index):
        """ O(N) prefix sum. """
        if index == 0:
            return 0
        sum_ = self.storage[0]
        for i in range(1, index):
            sum_ = self.binop(sum_, self.storage[i])
        return sum_

    def __setitem__(self, index, value):
        """ O(1) setitem. """
        self.storage[index] = value

    def __len__(self):
        return len(self.storage)

    def append(self, value):
        self.storage.append(value)


def rand_int_list(length, start=0, end=1_000_000):
    """ Use random numbers from 0, 1_000_000. """
    return [randint(start, end) for _ in range(length)]


def bit_dummy(lst, binop=lambda x, y: x + y):
    return BIT(lst, binop), DummyPS(lst, binop)


def test_basic():
    assert BIT() is not None
    assert BIT([1, 2, 3]) is not None
    assert BIT([], lambda x, y: x // y) is not None

    assert len(BIT()) == 0
    assert len(BIT(range(10))) == 10
    assert len(BIT([])) == 0


def test_layout_changes():
    
    assert BIT.bit_layout([]) == BIT([]).original_layout()
    for length in intensities[INTENSITY]:
        lst = rand_int_list(length)
        assert lst == BIT(lst).original_layout()


def test_sums():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))

        for i in range(length):
            assert bit[i] == dummy[i]

#!/usr/bin/env python
# pylint: disable=C0321, W0613, R0201, C0111
"""Tests for `bit` package. Will use a plain list holding values
in order to test against. This will most likely make things run
quite slow here due to many O(N) ops.
"""
from collections.abc import MutableSequence
from operator import add
from random import randint
import pytest
from bit import BIT


# quick toggle for test intensity.
INTENSITY = 'quick'
intensities = {
    'quick': {
        randint(0, 10),
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


class DummyPS(MutableSequence):
    """ The dumb version to find prefix sums. Wraps a list. """

    def __init__(self, iterable=None, op=add):
        self.binop = op
        self.storage = list(iterable) or []

    def __getitem__(self, index):
        """ O(N) prefix sum. """
        if index == 0:
            return 0
        op = self.binop
        sum_ = self.storage[0]
        for i in range(1, index):
            sum_ = op(sum_, self.storage[i])
        return sum_

    def __setitem__(self, index, value):
        """ Delegate to list. """
        self.storage[index] = value

    def update(self, index, value):
        """ Delegate.  O(1). """
        self.storage[index] += value

    def __delitem__(self, index):
        """ Delegate. O(N) """
        del self.storage[index]

    def __len__(self):
        return len(self.storage)

    def append(self, value):
        self.storage.append(value)

    def insert(self, index, value):
        self.storage.insert(index, value)


def rand_int_list(length, start=0, end=1_000_000):
    """ Use random numbers from 0, 1_000_000. """
    return [randint(start, end) for _ in range(length)]


def bit_dummy(lst, binop=add):
    return BIT(lst, binop), DummyPS(lst, binop)


def test_basic():
    # Quick initialization checks.
    assert BIT() is not None
    assert BIT([1, 2, 3]) is not None
    assert BIT([], lambda x, y: x // y) is not None

    # Quick len checks.
    assert len(BIT()) == 0
    assert len(BIT(range(10))) == 10
    assert len(BIT([])) == 0

    # Quick repr checks.
    assert repr(BIT()) == '[]'
    assert str(BIT()) == '[]'
    assert repr(BIT([1, 2, 5])) == '[1, 3, 5]'
    assert str(BIT([1, 5, 10])) == '[1, 6, 10]'


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

        # sanity, check that IndexError is raised.
        with pytest.raises(IndexError):
            bit[length+1]


def test_append():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy([])

        for idx, i in enumerate(rand_int_list(length)):
            bit.append(i)
            dummy.append(i)

            assert bit[idx] == dummy[idx]


def test_update():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))

        for i in range(length):
            rand_index, rand_value = randint(0, length-1), randint(0, 2**25)
            bit.update(rand_index, rand_value)
            dummy.update(rand_index, rand_value)
            # assert that all values have been updated correctly
            # (excluding previous indices).
            for ni in range(rand_index, length):
                assert bit[ni] == dummy[ni]

        # sanity, check that IndexError is raised.
        with pytest.raises(IndexError):
            bit.update(length+1, 0)


def test_iter():
    """ Both should use old iteration protocol (which
    invokes __getitem__
    """
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))

        for i, j in zip(bit, dummy):
            assert i == j


def test_reversed():
    """ Don't reverse in place, return iterator yielding sums
    reversed.
    """
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))

        for i, j in zip(reversed(bit), reversed(dummy)):
            assert i == j

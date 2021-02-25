#!/usr/bin/env python
# pylint: disable=C0321, W0613, R0201, C0111
"""Tests for `bit` package. Will use a plain list holding values
in order to test against. This will most likely make things run
quite slow here due to many O(N) ops.
"""
from random import randint, shuffle
from operator import add, sub
import pytest
from test_support import (
    intensities, rand_int_list, bit_dummy, timeouts,
)
from bit import BIT


# quick toggle [quick, thorough, overkill] for test intensity.
INTENSITY = 'quick'


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
    assert BIT.bit_layout([]) == BIT([], add, sub).original_layout()
    for length in intensities[INTENSITY]:
        lst = rand_int_list(length)
        assert lst == BIT(lst, add, sub).original_layout()

    # check that we can't build original layout without having an
    # inverse function defined:
    b = BIT([1, 2, 3, 4, 5])
    with pytest.raises(TypeError):
        b.original_layout()


def test_sums():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))

        for bi, di in zip(bit, dummy):
            assert bi == di

        # sanity, check that IndexError is raised.
        with pytest.raises(IndexError):
            bit[length]


def test_append():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy([])

        for idx, i in enumerate(rand_int_list(length)):
            bit.append(i)
            dummy.append(i)

            assert bit[idx] == dummy[idx]


@pytest.mark.timeout(timeouts[INTENSITY])
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
    # Both should use old iteration protocol (which
    # invokes __getitem__
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


@pytest.mark.timeout(timeouts[INTENSITY])
def test_iadd_extend():
    """ Implemented in MutableSequence; continuously calls append for
    every element in other. We toggle on calling __iadd__ or extend
    since both are drastically similar.
    """
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy([])
        rnd_lst = rand_int_list(length)

        # don't add to many chunks.
        added, toggle = 0, 0
        while added < length:
            # grab a random lengthed chunk,
            chunk = rnd_lst[:randint(1, length)]
            added += len(chunk) - 1
            if toggle:
                bit.extend(chunk)
                dummy.extend(chunk)
            else:
                bit += chunk
                dummy += chunk
            toggle ^= 1
            assert bit[added] == dummy[added]

    # check that extending with ourselves works fine.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))
        bit.extend(bit)
        dummy.extend(dummy)
        for i in range(len(bit)):
            assert bit[i] == dummy[i]


@pytest.mark.timeout(timeouts[INTENSITY])
def test_pop():
    # Pop from end and assert item popped is the same.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))
        while bit:
            assert bit.pop() == dummy.pop()

    # check the same for random indices, make sure sum
    # until end is valid after pop.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))
        while len(bit) > 1:
            rand_index = randint(0, len(bit)-2)
            assert bit.pop(rand_index) == dummy.pop(rand_index)
            assert bit[-1] == dummy[-1]

    # case where inverse isn't defined and we raise
    with pytest.raises(TypeError):
        b = BIT([1, 2, 3])
        b.pop()


@pytest.mark.timeout(timeouts[INTENSITY])
def test_insert():
    """ Insert in random positions and check the sums are
    correct. """
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))
        # insert 150 random elements.
        lst = [randint(0, length) for i in range(max(150, length))]

        for i in lst:
            rand_pos = randint(0, len(bit))
            bit.insert(rand_pos, i)
            dummy.insert(rand_pos, i)
            assert bit[-1] == dummy[-1]


@pytest.mark.timeout(timeouts[INTENSITY])
def test_set():
    """ Set (completely replace) value at specified index.
    BIT.__setitem__ should be O(logN).
    """
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))
        # set 150 random elements.
        lst = [randint(0, length) for i in range(max(150, length))]

        for rand_value in lst:
            rand_pos = randint(0, len(bit) - 1)
            bit[rand_pos] = rand_value
            dummy[rand_pos] = rand_value
            for i in range(rand_pos, len(bit)):
                assert bit[i] == dummy[i]

        # check index error is raised correctly.
        b = BIT()
        with pytest.raises(IndexError):
            b[10] = 20
        with pytest.raises(IndexError):
            b[0] = 20

        # check that setitem can't work without
        # inverse function supplied:
        b.append(20)
        with pytest.raises(TypeError):
            b[0] = 30

def test_index():
    """ Call underlying list, should be fine, checking for sanity. """
    for length in intensities[INTENSITY]:
        rand_lst = rand_int_list(length)
        bit, dummy = bit_dummy(rand_lst)

        shuffle(rand_lst)
        for v in rand_lst:
            assert bit.index(v) == dummy.index(v)

def test_remove():
    """ Call underlying list, should be fine, checking for sanity. """
    for length in intensities[INTENSITY]:
        rand_lst = rand_int_list(length)
        bit, dummy = bit_dummy(rand_lst)

        shuffle(rand_lst)
        for v in rand_lst:
            assert bit.remove(v) == dummy.remove(v)

def test_range_sum():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(rand_int_list(length))

        for _ in range(length // 2):
            i = randint(0, length - 2)
            j = randint(i, length-1)
            assert bit.range_sum(i, j) == dummy.range_sum(i, j)

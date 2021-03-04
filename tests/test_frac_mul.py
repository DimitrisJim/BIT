import pytest
from random import randint, shuffle
from support import bit_dummy, intensities, timeouts
from bit import BIT
ibf = None
from support import frac_mul as bf
from support import rand_frac_list as gl
INTENSITY = 'quick'

def test_sums():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)

        for bi, di in zip(bit, dummy):
            assert bi == di

        # sanity, check that IndexError is raised.
        with pytest.raises(IndexError):
            bit[length]


def test_append():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy([], bf, ibf)

        for idx, value in enumerate(gl(length)):
            bit.append(value)
            dummy.append(value)

            assert bit[idx] == dummy[idx]


@pytest.mark.timeout(timeouts[INTENSITY])
def test_update():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)

        lst = gl(max(20, length // 8))
        for value in lst:
            rand_index = randint(0, length-1)
            bit.update(rand_index, value)
            dummy.update(rand_index, value)
            # assert that all values have been updated correctly
            # (excluding previous indices).
            for ni in range(rand_index, length):
                assert bit[ni] == dummy[ni]

        # sanity, check that IndexError is raised.
        with pytest.raises(IndexError):
            bit.update(length+1, None)


def test_iter():
    # Both should use old iteration protocol (which
    # invokes __getitem__
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)

        for vb, vd in zip(bit, dummy):
            assert vb == vd


def test_reversed():
    # Don't reverse in place, return iterator yielding sums
    # reversed.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)

        for i, j in zip(reversed(bit), reversed(dummy)):
            assert i == j

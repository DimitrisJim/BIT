import pytest
from random import randint, shuffle
from support import bit_dummy, intensities, timeouts
from bit import BIT
ibf = None
from support import dec_add as bf
from support import rand_decimal_list as gl
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

from support import dec_add as bf
from support import dec_sub as ibf
from support import rand_decimal_list as gl
INTENSITY = 'quick'

def test_layout_changes():
    assert BIT.bit_layout([]) == BIT([], bf, ibf).original_layout()
    for length in intensities[INTENSITY]:
        lst = gl(length)
        assert lst == BIT(lst, bf, ibf).original_layout()

    # check that we can't build original layout without having an
    # inverse function defined:
    b = BIT([])
    with pytest.raises(TypeError):
        b.original_layout()


@pytest.mark.timeout(timeouts[INTENSITY])
def test_iadd_extend():
    # Implemented in MutableSequence; continuously calls append for
    # every element in other. We toggle on calling __iadd__ or extend
    # since both are drastically similar.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy([], bf, ibf)

        # add 50 chunks
        toggle = 0
        for i in range(50):
            # with a max length of 500.
            chunk = gl(max(length // 8, 500))
            if toggle:
                bit.extend(chunk)
                dummy.extend(chunk)
            else:
                bit += chunk
                dummy += chunk
            toggle ^= 1
            assert bit[-1] == dummy[-1]

    # check that extending with ourselves works fine.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)
        bit.extend(bit)
        dummy.extend(dummy)
        for index in range(len(bit)):
            assert bit[index] == dummy[index]


@pytest.mark.timeout(timeouts[INTENSITY])
def test_pop():
    # Pop from end and assert item popped is the same.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)
        while bit:
            assert bit.pop() == dummy.pop()

    # check the same for random indices, make sure sum
    # until end is valid after pop.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)
        while len(bit) > 1:
            rand_index = randint(0, len(bit)-2)
            assert bit.pop(rand_index) == dummy.pop(rand_index)
            assert bit[-1] == dummy[-1]

    # case where inverse isn't defined and we raise
    with pytest.raises(TypeError):
        b = BIT([gl(1).pop()])
        b.pop()


@pytest.mark.timeout(timeouts[INTENSITY])
def test_insert():
    # Insert in random positions and check the sums are
    # correct.
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)
        # insert 150 random elements.
        lst = gl(max(150, length))

        for value in lst:
            rand_pos = randint(0, len(bit))
            bit.insert(rand_pos, value)
            dummy.insert(rand_pos, value)
            assert bit[-1] == dummy[-1]


@pytest.mark.timeout(timeouts[INTENSITY])
def test_set():
    # Set (completely replace) value at specified index.
    # BIT.__setitem__ should be O(logN).
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)
        # set 150 random elements.
        lst = gl(max(150, length))

        for rand_value in lst:
            rand_pos = randint(0, len(bit) - 1)
            bit[rand_pos] = rand_value
            dummy[rand_pos] = rand_value
            for i in range(rand_pos, len(bit)):
                assert bit[i] == dummy[i]

        # check index error is raised correctly.
        b = BIT()
        with pytest.raises(IndexError):
            b[10] = None
        with pytest.raises(IndexError):
            b[0] = None

        # check that setitem can't work without
        # inverse function supplied:
        l = gl(1)
        b.append(l[-1])
        with pytest.raises(TypeError):
            b[0] = l[-1]

def test_index():
    # Call underlying list, should be fine, checking for sanity.
    for length in intensities[INTENSITY]:
        rand_lst = gl(length)
        bit, dummy = bit_dummy(rand_lst, bf, ibf)

        shuffle(rand_lst)
        for v in rand_lst:
            assert bit.index(v) == dummy.index(v)

def test_remove():
    ### Call underlying list, should be fine, checking for sanity.
    for length in intensities[INTENSITY]:
        rand_lst = gl(length)
        bit, dummy = bit_dummy(rand_lst, bf, ibf)

        shuffle(rand_lst)
        for v in rand_lst:
            assert bit.remove(v) == dummy.remove(v)

def test_range_sum():
    for length in intensities[INTENSITY]:
        bit, dummy = bit_dummy(gl(length), bf, ibf)

        for _ in range(length // 2):
            index_a = randint(0, length - 2)
            index_b = randint(index_a, length-1)
            assert bit.range_sum(index_a, index_b) == dummy.range_sum(index_a, index_b)

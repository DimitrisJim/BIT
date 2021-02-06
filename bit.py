"""Main module.

[TODO]: Explanations must be more thorough.
[TODO]: Probably need to expand on set/get/del item in order to
        support slices. Range queries will be pretty with slicing.
[XXX] Make append special case of insert? Insert, it seems likely, can't be
implemented in O(logn) while append can. I'm leaning towards keeping them
separate, that will make both more understandable and allow append to always
be worse case O(logn).
[XXX] Implement __iter__? MutableSequence.__iter__ uses old iteration protocol
(calling __getitem__ until IndexError) which also suits us here since our
__getitem__ returns the prefix sums. Probably leave as is.
"""
from operator import add, sub
from collections.abc import MutableSequence


class BIT(MutableSequence):
    """ Binary Indexed Tree, commonly known as a Fenwick Tree. """

    def __init__(self, iterable=None, binary_op=add):
        self._st = self.bit_layout(list(iterable or []), binary_op)
        self.binop = binary_op

    def __repr__(self):
        """ Return representation of Binary Index Tree. """
        # delegate to list, takes care of printing really big lists.
        return repr(self._st)

    def __getitem__(self, index):
        """ Return prefix sum until k exclusive. """
        length = len(self)
        if index > length:
            raise IndexError("Index out of range.")
        if index == 0:
            return 0

        # Set accumulator to value at index k. Doesn't
        # require it to be initialized to value that is
        # dependant on op.
        acc = self._st[index-1]
        index = index & (index - 1)
        while index > 0:
            acc = self.binop(acc, self._st[index-1])
            # clear leftmost bit.
            index = index & (index - 1)
        return acc

    # todo: use slice-iterable?
    def __setitem__(self, index, value):
        """ Update value for index k. """
        length = len(self)
        if index >= length:
            raise IndexError("Index out of range.")
        while index < length:
            self._st[index] = self.binop(self._st[index], value)
            index = index | index + 1

    # todo: use Union[int, slice]?
    def __delitem__(self, index):
        """ Op will probably be O(N), as insert will. """

    def __len__(self):
        """ Return number of elements in Binary Indexed Tree. """
        return len(self._st)

    def append(self, value):
        """ Append value to Binary Indexed Tree.  """
        length = len(self)
        # Index in which we will place new value is odd, can
        # just append.
        if length & 1 == 0:
            self._st.append(value)
            return

        # O(logn) -- worse case manifests on powers of 2.
        # Needs more explaining.
        # start from j == 4. All even indices will be divisible by
        # 2 so we just add st[length - 2//2 == 1] to our value whatever
        # the case.
        value = value + self._st[length - 1]
        # increase length to denote the will-be length.
        length, j = length + 1, 4
        # continue while we're a power of 2.
        while length % j == 0:
            # j -> 4, 8, 16, 32
            step, j = j // 2, j << 1
            # careful, haven't added item so length
            # must be decreased by one.
            value += self._st[length - 1 - step]
        self._st.append(value)

    def insert(self, index, value):
        """ Must we rebuild tree? Probably. """

    def original_layout(self):
        """ Return the original layout used to build the 
        Binary Indexed Tree.
        """
        op = sub
        length = j = len(self)
        arr = self._st.copy()
        while j := j // 2:
            for i in range(length-1, 0, -2*j):
                arr[i] = op(arr[i], arr[i-j])
        return arr

    @staticmethod
    def bit_layout(iterable, binary_op=add):
        """ Transform to fenwick (bit) representation. This
        loop makes serious sense when the intermediate
        representation in [tweakblogs] is understood.
        """
        arr = list(iterable)
        i, length = 1, len(arr)
        while i < length:
            j = 2*i - 1
            while j < length:
                arr[j] = binary_op(arr[j], arr[j-i])
                j += 2 * i
            i *= 2
        return arr

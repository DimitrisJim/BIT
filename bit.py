"""Main module."""
from operator import add, sub
from collections.abc import MutableSequence


class BIT(MutableSequence):
    """ Binary Indexed Tree.


    Notes:

     - MutableSequence.__iter__ uses __getitem__. We *want* this,
       using __getitem__ returns correct prefix sums. Yielding
       directly from _storage wont.
     - op should be able to be any binary operator that's sensible
       for the type of items contained.
    """

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

        # Set accumulator to value at index k. Doesn't
        # require it to be initialized to value based on
        # op this way.
        if index == 0:
            return 0
        acc = self._st[index-1]
        index = index & (index - 1)
        while index > 0:
            acc = self.binop(acc, self._st[index-1])
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
        # If next index is odd, just append value. Else, can use the
        # fact that st[-2] contains accumulated value until index
        # len - 2 and st[-1] contains the final value missing.
        # Combining v with these two values gives us the next value.
        # todo: re-evaluate this.
        # length = len(self)
        # if length & 1:
        #    acc_to_end = self.binop(self._st[-2], self._st[-1])
        #    value = self.binop(acc_to_end, value)
        # self._st.append(value)

    def insert(self, index, value):
        """ Must we rebuild tree? Probably. """

    def original_layout(self):
        """ Needs work. Looking at the intermediate
        repr we can figure out how to brake this apart.

        op plays a role, need it around.
        """
        # todo: fix this.
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

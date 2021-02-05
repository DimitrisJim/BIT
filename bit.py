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

    def __getitem__(self, k):
        """ Return prefix sum until k exclusive. """
        length = len(self)
        if k > length:
            raise IndexError("Index out of range.")

        # Set accumulator to value at index k. Doesn't
        # require it to be initialized to value based on
        # op this way.
        if k == 0:
            return self._st[0]
        acc = self._st[k-1]
        k = k & (k - 1)
        while k > 0:
            acc = self.binop(acc, self._st[k-1])
            k = k & (k - 1)
        return acc

    def __setitem__(self, k, v):
        """ Update value for index k. """
        length = len(self)
        if k >= length:
            raise IndexError("Index out of range.")
        while k < length:
            self._st[k] = self.binop(self._st[k], v)
            k = k | k + 1

    def __delitem__(self, index):
        """ Must we rebuild the tree? An option would be setting
        the value to 0 or 1 depending on op and . """

    def __len__(self):
        """ Return number of elements in Binary Indexed Tree. """
        return len(self._st)

    def insert(self, index, value):
        """ Must we rebuild tree? Probably. """

    def original_layout(self):
        """ Needs work. Looking at the intermediate
        repr we can figure out how to brake this apart.

        op plays a role, need it around.
        """
        # Need a formalized way of doing this.
        if self.binop is add:
            inverse = sub
        st, res = self._st, []
        acc = st[0]
        res.append(acc)
        for i in range(1, len(st)):
            if i & 1:
                res.append(inverse(st[i], acc))
            acc = self.binop(acc, res[i])
        return res

    @staticmethod
    def bit_layout(iterable, binary_op=add):
        """ Transform to fenwick (bit) representation. This
        loop makes serious sense when the intermediate
        representation in [tweakblogs] is understood.
        """
        lst = list(iterable)
        acc = lst[0]
        for i in range(1, len(lst)):
            acc = binary_op(acc, lst[i])
            if i & 1:
                lst[i] = acc
        return lst

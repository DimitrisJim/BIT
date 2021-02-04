"""Main module."""
from operator import add
from collections.abc import MutableSequence


class BIT(MutableSequence):
    """ Binary Indexed Tree.


    Notes:

     - MutableSequence.__iter__ uses __getitem__. We *want* this,
       using __getitem__ returns correct prefix sums. Yielding
       directly from _storage wont.
    """

    def __init__(self, iterable=None, op=add):
        self._st = self.to_bit(list(iterable or []), op)

    def __getitem__(self, index):
        """ Return prefix sum until k. """

    def __setitem__(self, index, value):
        """ Update value for index k. """
        pass

    def __delitem__(self, index):
        pass

    def __len__(self):
        return len(self._st)

    def insert(self, index, value):
        pass

    @staticmethod
    def to_list(arr, op=add):
        """ Needs work. Looking at the intermediate
        repr we can figure out how to brake this apart.

        op plays a role, need it around.
        """
        pass

    @staticmethod
    def to_bit(arr, op=add):
        """ Transform to fenwick (bit) representation. This
        loop makes serious sense when the intermediate
        representation in [tweakblogs] is understood.
        """
        i, length = 1, len(arr)
        while i < length:
            j = 2*i - 1
            while j < length:
                arr[j] = op(arr[j], arr[j-i])
                j += 2 * i
            i *= 2
        return arr

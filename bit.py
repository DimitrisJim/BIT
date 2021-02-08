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
[XXX] Make a couple of helper functions for traversing left/right. There's
      a lot of duplication currently going on.
[XXX] Binop might need to be commutative. Also, small-opt by assigning it
      to a local variable. Used in many loops.
[XXX] What should I do with inheritted reverse? No sense allowing in-place
      reversal. Remove it from class dict altogether?
[XXX] __setitem__ currently does the job of update. I forgot it temporarily,
     is it better if insert took the role of update? I'm thinking an update
     method would be better.

      - update      -> update value.
      - __setitem__ -> replace value.
      - insert      -> insert new value.
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
        # actually, should this raise?
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
        """ Replace value for index k. """
        # get old value, remove old value from
        # position, insert new value and go along
        # to other positions and update.
        # todo: sloppy, formalize.
        inverse_op = sub
        old = self._st[index]
        if index & 1:
            # similar logic to append.
            old = inverse_op(old, self._st[index-1])
            # odd indices hold prefix sums, go left
            # and find original value for old.
            j = 4
            while (index + 1) % j == 0:
                step, j = j // 2, j << 1
                old = inverse_op(old, self._st[index-step])

        # we have old and new. go right and update
        # indices using this value.
        while index < len(self):
            self._st[index] = inverse_op(self._st[index], old)
            self._st[index] = self.binop(self._st[index], value)
            index = index | index + 1

    # todo: use Union[int, slice]?
    def __delitem__(self, index):
        """ Op will probably be O(N), as insert will. """

    def __len__(self):
        """ Return number of elements in Binary Indexed Tree. """
        return len(self._st)

    def update(self, index, value):
        """ Update value for index k. """
        length = len(self)
        if index >= length:
            raise IndexError("Index out of range.")
        while index < length:
            self._st[index] = self.binop(self._st[index], value)
            index = index | index + 1

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
            value = self.binop(value, self._st[length - 1 - step])
        self._st.append(value)

    def insert(self, index, value):
        """ Must we rebuild tree? Probably. """
        # grab original layout, insert there, rebuild.
        # todo: could we not? think about it.
        arr = self.original_layout()
        arr.insert(index, value)
        self._st = self.bit_layout(arr)

    def original_layout(self):
        """ Return the original layout used to build the
        Binary Indexed Tree.

        This requires the inverse of the operator used to
        construct the BIT originally.

        Coarse counting of steps tells me this is O(N).
        """
        # placeholder: must formalize.
        op = sub
        length = len(self)
        # odd length doesn't have group of sums.
        # move downwards and start from there.
        # same logic here as in append.
        if length & 1:
            length -= 1
        arr = [*self._st]
        for i in range(length, 0, -2):
            j = 2
            while i % j == 0:
                step, j = j // 2, j << 1
                arr[i-1] = op(arr[i-1], arr[i-1-step])
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

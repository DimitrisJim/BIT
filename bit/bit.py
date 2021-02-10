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
[XXX] Binop might need to be commutative and associative. Also, small-opt
      by assigning it to a local variable. Used in many loops.
[XXX] __setitem__ currently does the job of update. I forgot it temporarily,
     is it better if insert took the role of update? I'm thinking an update
     method would be better.

      - update      -> update value.
      - __setitem__ -> replace value.
      - insert      -> insert new value.
[XXX] Handle negative indices. (done, double check and test pending)
"""
from collections.abc import MutableSequence
from .btypes import _T, _Gen, Iterable, List, Optional
from .binaryops import BinaryOP, Add


# todo: big todo, formalize way binary ops are used.
class BIT:
    """ Binary Indexed Tree, commonly known as a Fenwick Tree. """

    def __init__(
            self,
            iterable: Optional[Iterable[_T]] = None,
            binary_op: BinaryOP = Add
            ):
        """ BIT([iterable], [binary_op]) -- Initialize BIT.

        Binary op must be a commutative operator taking two values
        and returning one result.
        """
        self._st = self.bit_layout(list(iterable or []), binary_op)
        self.binop = binary_op

    def __repr__(self) -> str:
        """ repr(B) -> str -- Return representation of
        Binary Index Tree. """
        # delegate to list, takes care of printing really big lists.
        return repr(self._st)

    def __len__(self) -> int:
        """ len(B) -> int -- Return number of elements in
        Binary Indexed Tree. """
        return len(self._st)

    def __getitem__(self, index: int) -> _T:
        """ B[index] = value -- Get prefix sum until (including!) given
        index. Raises IndexError if BIT is empty or index is out of bounds.
        Valid bounds for index range in [0, len(B)).
        """
        # handle indexing behaviour.
        length = len(self)
        index = index + length if index < 0 else index
        if index >= length or length == 0:
            raise IndexError("Index out of range.")
        # count *until* (including) index
        index = index + 1

        # Set accumulator to value at index k. Doesn't
        # require it to be initialized to value that is
        # dependant on op.
        acc = self._st[index-1]
        index = index & (index - 1)
        for idx in self._follow_right(index):
            acc = self.binop(acc, self._st[idx-1])
        return acc

    # todo: use slice-iterable?
    # todo: inverse_op should depend on binop, formalize.
    def __setitem__(self, index: int, value: _T) -> None:
        """ B[index] = value -- Update value at given index.
        Raises IndexError if BIT is empty or index is out of bounds.
        """
        # get old value, remove old value from
        # position, insert new value and go along
        # to other positions and update.
        # adjust index if necessary
        length = len(self)
        index = index + length if index < 0 else index
        if index >= length or length == 0:
            raise IndexError("Index out of range.")
        inverse_op = self.binop.inverse
        old = self._st[index]
        if index & 1:
            # odd indices hold prefix sums, go left
            # and find original value for old.
            for step in self._powers_of_two(index + 1):
                old = inverse_op(old, self._st[index-step])

        # we have old and new. go right and update values.
        for idx in self._follow_left(index, length):
            self._st[idx] = inverse_op(self._st[idx], old)
            self._st[idx] = self.binop(self._st[idx], value)

    def update(self, index: int, value: _T) -> None:
        """ B.update(index, value) -- Update value at given index.
        Raises IndexError if BIT is empty or index is out of bounds.
        """
        length = len(self)
        index = index + length if index < 0 else index
        if index >= length or length == 0:
            raise IndexError("Index out of range.")

        for idx in self._follow_left(index, length):
            self._st[idx] = self.binop(self._st[idx], value)

    def append(self, value: _T) -> None:
        """ B.append(value) -- Append a new value to the BIT.
        Sums are updated automatically. """
        length = len(self)
        # Index in which we will place new value is odd, can
        # just append.
        if length & 1:
            # O(logn) -- worse case manifests on powers of 2.
            # Needs more explaining, pass will-be len.
            for step in self._powers_of_two(length + 1):
                # careful, haven't added item so length
                # must be decreased by one.
                value = self.binop(value, self._st[length - step])
        self._st.append(value)

    # todo: could we somehow not be O(N)? -- think about it
    def insert(self, index: int, value: _T) -> None:
        """ B.insert(index, value) -- Insert value before index. """
        # grab original layout, insert there, rebuild.
        arr: List[_T] = self.original_layout()

        # takes care of handling index.
        arr.insert(index, value)
        self._st = self.bit_layout(arr)

    # todo: use Union[int, slice]?
    def __delitem__(self, index: int) -> None:
        """ del B[key] -- Remove item at given index. Raises
        IndexError if BIT is empty or index is out of range.
        """
        _ = self.pop(index)

    def pop(self, index: int = -1) -> _T:
        """ B.pop([index]) -> item -- Remove and return item
        at given index (default -1). Raise IndexError if BIT
        is empty or index is out of range. """
        index = index + len(self) if index < 0 else index
        if index == len(self) - 1:
            value = self._st.pop()
            return value

        # get original layout, remove from there, rebuild array.
        # underlying list takes care of wrong index.
        arr: List[_T] = self.original_layout()
        value = arr[index]
        del arr[index]
        self._st = self.bit_layout(arr, self.binop)
        return value

    # todo: fix return type.
    def remove(self, value: _T) -> None:
        """ todo: Remove value from BIT. """

    # todo: fix return type.
    def index(self, value: _T) -> None:
        """ todo: Return index of given value. """

    def __iadd__(self, iterable: Iterable[_T]) -> 'BIT':
        """ B += iterable -- In-place addition of elements in
        iterable into B. """
        self.extend(iterable)
        return self

    def extend(self, iterable: Iterable[_T]) -> None:
        """ B.extend(iterable) -- extend Binary Indexed Tree by
        appending elements from iterable. """
        if isinstance(iterable, type(self)):
            # don't use sums!
            iterable = self.original_layout()
        for value in iterable:
            self.append(value)

    def count(self, value: _T) -> int:
        """ todo: count sums or values? values, probably. """
        return 0

    # Helpers.
    # todo: op is hardcoded. formalize.
    def original_layout(self) -> List[_T]:
        """ Return the original layout used to build the
        Binary Indexed Tree.

        This requires the inverse of the operator used to
        construct the BIT originally.

        Coarse counting of steps tells me this is O(N).
        """
        inverse_op = self.binop.inverse
        length = len(self)
        # odd length doesn't have group of sums.
        # move downwards and start from there.
        # same logic here as in append.
        if length & 1:
            length -= 1
        arr = [*self._st]
        for i in range(length, 0, -2):
            for step in self._powers_of_two(i):
                arr[i-1] = inverse_op(arr[i-1], arr[i-1-step])
        return arr

    @staticmethod
    def bit_layout(
            iterable: Iterable[_T],
            binary_op: BinaryOP = Add
            ) -> List[_T]:
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

    # todo: these all are related. haven't been able to unify
    # nicely yet. A single function centered around powers of
    # two seems (mentally for me at least) like the way to go.
    @staticmethod
    def _follow_left(index: int, stop: int) -> _Gen:
        """ Basically flipping left-most zero bits.  """
        while index < stop:
            yield index
            index |= index + 1

    @staticmethod
    def _follow_right(index: int, stop: int = 0) -> _Gen:
        """ Basically consuming any 1 set bits."""
        while index > stop:
            yield index
            index &= index - 1

    @staticmethod
    def _powers_of_two(index: int, start: int = 2) -> _Gen:
        """ Yields powers of two that perfectly divide index.
        We're basically consuming leftmost 0 bits in index.
        """
        while index & 1 == 0:
            yield start // 2
            start <<= 1
            index >>= 1


# Register as virtual subclass.
MutableSequence.register(BIT)

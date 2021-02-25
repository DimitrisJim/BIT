"""Main module.

[TODO]: Explanations must be more thorough.
[TODO]: Probably need to expand on set/get/del item in order to
        support slices. Range queries will be pretty with slicing.
[TODO]: Use sphinx documentation.
[TODO]: Small opts, assign to local names.
[XXX]: Make a BinOp abc class so operations that might require state
       can have a defined interface? (And allow it to be passed somehow
       to BIT class.)
[XXX]: Implement __iter__? MutableSequence.__iter__ uses old iteratio
       protocol (calling __getitem__ until IndexError) which also suit
       us here since our __getitem__ returns the prefix sums. Probably
       leave as is.
[XXX]: Handle negative indices. (done, double check and test pending)
"""
from collections.abc import MutableSequence
from operator import add
from typing import TypeVar, Callable, Generator, Iterable, List, Optional

# Can be anything.
_T = TypeVar('_T')
_Gen = Generator[int, None, None]


# todo: big todo, formalize way binary ops are used.
class BIT:
    """ Binary Indexed Tree, commonly known as a Fenwick Tree. """

    def __init__(
            self,
            iterable: Optional[Iterable[_T]] = None,
            binop: Callable[[_T, _T], _T] = add,
            inverse_binop: Optional[Callable[[_T, _T], _T]] = None
            ):
        """
        BIT([iterable], [binary_op], [inverse_binop]) -- Initialize BIT.

        Binary op must be an associative operator taking two values
        and returning one result. By default, it is set to
        operator add.
        """
        self._st = self.bit_layout(list(iterable or []), binop)
        self.binop = binop
        self.inverse = inverse_binop

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
        index.

        Raises IndexError if BIT is empty or index is out of bounds.
        Valid bounds for index range in [0, len(B)).
        """
        # handle indexing behaviour, count *including* index.
        index = self._nmlz_index(index, len(self)) + 1

        # Set accumulator to value at index k. Doesn't
        # require it to be initialized to value that is
        # dependant on op.
        binop = self.binop
        acc = self._st[index-1]
        index = index & (index - 1)
        for idx in self._c_one_lsb(index):
            acc = binop(acc, self._st[idx-1])
        return acc

    # todo: use slice-iterable?
    def __setitem__(self, index: int, value: _T) -> None:
        """ B[index] = value -- Update value at given index.

        Raises IndexError if BIT is empty or index is out of bounds.
        """
        # get old value, remove old value from
        # position, insert new value and go along
        # to other positions and update.
        # adjust index if necessary
        length, storage = len(self), self._st
        index = self._nmlz_index(index, length)
        binop, inverse = self.binop, self.inverse
        if not inverse:
            msg = "Inverse Operator is required to set an item. "
            raise TypeError(msg)
        old = storage[index]
        if index & 1:
            # odd indices hold prefix sums, go left
            # and find original value for old.
            for step in self._c_zero_lsb(index + 1):
                old = inverse(old, storage[index-step])

        # we have old and new. go right and update values.
        for idx in self._f_zero_lsb(index, length):
            storage[idx] = inverse(storage[idx], old)
            storage[idx] = binop(storage[idx], value)

    def update(self, index: int, value: _T) -> None:
        """ B.update(index, value) -- Update value at given index.

        Raises IndexError if BIT is empty or index is out of bounds.
        """
        storage, length = self._st, len(self)
        index = self._nmlz_index(index, length)

        binop = self.binop
        for idx in self._f_zero_lsb(index, length):
            storage[idx] = binop(storage[idx], value)

    def append(self, value: _T) -> None:
        """ B.append(value) -- Append a new value to the BIT.
        Sums are updated automatically. """
        storage, length = self._st, len(self)
        # Index in which we will place new value is odd, can
        # just append.
        if length & 1:
            # O(logn) -- worse case manifests on powers of 2.
            # Needs more explaining, pass will-be len.
            for step in self._c_zero_lsb(length + 1):
                # careful, haven't added item so length
                # must be decreased by one.
                value = self.binop(value, storage[length - step])
        storage.append(value)

    # todo: could we somehow not be O(N)? -- think about it
    def insert(self, index: int, value: _T) -> None:
        """ B.insert(index, value) -- Insert value before index. """
        # grab original layout, insert there, rebuild.
        # original list will take care of index.
        arr: List[_T] = self.original_layout()
        arr.insert(index, value)
        self._st = self.bit_layout(arr)

    # todo: use Union[int, slice]?
    def __delitem__(self, index: int) -> None:
        """ del B[key] -- Remove item at given index.

        Raises IndexError if BIT is empty or index is out of range.
        """
        _ = self.pop(index)

    def pop(self, index: int = -1) -> _T:
        """ B.pop([index]) -> item -- Remove and return item
        at given index (default -1).

        Raise IndexError if BIT is empty or index is out
        of range. """
        length = len(self)
        index = self._nmlz_index(index, length)
        if not self.inverse:
            msg = "Inverse Binary Operator is required for pop."
            raise TypeError(msg)
        if index == length - 1:
            # special case, can do O(logn) worse case
            # and O(1) in half/cases of pop with index == -1.
            storage = self._st

            value = storage.pop()
            if length & 1:
                return value
            # need to find original value placed here
            # todo: duplicate logic (here and setitem) move to function
            inverse_op = self.inverse
            for step in self._c_zero_lsb(index+1):
                value = inverse_op(value, storage[index - step])
            return value

        # todo: O(N) for random index. This *might* be able to
        # be improved but I'll need to think of it.
        # Get original layout, remove from there, rebuild array.
        # underlying list takes care of wrong index.
        arr: List[_T] = self.original_layout()
        value = arr[index]
        del arr[index]
        self._st = self.bit_layout(arr, self.binop)
        return value

    def remove(self, value: _T) -> None:
        """ BIT.remove(value) -- Remove first occurence of value.

        Raises ValueError if value is not present."""
        self.pop(self.index(value))

    def index(
            self,
            value: _T,
            start: int = 0,
            stop: Optional[int] = None
            ) -> int:
        """ BIT.index(value) -- Return index of first occurence of
        value.

        Raises ValueError if value is not present."""
        # delegate to original list.
        arr: List[_T] = self.original_layout()
        # to shut mypy up.
        if stop:
            return arr.index(value, start, stop)
        return arr.index(value, start)

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
            iterable = iterable.original_layout()
        for value in iterable:
            self.append(value)

    # todo: is a count method really sensible?
    def count(self, value: _T) -> int:
        """ todo: count sums or values? values, probably. """
        return 0

    # Additional methods commonly defined on fenwick trees
    # todo: can be done more efficiently.
    def range_sum(self, i: int, j: int) -> _T:
        """ BIT.range_sum(i, j) -> value. Return the range sum
        from i until j. Equivalent to self[j] - self[i].

        Raises IndexError if j < i and TypeError if the
        inverse function isn't defined."""
        # We'll need inverse here.
        if j < i:
            raise IndexError("j must be > than i.")
        if not self.inverse:
            msg = "Inverse operator required for range_sum. "
            raise TypeError(msg)
        return self.inverse(self[j], self[i])

    # Helpers.
    def original_layout(self) -> List[_T]:
        """ BIT.original_layout() -> List[items]. Return the original
        items in the list as used to build the Binary Indexed Tree.

        This requires the inverse of the operator used to
        construct the BIT originally. TypeError is raised if
        it isn't supplied.
        """
        if not self.inverse:
            msg = "Inverse Binary Operator is required for original_layout"
            raise TypeError(msg)
        inverse, length = self.inverse, len(self)
        # odd length doesn't have group of sums.
        # move downwards and start from there.
        # same logic here as in append.
        if length & 1:
            length -= 1
        arr = [*self._st]
        for i in range(length, 0, -2):
            for step in self._c_zero_lsb(i):
                arr[i-1] = inverse(arr[i-1], arr[i-1-step])
        return arr

    @staticmethod
    def bit_layout(
            iterable: Iterable[_T],
            binary_op: Callable[[_T, _T], _T] = add
            ) -> List[_T]:
        """ BIT.bit_layout(iterable, [binary_op]) -> List[items].
        Transform to fenwick (bit) representation.
        """
        # This loop makes serious sense when the intermediate
        # representation in [tweakblogs] is understood.
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
    def _f_zero_lsb(index: int, stop: int) -> _Gen:
        """ Flip zero set bits starting from LSB.  """
        while index < stop:
            yield index
            index |= index + 1

    @staticmethod
    def _c_one_lsb(index: int, stop: int = 0) -> _Gen:
        """ Consuming set bits starting from LSB."""
        while index > stop:
            yield index
            index &= index - 1

    @staticmethod
    def _c_zero_lsb(index: int, start: int = 2) -> _Gen:
        """ Yields powers of two that perfectly divide index.
        Consuming unset bits starting from LSB.
        """
        while index & 1 == 0:
            yield start // 2
            start <<= 1
            index >>= 1

    @staticmethod
    def _nmlz_index(index: int, length: int) -> int:
        """ Normalize index, bringing it in [0, len(self)),
        IndexError is raised if index is out of bounds.
        """
        index = index + length if index < 0 else index
        if index >= length or length == 0:
            raise IndexError("Index out of range.")
        return index


# Register as virtual subclass.
MutableSequence.register(BIT)

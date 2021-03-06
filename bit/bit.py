"""Main module.

[TODO]: Explanations must be more thorough.
[TODO]: Probably need to expand on set/get/del item in order to
        support slices. Range queries will be pretty with slicing.
[TODO]: Use sphinx documentation.
[XXX]: Make a BinOp abc class so operations that might require state
       can have a defined interface? (And allow it to be passed somehow
       to BIT class.)
[XXX]: Implement __iter__? MutableSequence.__iter__ uses old iteration
       protocol (calling __getitem__ until IndexError) which also suits
       us here since our __getitem__ returns the prefix sums. Probably
       leave as is.
[XXX]: Handle negative indices. (done, double check and test pending)
"""
from collections.abc import MutableSequence
from operator import add
from typing import (TypeVar, Callable, Generator, Iterable, List, Optional,
                    Union)
# Can be anything.
_T = TypeVar('_T')
_Gen = Generator[int, None, None]


# todo: big todo, formalize way binary ops are used.
class BIT:
    """ Binary Indexed Tree, commonly known as a Fenwick Tree. """

    def __init__(self,
                 iterable: Optional[Iterable[_T]] = None,
                 binop: Callable[[_T, _T], _T] = add,
                 inverse_binop: Optional[Callable[[_T, _T], _T]] = None):
        """
        Initialize a new Binary Indexed Tree with an optional iterable.

        >>> BIT(range(10))
        [0, 1, 2, 6, 4, 9, 6, 28, 8, 17]

        Binary operator ``binop`` must be an associative operator taking two
        values and returning one result. By default, it is set to
        ``operator.add``. If an inverse binary operator ``inverse_binop``
        is supplied, it can be used to restructure the initial array as well
        as support more methods.

        :complexity: :math:`O(n)` where `n` is the number of
                     items in the iterable.
        """
        self._st = self.bit_layout(list(iterable or []), binop)
        self.binop = binop
        self.inverse = inverse_binop

    def __repr__(self) -> str:
        """ Return a sensible representation of the
        Binary Index Tree.

        >>> b = BIT(range(10))
        >>> print(b)
        [0, 1, 2, 6, 4, 9, 6, 28, 8, 17]

        :complexity: :math:`O(n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        """
        # delegate to list, takes care of printing really big lists.
        # don't return original, it requires inverse op.
        return repr(self._st)

    def __len__(self) -> int:
        """ Return the number of elements in the
        Binary Indexed Tree.

        >>> b = BIT(range(10))
        >>> len(b)
        10

        :complexity: :math:`O(1)`
        """
        return len(self._st)

    def __getitem__(self, index: Union[int, slice]) -> _T:
        """ Return the prefix sum until (including!) the given
        index. ``BIT.__getitem__`` is shorthand for ``BIT.prefix_sum(i)``, both
        behave in exactly the same way:

        >>> b = BIT(range(10))
        >>> b[9]
        45
        >>> b[9] == b.prefix_sum(9)
        True

        :complexity: :math:`O(\log{}n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        :raises IndexError: If BIT is empty or index is out of bounds.
                            Valid bounds for index are in range
                            ``[0, len(B))``.
        """
        if isinstance(index, slice):
            # handle indices and call range_sum
            length = len(self)
            start, end = index.start, index.stop
            if start is None:
                start = 0
            else:
                start = start + length if start < 0 else start
            if end is None:
                end = length - 1
            else:
                end = end + length if end < 0 else end
            return self.range_sum(start, end)
        return self.prefix_sum(index)

    # todo: use slice-iterable?
    def __setitem__(self, index: int, value: _T) -> None:
        """ Replaces the value originally located at index ``index`` with a new
        value. In order to do this, a sensible ``inverse_binop`` is required.

        >>> b = BIT(range(10), inverse_binop = int.__sub__)
        >>> b[0] = 10
        >>> b.original_layout()
        [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        :complexity: :math:`O(\log{}n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        :raises IndexError: If BIT is empty or index is out of bounds.
        :raises TypeError: If ``inverse_binop`` hasn't been supplied.
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
                old = inverse(old, storage[index - step])

        # we have old and new. go right and update values.
        for idx in self._f_zero_lsb(index, length):
            storage[idx] = inverse(storage[idx], old)
            storage[idx] = binop(storage[idx], value)

    def update(self, index: int, value: _T) -> None:
        """ Updates the value at given index. This does not replace the original
        value that was placed there; the `value` supplied is applied to what
        was originally there by using `binop`.

        >>> b = BIT(range(10), inverse_binop = int.__sub__)
        >>> b.update(5, 10)
        >>> b.original_layout()
        [0, 1, 2, 3, 4, 15, 6, 7, 8, 9]

        :complexity: :math:`O(\log{}n)` where `n` is the number of items in the
                     Binary Indexed Tree.
        :raises IndexError: If BIT is empty or index is out of bounds.
        """
        storage, length = self._st, len(self)
        index = self._nmlz_index(index, length)

        binop = self.binop
        for idx in self._f_zero_lsb(index, length):
            storage[idx] = binop(storage[idx], value)

    def append(self, value: _T) -> None:
        """ Append a new value to the BIT.

        >>> b = BIT(range(10), inverse_binop = int.__sub__)
        >>> b.append(10)
        >>> b[10]
        55
        >>> b.original_layout()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        :complexity: :math:`O(\log{}n)` where `n` is the number of items
                     in the Binary Indexed Tree.
        """
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
        """ Insert value before index, requires ``inverse_binop`` be defined.

        >>> b = BIT(range(5), inverse_binop = int.__sub__)
        >>> prev_sum = b[4]
        >>> b.insert(0, 50)
        >>> prev_sum + 50 == b[5]
        True

        :complexity: :math:`O(n)` where `n` is the number of items in the
                     Binary Indexed Tree.
        """
        # grab original layout, insert there, rebuild.
        # list will take care of index.
        arr: List[_T] = self.original_layout()
        arr.insert(index, value)
        self._st = self.bit_layout(arr, self.binop)

    # todo: use Union[int, slice]?
    def __delitem__(self, index: int) -> None:
        """ Deletes item at given index. ``inverse_binop`` is required
        in order to perform the deletion.

        >>> b = BIT(range(5), inverse_binop = int.__sub__)
        >>> del b[0]
        >>> b.original_layout()
        [1, 2, 3, 4]

        :complexity: :math:`O(n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        :raises IndexError: If BIT is empty or index is out of range.
        """
        _ = self.pop(index)

    def pop(self, index: int = -1) -> _T:
        """ Remove and return item at given index (default -1).
        Requires `inverse_binop` be specified for indexes not
        equal to `-1`.

        >>> b = BIT(range(5), inverse_binop = int.__sub__)
        >>> b.pop()
        4
        >>> b.pop()
        3
        >>> b.pop()
        2
        >>> b.pop()
        1
        >>> b.pop()
        0

        :complexity: :math:`O(n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        :raises IndexError: If BIT is empty or index is out of range.
        :raises TypeError: If the `inverse_binop` hasn't been defined.
        """
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
            for step in self._c_zero_lsb(index + 1):
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
        """ Remove and return a given value.

        >>> b = BIT(range(5), inverse_binop = int.__sub__)
        >>> b.remove(0)
        >>> print(b)
        [1, 3, 3, 10]
        >>> b.remove(4)
        >>> print(b)
        [1, 3, 3]
        >>> b.remove(1)
        >>> print(b)
        [2, 5]

        :complexity: :math:`O(n)` where `n` is the number of items
                     in the Binary Indexed Tree.
        :raises ValueError: If the value is not present.
        """
        self.pop(self.index(value))

    def index(self,
              value: _T,
              start: int = 0,
              stop: Optional[int] = None) -> int:
        """ Return the index of the first occurence of value.
        `inverse_binop` is required in order to run `index`.

        >>> b = BIT(range(5), inverse_binop = int.__sub__)
        >>> b.index(4)
        4
        >>> b.index(0)
        0

        :complexity: :math:`O(n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        :raises ValueError: If value is not present in the collection.
        """
        # delegate to original list.
        arr: List[_T] = self.original_layout()
        # to shut mypy up.
        if stop:
            return arr.index(value, start, stop)
        return arr.index(value, start)

    def __iadd__(self, iterable: Iterable[_T]) -> 'BIT':
        """ Extend Binary Indexed Tree in-place by appending elements from
        the iterable. The `inverse_binop` is only required when the
        iterable is an instance of BIT.

        >>> b = BIT(range(5))
        >>> b += list(range(10))
        >>> print(b)
        [0, 1, 2, 6, 4, 4, 1, 13, 3, 7, 5, 18, 7, 15, 9]

        :complexity: :math:`O(n)` where `n` is the number of items in the
                     Binary Indexed Tree.
        :raises TypeError: If iterable is an instance of BIT and `inverse_op`
                           hasn't been specified.
        """
        self.extend(iterable)
        return self

    def extend(self, iterable: Iterable[_T]) -> None:
        """ Extend Binary Indexed Tree by appending elements from the
        iterable. The `inverse_binop` is only required when the
        iterable is an instance of BIT.

        >>> b = BIT(range(5))
        >>> b.extend(list(range(10)))
        >>> print(b)
        [0, 1, 2, 6, 4, 4, 1, 13, 3, 7, 5, 18, 7, 15, 9]

        :complexity: :math:`O(n)`
        :raises TypeError: If iterable is an instance of BIT and `inverse_op`
                           hasn't been specified.
        """
        if isinstance(iterable, type(self)):
            # don't use sums!
            iterable = iterable.original_layout()
        for value in iterable:
            self.append(value)

    # Additional methods commonly defined on fenwick trees
    # todo: can be done more efficiently.
    def range_sum(self, i: int = 0, j: Optional[int] = None) -> _T:
        """ Return the range sum until (including!) the given index.

        >>> b = BIT(range(10), inverse_binop=int.__sub__)
        >>> b.range_sum(3, 6)
        15

        :complexity: :math:`O(\log{}n)` where `n` is the number of items
                     in the Binary Indexed Tree.
        :raises IndexError: If BIT is empty, `i > j`, or any of `i`,`j` are
                            out of bounds. Valid bounds for index are in
                            range ``[0, len(B))``
        :raises TypeError: If `inverse_binop` hasn't been provided.
        """
        # We'll need inverse here.
        if j is None:
            j = len(self) - 1
        if j < i:
            raise IndexError("j must be > than i.")
        if not self.inverse:
            msg = "Inverse operator required for range_sum. "
            raise TypeError(msg)
        return self.inverse(self[j], self[i])

    def prefix_sum(self, index: int) -> _T:
        """ Return the prefix sum (or prefix ``<binop>``) until (including!) the
        given index. ``BIT.__getitem__`` is shorthand for ``BIT.prefix_sum(i)``
        both behave in exactly the same way:

        >>> b = BIT(range(10))
        >>> b.prefix_sum(9)
        45
        >>> b.prefix_sum(9) == b[9]
        True

        :complexity: :math:`O(\log{}n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        :raises IndexError: If BIT is empty or index is out of bounds.
                            Valid bounds for index are in range ``[0, len(B))``
        """
        # handle indexing behaviour, count *including* index.
        index = self._nmlz_index(index, len(self)) + 1

        # Set accumulator to value at index k. Doesn't
        # require it to be initialized to value that is
        # dependant on op.
        binop = self.binop
        acc = self._st[index - 1]
        index = index & (index - 1)
        for idx in self._c_one_lsb(index):
            acc = binop(acc, self._st[idx - 1])
        return acc

    # Helpers.
    def original_layout(self) -> List[_T]:
        """ Returns a list whose values, when transformed to a fenwick
        tree would equal self.

        >>> b = BIT(range(10), inverse_binop=int.__sub__)
        >>> b.original_layout()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> b[5] = 0
        >>> b.original_layout()
        [0, 1, 2, 3, 4, 0, 6, 7, 8, 9]

        :complexity: :math:`O(n)` where `n` is the number of items in
                     the Binary Indexed Tree.
        :raises TypeError: If `inverse_binop` isn't provided.
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
                arr[i - 1] = inverse(arr[i - 1], arr[i - 1 - step])
        return arr

    @staticmethod
    def bit_layout(iterable: Iterable[_T],
                   binary_op: Callable[[_T, _T], _T] = add) -> List[_T]:
        """ Transform iterable to fenwick (BIT) representation.

        >>> BIT.bit_layout([1, 20, 4, 32])
        [1, 21, 4, 57]
        >>> BIT.bit_layout(i for i in range(13))
        [0, 1, 2, 6, 4, 9, 6, 28, 8, 17, 10, 38, 12]

        :complexity: :math:`O(n)` where `n` is the number of items
                     in the iterable.
        """
        # This loop makes serious sense when the intermediate
        # representation in [tweakblogs] is understood.
        arr = list(iterable)
        i, length = 1, len(arr)
        while i < length:
            j = 2 * i - 1
            while j < length:
                arr[j] = binary_op(arr[j], arr[j - i])
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

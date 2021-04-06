Binary Indexed Tree
-------------------

Introduction
============

The Binary Indexed Tree implements the interface as defined by `collections.abc.MutableSequence`. Care needs to be taken on the distinction between the original values and the final value that are computed after `n` applications of the binary operator supplied.  

The class requires a sensible binary operator defined for the type of the values that will be present. The inverse binary operator, though not required to initialize and get and update items, is needed for most other operations.

Simple Example
==============

The simplest example would initialize a binary indexed tree from a given iterable and query the 
object through `__getitem__` or `prefix_sum`. For example::

    >>> from bit import BIT
    >>> b = BIT(range(50))   # use operator.add by default
    >>> b[-1]   # sum until 50
    1225
    >>> b[25]   # sum until 25
    325
    >>> # prefix_sum is the same as __getitem__
    >>> b.prefix_sum(49) == b.prefix_sum(-1) == b[-1]
    True

Without supplying the inverse operator, updating the value at a given index is also possible via `update`:

>>> b.update(0, 500)
>>> b[-1]
1725

Note that there's a subtle difference between `update` and `__setitem__`. `update` simplyadds to the previous value in the specified index without replacing it. `__setitem__` replaces the value previously present there. In order to do this, the inverse of the binary operator supplied is required.

Binary Indexed Tree (BIT) Class
===============================

.. autoclass:: bit.BIT
    :members:
    :special-members: __init__, __getitem__, __setitem__
            
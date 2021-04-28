Binary Indexed Tree
===================

Introduction
------------

A Binary Indexed Tree (Fenwick Tree) allows :math:`O(\log{}n)` queries for sums over a sequence of values.
Usually, when a sum is required, a full traversal of the sequence is performed, leading to
a modest but lacking :math:`O(n)`. When multiple queries are performed, it is more performant
to transform the array into a Binary Indexed Tree and perform the queries on it, instead. 

The Binary Indexed Tree cleverly accomplishes this by keeping partial sums in certain indices of the
supplied list. As a result, in order to build a sum until a given index, it only needs to sum certain
indices in the list. For more on how this is done, see Theory.

Operators
"""""""""

Though commonly used for partial sums, other binary operators can be supplied as the operation to be
applied on the elements. The sole requirement for the binary operator is that it is commutative, that is,
for a given operator :math:`*` on a set :math:`S`, the following holds for all :math:`x` and :math:`y` that
belong to :math:`S`:

.. centered::
    :math:`x * y = y * x`

For certain operations, the inverse of the binary operator supplied is needed. By using an inverse,
we can implemenent the transformation backwards and, among other things, support transitioning from
one view of the data (binary tree layout) to the original view, as supplied. With certain operators,
the inverse is trivially easy to find and use, with others, it might not. Look at the table in the
following section for operators which are currently used during testing and the inverses where those
are defined. 

Other possible operators:
"""""""""""""""""""""""""

The following operations with inverses defined exist:

1. Addition :math:`+` with an inverse of subtraction :math:`-` for ints, decimals and fractionals.
2. Multiset addition and subtraction. These are available in Python via `Counter`s 
   methods `__add__` and `__sub__`.
3. Bitwise xor `^` operation on integers. The inverse is, as one might expect, XOR itself

The following operations without inverses have been tested:

1. The union operator :math:`\cup` for two sets of arbitrary elements.
2. The intersection operator :math:`\cap` for two sets of arbitrary elements.
3. The symmetric difference operator :math:`\ominus` for two sets of arbitrary elements.
4. Multiplication for integers, fractionals.
5. The bitwise operators `&` (AND), `|` (OR) for integers.

Simple Example
---------------

As a simple example, we initialize a Binary Indexed Tree from a given iterable and query the 
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

Note that there's a subtle difference between `update` and `__setitem__`, `update` adds to the previous 
value in the specified index without replacing it while  `__setitem__` replaces the value previously 
present there. Due to the way the Binary Indexed Tree works, updating can be done *without* the inverse binary
operator being specified (while `__setitem__` requires it.

BIT Class
---------

In this section, the methods of the Binary Indexed Tree are presented. Note that
it implements the MutableSequence ABC allowing it to be used as a normal Python
list would.

.. autoclass:: bit.BIT
    :members:
    :special-members: __init__, __getitem__, __setitem__
            
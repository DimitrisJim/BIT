#!/usr/bin/env python
# pylint: disable=C0321, W0613, R0201, C0111
"""Tests for `bit` package. Will use a plain list holding values
in order to test against. This will most likely make things run
quite slow here due to many O(N) ops.
"""
from random import randint, shuffle
from operator import add, sub
import pytest
from test_support import (
    intensities, rand_int_list, bit_dummy, timeouts,
)
from bit import BIT


# quick toggle [quick, thorough, overkill] for test intensity.
INTENSITY = 'quick'
binop = set.union
inverse = set.intersection

def test_basic():
    # Quick initialization checks.
    assert BIT([{1}, {2}, {3}], binop) is not None

    # Quick len checks.
    assert len(BIT()) == 0
    assert len(BIT([{i} for i in range(10)], binop)) == 10
   
    # Quick repr checks.
    assert repr(BIT()) == '[]'
    assert str(BIT()) == '[]'
    assert repr(BIT([{i} for i in [1, 2, 5]], binop)) == '[{1}, {1, 2}, {5}]'
    assert str(BIT([{i} for i in [1, 5, 10]], binop)) == '[{1}, {1, 5}, {10}]'

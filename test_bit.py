#!/usr/bin/env python
"""Tests for `bit` package. Will use a plain list holding values
in order to test against. This will most likely make things run
quite slow here due to many O(N) ops.
"""
import pytest
from bit import BIT


def test_init():
    assert BIT() is not None
    assert BIT([1, 2, 3]) is not None
    assert BIT([], lambda x, y: x // y) is not None

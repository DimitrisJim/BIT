#!/usr/bin/env python
"""Tests for `bit` package."""
import pytest
from bit import BIT


def test_init():
    assert BIT() is not None

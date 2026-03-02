"""Tests for utils/globals.py — verifies each helper returns a float
within the documented range over a reasonable number of samples.
"""
import pytest
from utils import globals


NUM_SAMPLES = 200


class TestRandomFloat:
    """random_float() should return values in [0.08, 0.22]."""

    def test_returns_float(self):
        result = globals.random_float()
        assert isinstance(result, float)

    def test_lower_bound(self):
        for _ in range(NUM_SAMPLES):
            assert globals.random_float() >= 0.08, "random_float() returned value below 0.08"

    def test_upper_bound(self):
        for _ in range(NUM_SAMPLES):
            assert globals.random_float() <= 0.22, "random_float() returned value above 0.22"

    def test_not_in_old_buggy_range(self):
        """Values must never reach 0.8 (the old, incorrect lower bound)."""
        for _ in range(NUM_SAMPLES):
            assert globals.random_float() < 0.8, "random_float() reached the old buggy bound (0.8)"


class TestRandomHold:
    """random_hold() should return values in [0.05, 0.12]."""

    def test_returns_float(self):
        assert isinstance(globals.random_hold(), float)

    def test_bounds(self):
        for _ in range(NUM_SAMPLES):
            val = globals.random_hold()
            assert 0.05 <= val <= 0.12, f"random_hold() out of range: {val}"


class TestRandomDelay:
    """random_delay() should return values in [0.05, 0.18]."""

    def test_returns_float(self):
        assert isinstance(globals.random_delay(), float)

    def test_bounds(self):
        for _ in range(NUM_SAMPLES):
            val = globals.random_delay()
            assert 0.05 <= val <= 0.18, f"random_delay() out of range: {val}"

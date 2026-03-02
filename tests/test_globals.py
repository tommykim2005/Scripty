"""
Smoke tests for utils/globals.py

Verifies that each timing-helper function exists, is callable, and returns
a float within its expected range.  No external dependencies are required
(globals.py only uses the stdlib `random` module).

Known bug (tracked for follow-up, NOT fixed here):
    random_float() is defined as random.uniform(0.8, 0.22).
    The README documents the intended range as (0.08, 0.22).
    The leading zero is missing — '0.8' should be '0.08'.
    Python still returns a float (in [0.22, 0.80]), so no exception is
    raised, but the duration is much longer than intended.
"""

import pytest
from utils.globals import random_float, random_hold, random_delay


# ---------------------------------------------------------------------------
# random_float
# ---------------------------------------------------------------------------

def test_random_float_returns_float():
    assert isinstance(random_float(), float)


def test_random_float_in_range():
    # Reflects *actual* behavior: args are (0.8, 0.22) so Python returns
    # a value in [0.22, 0.80].  See module docstring for the bug note.
    result = random_float()
    assert 0.22 <= result <= 0.80, (
        f"random_float() returned {result!r}; expected in [0.22, 0.80]. "
        "Note: README says range should be (0.08, 0.22) — args look swapped."
    )


# ---------------------------------------------------------------------------
# random_hold
# ---------------------------------------------------------------------------

def test_random_hold_returns_float():
    assert isinstance(random_hold(), float)


def test_random_hold_in_range():
    result = random_hold()
    assert 0.05 <= result <= 0.12, (
        f"random_hold() returned {result!r}; expected in [0.05, 0.12]"
    )


# ---------------------------------------------------------------------------
# random_delay
# ---------------------------------------------------------------------------

def test_random_delay_returns_float():
    assert isinstance(random_delay(), float)


def test_random_delay_in_range():
    result = random_delay()
    assert 0.05 <= result <= 0.18, (
        f"random_delay() returned {result!r}; expected in [0.05, 0.18]"
    )

"""Test dspyfun."""

import dspyfun


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(dspyfun.__name__, str)

"""
Unit and regression test for the PredictDSSP package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import PredictDSSP


def test_PredictDSSP_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "PredictDSSP" in sys.modules

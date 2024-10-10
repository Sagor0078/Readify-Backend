# tests/test_simple.py

import pytest
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="passlib.utils")


@pytest.fixture
def simple_fixture():
    return "Hello, World!"

def test_simple(simple_fixture):
    assert simple_fixture == "Hello, World!"
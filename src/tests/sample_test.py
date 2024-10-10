# tests/test_simple.py

import pytest

@pytest.fixture
def simple_fixture():
    return "Hello, World!"

def test_simple(simple_fixture):
    assert simple_fixture == "Hello, World!"
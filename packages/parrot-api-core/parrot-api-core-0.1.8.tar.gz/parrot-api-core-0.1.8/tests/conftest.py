import pytest


@pytest.fixture()
def test_directory():
    import os
    return os.path.abspath(__file__).replace(
        'conftest.py', '')

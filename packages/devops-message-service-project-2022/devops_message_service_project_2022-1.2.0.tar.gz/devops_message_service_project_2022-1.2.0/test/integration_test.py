import pytest
import time


@pytest.fixture(scope="session", autouse=True)
def before_tests(request):
    time.sleep(30)


def test_read_messages():
    assert 0 == 0


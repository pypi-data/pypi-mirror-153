import pytest
from multiprocessing import Process

from cjen.tests.mock_service import mock_app


class MockProcess(Process):
    def __init__(self):
        super().__init__()

    def run(self): mock_app.run()


@pytest.fixture(scope='module', autouse=True)
def mock():
    mp = MockProcess()
    mp.start()
    yield
    mp.terminate()

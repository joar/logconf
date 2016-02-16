import logging
import pytest


@pytest.fixture
def handler(request):
    return TestHandler()


@pytest.fixture
def logger(handler):
    _log = logging.getLogger('test_logconf_test')
    _log.addHandler(handler)


class TestHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        self.emitted = []
        super(TestHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        self.emitted.append(record)

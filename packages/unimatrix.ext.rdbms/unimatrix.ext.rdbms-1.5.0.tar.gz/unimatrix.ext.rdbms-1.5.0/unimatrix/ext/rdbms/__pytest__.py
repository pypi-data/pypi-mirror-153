# pylint: skip-file
from unimatrix.lib.test import TEST_STAGE

from .fixtures import setup_databases


def pytest_sessionstart(*args, **kwargs) -> None:
    """If :attr:`unimatrix.lib.test.TEST_STAGE` is ``system``, and database
    connections are configured, create a test database for each connection.
    """
    if TEST_STAGE != 'system':
        return
    setup_databases()

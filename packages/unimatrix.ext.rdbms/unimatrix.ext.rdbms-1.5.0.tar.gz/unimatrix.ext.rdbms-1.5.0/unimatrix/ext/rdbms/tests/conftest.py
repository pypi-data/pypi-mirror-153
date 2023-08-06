# pylint: skip-file
import asyncio
import tempfile

import dsnparse
import pytest
from unimatrix.lib.rdbms.config import encode_dsn
from unimatrix.lib.rdbms.config import parse_environment

from ..connection import Connection


@pytest.fixture
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture
def sqlite():
    _, fn = tempfile.mkstemp()
    return Connection(
        encode_dsn(
            parse_environment({
                'DB_ENGINE': "sqlite",
                'DB_NAME': fn
            })
        )
    )


@pytest.fixture
def postgresql():
    return Connection(
        encode_dsn(
            parse_environment({
                'DB_ENGINE': 'postgresql',
                'DB_HOST': 'localhost',
                'DB_NAME': 'rdbms',
                'DB_USERNAME': 'rdbms',
                'DB_PASSWORD': 'rdbms',
            })
        )
    )

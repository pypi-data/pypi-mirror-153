"""Declares test fixtures to set up and tear down databases."""
import functools

import pytest
from unimatrix.ext import rdbms

from .testsession import TestSession


@pytest.mark.asyncio
@pytest.fixture(scope='function')
async def rdbms_transaction():
    methods = {}
    await rdbms.connect(debug=True)
    for alias, connection in dict.items(rdbms.connections.config):
        methods[alias] = connection.get_session
        session = connection.get_session()
        connection.get_session = TestSession(session)
    yield
    for alias, connection in dict.items(rdbms.connections.config):
        session = connection.get_session()
        await session.destroy()
        connection.get_session = methods[alias]

    await rdbms.disconnect()


def setup_databases():
    config = rdbms.connections.config
    rdbms.connections.config = {
        alias: connection.as_test()
        for alias, connection in dict.items(config)
    }

    # Create the test databases
    for connection in dict.values(rdbms.connections.config):
        connection.create_database()
    yield
    for connection in dict.values(rdbms.connections.config):
        connection.drop_database()
    rdbms.connections.config = config

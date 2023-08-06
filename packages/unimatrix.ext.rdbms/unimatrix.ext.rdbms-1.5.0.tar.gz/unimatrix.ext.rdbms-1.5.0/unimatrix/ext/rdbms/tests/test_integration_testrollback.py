# pylint: skip-file
import unittest

import pytest

from unimatrix.ext import rdbms
from unimatrix.ext.rdbms.testsession import TestSession


@pytest.mark.asyncio
@pytest.mark.usefixtures('rdbms_transaction')
async def test_session_is_wrapped():
    connection = rdbms.get('self')
    session = connection.get_session()
    assert type(session).__name__ == 'TestSession'


@pytest.mark.asyncio
@pytest.mark.usefixtures('rdbms_transaction')
async def test_generic_statements():
    connection = rdbms.get('self')
    async with connection.get_session() as session:
        async with session.begin():
            await session.execute("SELECT 1")

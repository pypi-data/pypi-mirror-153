# pylint: skip-file
import asyncio

import pytest

from unimatrix.ext import rdbms
from ..connection import Connection


@pytest.mark.asyncio
async def test_max_connections_raises(postgresql):
    engines = []
    for i in range(10):
        engines.append(Connection(postgresql.dsn))
    await asyncio.gather(*[x.connect(debug=True) for x in engines])

    futures = []
    for e in engines:
        session = e.get_session()

        async def f():
            await session.execute("SELECT 1")
            await asyncio.sleep(2)
            await session.close()

        futures.append(f())

    await asyncio.gather(*futures)
    raise Exception

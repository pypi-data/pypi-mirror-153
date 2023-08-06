# pylint: skip-file
import asyncio
import os

import sqlalchemy
from unimatrix.ext import rdbms


async def tx1(db):
    async with db.atomic() as repo:
        await repo.execute("INSERT INTO foo VALUES (1)")
        await asyncio.sleep(1.5)


async def tx2(db):
    async with db.atomic() as repo:
        result = list(await repo.execute("SELECT * FROM foo"))
        assert not result, result


async def main():
    await rdbms.connect()
    async with rdbms.connections.get('self').begin() as connection:
        await connection.execute(sqlalchemy.text("TRUNCATE foo CASCADE"))

    repo = rdbms.Repository()
    await asyncio.gather(
        tx1(repo),
        tx2(repo)
    )


if __name__ == '__main__':
    asyncio.run(main())

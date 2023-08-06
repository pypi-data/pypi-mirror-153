# pylint: skip-file
import asyncio

import sqlalchemy

from ..repository import Repository
from .base import BaseTestCase


class PostgreSQLTransactionIsolationTestCase(BaseTestCase):
    engine = 'postgresql'

    def setUp(self):
        super().setUp()
        self.add_connection('self', {
            'DB_ENGINE': self.engine,
            'DB_USERNAME': 'rdbms',
            'DB_PASSWORD': 'rdbms',
            'DB_NAME': 'rdbms'
        })
        self.connect_databases()
        self.connection = self.get_connection()
        self.relation = sqlalchemy.Table(
            'foo',
            self.metadata,
            sqlalchemy.Column(
                'id',
                sqlalchemy.String(7),
                primary_key=True
            )
        )
        self.run_async(self.setup)

    async def setup(self):
        async with self.connection.begin() as connection:
            await connection.run_sync(self.metadata.drop_all)
            await connection.run_sync(self.metadata.create_all)

    def test_mutation_is_not_visible(self):

        async def transaction_a(repo):
            async with repo.atomic() as session:
                await session.execute(
                    self.relation.insert()\
                        .values(id='foo')
                )
                await asyncio.sleep(0.5)
                result = list(await session.execute(self.relation.select()))
                assert result, result

        async def transaction_b(repo):
            async with repo.atomic() as session:
                result = list(await session.execute(self.relation.select()))
                assert not result, result
                await asyncio.sleep(1.5)
            async with repo.atomic() as session:
                result = list(await session.execute(self.relation.select()))
                assert result, result

        async def main():
            repo = Repository()
            await asyncio.gather(
                transaction_a(repo),
                transaction_b(repo),
            )

        self.run_async(main)


class MySQLTransactionIsolationTestCase(PostgreSQLTransactionIsolationTestCase):
    engine = 'mysql'

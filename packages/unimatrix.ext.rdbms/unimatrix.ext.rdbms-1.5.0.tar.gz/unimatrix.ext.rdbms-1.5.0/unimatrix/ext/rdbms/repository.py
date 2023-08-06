"""Declares :class:`Repository`."""
import typing

import sqlalchemy
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import Delete
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.selectable import Select
from unimatrix.ext import rdbms


EXECUTABLE = typing.Union[Delete, Update, Select]
RESULT = typing.Union[Result]


class Repository:
    """Integrates the :term:`Repository Layer` with relational database systems
    using the :mod:`sqlalchemy` package. Implements :class:`ddd.Repository`.
    """
    #: Specifies the connection that is used by the repository implementation,
    #: as specified using the :mod:`unimatrix.ext.rdbms` framework.
    alias: str = 'self'

    async def get_tuple(self, session: AsyncSession, query: EXECUTABLE):
        """Return a single tuple from the given query. The query is expected
        to yield exactly one tuple. Raises :class:`ddd.DoesNotExist` if there
        is no tuple matched by the predicate.
        """
        result = await self.execute(session, query)
        try:
            return result.one()
        except NoResultFound:
            raise self.DoesNotExist

    async def execute(self, session: AsyncSession, query: EXECUTABLE) -> Result:
        """Execute the given `query` and return the result. Does not evaluate
        the result.
        """
        return await session.execute(query)

    async def nextval(self, session: AsyncSession, name: str) -> int:
        """Return the next value of sequence `name`."""
        result = await self.execute(session, sqlalchemy.func.nextval(name))
        return result.scalars().one()

    async def persist_declarative(self,
        session: AsyncSession,
        dao: object,
        merge: bool = False,
        flush: bool = False
    ) -> 'dao':
        """Persist a declarative SQLAlchemy object."""
        if not merge:
            session.add(dao)
        else:
            await session.merge(dao)
        if flush:
            await session.flush()
        return dao

    def begin(self) -> AsyncSession:
        """Return the :class:`sqlalchemy.ext.asyncio.AsyncSession` instance
        that is used for this repository.
        """
        return rdbms.session(self.alias)

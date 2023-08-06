"""Declares :class:`QueryRunner`."""
from .connectionmanager import session as session_factory


class QueryRunner:
    """Provides an interface to query a relational database."""
    db_alias: str = 'self'

    async def execute(self, query, scalar=False):
        """Execute `query` and return the result."""
        result = await self.session.execute(query)
        if scalar:
            result = result.scalar()
        return result

    async def __aenter__(self):
        self.session=session_factory(self.db_alias)
        return self

    async def __aexit__(self, cls, exception, traceback):
        # Note that there is no commit or rollback here, since
        # QueryRunner does not mutate data.
        await self.session.close()

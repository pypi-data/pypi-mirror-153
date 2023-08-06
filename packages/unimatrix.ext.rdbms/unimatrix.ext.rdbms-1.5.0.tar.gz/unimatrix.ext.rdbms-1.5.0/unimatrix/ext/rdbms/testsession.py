# pylint: skip-file
import contextlib

from sqlalchemy.ext.asyncio import AsyncSession


class TestSession:
    __module__ = 'unimatrix.ext.rdbms.testsession'
    __test__ = False

    def __init__(self, session):
        assert session is not None # nosec
        assert isinstance(session, AsyncSession), session # nosec
        self.__session = session
        self.__transaction = None

    @contextlib.asynccontextmanager
    async def begin(self):
        yield

    async def close(self):
        # Do nothing, since we control the closing of the
        # session.
        pass

    async def destroy(self):
        if self.__transaction is not None:
            await self.__transaction.rollback()
        await self.__session.close()
        self.__session = self.__transaction = None

    def __getattr__(self, attname):
        assert self.__session is not None # nosec
        return getattr(self.__session, attname)

    def __call__(self, *args, **kwargs):
        return self

    async def __aenter__(self):
        if not self.__transaction:
            self.__transaction = await self.__session.begin()
        return self

    async def __aexit__(self, cls, exception, traceback):
        pass

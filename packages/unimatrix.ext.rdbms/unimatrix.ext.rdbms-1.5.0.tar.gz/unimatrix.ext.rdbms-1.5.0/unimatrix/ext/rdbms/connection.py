"""Declares :class:`Connection`."""
import copy
import threading
import typing
import os

import dsnparse
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from unimatrix.conf import settings


class Connection:
    """A wrapper around :class:`databases.Database`."""
    async_schemes = {
        'mysql'     : 'mysql+aiomysql',
        'postgresql': 'postgresql+asyncpg',
        'sqlite'    : 'sqlite+aiosqlite'
    }

    @property
    def db_name(self):
        return str.lstrip(self.__opts.get('path') or '', '/') or None

    @property
    def dsn(self) -> str:
        """Return the Data Source Name (DSN) for this connection."""
        return self.__dsn.geturl()

    @property
    def engine(self) -> typing.Optional[Engine]:
        if not hasattr(self.__local, 'engine'):
            self.__local.engine = None
        return self.__local.engine

    @engine.setter
    def engine(self, value):
        self.__local.engine = value

    @property
    def session_factory(self):
        return self.__local.session_factory

    @session_factory.setter
    def session_factory(self, value):
        self.__local.session_factory = value

    def __init__(self, dsn):
        self.__local = threading.local()
        self.__local.engine = None
        self.__local.session_factory = None
        self.__dsn = dsn
        self.__opts = self.__dsn.parse(self.__dsn.geturl())
        self.__session = None

    def as_test(self):
        """Return a new instance with its connection options configured
        for testing.
        """
        return type(self)(self.__dsn.test)

    def _get_server_engine(self):
        if self.__dsn.scheme == 'sqlite':
            return
        engine = create_engine(self.__dsn.admin.geturl(), echo=True)
        session = sessionmaker(bind=engine)()
        if self.__dsn.scheme == 'postgresql':
            session.connection()\
                .connection.set_isolation_level(0)
        return session

    def create_database(self):
        """Creates the database as specified by the connection parameters."""
        session = self._get_server_engine()
        if session is not None:
            session.execute(f"CREATE DATABASE {self.db_name}")

    def drop_database(self):
        """Drops the database as specified by the connection parameters."""
        session = self._get_server_engine()
        if session is not None:
            session.execute(f"DROP DATABASE {self.db_name}")

    def begin(self):
        """Begin a transaction without any session management using the
        underlying database connection.
        """
        return self.engine.begin()

    def clone(self):
        """Clones the connection."""
        assert not self.is_connected() # nosec
        return copy.deepcopy(self)

    async def connect(self, debug: bool = False, *args, **kwargs) -> None:
        """Connect to the database server."""
        if self.engine is not None:
            raise RuntimeError("Connection already established.")
        connect_args = {}
        if self.__dsn.scheme == "postgresql":
            connect_args['timeout'] = settings.DB_TIMEOUT
        self.engine = create_async_engine(
            self.get_dsn_async(),
            connect_args=connect_args,
            echo=debug,
            pool_size=settings.DB_MAX_CONNECTIONS,
            pool_timeout=settings.DB_TIMEOUT,
            poolclass=QueuePool,
        )
        self.session_factory = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def disconnect(self, *args, **kwargs) -> None:
        """Disconnect from the database server."""
        if self.engine is None:
            return
        await self.engine.dispose()
        self.engine = None
        self.session_factory = None

    def get_session(self, *args, **kwargs) -> AsyncSession:
        """Establish a new session."""
        if self.__session is not None:
            return self.__session

        return self.session_factory(*args, **kwargs)

    def get_dsn_async(self) -> str:
        """Return a string containing the Data Source Name (DSN)
        for asynchronous connections.
        """
        return str.replace(
            self.__dsn.geturl(),
            self.__dsn.scheme,
            self.async_schemes[self.__dsn.scheme]
        )

    def is_connected(self) -> bool:
        """Return a boolean indicating if the connection
        is established.
        """
        return self.engine is not None

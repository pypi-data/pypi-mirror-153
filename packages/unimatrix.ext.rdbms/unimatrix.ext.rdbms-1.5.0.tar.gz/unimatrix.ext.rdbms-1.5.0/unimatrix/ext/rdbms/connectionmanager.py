"""Declares :class:`ConnectionManager`."""
import os

from sqlalchemy.ext.asyncio import AsyncSession
from unimatrix.lib import rdbms

from .connection import Connection


class ConnectionManager:
    """Manages the connections for an application."""
    __module__ = 'unimatrix.ext.rdbms'

    @property
    def config(self) -> dict:
        """A mapping of aliases to :class:`Connection` objects."""
        return self.__connections

    @config.setter
    def config(self, value: dict) -> dict:
        """A mapping of aliases to :class:`Connection` objects."""
        self.__connections = value

    def __init__(self, environ=None):
        self.__connections = {
            name: Connection(opts.dsn)
            for name, opts in dict.items(
                rdbms.load_config(env=environ or os.environ)
            )
        }

    def _connection_factory(self, opts: dict) -> Connection:
        opts = rdbms.load_config(opts)
        return Connection(opts['self'].dsn)

    def add(self, name: str, opts: dict) -> None:
        """Add a new connection using the given parameters"""
        self.__connections[name] = self._connection_factory(opts)

    def get(self, name: str = 'self') -> Connection:
        """Return the named connection `name`."""
        return self.__connections[name]

    async def clear(self):
        """Disconnect all databases and remove them from the internal
        registry.
        """
        await self.disconnect()
        self.__connections = {}

    async def connect(self, *args, **kwargs):
        """Connect all database connections that are specified."""
        connected = []
        for name, connection in dict.items(self.__connections):
            try:
                await connection.connect(*args, **kwargs)
                connected.append(connection)
            except Exception as e:
                for active in connected:
                    await active.disconnect()
                raise

    async def disconnect(self):
        """Disconnect all database connections that are specified."""
        for name, connection in dict.items(self.__connections):
            try:
                await connection.disconnect()
            except Exception as e:
                pass


#: The connections that could be automatically determined from the application
#: environment and predefined locations.
connections = ConnectionManager()


def get(name: str) -> Connection:
    """Return the named connection `name`."""
    return connections.get(name)


def session(name: str) -> AsyncSession:
    """Create a new :class:`sqlalchemy.ext.asyncio.AsyncSession`
    instance for the named connection `name`.
    """
    connection = get(name)
    if not connection.is_connected():
        raise RuntimeError(f"Connection '{name}' is not established.")
    return connection.get_session()

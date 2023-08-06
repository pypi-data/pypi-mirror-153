# pylint: skip-file
from .connectionmanager import connections
from .connection import Connection
from .connectionmanager import get
from .connectionmanager import session
from .connectionmanager import ConnectionManager
from .declarative import declarative_base
from .queryrunner import QueryRunner
from .repository import Repository


__all__ = [
    'Connection',
    'ConnectionManager',
    'QueryRunner',
    'Repository',
    'add',
    'connect',
    'declarative_base',
    'disconnect',
    'get',
    'session',
    'setup_databases',
]


def add(name: str, **opts) -> None:
    """Add a new connection using the given parameters"""
    connections.add(name, opts)


async def connect(*args, **kwargs) -> None:
    """Connect all database connections that are specified in the default
    connection manager.
    """
    return await connections.connect(*args, **kwargs)


async def disconnect() -> None:
    """Disconnect all database connections that are specified in the default
    connection manager.
    """
    return await connections.disconnect()

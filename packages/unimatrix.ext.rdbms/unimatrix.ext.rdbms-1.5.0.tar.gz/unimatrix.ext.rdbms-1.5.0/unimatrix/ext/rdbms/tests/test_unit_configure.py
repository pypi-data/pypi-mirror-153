# pylint: skip-file
import tempfile

from .base import BaseTestCase


class ConfigurationTestCase(BaseTestCase):

    def test_configure_sqlite(self):
        self.add_connection('self', {
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ''
        })

    def test_connect_sqlite_memory(self):
        self.add_connection('self', {
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ':memory:'
        })
        self.assertCanConnect('self')

    def test_connect_sqlite_disk(self):
        _, fn = tempfile.mkstemp()
        self.add_connection('self', {
            'DB_ENGINE': 'sqlite',
            'DB_NAME': fn
        })
        self.assertCanConnect('self')

    def test_configure_postgresql(self):
        self.add_connection('self', {
            'DB_ENGINE': 'postgresql',
            'DB_HOST': 'localhost',
            'DB_NAME': 'rdbms',
            'DB_USERNAME': 'rdbms',
            'DB_PASSWORD': 'rdbms',
            'DB_PORT': "5432"
        })

    def test_configure_mysql(self):
        self.add_connection('self', {
            'DB_ENGINE': 'mysql',
            'DB_HOST': 'localhost',
            'DB_NAME': 'rdbms',
            'DB_USERNAME': 'rdbms',
            'DB_PASSWORD': 'rdbms',
            'DB_PORT': "3306"
        })

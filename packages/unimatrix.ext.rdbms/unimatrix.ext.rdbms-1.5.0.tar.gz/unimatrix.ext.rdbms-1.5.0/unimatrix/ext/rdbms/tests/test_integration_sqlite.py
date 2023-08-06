# pylint: skip-file
import tempfile

from .base import BaseTestCase


class SQLiteConnectionTestCase(BaseTestCase):

    def test_connect_memory(self):
        self.add_connection('self', {
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ':memory:'
        })
        self.assertCanConnect('self')

    def test_connect_disk(self):
        _, fn = tempfile.mkstemp()
        self.add_connection('self', {
            'DB_ENGINE': 'sqlite',
            'DB_NAME': fn
        })
        self.assertCanConnect('self')

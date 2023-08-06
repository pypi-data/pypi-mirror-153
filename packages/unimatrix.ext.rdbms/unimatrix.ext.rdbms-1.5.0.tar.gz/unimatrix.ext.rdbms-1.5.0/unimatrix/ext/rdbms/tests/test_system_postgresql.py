# pylint: skip-file
from .base import BaseTestCase


class PostgreSQLConnectionTestCase(BaseTestCase):

    def test_connect(self):
        self.add_connection('self', {
            'DB_ENGINE': 'postgresql',
            'DB_HOST': 'localhost',
            'DB_NAME': 'rdbms',
            'DB_USERNAME': 'rdbms',
            'DB_PASSWORD': 'rdbms',
        })
        self.assertCanConnect('self')

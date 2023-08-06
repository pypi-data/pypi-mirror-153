# pylint: skip-file
import unittest

import pytest

from unimatrix.ext import rdbms


@pytest.mark.usefixtures('rdbms')
class TestDatabaseSetupTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = rdbms.get('self')
        self.db_name = self.connection.db_name

    def test_connections_are_replaced(self):
        self.assertTrue(str.startswith(self.db_name, 'test_'), self.db_name)

    def test_databases_are_created(self):
        pass

# pylint: skip-file
import asyncio
import threading

from .base import BaseTestCase



class ThreadingTestCase(BaseTestCase):

    def test_connection_is_local(self):
        self.add_connection('self', {
            'DB_ENGINE': 'sqlite',
            'DB_NAME': ':memory:'
        })
        event = threading.Event()
        done = threading.Event()
        connections = {}

        def thread_a():
            self.connect_databases()
            c = self.get_connection('self')
            connections[1] = c.is_connected()
            event.set()

        def thread_b():
            event.wait()
            c = self.get_connection('self')
            connections[2] = c.is_connected()

        t1 = threading.Thread(target=thread_a, daemon=True)
        t2 = threading.Thread(target=thread_b, daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertTrue(connections[1])
        self.assertFalse(connections[2])

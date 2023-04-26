import unittest

from src.settings.environment import Environment


class TestEnvironment(unittest.TestCase):
    def test_instanciate_environment(self):
        env = Environment()

        self.assertIsNotNone(env.DATABASE_CONNECTION_STRING)

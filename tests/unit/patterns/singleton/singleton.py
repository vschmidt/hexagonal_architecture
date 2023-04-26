import unittest

from src.patterns.singleton import Singleton


class TestSingleton(unittest.TestCase):
    def test_singleton_single_instance(self):
        class SingletonImplementation(metaclass=Singleton):
            def __init__(self, propriety):
                self.propriety = propriety

        property_name = "property_name"
        impl_instance_1 = SingletonImplementation(property_name)

        impl_instance_2 = SingletonImplementation("whatever string")

        self.assertEqual(impl_instance_1.propriety, property_name)
        self.assertEqual(impl_instance_1.propriety, impl_instance_2.propriety)

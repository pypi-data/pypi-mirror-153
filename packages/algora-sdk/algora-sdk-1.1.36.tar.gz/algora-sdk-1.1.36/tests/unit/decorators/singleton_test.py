import unittest

from algoralabs.decorators.singleton import singleton


@singleton
class Obj:
    def __init__(self):
        self.x = 0

    def add(self, i: int):
        self.x = self.x + i
        return self.x


class SingletonTest(unittest.TestCase):
    def assert_singletons_equal(self, obj1, obj2):
        self.assertEqual(id(obj1), id(obj2))
        self.assertEqual(obj1.x, obj2.x)

    def test_singleton_creation(self):
        item1 = Obj()
        item2 = Obj()
        self.assert_singletons_equal(item1, item2)

    def test_singleton_interaction(self):
        item1 = Obj()
        item2 = Obj()

        item1.add(3)
        item2.add(5)

        self.assert_singletons_equal(item1, item2)
        self.assertEqual(item1.x, 8)
        self.assertEqual(item2.x, 8)

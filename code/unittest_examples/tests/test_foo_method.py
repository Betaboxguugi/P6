import unittest


def foo(a, b, x):
    if a > 1 and b == 0:
        x = x / a
    if a == 2 or x > 1:
        x = x + 1


class TestFoo(unittest.TestCase):
    def setUp(self):
        self.a = 2
        self.b = 0
        self.x = 3

    def test_assert_first_con(self):  # found a bug! a was a < 1 when it should have been a > 1
        self.assertGreater(self.a, 1)

    def test_assert_second_con(self):
        self.assertEqual(self.b, 0)

    def test_assert_third_con(self):
        self.assertEqual(self.a, 2)

    def test_assert_fourth_con(self):
        self.assertGreater(self.x, 1)



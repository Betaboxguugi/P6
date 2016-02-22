import unittest


class TestAsserts(unittest.TestCase):

    def test_equal(self):
        a = 1
        b = 1
        self.assertEqual(a, b)

    def test_not_equal(self):
        a = 1
        b = 2
        self.assertNotEqual(a, b)

    @unittest.skip("reason")
    def test_true(self):
        self.assertTrue()

    @unittest.skip("reason")
    def test_false(self):
        self.assertFalse()

    @unittest.skip("reason")
    def test_is(self):
        self.assertIs()

    @unittest.skip("reason")
    def test_is_not(self):
        self.assertIsNot()

    @unittest.skip("reason")
    def test_is_none(self):
        self.assertIsNone()

    @unittest.skip("reason")
    def test_is_not_none(self):
        self.assertIsNotNone()

    @unittest.skip("reason")
    def test_in(self):
        self.assertIn()

    @unittest.skip("reason")
    def test_not_in(self):
        self.assertNotIn()

    @unittest.skip("reason")
    def test_is_instance(self):
        self.assertIsInstance()

    @unittest.skip("reason")
    def test_not_is_instance(self):
        self.assertNotIsInstance()

suite = unittest.TestLoader().loadTestsFromTestCase(TestAsserts)
unittest.TextTestRunner(verbosity=2).run(suite)

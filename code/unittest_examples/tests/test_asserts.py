import unittest


class TestAsserts(unittest.TestCase):

    def test_equal(self):
        a = 'equal'
        b = 'equal'
        self.assertEqual(a, b)

    def test_not_equal(self):
        a = 1
        b = 2
        self.assertNotEqual(a, b)

    def test_true(self):
        self.assertTrue(True)

    def test_false(self):
        self.assertFalse(False)

    def test_is(self):  # Can't figure out how this is different to equal
        a = 'same object?'
        b = 'same object?'
        self.assertIs(a, b)

    def test_is_not(self):
        self.assertIsNot('lol','lmao')

    def test_is_none(self):
        self.assertIsNone(None)

    def test_is_not_none(self):
        self.assertIsNotNone(9001)

    def test_in(self):
        l = (1, 2)
        self.assertIn(1, l)

    def test_not_in(self):
        l = (1, 2)
        self.assertNotIn(None, l)

    def test_is_instance(self):
        x = 1
        self.assertIsInstance(x, int)

    def test_not_is_instance(self):
        x = 1
        self.assertNotIsInstance(x, str)

    @unittest.expectedFailure
    def test_equal_fail(self):
        a = 'equal'
        b = 'Equal'
        self.assertEqual(a, b)

    @unittest.expectedFailure
    def test_not_equal_fail(self):
        a = 1
        b = 1
        self.assertNotEqual(a, b)

    @unittest.expectedFailure
    def test_true_fail(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_false_fail(self):
        self.assertFalse(True)

    @unittest.expectedFailure
    def test_is_fail(self):  # Can't figure how this is different to equal
        a = 'same object?'
        b = 'same object'
        self.assertIs(a, b)

    @unittest.expectedFailure
    def test_is_not_fail(self):
        self.assertIsNot('lol','lol')

    @unittest.expectedFailure
    def test_is_none_fail(self):
        self.assertIsNone(4237508934)

    @unittest.expectedFailure
    def test_is_not_none_fail(self):
        self.assertIsNotNone(None)

    @unittest.expectedFailure
    def test_in_fail(self):
        l = (1, 2)
        self.assertIn(3, l)

    @unittest.expectedFailure
    def test_not_in_fail(self):
        l = (1, 2)
        self.assertNotIn(1, l)

    @unittest.expectedFailure
    def test_is_instance_fail(self):
        x = 1
        self.assertIsInstance(x, float)

    @unittest.expectedFailure
    def test_not_is_instance_fail(self):
        x = 1
        self.assertNotIsInstance(x, int)

    @unittest.skip('Demonstrating an unconditional skip!')
    def test_skip(self):
        print('This will never be executed')

    @unittest.skipIf(True, "Demonstrating a conditional skip!")
    def test_skip_if(self):
        print('This will never be executed')

    @unittest.skipUnless(False, "Demonstrating an inverse conditional skip!")
    def test_skip_unless(self):
        print('This will never be executed')

suite = unittest.makeSuite(TestAsserts)
unittest.TextTestRunner(verbosity=2).run(suite)  # This is for more detailed output when running the tests from here
if __name__ == '__main__':
    unittest.main(verbosity=2)

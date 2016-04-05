import unittest


class TestAsserts(unittest.TestCase):  # By making a TestCase class like this we can run tests

    def test_equal(self):  # every test must begin with 'test_' for it to be tested
        a = 'equal'
        b = 'equal'
        self.assertEqual(a, b)  # Assert that two objects are equal, using the == operator

    def test_not_equal(self):  # Every test needs the instance of the TestCase as an input parameter
        a = 1
        b = 2
        self.assertNotEqual(a, b)  # Use self. to call TestCase functions such as assert

    def test_true(self):
        self.assertTrue(True)  # Test if true

    def test_false(self):
        self.assertFalse(False)

    def test_is(self):
        a = 'same object?'
        b = 'same object?'
        self.assertIs(a, b)  # Test if the objects are the same

    def test_is_not(self):
        self.assertIsNot(0, 0.0)  # Objects are not the same even if they evaluate to the same value

    def test_is_none(self):
        self.assertIsNone(None)

    def test_is_not_none(self):
        self.assertIsNotNone(9001)

    def test_in(self):
        l = (1, 2)
        self.assertIn(1, l)  # check if an object is part of a list

    def test_not_in(self):
        l = (1, 2)
        self.assertNotIn(None, l)

    def test_is_instance(self):  # checks if the two objects are the same type
        x = 1
        self.assertIsInstance(x, int)

    def test_not_is_instance(self):
        x = 1
        self.assertNotIsInstance(x, str)

    @unittest.expectedFailure  # This is an attribute. The test right below has this attribute.
    def test_equal_fail(self):
        a = 'equal'
        b = 'Equal'
        self.assertEqual(a, b)

    @unittest.expectedFailure  # expectedFailure means that if the test fails, it is not counted as a failed test
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

    @unittest.skip('Demonstrating an unconditional skip!')  # a test with the skip attribute is not executed
    def test_skip(self):
        print('This will never be executed')

    @unittest.skipIf(True, "Demonstrating a conditional skip!")  # skipIf is skipped if the condition is true
    def test_skip_if(self):
        print('This will never be executed')

    @unittest.skipUnless(False, "Demonstrating an inverse conditional skip!")  # skipUnless is skipped if
    def test_skip_unless(self):                                                # the condition is false
        print('This will never be executed')

suite = unittest.makeSuite(TestAsserts)          # tests can be run without any of this
unittest.TextTestRunner(verbosity=2).run(suite)  # This is for more detailed output when running the tests from here

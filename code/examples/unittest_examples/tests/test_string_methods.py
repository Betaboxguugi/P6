import unittest
from time import sleep


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')  # check that .upper() changes letters to uppercase in a string

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())  # Assert that the string is uppercase
        self.assertFalse('Foo'.isupper())  # Assert that it is not

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])  # check if s.split produces the expected result
        sleep(0.05)  # Mikael wanted to know if the timing was correct
        with self.assertRaises(TypeError):  # check that s.split fails when the separator is not a string
            s.split(2)

suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)

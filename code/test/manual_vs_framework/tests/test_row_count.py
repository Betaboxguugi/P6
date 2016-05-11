import os
import unittest
from test.manual_vs_framework import framework_row_count_test
from test.manual_vs_framework.dw import setup
from test.manual_vs_framework import TestRowCount

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

# When you change number, be sure to delete the db so a fresh one is generated.
number = 1000
path = 'row_count.db'
if not os.path.isfile('./'+path):
    setup(path, number)
suite = unittest.defaultTestLoader.loadTestsFromModule(TestRowCount)
suite = unittest.makeSuite(TestRowCount)
unittest.TextTestRunner(verbosity=2).run(suite)
framework_row_count_test(path)

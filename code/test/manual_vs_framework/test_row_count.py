import unittest
from manual_row_count import TestRowCount
from framework_row_count import framework_row_count
from dw import setup

path = 'row_count.db'

setup(path, 1000)
suite = unittest.defaultTestLoader.loadTestsFromModule(TestRowCount)
suite = unittest.makeSuite(TestRowCount)
unittest.TextTestRunner(verbosity=2).run(suite)
framework_row_count(path)

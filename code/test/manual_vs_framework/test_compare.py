from dw import setup
from framework_compare import framework_compare

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

path = 'compare.db'

setup(path, 1000)
framework_compare(path)

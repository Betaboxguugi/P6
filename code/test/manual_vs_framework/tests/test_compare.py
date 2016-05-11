import os
from test.manual_vs_framework import framework_compare_test
from test.manual_vs_framework.dw import setup
from test.manual_vs_framework import manual_compare_test

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

# When you change number, be sure to delete the db so a fresh one is generated.
# Setting number to 1000 will generate 1 million rows for comparison.
# If it scales equally with number of rows, the comparison for the framework
# would, according to my estimate, take around 50 minutes to finish
# If you're willing to wait that long for just the framework part of the test,
# be my guest. The manual test seems to be faster at least.
number = 100
path = 'compare.db'
if not os.path.isfile('./'+path):
    setup(path, number)
framework_compare_test(path, number)
manual_compare_test(path, number)
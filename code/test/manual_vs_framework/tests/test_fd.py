import os
from test.manual_vs_framework import framework_fd_test
from test.manual_vs_framework.dw import setup

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

number = 100
dbname = 'fd.db'
if not os.path.isfile('./'+dbname):
    setup(dbname, number)
framework_fd_test(dbname)

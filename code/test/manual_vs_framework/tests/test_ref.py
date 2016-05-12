import os
from test.manual_vs_framework import manual_ref_test
from test.manual_vs_framework.dw import setup
from test.manual_vs_framework import framework_ref_test


dbname = 'ref.db'

number = 100
if not os.path.isfile('./'+dbname):
    setup(dbname, number)

manual_ref_test(dbname)

framework_ref_test(dbname)

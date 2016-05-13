import os
from test.manual_vs_framework import manual_not_null_test
from test.manual_vs_framework.dw import setup
from test.manual_vs_framework import framework_not_null_test


dbname = 'not_null.db'

number = 100
if not os.path.isfile('./'+dbname):
    setup(dbname, number)

manual_not_null_test(dbname, 'ft1', ['key1', 'key2'])

framework_not_null_test(dbname)

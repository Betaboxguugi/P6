import os
from test.manual_vs_framework import manual_no_duplicates_test
from test.manual_vs_framework.dw import setup
from test.manual_vs_framework import framework_dup_test


dbname = 'dup.db'
number = 1000
if not os.path.isfile('./'+dbname):
    setup(dbname, number)

manual_no_duplicates_test(dbname, 'ft1', ['key1', 'key2'])

framework_dup_test(dbname)

import os
from test.manual_vs_framework import framework_scd_test
from test.manual_vs_framework.dw import setup_scd
from test.manual_vs_framework import manual_scd_test

dbname = 'scd.db'
number = 10000 # keep in mind that scdensure is fairly slow
if not os.path.isfile('./'+dbname):
    setup_scd(dbname, number)
framework_scd_test(dbname)
manual_scd_test(dbname, 1, 1)
manual_scd_test(dbname, 1, 2)
manual_scd_test(dbname, 2, 2)

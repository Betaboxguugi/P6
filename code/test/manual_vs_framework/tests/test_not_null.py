from test.manual_vs_framework.manual_not_null import column_not_null
from test.manual_vs_framework.framework_not_null import framework_not_null
from test.manual_vs_framework.dw import setup

path = 'row_count.db'

setup(path, 1000)

column_not_null(path, 'ft1', ['key1', 'key2'])

framework_not_null(path)

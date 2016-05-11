from test.manual_vs_framework import manual__no_duplicates
from test.manual_vs_framework.dw import setup
from test.manual_vs_framework import framework_not_null


path = 'row_count.db'

setup(path, 1000)

manual__no_duplicates(path, 'ft1', ['key1', 'key2'])

framework_not_null(path)

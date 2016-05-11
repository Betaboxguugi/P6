from manual_dup import manual__no_duplicates
from framework_dup import framework_not_null
from dw import setup

path = 'row_count.db'

setup(path, 1000)

manual__no_duplicates(path, 'ft1', ['key1', 'key2'])

framework_not_null(path)
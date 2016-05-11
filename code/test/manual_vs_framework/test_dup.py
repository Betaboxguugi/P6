from manual_dup import manual__no_duplicates
from framework_dup import framework_not_null

manual__no_duplicates('row_count.db', 'ft1', ['key1', 'key2'])

framework_not_null('row_count.db')
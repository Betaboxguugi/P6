from manual_not_null import column_not_null
from framework_not_null import framework_not_null

column_not_null('row_count.db', 'ft1', ['key1', 'key2'])

framework_not_null('row_count.db')

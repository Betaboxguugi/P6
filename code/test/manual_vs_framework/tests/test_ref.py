from test.manual_vs_framework import manual_ref
from test.manual_vs_framework.dw import setup
from test.manual_vs_framework import framework_ref


path = 'row_count.db'

#setup(path, 100)

manual_ref(path)

framework_ref(path)
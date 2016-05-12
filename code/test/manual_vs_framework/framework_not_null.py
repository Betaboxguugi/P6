from test.manual_vs_framework.dw_rep import make_dw_rep
from framework.case import Case
from framework.predicates import ColumnNotNullPredicate
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Mikael Vind Mikkelsen'


def framework_not_null_test(dbname):
    dw_rep = make_dw_rep(dbname)
    not_null = ColumnNotNullPredicate('ft1', ['key1', 'key2'])
    case = Case(dw_rep, [not_null])
    start = time.monotonic()  # the instantiations take almost no time
    case.run()
    end = time.monotonic()
    elapsed = end - start
    print('{}{}'.format(round(elapsed, 3), 's'))

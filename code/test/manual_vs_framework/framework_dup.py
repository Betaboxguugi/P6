from test.manual_vs_framework.dw_rep import make_dw_rep
from framework.case import Case
from framework.predicates import NoDuplicateRowPredicate
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Mikael Vind Mikkelsen'


def framework_dup_test(dbname):
    dw_rep = make_dw_rep(dbname)
    dup = NoDuplicateRowPredicate('ft1', ['key1', 'key2'])
    case = Case(dw_rep, [dup])
    start = time.monotonic()  # the instantiations take almost no time
    case.run()
    end = time.monotonic()
    elapsed = end - start
    print('{}{}'.format(round(elapsed, 3), 's'))

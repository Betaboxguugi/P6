from dw_rep import make_dw_rep
from framework.case import Case
from framework.predicates import RowCountPredicate
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


def framework_row_count(path):
    dw_rep = make_dw_rep(path)
    count = RowCountPredicate('ft1', 1000000)
    case = Case(dw_rep, [count])
    start = time.monotonic()  # the instantiations take almost no time
    case.run()                # but we may as well measure the time for
    end = time.monotonic()    # executing the case
    elapsed = end - start
    print('{}{}'.format(round(elapsed, 3), 's'))

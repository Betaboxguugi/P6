from dw_rep import make_dw_rep
from framework.case import Case
from framework.predicates import CompareTablePredicate
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


def framework_compare(path):
    dw_rep = make_dw_rep(path)
    table = [
        {'attr1': 100, 'attr2': 1},
        {'attr1': 99, 'attr2': 2},
        {'attr1': 2, 'attr2': 99},
        {'attr1': 1, 'attr2': 100}
    ]
    compare = CompareTablePredicate('dim1', table, ['key1'], subset=True)
    case = Case(dw_rep, [compare])
    start = time.monotonic()  # the instantiations take almost no time
    case.run()                # but we may as well measure the time for
    end = time.monotonic()    # executing the case
    elapsed = end - start
    print('{}{}'.format(round(elapsed, 3), 's'))

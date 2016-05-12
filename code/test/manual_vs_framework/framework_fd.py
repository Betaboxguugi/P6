from test.manual_vs_framework.dw_rep import make_dw_rep
from framework.case import Case
from framework.predicates import FunctionalDependencyPredicate
import time

def framework_fd_test(path):
    dw_rep = make_dw_rep(path)
    print('Running Case')
    fd = FunctionalDependencyPredicate(['ft1'], ((('key1',), ('key2',)),))
    case = Case(dw_rep, [fd])
    start = time.monotonic()
    case.run()
    end = time.monotonic()
    elapsed = end - start
    print('Done: {}{}'.format(round(elapsed, 3), 's'))
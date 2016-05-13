from test.manual_vs_framework.dw_rep import make_scd_rep
from framework.case import Case
from framework.predicates import SCDVersionPredicate
import time

def framework_scd_test(dbname):
    dw_rep = make_scd_rep(dbname)
    print('Running Case')
    scd = SCDVersionPredicate('scd', {'attr2': 1}, 1)
    case = Case(dw_rep, [scd])
    start = time.monotonic()
    case.run()
    end = time.monotonic()
    elapsed = end - start
    print('Done: {}{}'.format(round(elapsed, 3), 's'))
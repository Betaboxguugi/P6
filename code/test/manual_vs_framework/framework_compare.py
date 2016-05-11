from test.manual_vs_framework.dw_rep import make_dw_rep
from framework.case import Case
from framework.predicates import CompareTablePredicate
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


def framework_compare_test(path, number):
    dw_rep = make_dw_rep(path)
    expected_rows = []
    counter = 0
    print('Generating expected table')
    start = time.monotonic()
    for i in range(1, number + 1):
        for j in range(1, number + 1):
            counter += 10
            expected_rows.append({'key1': i, 'key2': j, 'measure': counter})

    end = time.monotonic()
    elapsed = end - start
    print('Done: {}{}'.format(round(elapsed, 3), 's'))
    print('Running Case')
    compare = CompareTablePredicate('ft1', expected_rows)
    case = Case(dw_rep, [compare])
    start = time.monotonic()
    case.run()
    end = time.monotonic()
    elapsed = end - start
    print('Done: {}{}'.format(round(elapsed, 3), 's'))

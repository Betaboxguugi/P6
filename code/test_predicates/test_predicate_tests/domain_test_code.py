import sqlite3
from test_predicates.domain_predicate import DomainPredicate
from pygrametl.datasources import SQLSource


def constraint1(a):
    if a > 26:
        return True
    else:
        return False


def constraint_true():
    return False


def constraint_true():
    return True


def test():
    print("test was invoked")


def invoker(func):
    func()

dw_name = '.\dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)
dic = dict()
dic['sales'] = SQLSource(connection=dw_conn, query="SELECT * FROM factTable")
dic['book'] = SQLSource(connection=dw_conn, query="SELECT * FROM bookDim")
dic['location'] = SQLSource(connection=dw_conn, query="SELECT * FROM locationDim")
dic['time'] = SQLSource(connection=dw_conn, query="SELECT * FROM timeDim")

constrain_tester = DomainPredicate(dic, 'sales', 'sale', constraint1)

invoker(test)

constrain_tester.run()
constrain_tester.run()

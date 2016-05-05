# Imports
import sqlite3
from framework.predicates.column_not_null_predicate import \
    ColumnNotNullPredicate
from framework.predicates.rule_row_predicate import RuleRowPredicate
from framework.predicates.no_duplicate_row_predicate import \
    NoDuplicateRowPredicate
from framework.predicates.row_count_predicate import RowCountPredicate
from framework.predicates.rule_column_predicate import RuleColumnPredicate
from framework.predicates.column_not_null_predicate import ColumnNotNullPredicate
from framework.case import Case
from framework.reinterpreter.datawarehouse_representation \
    import DWRepresentation, DimRepresentation, FTRepresentation

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

"""
table_name1 = 'company'
table_name2 = 'bompany'
column_names1 = 'age'
column_names2 = ['age', 'salary']

def constraint_function1(a):
    if a < 50:
        return True
    else:
        return False

cnnp1 = ColumnNotNullPredicate('company', 'age')
cnnp2 = ColumnNotNullPredicate('company', ['age', 'salary'])
cnnp3 = ColumnNotNullPredicate('bompany', 'salary')
cnnp4 = ColumnNotNullPredicate('bompany', ['address', 'salary'])
rp1 = RulePredicate(table_name1, constraint_function1, column_names1)
rp2 = RulePredicate(table_name1, constraint_function1, None, column_names1)
rrp1 = RuleRowPredicate(table_name1, column_names1, constraint_function1)

ukp1 = UniqueKeyPredicate(table_name1, column_names2)
ndrp1 = NoDuplicateRowPredicate(table_name1, column_names2)
ndrp2 = NoDuplicateRowPredicate(table_name1, column_names2, True)

pAll = [cnnp1, cnnp2, cnnp3, cnnp4, rp1, rp2, rrp1, ukp1, ndrp1, ndrp2]

pl = [ukp1, ndrp1, ndrp2]
"""
# Case(None, None, pl, None)

csv_name = './region.csv'
dw_name = './dw.db'  # The one found in pygrametl_examples
dw_conn = sqlite3.connect(dw_name)

query1 = "SELECT * FROM bookDim WHERE bookid < 3"
query2 = "SELECT * FROM timeDim"
query3 = "SELECT * FROM locationDim"
query4 = "SELECT * FROM factTable WHERE bookid > 1"
book_dim = DimRepresentation('bookDim', 'bookid', ['book', 'genre'], dw_conn)

time_dim = DimRepresentation('timeDim', 'timeid', ['day', 'month', 'year'],
                             dw_conn)

location_dim = DimRepresentation('locationDim', 'locationid',
                                 ['city', 'region'], dw_conn, ['city'])

facttable = FTRepresentation('factTable', ['bookid', 'locationid', 'timeid'],
                             dw_conn, ['sale'])
"""
book_dim.query = query1
time_dim.query = query2
location_dim.query = query3
facttable.query = query4
"""

dw = DWRepresentation([book_dim, time_dim, location_dim], dw_conn, [facttable])

dup_tester1 = NoDuplicateRowPredicate('bookdim', ['book', 'genre'])
dup_tester2 = NoDuplicateRowPredicate('bookdim', ['genre', 'book'])
dup_tester3 = NoDuplicateRowPredicate('bookdim', ['bookid', 'book'], True)
row_tester1 = RowCountPredicate('bookdim', 4)
row_tester2 = RowCountPredicate('bookdim', 5)


def constraint1(a, b):
    print(a)
    print(b)
    return True


def constraint2(a):
    print(a)
    return False


def constraint3(a,b,c):
    print(a, b, c)
    return True

tab_tester1 = RuleColumnPredicate('bookdim', constraint1, ['book', 'genre'], False,
                                  False)
tab_tester2 = RuleColumnPredicate('bookdim', constraint2, ['genre'], False, False)
tab_tester3 = RuleColumnPredicate('timedim', constraint1, ['day', 'month'])

nn_tester1 = ColumnNotNullPredicate('bookdim', 'genre')

nn_tester2 = ColumnNotNullPredicate('bookdim', ['genre','book'], True)

rrp_tester1 = RuleRowPredicate('bookdim', constraint3)


print(dup_tester1.run(dw))
print(dup_tester2.run(dw))
print(dup_tester3.run(dw))
print(row_tester1.run(dw))
print(row_tester1.run(dw))
print(row_tester2.run(dw))
print(tab_tester1.run(dw))
print(tab_tester2.run(dw))
print(tab_tester3.run(dw))
print(nn_tester1.run(dw))
print(nn_tester2.run(dw))
print(rrp_tester1.run(dw))
# Eksempel på brug af itercolumns taget fra ColumnNotNullPredicate før det
# viste sig at være forkert at bruge der.
"""
 for e in dw_rep.get_data_representation(self.table_name).\
         itercolumns(self.column_names):
     print(e, ' ', row_counter)
     for key, value in e.items():
         if not value:
             self.__result__ = False
             self.rows_with_null.append(row_counter)
         print(key, value)
     row_counter += 1
 """
_author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# Imports
from framework.predicates.column_not_null_predicate import ColumnNotNullPredicate
from framework.predicates.rule_row_predicate import RuleRowPredicate
from framework.predicates.rule_predicate import RulePredicate
from framework.case import Case

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


pl = [rp1]
Case(None, None, pl, None)


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
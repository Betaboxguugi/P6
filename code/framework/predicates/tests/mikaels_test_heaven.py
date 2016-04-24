__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# Imports
from framework.predicates.column_not_null_predicate import ColumnNotNullPredicate
from framework.case import Case

cnnp1 = ColumnNotNullPredicate('company', 'age')
cnnp2 = ColumnNotNullPredicate('company', ['age', 'salary'])
cnnp3 = ColumnNotNullPredicate('bompany', 'salary')
cnnp4 = ColumnNotNullPredicate('bompany', ['address', 'salary'])

pl = [cnnp1, cnnp2, cnnp3, cnnp4]
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
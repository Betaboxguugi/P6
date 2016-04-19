__author__ = 'Alexander'
from framework.case import Case
from framework.predicates import ColumnNotNullPredicate
from framework.predicates import CompareTablePredicate
from framework.reinterpreter.datawarehouse_representation import *

n = ColumnNotNullPredicate('Company', 'Name')
m = CompareTablePredicate('Company','Bompany')

Case(None,None, [n, m], True)

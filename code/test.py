__author__ = 'Alexander'
from framework.case import Case
from framework.predicates import ColumnNotNullPredicate
from framework.reinterpreter.datawarehouse_representation import *

n = ColumnNotNullPredicate('Company', 'Name')
Case(None,None, [n], True)

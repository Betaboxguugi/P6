__author__ = 'Alexander'
from framework.case import Case
from framework.predicates.not_null import NotNull
from framework.reinterpreter.datawarehouse_representation import *

n = NotNull('Company', 'Name')
Case(None,None, [n], True)

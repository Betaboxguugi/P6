__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Alexander Brandborg & Arash Michael Sami Kjær'

# Bliver vist ikke brugt from .reinterpreter.reinterpreter import *
# Nok ikke så vigtig from test_predicates import *
from .reinterpreter.reinterpreter_mock import ReinterpreterMock as Reinterpreter
#from .reinterpreter.reinterpreter import Reinterpreter


class Case:
    """
    FrameworkTestCase for running predicate tests on a pygrametl program given a set of sources
    """

    def __init__(self, program, mapping, pred_list, program_is_path):
        """
        :param program: A path or string of a pygrametl program
        :param mapping: A map of sources
        :param pred_list: A list of predicates we wish to run
        """
        self.program = program
        self.mapping = mapping
        self.pred_list = pred_list
        self.program_is_path = program_is_path

        # Sets up and runs reinterpreter getting DWRepresentation object
        tc = Reinterpreter()
        # Reinterpreter(program=self.program, conn_scope=self.mapping, program_is_path = self.program_is_path)
        self.dw_rep = tc.run()

        # Runs all predicates and reports their results
        for p in self.pred_list:
            p.run(self.dw_rep)
            report = p.report()
            report.run()

"""
def constraint1(a):
    #print(a)
    return True


def constraint2(a, b):
    #print(a, b)
    return True


def properconstraint(a, b):
    if a > 0 and b > 0:
        return True
    else:
        return False


def list_constraint(a=[]):
    if a.__getitem__(0) > 0 and a.__getitem__(1) > 0:
        # print('True')
        return True
    else:
        # print('False')
        return False

def unlimited_args(aa, *bb):
    if isinstance(aa, str) and bb > 0:
        return True
    else:
        False


def unlimited_args2(*ab):
    if ab > 0:
        return True
    else:
        return False



print(inspect.getargspec(properconstraint))
print(inspect.getargspec(unlimited_args))


column_names1 = ["salary", 'age']
column_names2 = ["name", 'salary', 'age']
domt1 = DomainTablePredicate('company', 'ADDRESS', constraint1)
domt2 = DomainTablePredicate('company', ['ADDRESS'], constraint2)
domt3 = DomainTablePredicate('company', column_names1, constraint2)
domt4 = DomainTablePredicate('company', column_names1, properconstraint)
domt5 = DomainTablePredicate('company', column_names1, list_constraint, True)


dom = DomainPredicate('company', 'ADDRESS', constraint1)
nn1 = NotNull('company', 'ADDRESS')
nn2 = NotNull('company', 'AGE')
rowp1 = RowPredicate('company', 5)
rowp2 = RowPredicate('company', 6)
hi = HierarchyPredicate(['COMPANY'], [(['ADDRESS'], ['NAME'])])
com = ComparePredicate('company', 'bompany')
uk1 = UniqueKeyPredicate('company', column_names1)
uk2 = UniqueKeyPredicate('company', column_names2)
column_names1 = ["salary", 'age']
column_names2 = ["ADDRESS"]
"""


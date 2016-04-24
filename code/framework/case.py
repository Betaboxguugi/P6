__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Alexander Brandborg & Arash Michael Sami Kjær'

# Bliver vist ikke brugt from .reinterpreter.reinterpreter import *
# Nok ikke så vigtig from test_predicates import *
# from .reinterpreter.reinterpreter_mock import ReinterpreterMock as Reinterpreter
from .reinterpreter.reinterpreter import Reinterpreter


class Case:
    """
    FrameworkTestCase for running predicate tests on a pygrametl program given
    a set of sources
    """

    def __init__(self, program, sources, dw, pred_list, program_is_path):
        """
        :param program: A path or string of a pygrametl program
        :param pred_list: A list of predicates we wish to run
        """
        self.program = program
        self.sources = sources
        self.dw = dw
        self.pred_list = pred_list
        self.program_is_path = program_is_path

        # Sets up and runs reinterpreter getting DWRepresentation object
        # tc = Reinterpreter()
        tc = Reinterpreter(program=self.program, source_conns=self.sources,
                           dw_conn=self.dw,
                           program_is_path=self.program_is_path)
        self.dw_rep = tc.run()
        print(self.dw_rep)

        # Runs all predicates and reports their results
        for p in self.pred_list:
            p.run(self.dw_rep)
            report = p.report()
            report.run()

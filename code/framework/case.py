__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Alexander Brandborg & Arash Michael Sami Kjær'

from .reinterpreter.reinterpreter import Reinterpreter


class Case:
    """
    FrameworkTestCase for running predicate tests on a pygrametl program given
    a set of sources
    """

    def __init__(self, program, sources, dw_conn, pred_list, program_is_path):
        """
        :param program: A path or string of a pygrametl program
        :type program: str
        :param sources: sources used in the pygrametl program
        :param dw_conn: A connection to a DataWarehouse
        :param pred_list: A list of predicates we wish to run
        :type pred_list: list
        :param program_is_path: Bool telling whether the program input is a
        path or not. If it's not, it's a string.
        :type program_is_path: bool
        """
        self.program = program
        self.sources = sources
        self.dw_conn = dw_conn
        self.pred_list = pred_list
        self.program_is_path = program_is_path

        # Sets up and runs reinterpreter getting DWRepresentation object
        reinterpreter = Reinterpreter(program=self.program,
                                      source_conns=self.sources,
                                      dw_conn=self.dw_conn,
                                      program_is_path=self.program_is_path)
        self.dw_rep = reinterpreter.run()
        print(self.dw_rep)

        # Runs all predicates and reports their results
        if self.pred_list:
            for p in self.pred_list:
                p.run(self.dw_rep)
                report = p.report()
                report.run()
        else:
            raise RuntimeError('No predicates given')

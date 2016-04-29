__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Mathias Claus Jensen'

from .reinterpreter.reinterpreter import Reinterpreter


class Case:
    """
    FrameworkTestCase for running predicate tests on a pygrametl program given
    a set of sources
    """

    def __init__(self, program, sources, pred_list,  pep249_module,
                 program_is_path=False, **dw_conn_params):
        """
        :param program: A path or string of a pygrametl program
        :type program: str
        :param sources: sources used in the pygrametl program
        :param pred_list: A list of predicates we wish to run
        :type pred_list: list
        :param pep249_module: Module used for connecting to the DW.
        :param program_is_path: Bool telling whether the program input is a
        path or not. If it's not, it's a string.
        :type program_is_path: bool
        :param dw_conn_params: Dict of parameters used for connecting to DW.
        """
        self.program = program
        self.sources = sources
        self.dw_con_params = dw_conn_params
        self.pep249_module = pep249_module
        self.pred_list = pred_list
        self.program_is_path = program_is_path
        self.dw_rep = None
        self.dw_conn = None

    def run(self):
        """ Reinterprets the given program with the given sources, then runs
        all the given predicates on that resulting DW.
        """
        # Sets up and runs reinterpreter getting DWRepresentation object
        reinterpreter = Reinterpreter(program=self.program,
                                      source_conns=self.sources,
                                      program_is_path=self.program_is_path,
                                      pep249_module=self.pep249_module,
                                      dw_conn_params=self.dw_con_params)
        self.dw_rep, self.dw_conn = reinterpreter.run()

        # Runs all the predicates and saves the reports
        reports = []
        for p in self.pred_list:
            r = p.run(self.dw_rep)
            reports.append(r)

        # For debugging purposes, replace with some CL GUI stuff, maybe :D
        for r in reports:
            print(r)

        self.dw_conn.close()



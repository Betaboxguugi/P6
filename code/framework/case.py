from .reinterpreter.reinterpreter import Reinterpreter
from .reinterpreter.representation_maker import RepresentationMaker
import ast

__author__ = 'Alexander Brandborg & Arash Michael Sami Kjær'
__maintainer__ = 'Mathias Claus Jensen'


class Case:
    """
    FrameworkTestCase for running predicate tests on a pygrametl program given
    a set of sources
    """
    def __init__(self, program, pred_list,  pep249_module,
                 program_is_path=False, replace=False, sources=(),
                 **dw_conn_params):
        """
        :param program: A path or string of a pygrametl program
        :type program: str
        :param pred_list: A list of predicates we wish to run
        :type pred_list: list
        :param pep249_module: Module used for connecting to the DW.
        :param sources: sources used in the pygrametl program
        :param program_is_path: Bool telling whether the program input is a
        path or not. If it's not, it's a string.
        :type program_is_path: bool
        :param replace: Bool telling whether connections in program input
        should be replaced.
        :type replace: bool
        :param dw_conn_params: Dict of parameters used for connecting to DW.
        """

        if not replace and sources:
                raise RuntimeError('Sources should not be given,'
                                   ' when not replacing connections ')

        if program_is_path:
            try:
                with open(program, 'r') as f:
                    self.program = f.read()
            except:
                raise RuntimeError('pygrametl program not found at location')
        else:
            self.program = program

        self.sources = sources
        self.pred_list = pred_list
        self.pep249_module = pep249_module
        self.dw_conn_params = dw_conn_params
        self.replace = replace
        self.scope = {}
        self.dw_rep = None
        self.dw_conn = None

    def _execute_program(self):
        """
         Executes the pygrametl program.
         May replace connections in the program depending on the replace flag.
         :return dw_conn: PEP249 connection object to the DW
         :return scope: Local scope of the program after execution
         """

        if self.replace:
            # Replaces connections in pygrametl program
            dw_conn = self.pep249_module.connect(**self.dw_conn_params)
            reinterpreter = Reinterpreter(program=self.program,
                                          source_conns=self.sources,
                                          dw_conn=dw_conn)
            scope = reinterpreter.run()
            dw_conn.close()

        else:
            # Runs pygrametl program without replacing connections
            tree = ast.parse(self.program)
            p = compile(source=tree, filename='<string>', mode='exec')
            scope = {}
            exec(p, scope)

        # Reestablishes contact to the DW
        dw_conn = self.pep249_module.connect(**self.dw_conn_params)
        return dw_conn, scope

    def run(self):
        """ Reinterprets the given program with the given sources, then runs
        all the given predicates on that resulting DW.
        """
        self.dw_conn, self.scope = self._execute_program()

        # Creates the DWRepresentation with the transformed scope
        rep_maker = RepresentationMaker(dw_conn=self.dw_conn, scope=self.scope)
        self.dw_rep = rep_maker.run()
        print(self.dw_rep)

        # Executes predicates
        p_exe = PredicateExecuter(self.pred_list, self.dw_rep)
        p_exe.run()


class PredicateExecuter:
    def __init__(self, pred_list, dw_rep):
        """
        Executes predicates upon a DWRepresentation associated with a DW
        :param pred_list: list of predicates
        :param dw_rep: object representing a DW
        """
        self.pred_list = pred_list
        self.dw_rep = dw_rep

    def run(self):
        # Runs all the predicates and saves the reports
        reports = []
        for p in self.pred_list:
            r = p.run(self.dw_rep)
            reports.append(r)

        # For debugging purposes, replace with some CL GUI stuff, maybe :D
        for r in reports:
            print(r)

        self.dw_rep.connection.close()

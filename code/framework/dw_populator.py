from .reinterpreter.reinterpreter import Reinterpreter
from .reinterpreter.representation_maker import RepresentationMaker
from pygrametl import ConnectionWrapper
import ast

__author__ = 'Alexander Brandborg & Arash Michael Sami Kjr'
__maintainer__ = 'Mathias Claus Jensen'


class DWPopulator:
    """
    FrameworkTestCase for running predicate tests on a pygrametl program given
    a set of sources
    """
    def __init__(self, program,  pep249_module,
                 program_is_path=False, replace=False, sources=(),
                 **dw_conn_params):
        """
        :param program: A path or string of a pygrametl program
        :type program: str
        :param pep249_module: Module used for connecting to the DW
        :param sources: sources used in the pygrametl program
        :param program_is_path: Indicates whether the program input is a
        path or not.
        :type program_is_path: bool
        :param replace: Indicates whether connections in program input
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
            # The program must close the connection
            tree = ast.parse(self.program)
            p = compile(source=tree, filename='<string>', mode='exec')
            scope = {}
            exec(p, scope)

            # Closes connections to all DWs
            for x, value in scope.items():
                if isinstance(value, ConnectionWrapper):
                   scope[x].close()

        # Reestablishes contact to the DW
        dw_conn = self.pep249_module.connect(**self.dw_conn_params)
        return dw_conn, scope

    def run(self):
        """
        Runs the given program, then creates a representation of it.
        :return DWRepresentation of the DW used in the pygrametl program.
        """
        self.dw_conn, self.scope = self._execute_program()

        # Creates the DWRepresentation with the transformed scope
        rep_maker = RepresentationMaker(dw_conn=self.dw_conn, scope=self.scope)
        self.dw_rep = rep_maker.run()

        return self.dw_rep

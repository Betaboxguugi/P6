import ast
from .transform_visitor import TransformVisitor
from .representation_maker import RepresentationMaker

__author__ = 'Mathias Claus Jensen'
__all__ = ['Reinterpreter']


class Reinterpreter(object):
    """ Class in charge of reinterpreting a pygrametl program, using different
    connections.
    """

    def __init__(self, program, source_conns, dw_conn, program_is_path=False):
        """ 
        :param program: A string containing the program that is to be 
        reinterpreted or a path to it.
        :type program: str
        :param source_conns: A dictionary of string:connection pairs. Used to
        specify which connections should be used in the program. The dictionary
        must be ordered in the occurrence of use in the program, and there has
        to be as many connections in the dictionary as there are used in the
        program
        :param dw_conn: A connection to a DataWarehouse
        :param program_is_path: Boolean that specifies if the program string is 
        the actual program or a path to a file containing the program.
        """

        self.program = program
        self.dw_conn = dw_conn
        self.conn_scope = source_conns
        self.program_is_path = program_is_path
        self.source_ids = []

        # Generates id names for sources and DW,
        # zipping names an replacement objects into a dictionary,
        # which is later used as a scope.
        self.dw_id = '__0__'
        self.scope = {self.dw_id: self.dw_conn}
        counter = 0

        for entry in source_conns:
            source_id = "__" + str(source_conns.index(entry) + 1) + "__"
            self.source_ids.append(source_id)
            source = self.conn_scope.__getitem__(counter)
            self.scope[source_id] = source
            counter += 1

    def __transform(self, node):
        """
        :param node: an ast node that is the root of the node tree
        Swaps out the connections in the old program, with the ones given.
        """
        tv = TransformVisitor(self.source_ids, self.dw_id)
        tv.start(node)

        if not tv.dw_flag:
            raise RuntimeError('No ConnectionWrapper instantiated in' +
                               ' pygrametl program')
        elif tv.counter < len(self.source_ids):
            raise RuntimeError('Too many sources have been given')

    def run(self):
        """
        Reinterpretes the pygrametl program, returns a DWRepresentation
        :return: DWRepresentation of dw from the given program
        """
        #  Retrieves the program as a string or path
        if self.program_is_path:
            try:
                with open(self.program, 'r') as f:
                    program = f.read()
            except:
                raise RuntimeError('pygrametl program not found at location')
        else:
            program = self.program

        tree = ast.parse(program)  # Parsing the pygrametl program to an AST

        # Transforming the AST to include the user defined connections
        self.__transform(tree)

        # Executing the transformed AST
        p = compile(source=tree, filename='<string>', mode='exec')
        exec(p, None, self.scope)

        # Creates the DWRepresentation with the transformed scope
        rep_maker = RepresentationMaker(dw_conn=self.dw_conn, scope=self.scope)
        dw_rep = rep_maker.run()

        return dw_rep

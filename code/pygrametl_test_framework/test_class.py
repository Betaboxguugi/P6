""" This moduleholds the TestClass class
"""

import ast
from visitors import ModifyVisitor


__author__ = 'Mathias Claus Jensen'
__all__ = ['TestClass']


# CONSTANTS
BASE_SOURCES = []
AGGREGATED_SOURCES = []
DIM_CLASSES = []
FT_CLASSES = []


class TestClass(object):
    """ TestClass object, used for testing a pygrametl program_path with the given
    sources. It tests whether the given predicates are true or not.
    """
    def __init__(self, program_path, predicates, conn_map=None):
        """
        :param program_path: The pygrametl program_path that will be tested.
        :param predicates: The predicates we will test for.
        :param conn_map: A dictionary that maps variable names to connection
        objects, e.g., {'conn1': conn1, 'conn2': conn2}. This is used to specify
        which source and wrappers will have their connections changed. This dict
        should be orderede by the occurences of said source or wrapper 
        instantiations. An entry can be None, if you wish not to change the
        connection. E.g. {'conn1': conn1, 'conn2': None, 'conn3': conn3}, in
        this case the second source or wrapper object that occurs in the
        pygrametl program_path will not changed. Defaults to None.
        """
        self.conn_map = conn_map
        self.program_path = program_path

        
    def __modify_program(self):
        """ We make an AST of the program code and then we call the use the
        ModifyVisitor on it.
        :return: The modified AST
        """
        with open(self.program_path, 'r') as f:
            program = f.read()
        mv = ModifyVisitor(self.conn_map)
        tree = ast.parse(program)
        mv.visit(tree)
        return tree

    
    def run(self):
        """ We modify the program to use the user specified sources, then run
        the modified program, and tests to see if our predicates hold true on
        the resulting DBs.
        """
        tree = self.__modify_program()
        p = compile(source=tree, filename=self.program_path, mode='exec')
        scope = globals().update(self.conn_map)
        exec(p, scope)
        # TODO: Load the now populated dbs data in.
        # TODO: Run predicates on the loaded data.
        # TODO: Report Errors in a nice way :0)
    



        
            
            
            
        

    
        

    

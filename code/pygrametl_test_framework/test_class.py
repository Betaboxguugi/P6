""" This moduleholds the TestClass class
"""

import ast
from visitors import ModifyVisitor, ExtractVisitor


__author__ = 'Mathias Claus Jensen'
__all__ = ['TestClass']


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
        self._no_aggr_srcs = True

        
    def __modify_program(self):
        """ We make an AST of the program code and then we call the use the
        ModifyVisitor on it.
        :return: The modified AST
        """
        with open(self.program_path, 'r') as f:
            program = f.read()
        mv = ModifyVisitor(self.conn_map)
        tree = ast.parse(program)
        mv.start(tree) # We start visiting the root of the tree
        return tree

    def __make_assign_nodes(self, expr_list):
        """ Make a list of assign nodes, each within its own module, from a
        list of expression nodes. Each assign will assign to the variable name
        src<i>, where <i> is a number we increment for each expression in the
        expression list
        :param expr_list: A list of Expr node
        :return: A list of modules, each containing one Assign Node in their
        body. 
        """
        # We make the assign list
        assign_list = []
        i = 0
        for node in expr_list:
            assign = ast.Assign(targets=[ast.Name(id='src' + str(i),
                                                  ctx=ast.Store())],
                                value=node)
            assign_list.append(assign)
            i += 1
            
        # We make the Module list
        module_list = []
        for a in assign_list: # Maybe put all the assigns into one module instead
            module_node = ast.Module(lineno=1, col_offset=0, body=[a])
            ast.fix_missing_locations(module_node)
            module_list.append(module_node)
        return module_list 
            
    
    def __get_src_call_nodes(self, node):
        """ Gets all the needed src call nodes from a node.
        :param node: The node from which we will find/make all the Call nodes.
        :return: A list of modules, each containing one assign node.
        """
        ev = ExtractVisitor()
        atom_srcs, aggr_srcs, dim_srcs, ft_srcs = ev.start(node)
        src_list = atom_srcs + aggr_srcs + dim_srcs + ft_srcs
        module_list = self.__make_assign_nodes(src_list)
        
        if len(aggr_srcs) == 0: # If we dont have any aggregated src nodes
            self._no_aggr_srcs = True
        else:
            self._no_aggr_srcs = False
    
        return module_list
        

    def run(self):
        """ We modify the program to use the user specified sources, then run
        the modified program, and tests to see if our predicates hold true on
        the resulting DBs.
        """
        scope = self.conn_map.copy()
        
        # We modify and run the pygrametl program
        # TODO: Dont close() connections
        tree = self.__modify_program()
        p1 = compile(source=tree, filename=self.program_path, mode='exec')
        exec(p1, None, scope)

        # We get the needed src objects and reload the data
        module_list = self.__get_src_call_nodes(tree)
        for module in module_list:
            p2 = compile(source=module, filename='<string>', mode='exec')
            exec(p2, None, scope)

        # TODO: Take our newly found sources and order them
        # Distinguish between input srcs and dw srcs.
        # Maybe between fts and dims aswell.
        # Find some logic for how to handle aggregated srcs

        # TODO: Feed the sources to some predicates

        # TODO: Report errors

        # TODO: Close connections

        return scope # For Debugging





        
            
            
            
        

    
        

    

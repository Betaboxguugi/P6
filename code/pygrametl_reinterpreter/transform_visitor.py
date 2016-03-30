import ast

__author__ = 'Mathias Claus Jensen'
__maintainer__ = 'Mathias Claus Jensen'
__all__ = ['TransformVisitor']

ATOMIC_SOURCES = ['SQLSource', 'CSVSource']
AGGREGATED_SOURCES = ['JoiningSource']
WRAPPERS = ['ConnectionWrapper']
DIM_CLASSES = ['Dimension']
FT_CLASSES = ['FactTable']
MODIFY_LIST = ATOMIC_SOURCES + WRAPPERS

class TransformVisitor(ast.NodeVisitor):
    """ Class responsible for making changes to an AST so that it can be run with
    specific connections
    """
    def __init__(self, conn_scope):
        """
        :param conn_scope: A dictionary of the connections that will replace the 
        ones already found in the pygrametl program.
        """
        self.conn_scope = conn_scope
        self._counter = 0

        
    def __get_id(self):
        """ Iterates through the keys of the conn_dict.
        """
        key_list = [key for key in self.conn_scope.keys()]
        if self._counter == len(key_list):
            raise StopIteration('There are no more mappings to use')
        else:
            id = key_list[self._counter]
            self._counter += 1
            return id
        
        
    def __replace_connection(self, node):
        """ Replaces a connection in the given node with use specified ones.
        :param node: The node for which a connection will be replaced.
        """
        id = self.__get_id()
        newode = ast.Name(id=id, ctx=ast.Load())
        if len(node.args) != 0:    # Conn given as positional arg
            node.args[0] = newode
        else:                      # Conn given by keyword
            for keyword in node.keywords:
                if keyword.arg == 'connection':
                    keyword.value = newode
        ast.fix_missing_locations(node)   
        
        
    def __find_call_name(self, node):
        """ Function that finds the name of a call node
        :param node: The call node, whoms name we will find.
        :return: The name of the call node
        """
        name = None
        if hasattr(node.func, 'id'):       # SQLSource() type call
            name = node.func.id
        elif hasattr(node.func, 'attr'): # pygrametl.SQLSource() type call
            name = node.func.attr
        else:
            raise NotImplementedError('Cannot get the name of ' + str(node))
        return name

        
    def visit_Call(self, node):
        """ The visit of a call node
        :param node: A call node
        """
        name = self.__find_call_name(node)
        if name in MODIFY_LIST:
            self.__replace_connection(node)

        
    def start(self, node):
        """ We start the visitor.
        :param node: the root of an AST.
        """
        self._counter = 0
        self.visit(node)

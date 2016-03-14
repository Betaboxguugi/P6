""" This module holds the Visitor classes used for performing operations based
on ASTs of pygrametl programs.
"""

import ast


__author__ = 'Mathias Claus Jensen'
__all__ = ['ModifyVisitor']


# CONSTANTS
BASE_SOURCES = ['SQLSource', 'CSVSource']
AGGREGATED_SOURCES = ['JoiningSource']
DIM_CLASSES = ['Dimension']
FT_CLASSES = ['FactTable']
WRAPPERS = ['ConnectionWrapper']
WANTED_LIST = BASE_SOURCES + WRAPPERS


class ModifyVisitor(ast.NodeVisitor):
    """ A visitor class that derives from the standard NodeVisitor class from 
    the ast python package. This class formats the AST of a pygrametl program to
    to use user specified connections.
    """
    def __init__(self, conn_map):
        """ We setup the ModifyVisitor object.
        :param conn_map: A dictionary that maps variable names to connection
        objects, e.g., {'conn1': conn1, 'conn2': conn2}. This is used to specify
        which source and wrappers will have their connections changed. This dict
        should be orderede by the occurences of said source or wrapper 
        instantiations. An entry can be None, if you wish not to change the
        connection. E.g. {'conn1': conn1, 'conn2': None, 'conn3': conn3}, in
        this case the second source or wrapper object that occurs in the
        pygrametl program will not changed. 
        """
        self.conn_map = conn_map
        self.__counter = 0
        if self.conn_map is not None:
            self.__conn_len = len(conn_map)

    def __get_id(self):
        """ Iterates through the keys of the conn_dict.
        """
        key_list = [key for key in self.conn_map.keys()]
        id = key_list[self.__counter]
        if self.__counter == self.__conn_len:
            raise StopIteration('There are no more mappings to use')
        else:
            self.__counter += 1
        return id

        
    def __replace_connection(self, node):
        """ Replaces a connection in the given node with use specified ones. If 
        a connection maps to none, we dont do anything.
        :param node: The node for which a connection will be replaced.
        """
        id = self.__get_id()
        if self.conn_map[id] is not None:
            newode = ast.Name(id=id, ctx=ast.Load())
            if len(node.args) != 0:    # Conn given as positional arg
                node.args[0] = newode
            else:                      # Conn given by keyword
                for keyword in node.keywords:
                    if keyword.arg == 'connection':
                        keyword.value = newode
            ast.fix_missing_locations(node) 

                        
    def visit_Call(self, node):
        """ The visit call of a Call node. We find the name of the call and if
        it matches with any in our WANTED_LIST we call __replace_connection on
        the node. If self.conn_map is None we do nothing.
        :param node: The node we're visiting
        """
        if self.conn_map is not None:
            name = None
            if hasattr(node.func, 'id'):       # SQLSource() type calls
                name = node.func.id
            else:
                if hasattr(node.func, 'attr'): # pygrametl.SQLSource() type calls
                    name = node.func.attr
            if name in WANTED_LIST:
                self.__replace_connection(node)

            
        

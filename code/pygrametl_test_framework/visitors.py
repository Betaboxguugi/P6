""" This module holds the Visitor classes used for performing operations based
on ASTs of pygrametl programs.
"""

import ast


__author__ = 'Mathias Claus Jensen'
__all__ = ['ModifyVisitor', 'ExtractVisitor']


# CONSTANTS
ATOMIC_SOURCES = ['SQLSource', 'CSVSource']
AGGREGATED_SOURCES = ['JoiningSource']
WRAPPERS = ['ConnectionWrapper']
DIM_CLASSES = ['Dimension']
FT_CLASSES = ['FactTable']
MODIFY_LIST = ATOMIC_SOURCES + WRAPPERS



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
        """ Replaces a connection in the given node with use specified ones.
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
            ast.fix_missing_locations(node) # Fixes Indenting and line numbers
       

            
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
        """ The visit call of a Call node. We find the name of the call and if
        it matches with any in our MODIFY_LIST we call __replace_connection on
        the node. If self.conn_map is None we do nothing.
        :param node: The node we're visiting
        """
        name = self.__find_call_name(node)           
        if self.conn_map is not None:
            if name in MODIFY_LIST:
                self.__replace_connection(node)

            
    def start(self, node):
        """ Starts the visitor at the given node, resets the counter.
        :param node: The node we start visiting at.
        """
        self.__counter = 0
        self.visit(node)


       
class ExtractVisitor(ast.NodeVisitor):
    """ Visitor in charge of extracting different nodes that will later be used
    to reread the data from the different DBs.
    """
    def __init__(self):
        """ We set up a set of list for manipulating and storing nodes of 
        interest. Only supports a single wrapper per program.
        """
        self.atom_srcs = []
        self.aggr_srcs = []
        self.wrapper = None
        self.dims = []
        self.fts = []
        self.dim_srcs = []
        self.ft_srcs = []


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


    def __pluck_wrapper_conn(self, wrapper_node):
        """ Takes a wrapper node and returns its connection node
        :param wrapper_node: The wrapper node whoms connections will be returned.
        :return: A connection node
        """
        conn = None
        if len(wrapper_node.args) != 0:    # Conn given as positional arg
            conn = wrapper_node.args[0] 
        else:                              # Conn given by keyword
            for keyword in wrapper_node.keywords:
                if keyword.arg == 'connection':
                    conn = keyword.value
        if conn is None:
            raise ValueError('Could not find a connection in wrapper')
        return conn


    def __find_table_name(self, node):
        """ Finds the name of the table in the given call node.
        :param node: A call node containing a table instantiation. 
        :return: The name of the table
        """
        name = None
        if len(node.args) != 0:    # Positional arg
            name = node.args[0].s
        else:                      # Keyword arg
            for keyword in node.keywords:
                if keyword.arg == 'name':
                    name = keyword.value.s
        if name is None:
            raise ValueError('Could not find the name of the table')
        return name
                    
    
    def __make_table_query(self, node):
        """ Makes a query string out of a ft/dim node.
        :param node: The ft/dim node we will make a query string from.
        :return: An SQL query string.
        """
        return 'SELECT * FROM ' + self.__find_table_name(node)        
        
    
    def __make_src_from_table(self, node):
        """ Makes a Call node of a SQLSource instantiation from a Call node
        containing a table instantiation. The SQLSource Call node will read 
        from the wrappers connection and read everything from the table with 
        the same name as the given Table Call node
        :param node: A Call node containing a table instantiation.
        :return: A Call node containing a SQLSource instantiation.
        """
        conn_node = self.__pluck_wrapper_conn(self.wrapper) # Why do it here?
        query = self.__make_table_query(node)
        src_node = ast.Call(func=ast.Name(id='SQLSource', ctx=ast.Load()),
                            args=[conn_node, ast.Str(s=query)], keywords=[])
        return src_node   
       
        
    def visit_Call(self, node):
        """ The function that is run every time we visit a Call node. It makes
        saves all of the nodes of interest to lists.
        :param node: The Call we're visiting.
        """
        name = self.__find_call_name(node)
        if name in ATOMIC_SOURCES:
            self.atom_srcs.append(node)
        elif name in AGGREGATED_SOURCES:
            self.aggr_srcs.append(node)
        elif name in WRAPPERS:
            self.wrapper = node
        elif name in DIM_CLASSES:
            self.dims.append(node)
        elif name in FT_CLASSES:
            self.fts.append(node)

            
    def start(self, node):
        """ Starts the visitor and makes the dim/ft src objects.
        :param node: The node the visitor starts at. Should be a Module Node
        :return: The lists of sources found in the given node.
        """
        self.visit(node)
        if self.wrapper is None:
            raise ValueError('No wrapper was found in the program')

        # We make src call nodes for each dim and ft node
        for node in self.dims: 
            src_node = self.__make_src_from_table(node)
            self.dim_srcs.append(src_node)
        for node in self.fts:
            src_node = self.__make_src_from_table(node)
            self.ft_srcs.append(src_node)
            
        return (self.atom_srcs.copy(), self.aggr_srcs.copy(),
                self.dim_srcs.copy(), self.ft_srcs.copy())
        
        

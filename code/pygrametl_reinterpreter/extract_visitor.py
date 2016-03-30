from ast import *

__author__ = 'Mathias Claus Jensen'
__Maintainer__ = 'Mathias Claus Jensen'
__all__ = ['ExtractVisitor']

ATOMIC_SOURCES = ['SQLSource', 'CSVSource']
AGGREGATED_SOURCES = ['JoiningSource']
WRAPPERS = ['ConnectionWrapper']
DIM_CLASSES = ['Dimension']
FT_CLASSES = ['FactTable']
MODIFY_LIST = ATOMIC_SOURCES + WRAPPERS


class ExtractVisitor(NodeVisitor):
    """ Class that creates AST nodes representing datasource objects for each 
    dimension and facttable given in a root node.
    """

    def __init__(self, result_varname):
        """
        :param result_varname: The name we give the module that is returned
        by the start function.
        """
        if isinstance(result_varname, str):
            self.result_varname = result_varname
        else:
            raise TypeError('Expected' + str(type('')) + ', recieved ' +
                            str(type(result_varname)))
        self.dims = []
        self.fts = []
        self.dim_srcs = {}
        self.ft_srcs = {}
        self.wrapper_conn = None

    def __pluck_wrapper_conn(self, wrapper_node):
        """ Takes a wrapper node and returns its connection node
        :param wrapper_node: The wrapper node whoms connections will be returned.
        :return: A connection node
        """
        conn = None
        if len(wrapper_node.args) != 0:  # Conn given as positional arg
            conn = wrapper_node.args[0]
        else:  # Conn given by keyword i.e. "Connection = x"
            for keyword in wrapper_node.keywords:
                if keyword.arg == 'connection':
                    conn = keyword.value
        if conn is None:
            raise ValueError('Could not find a connection in wrapper')
        return conn

    def __find_call_name(self, node):
        """ Function that finds the name of a call node
        :param node: The call node, who's name we will find.
        :return: The name of the call node
        """
        name = None
        if hasattr(node.func, 'id'):  # SQLSource() type call
            name = node.func.id
        elif hasattr(node.func, 'attr'):  # pygrametl.SQLSource() type call. Occurs when we don't import with "From".
            name = node.func.attr
        else:
            raise NotImplementedError('Cannot get the name of ' + str(node))
        return name

    def __find_table_name(self, node):
        """ Finds the name of the table in the given call node.
        :param node: A call node containing a table instantiation. 
        :return: The name of the table
        """
        name = None
        if len(node.args) != 0:  # Positional arg
            name = node.args[0].s
        else:  # Keyword arg i.e. "name = x"
            for keyword in node.keywords:
                if keyword.arg == 'name':
                    name = keyword.value.s
        if name is None:
            raise ValueError('Could not find the name of the table')
        return name

    def visit_Call(self, node):
        """ The function that is run every time we visit a Call node.
        It saves all of the nodes of interest to lists.
        :param node: The Call we're visiting.
        """
        name = self.__find_call_name(node)
        if name in DIM_CLASSES:
            self.dims.append(node)
        elif name in FT_CLASSES:
            self.fts.append(node)
        elif name in WRAPPERS:
            self.wrapper_conn = self.__pluck_wrapper_conn(node) # Returns connection within wrapper

    def make_dict_assign(self, dictionary):
        """ Makes a module node that represents an assign of a dictionary that
        contains every dimension/facttable datasource
        :param dictionary: A dictionary of name:node pairs. where the name is 
        the name of a table and node is an AST node representing the datasource
        for that table.
        :return: A module node
        """
        assign_list = []
        key_list = []
        for key, value in dictionary.items():
            key_node = Str(s=key)
            key_list.append(key_node)
            assign_list.append(value)

        dict_node = Dict(keys=key_list, values=assign_list)

        # Create Assignment node that assigns the dictionary of DW tables to result_varname
        # result_varname is an extension of the AST's scope, and is later returned from the reinterpreter
        dict_assign = Assign(targets=[Name(id=self.result_varname, ctx=Store())],
                             value=dict_node)

        #Instantiation of module
        module = Module(lineno=1, col_offset=0, body=[dict_assign])

        # Call to fill in line number and indentation information for the new module and its children.
        fix_missing_locations(module)
        return module

    def make_src(self, node):
        """ Makes a node that represents a datasource instantiation of a table 
        found in the given node
        :param node: A node representing a table instantiation
        :return 0: The name of the table found in the node 
        :return 1: The node representing the datasource for this table.
        """
        table_name = self.__find_table_name(node)
        query = 'SELECT * FROM ' + table_name  # TODO: Dont use *
        src_node = Call(func=Name(id='SQLSource', ctx=Load()),
                        args=[self.wrapper_conn, Str(s=query)],
                        keywords=[])
        return table_name, src_node

    def start(self, node):
        """ Makes the AST nodes necessary for extracting data from dimensions
        and facttables.
        :param node: The root of an AST
        :return: A node representing an assign of a dictionary containing all the 
        datasources
        """
        # Walks through the AST and appends all dimension and fact table nodes to lists
        self.visit(node)

        # For testing to be possible we need a DW to connect to
        if self.wrapper_conn is None:
            raise ValueError('No wrapper found in the program')

        # Creates (name, node) pairs for each dimnesion and fact table
        for dim_node in self.dims:
            name, src_node = self.make_src(dim_node)
            self.dim_srcs.update({name: src_node})

        for dim_node in self.fts:
            name, src_node = self.make_src(dim_node)
            self.dim_srcs.update({name: src_node})

        temp = {}
        temp.update(self.dim_srcs)
        temp.update(self.ft_srcs)

        # Makes a new ast out of the collected nodes
        result = self.make_dict_assign(temp)

        return result

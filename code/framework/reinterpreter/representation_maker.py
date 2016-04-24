__author__ = 'Alexander'
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

from .datawarehouse_representation import DWRepresentation, DimRepresentation, FTRepresentation


class RepresentationMaker(NodeVisitor):
    """ Class that creates AST nodes representing datasource objects for each
    dimension and facttable given in a root node.
    """
    def __init__(self, dw_conn):
        """
        :param result_varname: The name we give the dictionary that is returned
        by the start function.
        """
        self.dw_conn = dw_conn


        # Contains nodes instantiating dimensions and fact tables
        self.dims = []
        self.fts = []

        # Contains representations of dimension and fact table
        self.dim_reps = []
        self.fts_reps = []



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
        """ The function that is run every time we visit a Call node. It makes
        saves all of the nodes of interest to lists.
        :param node: The Call we're visiting.
        """
        name = self.__find_call_name(node)
        if name in DIM_CLASSES:
            self.dims.append(node)
        elif name in FT_CLASSES:
            self.fts.append(node)

    def node_to_dimrep(self, node):

        if len(node.args) != 0:    # Positional arg
            name = node.args[0].s
            key = node.args[1].s
            att = []
            for e in node.args[2]:
                att.append(e.s)

            if 3 < len(node.args):
                look = []
                for e in node.args[3]:
                    look.append(e.s)
                res = DimRepresentation(name,key,att,self.dw_conn,look)
            else:
                res = DimRepresentation(name,key,att,self.dw_conn)

        else:  # Keyword arg

            keyword_dict = {}
            for keyword in node.keywords:
                keyword_dict[keyword.arg] = keyword


            name = keyword_dict['name'].value.s
            key = keyword_dict['key'].value.s
            att = []
            for e in keyword_dict['attributes']:
                att.append(e.value)
            if 'lookupatts' in keyword_dict.keys():
                look = []
                for e in keyword_dict['lookupatts']:
                    look.append(e.value)
                res = DimRepresentation(name,key,att,self.dw_conn,look)
            else:
                res = DimRepresentation(name,key,att,self.dw_conn)

        return res

    def node_to_fact(self, node):
        if len(node.args) != 0: # Positional arg:
            name = node.args[0].s
            refs = []
            for entry in node.args[1]:
                refs.append(entry)

            if 2 < len(node.args):
                mes = []
                for entry in node.args[2]:
                    mes.append(entry)
                res = FTRepresentation(name, refs,mes,self.dw_conn)
            else:
                res = FTRepresentation(name, refs,self.dw_conn)

        else: # Keyword arg
            keyword_dict = {}
            for keyword in node.keywords:
                keyword_dict[keyword.arg] = keyword

            name = keyword_dict['name'].value.s
            refs = []
            for entry in keyword_dict['keyrefs']:
                refs.append(entry.value.s)
            if 'measure' in keyword_dict.keys():
                mes = []
                for entry in keyword_dict['measure']:
                    mes.append(entry.value.s)
                res = FTRepresentation(name, refs,mes,self.dw_conn)
            else:
                res = FTRepresentation(name, refs,self.dw_conn)

        return res



    def start(self, node):
        self.visit(node)

        for node in self.dims:
            self.dim_reps.append(self.node_to_dimrep(node))

        for node in self.fts:
            self.fts_reps.append(self.node_to_fact(node))

        res = DWRepresentation(self.dim_reps, self.fts_reps, self.dw_conn)

        return res

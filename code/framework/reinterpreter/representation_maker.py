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

from .datawarehouse_representation import DWRepresentation,\
    DimRepresentation, FTRepresentation

from pygrametl.tables import Dimension, FactTable

class RepresentationMaker():
    """ Class that creates AST nodes representing datasource objects for each
    dimension and facttable given in a root node.
    """
    def __init__(self, dw_conn, scope):
        """

        """
        self.dw_conn = dw_conn
        self.scope = scope
        # Contains representations of dimension and fact table
        self.dim_reps = []
        self.fts_reps = []

    def run(self):
        pygrametl = self.scope['pygrametl']

        tables = pygrametl._alltables
        for table in tables:
            if isinstance(table,Dimension):
                dim = DimRepresentation(table.name, table.key,
                                        table.attributes, self.dw_conn,
                                        table.lookupatts)
                self.dim_reps.append(dim)
            elif isinstance(table,FactTable):
                ft = FTRepresentation(table.name, table.keyrefs, self.dw_conn,
                                      table.measures)
                self.fts_reps.append(ft)

        dw = DWRepresentation(self.dim_reps, self.fts_reps, self.dw_conn)
        pygrametl._alltables.clear()

        return dw

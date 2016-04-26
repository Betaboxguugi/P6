from .datawarehouse_representation import DWRepresentation,\
    DimRepresentation, FTRepresentation
from pygrametl.tables import Dimension, FactTable

__author__ = 'Alexander, Arash'
__Maintainer__ = 'Alexander, Arash'
__all__ = ['RepresentationMaker']
DIM_CLASSES = ['Dimension']
FT_CLASSES = ['FactTable']
# TODO more table types


class RepresentationMaker(object):
    """
    Creates a DWRepresentation object from an associated program scope
    """
    def __init__(self, dw_conn, scope):
        """
        :param dw_conn: PEP249 connection to DW
        :param scope: A program scope containing a pygrametl program
        """
        self.dw_conn = dw_conn
        self.scope = scope
        # Contains representations of dimension and fact table
        self.dim_reps = []
        self.fts_reps = []

    def run(self):
        """
        Extracts table objects from the scope, then creates new representation
        objects which are placed into the DWRepresentation
        :return: A DWRepresentation object for the given scope
        """

        # Gets all table objects in the scope
        pygrametl = self.scope['pygrametl']
        tables = pygrametl._alltables

        # Creates representation objects
        for table in tables:
            if isinstance(table, Dimension):
                dim = DimRepresentation(table.name, table.key,
                                        table.attributes, self.dw_conn,
                                        table.lookupatts)
                self.dim_reps.append(dim)
            elif isinstance(table, FactTable):
                ft = FTRepresentation(table.name, table.keyrefs, self.dw_conn,
                                      table.measures)
                self.fts_reps.append(ft)

        dw_rep = DWRepresentation(self.dim_reps, self.fts_reps, self.dw_conn)

        # Clears the list of table as it's contents may otherwise be retained
        # when a new case is executed
        # TODO Find out how this works. Does it also retain default wrapper
        pygrametl._alltables.clear()

        return dw_rep

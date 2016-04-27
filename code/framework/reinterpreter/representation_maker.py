from .datawarehouse_representation import DWRepresentation,\
    DimRepresentation, FTRepresentation, Type1DimRepresentation, \
    Type2DimRepresentation
from pygrametl.tables import Dimension, FactTable, \
    TypeOneSlowlyChangingDimension, CachedDimension, SlowlyChangingDimension, \
    SCDimension, BulkDimension, CachedBulkDimension, BatchFactTable, \
    BulkFactTable, SnowflakedDimension

__author__ = 'Alexander, Arash'
__Maintainer__ = 'Alexander, Arash'
__all__ = ['RepresentationMaker']
DIM_CLASSES = [Dimension, CachedDimension,
               TypeOneSlowlyChangingDimension, SlowlyChangingDimension,
               SCDimension, BulkDimension, CachedBulkDimension]
FT_CLASSES = [FactTable, BatchFactTable, BulkFactTable]
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

    def check_table_type(self, table, typelist):
        for table_type in typelist:
            if isinstance(table, table_type):
                return True
        return False

    def run(self):
        """
        Extracts table objects from the scope, then creates new representation
        objects which are placed into the DWRepresentation
        :return: A DWRepresentation object for the given scope
        """

        # Gets all table objects in the scope
        pygrametl = self.scope['pygrametl']
        tables = pygrametl._alltables





        #for variables in self.scope:


        # Creates representation objects

        for table in tables:
            if self.check_table_type(table, DIM_CLASSES):
                dim = None

                if isinstance(table, TypeOneSlowlyChangingDimension):
                    dim = Type1DimRepresentation(table.name, table.key,
                                                 table.attributes,
                                                 self.dw_conn,
                                                 table.lookupatts,
                                                 table.type1atts)
                elif isinstance(table, SlowlyChangingDimension):
                    dim = Type2DimRepresentation(table.name, table.key,
                                                 table.attributes,
                                                 self.dw_conn,
                                                 table.lookupatts,
                                                 table.versionatt,
                                                 table.fromatt)
                else:
                    dim = DimRepresentation(table.name, table.key,
                                            table.attributes, self.dw_conn,
                                            table.lookupatts)
                self.dim_reps.append(dim)
            elif self.check_table_type(table, FT_CLASSES):
                    ft = FTRepresentation(table.name, table.keyrefs,
                                          self.dw_conn, table.measures)
                    self.fts_reps.append(ft)

        snowflakes = []
        for x, value in self.scope.items():
            if isinstance(value,SnowflakedDimension):
                snowflakes.append(value)

        dw_rep = DWRepresentation(self.dim_reps, self.fts_reps,
                                  self.dw_conn, snowflakes)

        # Clears the list of table as it's contents may otherwise be retained
        # when a new case is executed
        # TODO Find out how this works. Does it also retain default wrapper
        pygrametl._alltables.clear()




        return dw_rep

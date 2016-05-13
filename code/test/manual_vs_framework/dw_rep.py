import sqlite3
import pygrametl
from pygrametl.tables import Dimension, FactTable, SlowlyChangingDimension
from framework.reinterpreter.datawarehouse_representation import \
    DimRepresentation, FTRepresentation, DWRepresentation, \
    SCDType2DimRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

def make_dw_rep(dbname):
    conn = sqlite3.connect(dbname)
    wrapper = pygrametl.ConnectionWrapper(connection=conn)

    dim1 = Dimension(
        name='dim1',
        key='key1',
        attributes=['attr1', 'attr2']
    )

    dim2 = Dimension(
        name='dim2',
        key='key2',
        attributes=['attr3', 'attr4'],
    )

    ft1 = FactTable(
        name='ft1',
        keyrefs=['key1', 'key2'],
        measures=['measure']
    )

    dim1rep = DimRepresentation(dim1, conn)
    dim2rep = DimRepresentation(dim2, conn)
    ft1rep = FTRepresentation(ft1, conn)
    dw_rep = DWRepresentation([dim1rep, dim2rep], conn, [ft1rep])

    return dw_rep


def make_scd_rep(dbname):
    conn = sqlite3.connect(dbname)
    wrapper = pygrametl.ConnectionWrapper(connection=conn)

    output_wrapper = pygrametl.ConnectionWrapper(connection=conn)

    scd = SlowlyChangingDimension(
        name='scd',
        key='key',
        attributes=['attr1', 'attr2', 'version'],
        lookupatts=['attr2'],
        versionatt='version'
    )

    scd_rep = SCDType2DimRepresentation(scd, conn)
    dw_rep = DWRepresentation([scd_rep], conn)

    return dw_rep

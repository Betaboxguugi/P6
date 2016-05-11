import sqlite3
import pygrametl
from pygrametl.tables import Dimension, FactTable
from framework.reinterpreter.datawarehouse_representation import \
    DimRepresentation, FTRepresentation, DWRepresentation
from framework.case import Case
from framework.predicates import RowCountPredicate
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


def framework_row_count(path):

    conn = sqlite3.connect(path)
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
    count = RowCountPredicate('ft1', 1000000)
    case = Case(dw_rep, [count])
    start = time.monotonic()
    case.run()
    conn.close()
    end = time.monotonic()
    elapsed = end - start
    print('{}{}'.format(round(elapsed, 3), 's'))

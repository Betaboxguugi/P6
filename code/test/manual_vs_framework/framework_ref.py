import sqlite3
import pygrametl
from pygrametl.tables import Dimension, FactTable
from framework.reinterpreter.datawarehouse_representation import \
    DimRepresentation, FTRepresentation, DWRepresentation
from framework.case import Case
from framework.predicates import ReferentialIntegrityPredicate
import time

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Mikael Vind Mikkelsen'


def framework_ref_test(path):

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
    not_null = ReferentialIntegrityPredicate()
    case = Case(dw_rep, [not_null])
    start = time.monotonic()  # the instantiations take almost no time
    case.run()                # but we may as well measure the time for
    conn.close()              # executing the case
    end = time.monotonic()
    elapsed = end - start
    print('{}{}'.format(round(elapsed, 3), 's'))

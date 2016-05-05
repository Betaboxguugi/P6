from pygrametl.tables import Dimension, SnowflakedDimension
import pygrametl
import os
import sqlite3
from framework.predicates import FunctionalDependencyPredicate
from framework.reinterpreter.datawarehouse_representation import \
    DWRepresentation, DimRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

open(os.path.expanduser('func.db'), 'w')

conn = sqlite3.connect('func.db')

cur = conn.cursor()

cur.execute("CREATE TABLE dim1 " +
            "(key1 INTEGER PRIMARY KEY, attr1 INTEGER, key2 INTEGER, "
            "key3 INTEGER)")

cur.execute("CREATE TABLE dim2 " +
            "(key2 INTEGER PRIMARY KEY, attr2 INTEGER, key4 INTEGER)")

cur.execute("CREATE TABLE dim3 " +
            "(key3 INTEGER PRIMARY KEY, attr3 INTEGER)")

cur.execute("CREATE TABLE dim4 " +
            "(key4 INTEGER PRIMARY KEY, attr4 INTEGER)")


data = [
    {'attr1': 3,
     'attr2': 6,
     'attr3': 3,
     'attr4': 9},

    {'attr1': 2,
     'attr2': 8,
     'attr3': 6,
     'attr4': 4},

    {'attr1': 4,
     'attr2': 5,
     'attr3': 3,
     'attr4': 3},

    {'attr1': 1,
     'attr2': 3,
     'attr3': 4,
     'attr4': 4}
]

wrapper = pygrametl.ConnectionWrapper(connection=conn)

dim1 = Dimension(
    name='dim1',
    key='key1',
    attributes=['attr1', 'key2', 'key3'],
    lookupatts=['attr1']
)

dim2 = Dimension(
    name='dim2',
    key='key2',
    attributes=['attr2', 'key4'],
    lookupatts=['attr2']
)

dim3 = Dimension(
    name='dim3',
    key='key3',
    attributes=['attr3']
)

dim4 = Dimension(
    name='dim4',
    key='key4',
    attributes=['attr4']
)

special_snowflake = SnowflakedDimension(references=[(dim1, [dim2, dim3]),
                                                    (dim2, dim4)])

for row in data:
    special_snowflake.insert(row)

conn.commit()

dim1_rep = DimRepresentation(dim1.name, dim1.key, dim1.attributes, conn,
                             dim1.lookupatts)
dim2_rep = DimRepresentation(dim2.name, dim2.key, dim2.attributes, conn,
                             dim2.lookupatts)
dim3_rep = DimRepresentation(dim3.name, dim3.key, dim3.attributes, conn,
                             dim3.lookupatts)
dim4_rep = DimRepresentation(dim4.name, dim4.key, dim4.attributes, conn,
                             dim4.lookupatts)

snow_dw_rep = DWRepresentation([dim1_rep, dim2_rep, dim3_rep, dim4_rep],
                               conn, snowflakeddims=(special_snowflake, ))

for dim in snow_dw_rep.dims:
    allatts = dim.all.copy()

    for row in dim.itercolumns(allatts):
        print(dim.name, row)
print('\n')
a = ('key3',)
b = ('key1',)
c = (a, b)

d = ('key4',)
e = ('attr2',)
f = (d, e)

g = ('key2',)
h = (d, g)


func_dep1 = FunctionalDependencyPredicate([dim1_rep.name], (c,))
func_dep2 = FunctionalDependencyPredicate([dim2_rep.name], (f,))
func_dep3 = FunctionalDependencyPredicate([dim2_rep.name, dim4_rep.name], (h,))
func_dep4 = FunctionalDependencyPredicate([dim2_rep.name], (h,))

print(func_dep1.run(snow_dw_rep))
print(func_dep2.run(snow_dw_rep))
print(func_dep3.run(snow_dw_rep))
print(func_dep4.run(snow_dw_rep))

conn.close()

""" Dette er eksempel på hvordan vi pt kan teste om pygrametlprogrammer overholder
forskellige egenskaber. Dette er bare hvordan det virker lige nu, vi regner med at
gøre dette en del mere strømlignet og brugervenligt.

Det som der gøres er at vi definere nogle connections til nogle databaser, som vi
ønsker at bruge i stedet for dem som allerede findes i ens pygrametl program. 
Pygrametl programmet bliver så kørt igennem med disse connections i stedet for di 
gamle. 
I fremtiden vil vi også gerne supporte andre måder at give ens input til 
reinterpreteren, så som i form af dicts der representere databaser eller noget lign.

Herefter tester vi om den DW som ens pygrametl program gerne burde have populeret
overholder nogle egenskaber.
"""
# Import af vores ting
from reinterpreter import Reinterpreter
from predicate import DuplicatePredicate


# Import af et eller andet SQL libary
import SQL

# Vi laver nogle connections til forskellige databaser
# Først et DW som skal blive brugt af connection wrapperen i ens pygrametl program
conn_dw = SQL.connect('a.db')

# Derefter connecter vi til de databaser som skal bruges som skal bruges i extract
# delen af ens pygrametl program
conn_input_1 = SQL.connect('b.db')
conn_input_2 = SQL.connect('c.db')

# Vi definere et pygrametl program, dette kunne også gives som en path til en fil.
program =\
"""
import pygrametl
from pygrametl.datasources import *
from pygrametl.tables import *
import sqlite3

conn_out = sqlite3.connect('out.db')
conn_in1 = sqlite3.connect('in1.db')
conn_in2 = sqlite3.connect('in2.db') 

wrapper = pygrametl.ConnectionWrapper(conn_out)
sqlsource1 = SQLSource(conn_in1, query="SELECT * FROM tablename")
sqlsource2 = SQLSource(connection=conn_in2, "SELECT * FROM othertablename")

ft = FactTable(
    name='ft1',
    keyrefs=['t1', 't2'],
    measures=[])

dim = Dimension(
    name='dim1',
    key='key1',
    attributes=['attr1', 'attr2'],
    lookupatts=[])
"""


# Vi laver et Dict hvor vi mapper en string til vores connection. Dette dict skal
# være ordered efter den række følge som vores connections blive brugt af
# datasources i vores pygrametl program. Dette dict blive brugt som et scope i
# ens pygrametl program, og gør at vi kan bruge disse, i stedet for hardcodede.
# Værdien af strengen skal bare være noget som man ikke allerede brugere som et
# variable navn i ens pygrametl program.
scope = {'conn_a': conn_dw, 'conn_b': conn_input_1, 'conn_c': conn_input_2}


# Vi giver programmet og scopet til vores reinterpreter. Reinterpreteren vil
# eksekvere vores pygrametl kode, men med pointere til de connections vi gerne
# vil have at den skal bruge.
reint = Reinterpreter(program=program, conn_scope=scope, program_is_path=False)

# Vi kalder run på reinterpreter, dette eksekvere pygrametl koden som vi gerne
# ville have den. Og returnere et dictionary af SQLSource objekter, en får hver
# Dimension eller FactTable instantiering pygrametl koden. Dette gøres for at
# brugeren nu nemt kan give de forskellige tables i deres DW til predicates.
# Dictets keys er navne på tabellerne som indeholde den pågældende dimension/ft
dw_tables = reint.run()

# Vi henter dim1 ud fra dw_tables
dim1 = dw_tables['dim1']

# Vi tester om der er duplikerede tubler i denne tabel
dubpred = DublicatePredicate(dim1)
dubpred.run()






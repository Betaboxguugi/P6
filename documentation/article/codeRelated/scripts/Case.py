import sqlite3

# We execute a pygrametl program using our specified
# sources and create a DWRepresentation.
program = './myetlprogram.py'
src1 = sqlite3.connect(datasource='./db1')
src2 = sqlite3.connect(datasource='./db2')
dwp = DWPopulator(program=program,
                  pep249_module=sqlite3,
                  sources=(src1, src2),
                  datasource='./dw')

dwrep = dwp.run()

# We create our predicates
p1 = ReferentialIntegretyPredicate()
p2 = RowCountPredicate(table_name='table1',
                       number_of_rows=99)

# We create our Case and run it
c = Case(dw_rep=dwrep,
         pred_list=[p1, p2])
c.run()


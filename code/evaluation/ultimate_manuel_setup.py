import sqlite3
import time

start = time.monotonic()
dw_path = './dw.db'
conn = sqlite3.connect(dw_path)
c = conn.cursor()

def time_passed(start):
    end = time.monotonic()
    elapsed = end - start
    return '{}{}'.format(round(elapsed, 3), 's')

# Not Null
c.execute("""SELECT *
             FROM authordim
             WHERE aid IS NULL
               OR city IS NULL
               OR name IS NULL
               OR cid  IS NULL""")
not_null_list = c.fetchall()
if not_null_list:
    print('Null found on the following elements:')
    for row in not_null_list:
        print(row)
else:
    print('Not Null Test - Success')

# Compare Table - *shrug* Wait til its done i quess.
c.execute("""""")
some_list = c.fetchall()
if some_list:
    print('Failed')
    for row in some_list:
        print(row)
else:
    print('Success')

# Functional Dependency
c.execute("""SELECT DISTINCT t1.cid ,t1.city
             FROM (authordim NATURAL JOIN countrydim) as t1 ,
                  (authordim NATURAL JOIN countrydim) as t2
             WHERE  t1.cid = t2.cid  AND (  (t1.city <> t2.city)  )""")
func_dep_list = c.fetchall()
if func_dep_list:
    print('Functional Dependency did not hold on the following elements:')
    for row in func_dep_list:
        print(row)
else:
    print('Functional Dependency Test - Success')

# No Duplicate Row
c.execute(""" SELECT name,city,aid,cid ,COUNT(*)
              FROM authordim
              GROUP BY name,cid HAVING COUNT(*) > 1 """)
some_list = c.fetchall()
if some_list:
    print('Duplicates found on the following elements:')
    for row in some_list:
        print(row)
else:
    print('No Duplicate Row Test - Success')

# Referential Integrity
c.execute("""SELECT *
             FROM authordim
             WHERE NOT EXISTS(
                SELECT NULL
                FROM countrydim
                WHERE authordim.cid = countrydim.cid)""")
ref_integ_list = c.fetchall()
c.execute("""SELECT *
             FROM countrydim
             WHERE NOT EXISTS(
                SELECT NULL
                FROM authordim
                WHERE countrydim.cid = authordim.cid)""")
ref_integ_list += c.fetchall()
c.execute("""SELECT *
             FROM facttable
             WHERE NOT EXISTS(
                SELECT NULL
                FROM authordim
                WHERE facttable.aid = authordim.aid)""")
ref_integ_list += c.fetchall()
c.execute("""SELECT *
             FROM authordim
             WHERE NOT EXISTS(
                SELECT NULL
                FROM facttable
                WHERE authordim.aid = facttable.aid)""")
ref_integ_list += c.fetchall()
c.execute("""SELECT *
             FROM facttable
             WHERE NOT EXISTS(
                SELECT NULL
                FROM bookdim
                WHERE facttable.bid = bookdim.bid)""")
ref_integ_list += c.fetchall()
c.execute("""SELECT *
             FROM bookdim
             WHERE NOT EXISTS(
                SELECT NULL
                FROM facttable
                WHERE bookdim.bid = facttable.bid)""")
ref_integ_list += c.fetchall()
if some_list:
    print('Referential Integrity did not hold on the following elements')
    for row in some_list:
        print(row)
else:
    print('Referential Integrity Test - Success')

# Row Count - Erhm yeah... About that O_o

# Rule Column - Erhm yeah... About that O_o

# SCD Version
c.execute("""SELECT max(version)
             FROM bookdim
             WHERE title = 'EZ PZ ETL'""")
some_list = c.fetchall()
if some_list:
    print('Failed')
    for row in some_list:
        print(row)
else:
    print('Success')
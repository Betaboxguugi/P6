import sqlite3
import time

start = time.monotonic()

def time_passed(start_time):
    end = time.monotonic()
    elapsed = end - start_time
    return '{}{}'.format(round(elapsed, 3), 's')

# We run the ETL program
etl_path = './etl.py'
with open(etl_path, 'r') as f:
    code = compile(f.read(), etl_path, 'exec')
    exec(code)

dw_path = './dw.db'
conn = sqlite3.connect(dw_path)
c = conn.cursor()

time_before_test = time_passed(start)
print(time_before_test)

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

# Compare Table
c.execute("""SELECT *
             FROM goodbooksdim
             EXCEPT
                SELECT *
                FROM bookdim """)
some_list = c.fetchall()
if some_list:
    print('Failed to compare tables')
    for row in some_list:
        print(row)
else:
    print('Successfully compared tables')

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

# Row Count
c.execute("""SELECT COUNT(*)
             FROM bookdim """)
row_count = c.fetchall()[0]
if row_count == 6:
    print('Row Count Test - Success')
else:
    print('Row count did not hold\nThere are {} rows when there should be 6')

# SCD Version
c.execute("""SELECT max(version)
             FROM bookdim
             WHERE title = 'EZ PZ ETL'""")
scdv_list = c.fetchall()
if scdv_list[0] == 4:
    print('SCD Version Test - Success')
else:
    print('SCD Version did not hold. Should have been 4 but was ' +
          str(scdv_list[0][0]))


time_after_test = time_passed(start)
# Checking how long it took.
print(" TIME BEFORE TEST " + time_before_test)
print(" TIME AFTER TEST " + time_after_test)

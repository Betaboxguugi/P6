"""My own little test place, for now it just contains various examples of how to insert data into a table
 and what to note when creating table."""

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sqlite3
import os,sys
import os.path


"This just insures we have a fresh database to work with."
if os.path.isfile('test.db'):
   os.remove('test.db')
   print("Deleted previous database")
   conn = sqlite3.connect('test.db')
else:
   conn = sqlite3.connect('test.db')

c = conn.cursor()
print("Opened database successfully")

"""Creating a table, note that ID has the constraints PRIMARY KEY, AUTOINCREMENT and NOT NULL
    PRIMARY KEY insures that ID must contain a unique value in the table.
    AUTOINCREMENT insures that if our ID column is not explicitly given a value,
    then it will be filled automatically with an unused integer.
    NOT NULL enforces a column to NOT accept NULL values"""
c.execute('''CREATE TABLE COMPANY
    (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
    NAME           TEXT   NOT NULL,
    AGE            INT    NOT NULL,
    ADDRESS        CHAR(50),
    SALARY         REAL);''')
print("Table created successfully")

"To insert people int the database the following examples can be used"
"execute, executes one SQL statement, which limits us to only do one insert at a time"
c.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES ('Paul', 32, 'California', 20000.00 )")

c.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES ('Allen', 25, 'Texas', 15000.00 )")

"So we can see changes in the database"
print("execute inserts successful")
c.execute("SELECT * FROM COMPANY")
print(c.fetchall())

"excecutescript, is a nonstandard way of executing multiple SQL statements, allowing us to perform multiple inserts"
c.executescript("""
    INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES ('Teddy', 23, 'Norway', 20000.00 );
    INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES ('Mark', 25, 'Rich-Mond ', 65000.00 );""")

"So we can see changes in the database"
print("executescripts inserts successful")
c.execute("SELECT * FROM COMPANY")
print(c.fetchall())


"List with people we wish to put into our table:"
company_info = [('Anders', 43, 'Denmark', 21000.00),
                ('Charles', 50, 'Texas', 25000.00),
                ('Wolf', 28, 'Sweden', 19000.00),
                ('Hannibal', 455, 'America', 65000.00),
                ]

"excecutemany, executes an SQL command against all parameter sequences or mappings found in the sequence sql"
conn.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)

"So we can see changes in the database"
print("executemany inserts successful")
c.execute("SELECT * FROM COMPANY")
print(c.fetchall())




print ("Operation done successfully")
conn.commit()
conn.close()

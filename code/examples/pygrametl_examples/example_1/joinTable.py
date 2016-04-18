__author__ = 'Alexander'
__maintainer__ = 'Alexander'

# IMPORTS
import pygrametl
import sqlite3

# CONSTANTS
DW_NAME = './dw.db'

# We then connect to these DBs
dw_conn = sqlite3.connect(DW_NAME)
dw_conn_wrapper = pygrametl.ConnectionWrapper(connection=dw_conn)
cursor = dw_conn_wrapper.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'ORDER BY name;")
table_list = cursor.fetchall()
for x in table_list:
    print(x)



# Making the join
cursor.execute("SELECT * FROM factTable f LEFT OUTER JOIN bookDim b  ON f.bookid = b.bookid" +
               " LEFT OUTER JOIN locationDim l ON f.locationid = l.locationid" +
               " LEFT OUTER JOIN timeDim t ON f.timeid = t.timeid " )

dic1 = cursor.fetchall()

cursor.execute("SELECT * FROM factTable f LEFT OUTER JOIN bookDim b  ON f.bookid = b.bookid" +
               " LEFT OUTER JOIN locationDim l ON f.locationid = l.locationid" +
               " LEFT OUTER JOIN timeDim t ON f.timeid = t.timeid " )

dic2 = cursor.fetchall()

for (f, b) in zip(dic1, dic2):
    print(f == b)


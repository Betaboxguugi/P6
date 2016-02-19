import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

cursor =conn.execute("SELECT EMP_ID, NAME, DEPT FROM COMPANY NATURAL JOIN DEPARTMENT;")
for row in cursor:
   print("ID = ", row[0])
   print("NAME = ", row[1])
   print("ADDRESS = ", row[2], "\n")

print ("Operation done successfully")
conn.close()

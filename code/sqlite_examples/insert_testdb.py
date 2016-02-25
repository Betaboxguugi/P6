import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
      VALUES ('Paul', 32, 'California', 20000.00 )")

conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
      VALUES ('Allen', 25, 'Texas', 15000.00 )")

conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
      VALUES ('Teddy', 23, 'Norway', 20000.00 )")

conn.execute("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) \
      VALUES ('Mark', 25, 'Rich-Mond ', 65000.00 )")


conn.execute("INSERT INTO DEPARTMENT (DEPT,EMP_ID) \
      VALUES ('NSDAP', 20 )")

conn.execute("INSERT INTO DEPARTMENT (DEPT,EMP_ID) \
      VALUES ('DKP', 40 )")


conn.commit()
print("Records created successfully")
conn.close()

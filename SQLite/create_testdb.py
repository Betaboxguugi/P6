import sqlite3

conn = sqlite3.connect('test.db')
print("Opened database successfully")

conn.execute("DROP TABLE COMPANY;")
conn.execute("DROP TABLE DEPARTMENT;")


conn.execute('''CREATE TABLE COMPANY
       (ID INTEGER PRIMARY KEY    NOT NULL,
       NAME           TEXT   NOT NULL,
       AGE            INT    NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
print("Table created successfully")

conn.execute('''CREATE TABLE DEPARTMENT(
       ID INTEGER PRIMARY KEY      NOT NULL,
       DEPT           CHAR(50) NOT NULL,
        EMP_ID         INT      NOT NULL);''')
print("Table created successfully")


conn.close()
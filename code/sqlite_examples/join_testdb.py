"""Examples of join between 2 tables"""

__author__ = 'Mikael Vind Mikkelsen'
__maintainer__ = 'Mikael Vind Mikkelsen'

# IMPORTS
import sqlite3
import os, sys
import os.path


# Function to print a table
def print_table(str, name=None):
    print("-----------------------------")
    if name is not None:
        print("Table: " + name)
    for row in c.execute(str):
        print(row)
    print("-----------------------------")
    return []


# This just insures we have a fresh database to work with.
if os.path.isfile('test.db'):
    os.remove('test.db')
    print("Deleted previous database")
    conn = sqlite3.connect('test.db')
else:
    conn = sqlite3.connect('test.db')
c = conn.cursor()
print("Opened database successfully")

# Table over a group of persons
c.execute('''CREATE TABLE PERSONS
    (ID     INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
    NAME    TEXT                                NOT NULL,
    AGE     INT                                 NOT NULL);
    ''')

# Table over the persons hobbies, not PERSON_ID which we wil use to identify who has each hobby.
c.execute('''CREATE TABLE HOBBIES
    (ID INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
    PERSON_ID           INT                 NOT NULL,
    NAME                TEXT                NOT NULL);
    ''')
print("Tables created successfully")

# Inserting array into the relevant table
persons_list = [('Anders', 43),
                ('Maria', 33),
                ('Sandra', 13),
                ('Charles', 50),
                ('Wolf', 28),
                ('Hannibal', 45),
                ]
c.executemany("INSERT INTO PERSONS (NAME,AGE) VALUES (?,?)", persons_list)

print_table("SELECT * FROM PERSONS",
            "Persons")

# Inserting array into the relevant table
hobbies_list = [(4, 'Bowling'),
                (3, 'Warhammer 40k'),
                (2, 'Beer Brewing'),
                (6, 'Cooking'),
                (6, 'Murder'),
                ]

c.executemany("INSERT INTO HOBBIES (PERSON_ID,NAME) VALUES (?,?)", hobbies_list)

print_table("SELECT * FROM HOBBIES",
            "Hobbies")

# The join of the 2 table, PERSON AND HOBBIES.
# Since NAME is a parameter in both tables, we must specify what we wish to see by using PERSONS.NAME and HOBBIES.NAME
print_table("SELECT PERSONS.NAME, HOBBIES.NAME FROM PERSONS JOIN HOBBIES",
            "Joined Table")

# The table "Joined Table", shows all combinations between all the names from the 2 tables.
# So to only see what hobbies each persons have we add "ON PERSONS.ID = HOBBIES.PERSON_ID".
print_table("SELECT PERSONS.NAME, HOBBIES.NAME FROM PERSONS JOIN HOBBIES ON PERSONS.ID = HOBBIES.PERSON_ID",
            "Specified Joined Table")

# The table "Specified Joined Table", does not show Anders and Wolf as they have no hobbies.
# So we use LEFT OUTER JOIN to insure we show all the people from the table PERSONS
print_table("SELECT PERSONS.NAME, HOBBIES.NAME FROM PERSONS LEFT OUTER JOIN HOBBIES ON PERSONS.ID = HOBBIES.PERSON_ID",
            "Specified Left Outer Joined Table")



print("Operation done successfully")
conn.commit()
conn.close()

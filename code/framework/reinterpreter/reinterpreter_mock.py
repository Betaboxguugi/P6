from .datawarehouse_representation import *
__author__ = 'Mathias Claus Jensen'
__all__ = ['Reinterpreter']

import os
import sqlite3

class ReinterpreterMock(object):
    """ Class in charge of reinterpreting a pygrametl program, using different
    connections.
    """

    def run(self):
        """ Reinterpretes the pygrametl program, returns a dict containing 
        :return: A dictionary with all the dimension/facttable datasources.
        """

        # Ensures a fresh database to work with.

        TEST_DB = 'test.db'
        open(os.path.expanduser('test.db'), 'w')

        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()

        # Making table to test on...
        c.execute('''CREATE TABLE COMPANY
            (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
            NAME           TEXT   NOT NULL,
            AGE            INT    NOT NULL,
            ADDRESS        CHAR(50),
            SALARY         REAL);''')

        company_info = [('Anders', 43, 'Denmark', 21000.00),
                        ('CharLes', 50, 'Texas', 25000.00),
                        ('Wolf', 28, 'Sweden', 19000.00),
                        ('Hannibal', 45, 'America', 65000.00),
                        ('Buggy Bug', 67, 'America', 2000)
                        ]

        # ... and inserting the necessary data.
        c.executemany("INSERT INTO COMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)

        p = conn.cursor()

        p.execute('''CREATE TABLE BOMPANY
            (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
            NAME           TEXT   NOT NULL,
            AGE            INT    NOT NULL,
            ADDRESS        CHAR(50),
            SALARY         REAL);''')

        company_info = [('Anders', 43, 'Denmark', 21000.00),
                        ('CharLes', 50, None, 25000.00),
                        ('Wolf', 28, 'Sweden', 19000.00),
                        ('Hannibal', 45, 'America', 65000.00),
                        ('Buggy Bug', 67, 'America', None)
                        ]

        # ... and inserting the necessary data.
        p.executemany("INSERT INTO BOMPANY (NAME,AGE,ADDRESS,SALARY) VALUES (?,?,?,?)", company_info)

        aa = DimRepresentation('COMPANY', 'ID', ['AGE', 'ADDRESS', 'SALARY'], conn, ['NAME'])
        bb = FTRepresentation('BOMPANY', ['NAME', 'ADDRESS', 'ID'], ['AGE', 'SALARY'], conn)
        cc = DWRepresentation([aa], [bb], conn)

        """print(cc.get_data_representation('BOMPANY').name)
        for d in cc.get_data_representation('BOMPANY').itercolumns(['ID']):
            print(d['ID'])"""
        return cc


"""     scope = self.conn_scope.copy()
        program = ''
        if self.program_is_path:
            with open(self.program, 'r') as f:
                program = f.read()
        else:
            program = self.program

        tree = ast.parse(program) # Parsing the pygrametl program to an AST

        self.__transform(tree)  # Transforming the AST to include the user defined connections
        self.__compile_exec(node=tree, gscope=None, lscope=scope)  # Executing the transformed AST

        src_module = self.__extract(tree)  # Creating a new AST for extracting DW tables
        self.__compile_exec(node=src_module, gscope=None, lscope=scope)  # Executing executing extract AST

        # The extract AST extends the scope to include source objects for all DW tables.
        # This is returned here for the user to test upon.
        return scope[self.varname]"""

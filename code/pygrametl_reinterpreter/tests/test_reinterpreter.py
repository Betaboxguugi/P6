import sys
sys.path.append('../')
from unittest import *
from reinterpreter import Reinterpreter
import sqlite3


class TestReinterpreter(TestCase):
    def setUp(self):
        self.conn1 = sqlite3.Connection('a.db')
        self.conn2 = sqlite3.Connection('b.db')
        self.conn_scope = {'conn_a': self.conn1, 'conn_b': self.conn2}
        self.program = \
"""import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
import sqlite3

input_conn = sqlite3.connect('input.db')
output_conn = sqlite3.connect('output.db')

input_src = SQLSource(input_conn, query='SELECT * dim1')
output_wrapper = pygrametl.ConnectionWrapper(connection=output_conn)

dim1 = Dimension(
    name='dim1',
    key='key1',
    attributes=['attr1', 'attr2']
)

dim2 = Dimension(
    name='dim2',
    key='key2',
    attributes=['attr3', 'attr4']
)

ft1 = FactTable(
    name='ft1',
    keyrefs=['key1',]
)

input_conn.close()
output_conn.close()
"""
        self.reinterpreter = Reinterpreter(program=self.program,
                                           conn_scope=self.conn_scope,
                                           program_is_path=False)
        
    def tearDown(self):
        self.conn1.close()
        self.conn2.close()

    def test_run(self):
        # Arrange
        reinterpreter = self.reinterpreter

        # Act
        scope = reinterpreter.run()

        # Assert
        self.assertIn('dim1', scope)
        self.assertIn('dim2', scope)
        self.assertIn('ft1', scope)
        self.assertEqual(len(scope), 3)
        
        
suite = makeSuite(TestReinterpreter)
TextTestRunner(verbosity=2).run(suite)

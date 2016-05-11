import sqlite3
import unittest

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'


class TestRowCount(unittest.TestCase):

    def test_rowcount(self):
        conn = sqlite3.connect('row_count.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM ft1')
        l = cur.fetchall()
        self.assertEqual(l.__len__(), 1000000)

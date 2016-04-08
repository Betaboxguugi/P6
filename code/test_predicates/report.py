import os
import sqlite3
import sys
import sqlite3
sys.path.append('../')
from pygrametl.datasources import *
from t_predicate import TPredicate
from pygrametl_reinterpreter import *


class Report(object):
    def __init__(self, name_of_predicate='', result=False, message_if_true=None, message_if_false=None,
                 list_of_wrong_elements=()):
        """
        :param name_of_predicate:
        :param result:
        :param message_if_true:
        :param message_if_false:
        :param list_of_wrong_elements:
        """
        self.nop = name_of_predicate
        self.r = result
        self.mit = message_if_true
        self.mif = message_if_false
        self.l = list_of_wrong_elements
        self.run()

    def run(self):
        """
        Checks if results are true or false, 
        """
        if self.r is True:
            print('{} returned {} {}'.format(self.nop, self.r, self.mit))
        elif self.r is False:
            print('{} returned {} at the following elements {} {} '.format(self.nop, self.r, self.l, self.mif))
        else:
            print('Failure to report, please contact us at voresfællesemail@student.aau.dk if you see this message')


"""
Navn
Boolean værdi
evtuel besked
information om entries der fejlede
"""
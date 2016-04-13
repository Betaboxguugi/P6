import os
import sqlite3
import sys
import sqlite3
sys.path.append('../')
from pygrametl.datasources import *
from pygrametl_reinterpreter import *


class Report(object):
    def __init__(self, name_of_predicate='', result=False, message_if_true='', message_if_false='',
                 list_of_wrong_elements=None):
        """
        :param name_of_predicate: name of the the predicate class used, for the lazy just use: self.__class__.__name__
        :type name_of_predicate: str
        :param result: final result of the test
        :type result: bool
        :param message_if_true: message which will be printed if results are True
        :type message_if_false: str
        :param message_if_false: message which will be printed if results are False
        :type message_if_false: str
        :param list_of_wrong_elements: list of all the elements in which the predicate returned false
        """
        self.nop = name_of_predicate
        self.r = result
        self.mit = message_if_true
        self.mif = message_if_false
        self.l = list_of_wrong_elements

    def run(self):
        """
        Checks if results are true or false, prints the predicate used, result, message which is different dependent on
        results and if result is false, also prints a list of the elements which returned false if any are provided.
        In the cause that result is somehow neither, a failed message will show.
        """
        if self.r is True:
            print('{} returned {} {}'.format(self.nop, self.r, self.mit))
        elif self.r is False:
            if self.l is not None:
                print('{} returned {} at the following elements {} {} '.format(self.nop, self.r, self.l, self.mif))
            else:
                print('{} returned {} {} '.format(self.nop, self.r, self.mif))
        else:
            # TODO: Make/get a mail people can report errors to
            print('Failure to report, please contact us at errorReport@pyrgrametl.dk if you see this message')

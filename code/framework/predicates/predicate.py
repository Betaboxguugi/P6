__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'
from pygrametl.datasources import *
from csv import DictReader


class Predicate:
    """A class that implements basic functionality of a predicate.
    It is the superclass to all predicates of the framework.
    """

    __result__ = False

    def run(self, *args):
        """ Runs the actual test. Stores result in __result__"""
        self.__result__ = True

    def report(self):
        """
        returns the result of the test
        """


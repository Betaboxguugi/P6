__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'

class TestPredicate:
    """A class that implements basic functionality of a predicate.
    It is the superclass to all predicates of the framework.
    """

    __result__ = False

    def dictify(self, conn):
        """ Creates an iterable of dicts from our connection
        :param  conn: a pygrametl connection object, which we wish to fetch data from"""


    def run(self):
        """ Runs the actual test. Stores result in __result__"""
        #Run actual test

    def report(self):
        """
        returns the result of the test
        """
        return self.__result__

    def __init__(self, conns):
        """
        :param conns: a tuple of object connections to the data we need to test.
        """


#What kind of connections? SQLSource? PEP249?
#Need for good way of iterating? What if we just iterate using an SQLSource?
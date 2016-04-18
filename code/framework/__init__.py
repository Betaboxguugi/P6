__author__ = 'Alexander Brandborg'
__maintainer__ = 'Alexander Brandborg'

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


class DWRepresentation(object):
    """
    Class used to represent an entire DW.
    Allows for access to specific tables simply through their name.
    """

    def __init__(self, dims, fts, connection):
        """
        :param dims: A list of DimensionRepresentation Objects
        :param fts: A lost of FTRepresentation Objects
        :param connection: A PEP 249 connection to a database
        """

        try:
            self.dims = dims
            self.fts = fts
            self.connection = connection

            # Turns all our names to lower case as SQL is case insensitive
            # Also collects a list of names for a later check
            name_list = []
            self.rep = self.dims + self.fts
            for entry in self.rep:
                low = entry.name.lower()
                entry.name = low
                name_list.append(low)

            # Makes sure that no two tables have the same name. Else we raise an exception.
            if len(name_list) != len(list(set(name_list))):
                raise ValueError("Table names are not unique")

            # Fills the up our dictionary with tables keyed by their names.
            self.tabledict = {}
            for entry in self.rep:
                self.tabledict[entry.name] = entry

        finally:
            try:
                pass
            except Exception:
                pass

    def __str__(self):
        return self.tabledict.__str__()

    def __repr__(self):
        return self.__str__()

    def get_data_representation(self, name):
        """
        :param name: Name of the requested table
        :return: A TableRepresentation Object corresponding to the name
        """
        return self.tabledict[name.lower()]


class TableRepresentation(object):
    """
    Super class for representing tables in a DW
    """

    def __iter__(self):
        """
        :return: A generator for iterating over the contents of the table
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(self.query)
            names = [t[0] for t in cursor.description]

            while True:
                data = cursor.fetchmany(500)
                # Some cursor.description return null if the cursor hasn't fetched.
                # Thus we call it again after fetch if this is the case.
                if not names:
                    names = [t[0] for t in cursor.description]
                if not data:
                    break
                # Checks that the entries have the correct amount of attributes
                if len(names) != len(data[0]):
                    raise ValueError(
                        "Incorrect number of names provided. " +
                        "%d given, %d needed." % (len(names), len(data[0])))
                for row in data:
                    yield dict(zip(names, row))
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def itercolumns(self, column_names):
        """
        Lets us fetch only a subset of columns from the table
        :param column_names: The subset of columns of interest
        :return: A generator for iterating over the contents of the table
        """
        for data in self.__iter__():
            result = {}
            for name in column_names:
                result.update({name: data[name]})
            yield result


class DimRepresentation(TableRepresentation):
    """
    An object for representing data in a DW dimension
    """
    def __init__(self, name, key, attributes, connection, lookupatts=None, query=None):
        """
        :param name: Name of table
        :param key: Name of primary key attribute
        :param attributes: List of non-lookup attributes of the table
        :param lookupatts: List of lookup attributes of the table
        :param connection: PEP249 connection to a database
        :param query: SQL query used for fetching contents of the table
        """
        self.name = name
        self.key = key
        self.attributes = attributes
        if lookupatts:
            self.lookupatts = lookupatts
        else:
            self.lookupatts = self.attributes
        self.connection = connection
        self.all = [self.key] + self.attributes + self.lookupatts

        if query is None:
            self.query = "SELECT " + ",".join(self.all) + " FROM " + self.name
        else:
            self.query = query

    def __str__(self):
        row_list = []
        for row in self.itercolumns(self.all):
            row_list.append(row)
        text = "{} {}".format(self.name, row_list)
        return text

    def __repr__(self):
        return self.__str__()


class FTRepresentation(TableRepresentation):
    """
    An Object for representing data in a DW fact table
    """
    def __init__(self, name, keyrefs, measures, connection, query=None):
        """
        :param name: Name of table
        :param keyrefs: List of attributes that are foreign keys to other tables
        :param measures: List of attributes containing non-key values
        :param connection: PEP249 connection to a database
        :param query: SQL query used for fetching contents of the table
        """
        self.name = name
        self.keyrefs = keyrefs
        self.measures = measures
        self.connection = connection
        self.all = self.keyrefs + self.measures

        if query is None:
            self.query = "SELECT " + ",".join(self.all) + " FROM " + self.name
        else:
            self.query = query

    def __str__(self):
        row_list = []
        for gen in self.itercolumns(self.all):
            row_list.append(gen)
        text = "{} {}".format(self.name, row_list)
        return text

    def __repr__(self):
        return self.__str__()


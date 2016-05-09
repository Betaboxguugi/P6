__author__ = 'Mathias Claus Jensen & Alexander Brandborg'
__maintainer__ = 'Mathias Claus Jensen'

class DWRepresentation(object):
    """
    Class used to represent an entire DW.
    Allows for access to specific tables simply through their name.
    """

    def __init__(self, dims,  connection, fts=[], snowflakeddims=()):
        """
        :param dims: A list of DimensionRepresentation Objects
        :param fts: A lost of FTRepresentation Objects
        :param snowflakeddims: Tuple of SnowflakedDimensions
        :param connection: A PEP 249 connection to a database
        """

        try:
            self.dims = dims
            self.fts = fts
            self.connection = connection
            self.snowflakeddims = snowflakeddims

            # Turns all our names to lower case as SQL is case insensitive
            # Also collects a list of names for a later check
            name_list = []
            self.rep = self.dims + self.fts

            for entry in self.rep:
                low = entry.name.lower()
                entry.name = low
                name_list.append(low)

            # Makes sure that no two tables have the same name.
            # Else we raise an exception.
            if len(name_list) != len(list(set(name_list))):
                raise ValueError("Table names are not unique")

            # Fills the dictionary with tables keyed by their names.
            self.tabledict = {}
            for entry in self.rep:
                self.tabledict[entry.name] = entry

            # Re-creates the referencing structure of the DW
            self.refs = self._find_structure()
        finally:
            try:
                pass
            except Exception:
                pass

    def _find_structure(self):
        """
        Re-creates the referencing structure of the DW.
        Reuses the referencing dicts from SnowflakedDimension objects,
        then builds upon them by finding the references between fact tables
        and dimensions.
        For this to work there are some restrictions to keep in mind:
        - Facttable may only refer to the root of a Snowflaked Dimension.
        - There may be no overlap between the dimensions of on Snowflaked
          dimension and another.
        - Primary/Foreign key pairs have to share attribute name.

        :return: A dictionary where each key is a fact table or dimension,
        pointing to a set of dimensions, which it references.
        """

        references = {}
        all_dims = set(self.dims)

        for flake in self.snowflakeddims:
            # Extends our references with internal snowflake refs
            rep_refs = {}
            for key, value in flake.refs.items():
                key = self._find_dim_rep(key, all_dims)
                l = set()
                for dim in value:
                    l.add(self._find_dim_rep(dim, all_dims))
                rep_refs[key] = l

            references.update(rep_refs)
            for key, value in rep_refs.items():
                # Removes all non-root dimensions from the overall list of
                # dimensions, so that they cannot be referenced by fact tables.
                all_dims.difference_update(value)

        # For each fact table we find the set of all dimensions,
        # which it references.
        for ft in self.fts:
            ft_refs = set()
            for keyref in ft.keyrefs:
                for dim in all_dims:
                    if keyref == dim.key:
                        ft_refs.add(dim)
                        break
            references[ft] = ft_refs

        return references

    def _find_dim_rep(self, dim, all_dims):
        for rep in all_dims:
            if rep.name == dim.name:
                return rep
        raise Exception('Snowflaked dimension rep not found.')

    def __str__(self):
        return self.tabledict.__str__()

    def __repr__(self):
        return self.__str__()

    def iter_join(self, names):
        """ Iterate over a natural join of the given table names
        :param names: List of table names
        :yield: A dictionary representing a row
        """
        if len(names) == 1:
            query = "SELECT * FROM " + names[0]
        else:
            query = "SELECT * FROM " + " NATURAL JOIN ".join(names)
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            names = [t[0] for t in cursor.description]

            while True:
                data = cursor.fetchmany(500)
                if not names:
                    names = [t[0] for t in cursor.description]
                if not data:
                    break
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

    def get_data_representation(self, name):
        """
        :param name: Name of the requested table
        :return: A TableRepresentation Object corresponding to the name
        """
        return self.tabledict[name.lower()]


class TableRepresentation(object):
    """ Super class for representing tables in a DW
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
                # Some cursor.description return null if the cursor hasn't
                # fetched.
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
        """Lets us fetch only a subset of columns from the table
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
    def __init__(self, name, key, attributes, connection, lookupatts=()):
        """
        :param name: Name of table
        :param key: Name of primary key attribute
        :param attributes: List of non-lookup attributes of the table
        :param lookupatts: List of lookup attributes of the table
        :param connection: PEP249 connection to a database
        """
        self.name = name
        self.key = key
        self.attributes = attributes
        if lookupatts == ():
            self.lookupatts = self.attributes
        else:
            self.lookupatts = lookupatts

        self.connection = connection
        self.all = [self.key] + self.attributes
        self.query = "SELECT " + ",".join(self.all) + " FROM " + self.name

    def __str__(self):
        text = "{} {} {} {}".format(self.name, self.key, self.attributes,
                                    self.lookupatts)
        return text

    def __repr__(self):
        return self.__str__()


class SCDType1DimRepresentation(DimRepresentation):
    def __init__(self, name, key, attributes, connection, lookupatts,
                 type1atts=()):
        DimRepresentation.__init__(self,
                                   name,
                                   key,
                                   attributes,
                                   connection,
                                   lookupatts)
        if type1atts == ():
            self.type1atts = list(set(self.attributes) - set(self.lookupatts))
        else:
            self.type1atts = type1atts


class SCDType2DimRepresentation(DimRepresentation):
    def __init__(self, name, key, attributes, connection, lookupatts,
                 versionatt, fromatt=None):
        DimRepresentation.__init__(self,
                                   name,
                                   key,
                                   attributes,
                                   connection,
                                   lookupatts)
        self.versionatt = versionatt
        self.fromatt = fromatt


class FTRepresentation(TableRepresentation):
    """
    An Object for representing data in a DW fact table
    """
    def __init__(self, name, keyrefs, connection, measures=()):
        """
        :param name: Name of table
        :param keyrefs: List of attributes that are foreign keys to other
        tables
        :param connection: PEP249 connection to a database
        :param measures: List of attributes containing non-key values
        """
        self.name = name
        self.keyrefs = keyrefs
        self.measures = measures
        self.connection = connection
        if self.measures == ():
            self.all = self.keyrefs
        else:
            self.all = self.keyrefs + self.measures
        self.query = "SELECT " + ",".join(self.all) + " FROM " + self.name

    def __str__(self):
        text = "{} {} {}".format(self.name, self.keyrefs, self.measures)
        return text

    def __repr__(self):
        return self.__str__()

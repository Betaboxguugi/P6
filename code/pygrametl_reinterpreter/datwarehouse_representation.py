__author__ = 'Mathias Claus Jensen'


class DWRepresentation(object):
    def __init__(self, dims, fts, connection):
        self.dims = dims
        self.fts = fts


class TableRepresentation(object):
    def __iter__(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(self.query)
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
                    yield  dict(zip(names, row))
        finally:
            try:
                cursor.close()
            except Exception:
                pass

            
    def itercolumns(self, column_names):       
        for data in __iter__():
            result = {}
            for name in column_names:
                result.update({name: data[name]})
            yield result
        

class DimRepresentation(TableRepresentation):
    def __init__(self, name, key, attributes, lookupatts, connection):
        self.name = name
        self.key = key
        self.attributes = attributes
        self.lookupatts = lookupatts
        self.connection = connection
        self.all = [self.key] + self.attributes
        

class FTRepresentation(TableRepresentation):
    def __init__(self, name, keyrefs, measures, connection):
        self.name = name
        self.keyrefs = keyrefs
        self.measures = measures
        self.connection = connection

__author__ = 'Alexander'
__maintainer__ = 'Alexander'

# This file contains different functions to be used as workers in Step objects.
# Be adviced that not all functions can be used with all types of Step objects.
# Each function is marked with the type of Step that it can work for.


def cookbook_fix(att_value):  # For use with a MappingStep object
    """
    Arguments:
    - att_value: Value of a specific attribute from a row.
    Attribute specified to MappingStep along with cookbook_fix
    Return:
    - The value, which we wish the given attribute to be changed to.
    """
    if att_value == 'Cockbook':
        return 'Cookbook'


def split_timestamp(row):
    """Splits a timestamp containing a date into its three parts
    """

    # Splitting of the timestamp into parts
    timestamp = row['timestamp']
    timestamp_split = timestamp.split('/')

    # Assignment of each part to the dictionary
    row['year'] = timestamp_split[0]
    row['month'] = timestamp_split[1]
    row['day'] = timestamp_split[2]

def check_locationid(row):
 if not row['locationid']:
       raise ValueError("city was not present in the location dimension")
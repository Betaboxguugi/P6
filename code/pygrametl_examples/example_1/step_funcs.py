__author__ = 'Alexander'
__maintainer__ = 'Alexander'

# This file contains different functions to be used as workers in Step objects.
# Be adviced that not all functions can be used with all types of Step objects.
# Each function is marked with the type of Step that it can work for.

def split_timestamp(row): # For use with a Step object
    """
    Splits a timestamp containing a date into its three parts, creating new attributes.
    Arguments:
        - row: contains a timestamp attribute with entries of the form YY/MM/DD
    """

    # Splitting of the timestamp into parts
    timestamp = row['timestamp']
    timestamp_split = timestamp.split('/')

    # Assignment of each part to the dictionary
    row['year'] = timestamp_split[0]
    row['month'] = timestamp_split[1]
    row['day'] = timestamp_split[2]

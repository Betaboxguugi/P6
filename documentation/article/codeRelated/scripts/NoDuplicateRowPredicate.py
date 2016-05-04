NoDuplicateRowPredicate(table_name='logins',
                        column_names=
                            ['userid', 'usernames'],
                        column_names_exclude=False,
                        verbose=False)

# Also acceptable instantiation, which checks all columns in each row.
NoDuplicateRowPredicate(table_name='Address')
# Please work now
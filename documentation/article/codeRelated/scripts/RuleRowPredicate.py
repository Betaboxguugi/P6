def no_autos(name, title):
    return not name == title 

RuleRowPredicate(table_name=['AuthorDim','FactTable','BookDim']
                 constraint_function=no_autos,
                 column_names=['name', 'title'],
                 constraint_args=[],
                 column_names_exclude=False)
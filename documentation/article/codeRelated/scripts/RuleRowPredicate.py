def initials_id(aid, name):
    return aid == get_initials(name)

RuleRowPredicate(table_name='AuthorDim',
                 constraint_function=initials_id,
                 column_names=['aid', 'name'],
                 constraint_args=[],
                 column_names_exclude=False)
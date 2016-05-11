def no_forgotten_cities(city, old_city_name):
    return old_city_name not in city

RuleColumnPredicate(table_name='AuthorDim',
                    constraint_function=no_forgotten_cities,
                    column_names=['city'],
                    constraint_args=['Constantinople'],
                    column_names_exclude=False)

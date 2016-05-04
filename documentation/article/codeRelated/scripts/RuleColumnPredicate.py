def constraint1(a,b):
	if a > 20000 and b < 80:
		return true
	else:
		return false

RuleColumnPredicate(table_name='company',
                    constraint_function=constraint1,
                    column_names=['sales', 'age'],
                    return_list=None)
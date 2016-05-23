def run(self):
	pygrametl = self.scope['pygrametl']
	tables = pygrametl._alltables

	# Creates representation objects
        for table in tables:

            # If the table is a dimension.
            if self.check_table_type(table, DIM_CLASSES):
                if isinstance(table, TypeOneSlowlyChangingDimension):
                    dim = SCDType1DimRepresentation(table, self.dw_conn)
                elif isinstance(table, SlowlyChangingDimension):
                    dim = SCDType2DimRepresentation(table, self.dw_conn)
                else:
                    dim = DimRepresentation(table, self.dw_conn)
                self.dim_reps.append(dim)

            # If the table is a fact table
            elif self.check_table_type(table, FT_CLASSES):
                    ft = FTRepresentation(table, self.dw_conn)
                    self.fts_reps.append(ft)

	#SnowflakedDimensions
	snowflakes = []
	for x, value in self.scope.items():
		if isinstance(value, SnowflakedDimension):
			snowflakes.append(value)

	dw_rep = DWRepresentation(self.dim_reps, self.dw_conn, self.fts_reps, snowflakes)
	pygrametl._alltables.clear()

	return dw_rep
def run(self):
	pygrametl = self.scope['pygrametl']
	tables = pygrametl._alltables

	for table in tables:
		# If the table is a dimension.
		if self.check_table_type(table, DIM_CLASSES):
			# Create DimensionRepresentation and append to self.dim_reps
		# If the table is a fact table.
		elif self.check_table_type(table, FT_CLASSES):
			# Create FactTableRepresentation and append to self.ft_reps 

	#SnowflakedDimensions
	snowflakes = []
	for x, value in self.scope.items():
		if isinstance(value, SnowflakedDimension):
			snowflakes.append(value)

	dw_rep = DWRepresentation(self.dim_reps, self.dw_conn, self.fts_reps, snowflakes)
	pygrametl._alltables.clear()

	return dw_rep
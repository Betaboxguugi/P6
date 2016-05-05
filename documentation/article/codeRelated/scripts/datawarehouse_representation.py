def _find_structure(self):
	"""
	Re-creates the referencing structure of the DW.
	Reuses the referencing dicts from SnowflakedDimension objects,
	then builds upon them by finding the references between fact tables
	and dimensions.
	For this to work there are some restrictions to keep in mind:
	- Facttable may only refer to the root of a Snowflaked Dimension.
	- There may be no overlap between the dimensions of on Snowflaked
	  dimension and another.
	- Primary/Foreign key pairs have to share attribute name.

	:return: A dictionary where each key is a fact table or dimension,
	pointing to a set of dimensions, which it references.
	"""

	references = {}
	all_dims = set(self.dims)

	for flake in self.snowflakeddims:
		# Extends our references with internal snowflake refs
		rep_refs = {}
		for key, value in flake.refs.items():
			key = self._find_dim_rep(key, all_dims)
			l = set()
			for dim in value:
				l.add(self._find_dim_rep(dim, all_dims))
			rep_refs[key] = l

		references.update(rep_refs)
		for key, value in rep_refs.items():
			# Removes all non-root dimensions from the overall list of
			# dimensions, so that they cannot be referenced by fact tables.
			all_dims.difference_update(value)

	# For each fact table we find the set of all dimensions,
	# which it references.
	for ft in self.fts:
		ft_refs = set()
		for keyref in ft.keyrefs:
			for dim in all_dims:
				if keyref == dim.key:
					ft_refs.add(dim)
					break
		references[ft] = ft_refs

	return references


ReferentialIntegrityPredicate(
    refs={facttable: [BookDim, AuthorDim], AuthorDim: [CountryDim]},
    points_to_all=True,
    all_pointed_to=True
)

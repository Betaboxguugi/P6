SELECT aid, name, year, COUNT(*) 
FROM AuthorDim 
GROUP BY aid
HAVING COUNT(*) > 1 

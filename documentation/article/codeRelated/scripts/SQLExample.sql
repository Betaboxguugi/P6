SELECT t1.genre, t1.book FROM bookdim as t1, bookdim as t2 WHERE t1.genre = t2.genre AND ( (t1.book <> t2.book) )

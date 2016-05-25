from setup_dw import mk_dw
from setup_inputs_large import mk_author_db, mk_book_db, mk_country_csv
import sqlite3
import pygrametl
from pygrametl.datasources import SQLSource, CSVSource
from pygrametl.tables import FactTable, Dimension, SlowlyChangingDimension, \
    SnowflakedDimension

dw_path = './dw.db'
author_path = './author.db'
book_path = './book.db'
country_path = './country.csv'

mk_dw(dw_path)
mk_author_db(author_path)
mk_book_db(book_path)
mk_country_csv(country_path)

# Connections
dw_conn = sqlite3.connect(dw_path)
author_conn = sqlite3.connect(author_path)
book_conn = sqlite3.connect(book_path)
country_handle = open(country_path, "r")

wrapper = pygrametl.ConnectionWrapper(dw_conn)

# Sources
author_src = SQLSource(connection=author_conn, query="SELECT * FROM author")
book_src = SQLSource(connection=book_conn, query="SELECT * FROM book")
country_src = CSVSource(f=country_handle, delimiter=',')


# Tables
author_dim = Dimension(
    name='authordim',
    key='aid',
    attributes=['name', 'city', 'cid'])

book_dim = SlowlyChangingDimension(
    name='bookdim',
    key='bid',
    attributes=['title', 'year', 'version'],
    lookupatts=['title'],
    versionatt='version')

country_dim = Dimension(
    name='countrydim',
    key='cid',
    attributes=['country'],
    lookupatts=['country'])

fact_table = FactTable(
    name='facttable',
        keyrefs=['aid', 'bid'])

snowflake = SnowflakedDimension([(author_dim, country_dim)])

# We map cities to countries and populate the countrydim
cid_map = {}
for row in country_src:
    cid = (country_dim.ensure(row)) 
    cid_map[row['city']] = cid

# We populate the authordim and the fact table
for row in author_src:
    if row['city'] in ['Hadsten','Skanderborg','Kobenhavn']:
        row['cid'] = cid_map[row['city']]
    else:
        row['cid'] = None
    row['name'] = row['firstname'] + ' ' + row['lastname']
    row.pop('aid', 0) # Gets rid of aid so that pygrametl can generate them
    
    # Placing new row in author_dim
    row['aid'] = author_dim.ensure(row)

    # Placing new row in fact_table
    fact_table.ensure(row)
    
# Places books directly into book_dim
for row in book_src:
    book_dim.scdensure(row)

wrapper.commit()
wrapper.close()

author_conn.close()
book_conn.close()
country_handle.close()


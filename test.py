from pymysql import DATE
from sqlalchemy import create_engine, Float, Text, VARCHAR, JSON, BOOLEAN, func, DATETIME
from sqlalchemy import Table, Column, Integer, String, MetaData

db_name = 'bitech'
db_login = 'postgres'
db_password = 'nef441'
db_host = 'sw.neafiol.site'
db_port = 5432

# db_host = "3da.database.windows.net"
# db_name = "temp_3da"
# db_login = "renat_test_user"
# db_password = "R314n@t!"

engine = create_engine(f"postgresql://{db_login}:{db_password}@{db_host}/{db_name}", echo=False)
# engine = create_engine(f"mssql+pymssql://{db_login}:{db_password}@{db_host}/{db_name}", echo=True)

meta = MetaData()

calalog = Table(
    'SKUs_1', meta,
    Column('id', Integer, primary_key=True),
    Column('Name', VARCHAR(length=200)),
    Column('Weight', Float),
    Column('Richness', Float),
    Column('CategoryName', VARCHAR(length=200)),
    Column('SubCategoryName', VARCHAR(length=200)),
    Column('BrandId', VARCHAR(length=200)),
    Column('MappingKey', Integer),
    Column('AdditionName', VARCHAR(length=500)),
)

assortiment = Table(
    'SKUs_2', meta,
    Column('SKUId', Integer, primary_key=True),
    Column('UniqueName', VARCHAR(length=200)),
    Column('ChainName', VARCHAR(length=200)),
    Column('Name', VARCHAR(length=200)),
    Column('Weight', Float),
    Column('Richness', Float),
    Column('CategoryName', VARCHAR(length=200)),
    Column('SubCategoryName', VARCHAR(length=200)),
    Column('BrandName', VARCHAR(length=200)),
    Column('ManufacturerName', VARCHAR(length=200)),
    Column('UnitsTypeName', VARCHAR(length=200)),
    Column('BarCode', VARCHAR(length=500)),
    # Column('DateCreate', DATE),
)

searchresult = Table(
    'searchresult', meta,
    Column('id', Integer, primary_key=True),
    Column('orig_name', VARCHAR),
    Column('name', VARCHAR),
    Column('url', VARCHAR),
    Column('options', JSON, default=[]),
    Column('specifications', JSON, default={}),
    Column('done', BOOLEAN),
)

resulttable = Table(
    'resulttable', meta,
    Column('id', Integer, primary_key=True),
    Column('catalog_id', Integer),
    Column('item_id', Integer),
    Column('catalog_name', VARCHAR),
    Column('item_name', VARCHAR),
    Column('specifications', JSON, default={}),
    Column('score', Float),

)

# with engine.connect() as conn:
#     # s = calalog.all().count()
#     # s = func.count(calalog.catalog_id)
#
#     # result = conn.execute(s)
#     print(conn.)
# for row in result:
#     print(dict(row))
#
meta.create_all(engine)

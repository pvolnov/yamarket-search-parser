# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys
import urllib

from sqlalchemy import Table, Column, Integer, MetaData
from sqlalchemy import create_engine, Float, VARCHAR
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x

# Создание строки подлкючения к удалённой БД
print('Подключение к БД')
server = '3da.database.windows.ne'
database = 'temp_3da'
username = 'renat_test_user'
password = 'R314n@t!'

# db_host = "3da.database.windows.net"
# db_name = "temp_3da"
# db_login = "renat_test_user"
# db_password = "R314n@t!"

driver = '{ODBC Driver 17 for SQL Server}'
cnxn = urllib.parse.quote_plus(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# Создание объектно-реляционной модели базы
print('Подключение к БД')
Base = automap_base()
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(cnxn),
                       pool_recycle=3600,
                       echo=True
                       )

Base.prepare(engine, reflect=True, schema='test')
session = Session(engine)

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

# with engine.connect() as conn:
#     s = calalog.select().limit(10)
#     # s = func.count(calalog.catalog_id)
#     result = conn.execute(s)
#     for row in result:
#         print(dict(row))

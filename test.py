import sqlalchemy as sa
from sqlalchemy import Table, Integer, VARCHAR, Float, MetaData, Column, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_name = 'bitech'
db_login = 'SA'
db_password = 'Admin111'
db_host = 'localhost'

engine = sa.create_engine(f"mssql+pymssql://{db_login}:{db_password}@{db_host}/{db_name}", echo=False)
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

meta = MetaData()

DeclarativeBase = declarative_base()


class Tasts(DeclarativeBase):
    __tablename__ = 'tasks'
    metadata = meta

    id = Column(Integer, primary_key=True)
    orig_name = Column('name', sa.types.UnicodeText)

    def __repr__(self):
        return f"{self.id} {self.orig_name}"


class SearchResult(DeclarativeBase):
    metadata = meta
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    orig_name = Column('orig_name', UnicodeText)
    name = Column('name', UnicodeText)
    url = Column('url', UnicodeText)
    options = Column('options', UnicodeText)
    specifications = Column('specifications',UnicodeText)


# session.add(Tasts(orig_name='Millstream Питьевая вода негазированная Оштен, 500 мл*От 6-ти бутылок'))
# session.add(Tasts(orig_name='Вода BONAQUA ГАЗ./НЕГАЗ. 1Л'))
# session.add(Tasts(orig_name='Тест русского'))
# session.commit()
#
for post in session.query(SearchResult):
    print(post.orig_name,post.name)

# SearchResult.__table__.drop(engine)

meta.create_all(engine)

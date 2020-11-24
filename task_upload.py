import json
import re

import pandas as pd
import sqlalchemy as sa
from sqlalchemy import Integer, MetaData, Column, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs import db_ms_login, db_ms_password, db_ms_host, db_ms_name
from parser.Models import SearchResult, MergeData

engine = sa.create_engine(f"mssql+pymssql://{db_ms_login}:{db_ms_password}@{db_ms_host}/{db_ms_name}", echo=False)
connection = engine.connect()

Session = sessionmaker(bind=engine)
meta = MetaData()
DeclarativeBase = declarative_base()


class Tasts(DeclarativeBase):
    __tablename__ = 'tasks'
    metadata = meta

    id = Column(Integer, primary_key=True)
    orig_name = Column('name', sa.types.UnicodeText)

    def __repr__(self):
        return f"{self.id} {self.orig_name}"


class Result(DeclarativeBase):
    metadata = meta
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    orig_name = Column('orig_name', UnicodeText)
    name = Column('name', UnicodeText)
    url = Column('url', UnicodeText)
    options = Column('options', UnicodeText)
    specifications = Column('specifications', UnicodeText)


# new_post = Post(orig_name='Two record')
# # Добавляем запись
# session.add(new_post)
# session.commit()
def get_current_tasks():
    session = Session()
    tasks = []
    for task in session.query(Tasts):
        tasks.append(task.orig_name)
    return tasks


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--export", action="store_true", dest="file_load_path")
    parser.add_argument("-e", "--export", action="store_true", dest="file_export_path")
    parser.add_argument("-s", "--status", action="store_true", dest="show_status")
    parser.add_argument("-i", "--init", action="store_true", dest="init")

    args = parser.parse_args()

    if args.init:
        MergeData.create_table()
        SearchResult.create_table()
        meta.create_all(engine)

        print("Table created")

    if args.show_status:
        n = SearchResult.select().where(SearchResult.done == True).count()
        n1 = SearchResult.select().count()
        print(f"Loaded {n}/{n1} tasks")

    if args.file_load_path:
        data = get_current_tasks()
        n = SearchResult.insert_many([{"orig_name": line} for line in data]).on_conflict_ignore().execute()
        print(f"Added {len(data)} tasks")

    if args.file_export_path:
        data = get_current_tasks()
        print(f"Export {len(data)} items begin")

        items = SearchResult.select().where(SearchResult.orig_name.in_(data)).execute()

        session = Session()
        for it in items:
            session.add(Result(orig_name=it.orig_name, name=it.name, url=it.url, options=json.dumps(it.options),
                               specifications=json.dumps(it.specifications)))
        session.commit()

        pd.DataFrame.from_records([{"orig_name": i.orig_name,
                                    "name": i.name,
                                    "url": i.url,
                                    "volume": re.findall(r"\d+,?\d*", i.orig_name)[0] if len(
                                        re.findall(r"\d+,?\d*", i.orig_name)) else "",
                                    "options": ";".join([o["name"] for o in i.options]),
                                    **i.specifications
                                    } for i in items]).to_csv("result.csv")
        print(f"complete {len(items)} tasks")

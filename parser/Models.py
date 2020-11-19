from peewee import Model, TextField, BooleanField, IntegerField
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField

from configs import *

db = PostgresqlExtDatabase(db_name, user=db_login, password=db_password,
                           host=db_host, port=db_port)


class SearchResult(Model):
    orig_name = TextField(unique=True)
    name = TextField(default="")
    url = TextField(default="")
    options = JSONField(default=[])
    specifications = JSONField(default={})
    done = BooleanField(default=False)

    class Meta:
        database = db


class MergeData(Model):
    catalog_name = TextField(default="")
    item_name = TextField(default="")
    type = TextField(default="")
    fatness = TextField(default="")
    sort = TextField(default="")
    fasofka = TextField(default="")
    milk_type = TextField(default="")
    cheese_type = TextField(default="")
    weight = TextField(default="")
    score = IntegerField()
    sure = BooleanField(default=False)

    class Meta:
        database = db


# print(SearchResult.select().where(SearchResult.done == False).count())
# MergeData.drop_table()
# MergeData.create_table()
# SearchResult.create_table()
# n = SearchResult.update({SearchResult.done:False}).where(SearchResult.url=="").execute()
# print(n)
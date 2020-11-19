from peewee import Model, IntegerField, BooleanField, DateTimeField, TextField, CharField, FloatField
# from peewee_mssql import MssqlDatabase
from playhouse.postgres_ext import ArrayField, JSONField

db = MssqlDatabase('temp_3da', host='3da.database.windows.net', user='renat_test_user',
                   password='R314n@t!', port=1433)


class Catalog(Model):
    SKUId = IntegerField()
    Name = CharField(max_length=200)
    Weight = FloatField()
    Richness = FloatField()
    CategoryName = CharField(max_length=200)
    SubCategoryName = CharField(max_length=200)
    BrandId = CharField(max_length=200)
    MappingKey = CharField(max_length=500)
    MarketShareSKUId = IntegerField()
    AdditionName = CharField(max_length=500)

    class Meta:
        database = db
        db_table = 'SKUs_1'


print(Catalog.select().count())

from sqlalchemy import create_engine, MetaData, Table
import json

engine = create_engine('sqlite:///dm.sqlite')
metadata = MetaData(bind=engine)
conn = engine.connect()
searched = Table('searchresult', metadata, autoload=True)

raw_data = searched.select().execute()
data = [{x.keys()[i]: x[i] for i in range(len(x))} for x in raw_data]

print(data[0].keys())
k = set()
names = set()
for i in data:
	#print(i)
	names.add(i["name"])
	for j in list(json.loads(i["specifications"].replace('\\\\','\\')).keys()):
	    k.add(j)

print(names)
print()
print(k)

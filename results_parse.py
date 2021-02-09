from sqlalchemy import create_engine, MetaData, Table
import json
import csv

engine = create_engine('sqlite:///dm.sqlite')
metadata = MetaData(bind=engine)
conn = engine.connect()
searched = Table('searchresult', metadata, autoload=True)

raw_data = searched.select().execute()
data = [{x.keys()[i]: x[i] for i in range(len(x))} for x in raw_data]

key = set()
for i in data:
    # print(i["name"], i["url"])
    for j in list(json.loads(i["specifications"].replace('\\\\', '\\')).keys()):
        key.add(j)

res = list()
for i in data:
    dct = dict()
    if len(json.loads(i["specifications"].replace('\\\\', '\\')).values()) == 0:
        continue
    for j in sorted(key):
        try:
            dct.update({j: json.loads(i["specifications"].replace('\\\\', '\\'))[j]})
        except KeyError:
            continue
    res.append(dct)

with open("parsed_spec.csv", 'w') as f:
    w = csv.DictWriter(f, sorted(key), dialect="excel")
    w.writeheader()
    for i in res:
        w.writerow(i)

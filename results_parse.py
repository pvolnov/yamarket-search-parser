from sqlalchemy import create_engine, MetaData, Table
import json
from configs import db_ms_login, db_ms_password, db_ms_host, db_ms_name

engine = create_engine(f"mysql+pymysql://{db_ms_login}:{db_ms_password}@{db_ms_host}/{db_ms_name}", echo=False)
metadata = MetaData(bind=engine)
conn = engine.connect()
searched = Table('searchresult', metadata, autoload=True)
prs = Table('edadeal_parsed_uniq', metadata, autoload=True)

raw_data = searched.select().execute()
data = [{x.keys()[i]: x[i] for i in range(len(x))} for x in raw_data]

key = set()
for i in data:
    try:
        for j in list(json.loads(i["specifications"].replace('\\\\', '\\')).keys()):
            key.add(j)
    except AttributeError as err:
        print(err)

res = list()
for i in data:
    dct = {"orig_name": i["orig_name"]}
    try:
        if len(json.loads(i["specifications"].replace('\\\\', '\\')).values()) == 0:
            continue
        for j in sorted(key):
            try:
                dct.update({j: json.loads(i["specifications"].replace('\\\\', '\\'))[j]})
            except KeyError:
                continue
        res.append(dct)
    except AttributeError as err:
        print(err)

for r in res:
    dct = {"ya_category" if i == "category" else i: r[i] if i in r.keys() else None for i in ["brend",
                                                                                              "category",
                                                                                              "Вкус",
                                                                                              "Напиток",
                                                                                              "Степень",
                                                                                              "Газированная",
                                                                                              "Упаковка"]}
    prs.update().values(**dct).where(prs.c.name == r["orig_name"]).execute()
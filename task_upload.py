import json
import re

from playhouse.shortcuts import model_to_dict
import pandas as pd

from parser.Models import SearchResult, MergeData

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--load_from_file", default=None, dest="file_load_path",
                        help="File, contains colemn 'orig_name'",
                        type=str)

    parser.add_argument("-e", "--export", default=None, dest="file_export_path",
                        help="File, contains colemn 'orig_name'",
                        type=str)

    parser.add_argument("--server", default="dig7.neafiol.site", dest="selenoid_ip",
                        help="Server with selenoid",
                        type=str)
    parser.add_argument("-s", "--status", action="store_true", dest="show_status")
    parser.add_argument("-i", "--init", action="store_true", dest="init")

    args = parser.parse_args()

    if args.init:
        MergeData.create_table()
        SearchResult.create_table()
        print("Table created")

    if args.show_status:
        n = SearchResult.select().where(SearchResult.done == True).count()
        n1 = SearchResult.select().count()
        print(f"Loaded {n}/{n1} tasks")

    if args.file_load_path:
        data = list(pd.read_csv(args.file_load_path)["orig_name"])
        n = SearchResult.insert_many([{"orig_name": line} for line in data]).on_conflict_ignore().execute()
        print(f"Added {len(data)} tasks")

    if args.file_export_path:
        data = list(pd.read_csv(args.file_export_path)["orig_name"])
        print(f"Export {len(data)} items begin")
        items = SearchResult.select().where(SearchResult.orig_name.in_(data)).execute()

        pd.DataFrame.from_records([{"orig_name":i.orig_name,
                                 "name":i.name,
                                 "url":i.url,
                                 "volume":re.findall(r"\d+,?\d*",i.orig_name)[0] if len(re.findall(r"\d+,?\d*",i.orig_name)) else "",
                                 "options":";".join([o["name"] for o in i.options]),
                                 **i.specifications
                                 } for i in items]).to_csv("result.csv")
        print(f"complete {len(items)} tasks")

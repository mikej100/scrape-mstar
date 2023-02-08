import os
from pymongo import MongoClient


class SecuritiesDb:

    def __init__(self):
        self.client = MongoClient(os.environ["MONGO_CONN_STRING"])
        self.coll = self.client.mstar.scraped_items

    def get_latest_crawl(self):
        cursor = self.coll.find({}, {"run_id": 1, "_id": 0}).sort(
            "run_id", -1).limit(1)
        latest_crawl_id = cursor.next()["run_id"]
        return latest_crawl_id

    def get_crawl_all(self, crawl_id):
        cursor = self.coll.find({"run_id": f"{crawl_id}"})
        docs = list(cursor)
        return docs

# if __name__ == "main":

import os
import time
from pymongo import MongoClient


class SecuritiesDb:

    def __init__(self):
        self.client = MongoClient(os.environ["MONGO_CONN_STRING"])
        self.coll = self.client.mstar.scraped_items

    def get_latest_crawl(self):
        cursor = self.coll.find({}, {"src_meta.run_id": 1, "_id": 0}).sort(
            "src_meta.run_id", -1).limit(1)
        latest_crawl_id = cursor.next()["src_meta"]["run_id"]
        return latest_crawl_id

    def get_crawl_all(self, crawl_id):
        cursor = self.coll.find({"src_meta.run_id": f"{crawl_id}"})
        docs = list(cursor)
        return docs

    def wait_for_crawl(self, crawl_id, timeout=30):
        interval = 0.5
        timetaken = 0
        while timetaken < timeout:
            if self.get_latest_crawl() == crawl_id:
                return timetaken
            timetaken = timetaken + interval
            time.sleep(interval)
        return -timeout
# if __name__ == "main":

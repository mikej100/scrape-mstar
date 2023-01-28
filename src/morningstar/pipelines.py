import os
from pymongo import MongoClient
from scrapy.conf import settings
from scrapy import log
from scrapy import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MorningstarPipeline:
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(slef):
        connection = MongoClient(os.environ["MONGO_CONN_STRING"])
        db = connection(settings['MONGODB_DB'])
        self.collection = db[settings["MONGODB_COLLECTION"]]

    def process_item(self, item, spider):
        value = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!", format(data))
            if valid:
                self.collection.insert(dict(item))
                log.msg("Document added to MongoDB database",
                    level=log.DEBUG, spider=spider)
            return item


import logging
import os
from pymongo import MongoClient
class Fx:


    def __init__(self, currencies = "GBPUSD"):
        self.currencies = currencies
        logger = logging.getLogger("fx")

        client = MongoClient(os.environ["MONGO_CONN_STRING"]) 
        db_names = client.list_database_names()
        logger.debug(f"MongoDB database names {db_names}")

        db = client.test 
        coll = db.fx_gbpusd
        doc = coll.find_one()
        time = doc["time"]
        doc["ver"]


        aa = 21

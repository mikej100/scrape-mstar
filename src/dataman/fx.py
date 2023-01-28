import sys
#import functools
#print (functools.reduce(lambda a,b:a+"\n\t"+b, sys.path, "sys path: "))
import logging
import os
from pymongo import MongoClient
import datetime
import dateutil.parser as dparser

logger = logging.getLogger("fx")

def posixdtime_to_mm(px_dtime):
    """ Convert POSIX time to minutes format used by EA Trading Academy
        data source, which is minutes after a different base date (mm).
        Base date
        posix: seconds after 1970-0101T00:00
        python date: days after 0001-01-01
        mm seems to be minutes after  1800-01-01T00:00

        :type px_time: datetime object
        :return: minutes after base date
        :rtype: integer
        """
    px_stamp = px_dtime.timestamp()
    base_mm = 946771200    # seconds difference between baselines
    return int((px_stamp - base_mm) / 60)


def posixtimestamp_to_mm(px_timestamp):
    dt = datetime.datetime.fromtimestamp(px_timestamp)
    return posixdtime_to_mm(dt) 


def pydate_to_mm(pydate):
    """ Convert python date ordinal to minutes format used by EA Trading Academy
        data source, which is minutes after a different base date.

        :param pydate_ord: python date in ordinal form
        :type px_time: integer
        :return: minutes after base date
        :rtype: integer
        """
    dt = datetime.datetime.fromordinal( pydate.toordinal() ) 
    return posixdtime_to_mm(dt)


def xldate_to_mm(xldate):
    """ Convert xl date number to minutes format used by EA Trading Academy
        data source, which is minutes after a different base date.

        :param pydate_ord: xl date 
        :type px_time: integer
        :return: minutes after base date
        :rtype: integer
        """
    logger.info(f"xldate_to_mm xldate: {xldate}")
    xl_base = dparser.parse("1900-01-01T00+00").date().toordinal()
    dt = datetime.datetime.fromordinal(xldate + xl_base -2 )
    return posixdtime_to_mm(dt)

def xldate_to_pxdtime(xldate):
    xl_base = dparser.parse("1900-01-01T00+00").date().toordinal()
    dt = datetime.datetime.fromordinal(xldate + xl_base -2 )
    return (dt)

class Fx:


    def __init__(self, currencies = "GBPUSD"):
        self.currencies = currencies

        client = MongoClient(os.environ["MONGO_CONN_STRING"]) 
        db_names = client.list_database_names()
        logger.debug(f"MongoDB database names {db_names}")

        fx = client.test.fx_gbpusd.find_one()

        self.fxtime = fx["time"]
        self.fxclose = fx["close"]

    def rate(self, px_dtime):
        mm_time = posixdtime_to_mm( px_dtime )

        # TODO review this clumsy coding
        fx_match = next(filter( lambda t: t > mm_time, self.fxtime), False)
        index = self.fxtime.index(fx_match)
        fx = self.fxclose[index]
        return fx



if __name__ == "__main__":
    xl_date = int(sys.argv[1])
    fx = Fx()
    px_dtime = xldate_to_pxdtime(xl_date)
    fxrate = fx.rate(px_dtime)
    sys.exit(fxrate)


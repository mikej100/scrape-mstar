from hamcrest import *
import logging
import logging.config
import yaml

with open("./logging.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.debug("Testing")

import datetime

#from morningstar.spiders.Securities_spiders import FundsSpider
import run_securities as rs

def test_run_consolidated_funds_spider():
    crawl_id = "test_crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    symbols = '{"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}'
    rs.run_securities(symbols, crawl_id)
    pass
   

from hamcrest import *
import logging
import logging.config
import yaml

from dataman import crawl_data

with open("./logging.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.debug("Testing")

import datetime

#from morningstar.spiders.Securities_spiders import FundsSpider
import run_securities as rs

def test_run_single_security_of_each_type_spider():
    crawl_id = "crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    symbols = '{"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}'
    rs.run_securities(symbols, crawl_id)

    secdb = crawl_data.SecuritiesDb()
    timer = secdb.wait_for_crawl(crawl_id)
    all_data = secdb.get_crawl_all(crawl_id)
    assert_that(timer, is_(greater_than_or_equal_to(0)))
   
def test_run_single_fund_spider():
    crawl_id = "crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    symbols = '{"fund_symbols": ["F000013G37"], "cef_symbols": [], "equity_symbols": []}'
    rs.run_securities(symbols, crawl_id)

    secdb = crawl_data.SecuritiesDb()
    timer = secdb.wait_for_crawl(crawl_id)
    all_data = secdb.get_crawl_all(crawl_id)
    assert_that(timer, is_(greater_than_or_equal_to(0)))

def test_DISABLED_run_all_securities_on_spider():
    return True # Switch test off as it consumes lots of resource
    crawl_id = "test_crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    symbols = '{"fund_symbols": ["F00000X2PR", "F000013G37", "F00000VQUU", "F00000U58R", "F00000H2TK", "F00000GWFO", "F00000GWFO", "F0GBR053M8", "F00000UE35", "F00000SX2A", "F00000JOLL", "F00000OTJO", "0P0001HPYK", "F00000XSS0", "F0000103JP", "F0GBR06HUW", "F0GBR04SAT", "F00000XHC4", "F00000OSWG", "F00000MWKK", "F00000PTMF", "F0GBR06I60", "F0GBR053MY", "F00000JWH9", "F00000PBFG", "F0000045LU", "F00000P869", "F00000P86D", "F00000NQ9V", "F00000NQ9X", "F00000PW29", "F0GBR04H80", "F00000YQSV", "F00000OU8T", "F00000ZTV1", "F00000XWYA", "F00000ZDCD", "F00000MLUS", "F00000MLUM", "F00000PZUV", "F000003YD7"], "cef_symbols": ["F000011FTC", "F000000JUY", "E0GBR01Q40", "F00000Q7PL"], "equity_symbols": ["0P0000004C", "0P0001DWW4", "0P0001C5WG", "0P00008ZNF", "E0GBR01R9F", "0P00007OK1", "0P000003MH", "0P000187DJ", "0P00016CGN", "0P0000WDY1", "0P00007Z3Q", "0P00007OY0"]}'
    
    rs.run_securities(symbols, crawl_id)

    secdb = crawl_data.SecuritiesDb()
    timer = secdb.wait_for_crawl(crawl_id)
    logger.info("Scrapy run for all securities took about {timer}s")
    all_data = secdb.get_crawl_all(crawl_id)
    assert_that(timer, is_(greater_than_or_equal_to(0)))

    
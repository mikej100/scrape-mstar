from hamcrest import *
import logging

import scrapyd_manager
import scrape_utils


# with open("./logging.yaml", "r") as stream:
#     config = yaml.load(stream, Loader=yaml.FullLoader)
# logging.config.dictConfig(config)


logger = logging.getLogger(__name__)


#from morningstar.spiders.Securities_spiders import FundsSpider
import run_securities as rs

def test_delete_twistd_pid_file():
    """This is not a automatest.
    You need to create a pid file by running and crashing scrapyd and 
    check this deletes it.
    """    
    scrapyd_mgr = scrapyd_manager.ScrapydManager()
    scrapyd_mgr.delete_pid_file()
    pass


def test_is_scrapy_running():
    scrapyd_mgr = scrapyd_manager.ScrapydManager()
    logger.debug("test_is_scrapy_running")
    result = scrapyd_mgr.is_running()
    pass


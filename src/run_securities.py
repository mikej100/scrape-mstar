from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from morningstar.spiders.Securities_spiders import FundsSpider
import logging


def run_securities(symbols, run_id=""):
    logger = logging.getLogger("Run_securities")
    logger.info('Starting')
    process = CrawlerProcess(get_project_settings())

    process.crawl(FundsSpider, symbols=symbols, run_id=run_id)
    process.start()
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.morningstar.spiders.Securities_spiders import Funds1Spider, Funds2Spider, Funds3Spider
import logging


def run_securities(symbols, run_id=""):
    logger = logging.getLogger("Run_securities")
    logger.info('Starting')
    spider_list = [Funds1Spider, Funds2Spider, Funds3Spider]

    # process = CrawlerProcess(get_project_settings())
    process = CrawlerProcess(get_project_settings())

    for spider in spider_list:
        process.crawl(spider, symbols=symbols, run_id=run_id)
    process.start()
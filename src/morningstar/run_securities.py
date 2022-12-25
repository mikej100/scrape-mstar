from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.Securities_spiders import Funds1Spider, Funds2Spider, Funds3Spider
import logging

logger = logging.getLogger("Run_securities")
logger.info('Starting')

#process = CrawlerProcess(get_project_settings())
process = CrawlerProcess(
         settings={
            "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
             "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
             "DOWNLOAD_HANDLERS": {
                 "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                 "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
             },
             "CONCURRENT_REQUESTS": 32,
             "FEED_URI":'Products.jl',
             "FEED_FORMAT":'jsonlines',
             "LOG_FILE" : "logs/scrapy.log"
         }
     )
process.crawl(Funds1Spider)
process.start()
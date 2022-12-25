from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.LinuxPWright import LinuxPWright
import logging

logger = logging.getLogger("RunScript")
logger.info('Starting playwright prototype requests')

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
         }
     )
process.crawl(LinuxPWright)
process.start()
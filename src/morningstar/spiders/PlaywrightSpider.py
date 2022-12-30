import scrapy
import re
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import asyncio

logger = logging.getLogger("runScript")

class PlaywrightSpider(scrapy.Spider):
    name = "playwright1"
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def start_requests(self):
        url_1 = "https://docs.scrapy.org/en/latest/index.html"
        logger.info('Starting playwright prototype requests')

        yield scrapy.Request(
                url=url_1,
                meta={"playwright": True}
                )

    def parse(self, response):
        self.logger.info('Playwright parsing Scrapy docs')
        nav_text_list = response.xpath("//div[@role='navigation']/ul/li/text()").getall()
        nav_text = "".join(nav_text_list)
        latest_version = re.search( r"Scrapy.(\d+\.\d+)", nav_text).group(1)
        data = { "latest_version" : latest_version }
        yield data

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    process = CrawlerProcess(
             settings={
                "LOG_FILE": 'morningstar\logs\scrapy.log',
                "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
                 "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
                 "DOWNLOAD_HANDLERS": {
                     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                 },
                 "CONCURRENT_REQUESTS": 32,
                 "FEED_URI":'scrapyscrape.jl',
                 "FEED_FORMAT":'jsonlines',
             }
         )
    process.crawl(PlaywrightSpider)
    process.start()
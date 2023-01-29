from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.morningstar.spiders.Securities_spiders import Funds1Spider, Funds2Spider, Funds3Spider
import logging

def run_securities(symbols, crawl_id=""):
    logger = logging.getLogger("Run_securities")
    logger.info('Starting')

    #process = CrawlerProcess(get_project_settings())
    process = CrawlerProcess(get_project_settings())
#l             settings={
#l                "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
#l                 "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
#l                 "DOWNLOAD_HANDLERS": {
#l                     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#l                     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#l                 },
#l                 "CONCURRENT_REQUESTS": 32,
#l                 "FEED_URI": f"./data/securities_data_{crawl_id}.json",
#l                 "FEED_FORMAT":'jsonlines',
#l                 "LOG_FILE" : "logs/scrapy.log"
#l             }
    process.crawl(Funds1Spider, symbols=symbols)
    process.start()

# if __name__ == "__main__":
#     #symbols =  '{"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}'
#     symbols =  '{"fund_symbols": ["F000013G37"], "cef_symbols": [], "equity_symbols": ["0P0000004C"]}'
#     run_securities(symbols,"1")
import scrapy
import re
import numpy as np
import logging
import datetime
import json
from scrapy_playwright.page import PageMethod

# pylint:disable=no-member  
"""Base Morningstar urls for the specific security types.
"""
logger = logging.getLogger("Securities_spiders")
logger.info('Starting')

url_fund = "https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id={sym}&tab={view}"
url_cef = "https://www.morningstar.co.uk/uk/report/cef/quote.aspx?t={sym}&tab={view}"
url_equity = "https://tools.morningstar.co.uk/uk/stockreport/default.aspx?tab=0{view}&SecurityToken={sym}%5d3%5d0%5dE0WWE$$ALL"

class FundsSpider(scrapy.Spider):
    name = "funds_all"
    logger.info('Start_request next line')
    
    def start_requests(self):
        symbols = json.loads(self.symbols)

        src_meta_fs = dict( src = "mstar", run_id=self.run_id,
                        security_type="fund", scrape_type="summary")

        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(
                callback=self.parse_funds_summ,
                url=url_fund.format(sym=symbol, view="0"),
                cb_kwargs=dict(symbol=symbol, src_meta=src_meta_fs)
            )
        #======================================
        src_meta_cs = dict( src = "mstar", run_id=self.run_id,
                        security_type="cef", scrape_type="summary")
        for symbol in symbols['cef_symbols']:
            yield scrapy.Request(
                callback=self.parse_cefs_summ,
                url=url_cef.format(sym=symbol, view="0"),
                meta= dict(
                    playwright = True,
                    playwright_include_page = True,
                    playwright_page_methods = 
                        [PageMethod('wait_for_selector', 'span.as-of')]
                ),
                cb_kwargs=dict(symbol=symbol, src_meta=src_meta_cs)
            )

        #======================================
        src_meta_es = dict( src = "mstar", run_id=self.run_id,
                        security_type="equity", scrape_type="summary")
        for symbol in symbols['equity_symbols']:
            yield scrapy.Request(
                callback=self.parse_equities_summ,
                url=url_equity.format(sym=symbol, view=""),
                cb_kwargs=dict(symbol=symbol, src_meta=src_meta_es)
            )

        #======================================

        src_meta_fp = dict( src = "mstar", run_id=self.run_id,
                        security_type="fund", scrape_type="performance")
        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(
                callback=self.parse_funds_perf,
                url=url_fund.format(sym=symbol, view="1"),
                cb_kwargs=dict(symbol=symbol, src_meta=src_meta_fp)
            )
        #======================================
        src_meta_cp = dict( src = "mstar", run_id=self.run_id,
                        security_type="cef", scrape_type="performance")
        for symbol in symbols['cef_symbols']:
            yield scrapy.Request(
                callback=self.parse_cef_perf,
                url=url_cef.format(sym=symbol, view="1"),
                cb_kwargs=dict(symbol=symbol, src_meta=src_meta_cp)
            )

        #======================================

        src_meta_ep = dict( src = "mstar", run_id=self.run_id,
                        security_type="equity", scrape_type="performance")
        for symbol in symbols['equity_symbols']:
            yield scrapy.Request(
                callback=self.parse_equities_perf,
                url=url_equity.format(sym=symbol, view="&vw=pf"),
                cb_kwargs=dict(symbol=symbol, src_meta=src_meta_ep)
            )

        #======================================
        src_meta_fr = dict( src = "mstar", run_id=self.run_id,
                        security_type="fund", scrape_type="risk")
        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(
                callback=self.parse_funds_rating,
                url=url_fund.format(sym=symbol, view="2"),
                cb_kwargs=dict(symbol=symbol, src_meta=src_meta_fr)
            )


    def parse_funds_summ(self, response, symbol, src_meta):
        self.logger.info('Parsing funds summary')
        isin_text = response.xpath("//td[text()='ISIN']/following-sibling::*/text()").getall()[1]
        name_text = response.xpath("//div[@class='snapshotTitleBox']/h1/text()").getall()[0]

        price_elems =  response.xpath("//td[text()='NAV']/following-sibling::*/text()").getall()
        if len(price_elems) > 1 :
            price_text = price_elems[1]
            date_text =  response.xpath("//td[text()='NAV']/span/text()").get()
        else:
            # Some funds have Closing Price rather than NAV
            price_text =  response.xpath("//td[text()='Closing Price']/following-sibling::*/text()").getall()[1]
            date_text =  response.xpath("//td[text()='Closing Price']/span/text()").get()

        top_region_text =response.xpath("//div[@id='overviewPortfolioTopRegionsDiv']//td/text()").getall()
        top_sectors_text =response.xpath("//div[@id='overviewPortfolioTopSectorsDiv']//td/text()").getall()
        asset_allocation_text =response.xpath("//div[@id='overviewPortfolioAssetAllocationDiv']//td/text()").getall()

        if len(top_region_text) >0 :
            tmp_table = np.asarray(top_region_text).reshape(6,2)
            tr_data = {"region": tmp_table[1:, 0].tolist(), "allocation": tmp_table[1:,1].tolist()}
        else:
            tr_data = "n/a"

        if len(top_sectors_text) >0 :
            tmp_table = np.asarray(top_sectors_text).reshape(6,2)
            ts_data = {"sector": tmp_table[1:, 0].tolist(), "allocation": tmp_table[1:,1].tolist()}
        else:
            ts_data = "n/a"

        if len(asset_allocation_text) >0 :
            tmp_table = np.asarray(asset_allocation_text[1:]).reshape(6,4)
            aa_data = {"type": tmp_table[1:, 0].tolist(), "allocation": tmp_table[1:,3].tolist()}
        else:
            aa_data = "n/a"
        # aa_json = aa_df.to_json(orient="records")

        src_meta.update({"created": datetime.datetime.now().timestamp()})
        data = {
            "symbol": symbol,
            "src_meta": src_meta,
            "isin" : isin_text,
            "name": name_text,
            "price": re.search(r"[0-9]+\.?[0-9]+",price_text).group(),
            "currency" : re.search("^.{3}", price_text).group(),
            "date": date_text,
            "asset_allocation": aa_data,
            "top_region": tr_data,
            "top_sectors": ts_data
            }
        yield data

    async def parse_cefs_summ(self, response, symbol, src_meta):
        page = response.meta['playwright_page']
        await page.screenshot(
            path= 'logs/screenshot%s.png' % datetime.datetime.now().strftime('%Y%m%dT%H%M%S'),
            full_page=True)
        await page.close()

        # info under chart with currency and date.
        info_text = response.xpath("//div[@class='sal-mip-quote__indicate']//text()").getall()

        data = {
            "symbol": symbol,
            "src_meta": src_meta,
            #"isin" : isin_text,
            "name": response.xpath("//span[@class='sal-component-title1']//text()").get(),
            "price": response.xpath("//div[contains(text(), 'Last Closing Share Price')]/..//text()").getall()[2],
            "currency" : info_text[0],
            "date": re.search(r"\d{2}/\d{2}/\d{4}", info_text[6]).group()
            }
        yield data


    def parse_equities_summ(self, response, symbol, src_meta):
        # Cannot fetch the following data from page
        # sector_text = response.xpath("//h3[text()='Sector']/parent::*/text()").getall()
        time_text = response.xpath("//p[@id='Col0PriceTime']/text()").get()
        isin_text =	response.xpath("//td[@id='Col0Isin']/text()").getall()[0]
        price_text = response.xpath("//span[@id='Col0Price']/text()").getall()[0]
        price_info_text = response.xpath("//p[@id='Col0PriceTime']/text()").getall()  

        currency = re.search(r"\|\s(\w{3})", price_info_text[2]).group(1)
        yield {
            "symbol": symbol,
            "src_meta": src_meta,
            "isin" : isin_text,
            "name": response.xpath("//span[@class='securityName']/text()").get(),
            "price": price_text,
            "currency" : currency,
            "date": re.search(r"\d{2}/\d{2}/\d{4}", price_info_text[0]).group()
        }

    def parse_funds_perf(self, response, symbol, src_meta):
        tr_ret_text =  response.xpath(
            "//table[contains(@class, 'returnsTrailingTable')]//td[contains(@class, 'col2')]//text()") \
            .getall()
        values = [item for item in tr_ret_text[1:9]]
        periods = [ '1d', '1w', '1m', '3m', '6m', 'ytd', '1y', '3y']
        trailing_returns = dict( zip( periods, values))

        data = {
            "symbol" : symbol,
            "src_meta": src_meta,
            "trailing_returns" : trailing_returns
            }
        yield data

    def parse_cef_perf(self, response, symbol, src_meta):
        tr_price_text = response.xpath(
            "//div[@id='TrailingReturns']//tr[@class='rowSecurity']//text()") .getall()
        tr_nav_text = response.xpath(
            "//div[@id='TrailingReturns']//tr[@class='rowNav alternate']//text()").getall()

        periods = [ '1d', '1w', '1m', '3m', '6m', '1y', '3y', '5y', '10y']

        tr_price_values = [item for item in tr_price_text[1:10]]
        trailing_returns_price = dict( zip( periods, tr_price_values))

        tr_nav_values = [item for item in tr_nav_text[1:10]]
        trailing_returns_nav = dict( zip( periods, tr_nav_values))

        data = {
            "symbol" : symbol,
            "src_meta": src_meta,
            }
        yield data


    def parse_equities_perf(self, response, symbol, src_meta):
        tr_text = response.xpath(
            "//div[@id='TrailingReturns']//tr[@class='rowSecurity']//text()") .getall()

        periods = [ '1m', '3m', '1y', '3y', '5y', '10y', 'ytd']

        tr_values = [item for item in tr_text[1:8]]
        trailing_returns = dict( zip( periods, tr_values))

        yield {
            "symbol" : symbol,
            "src_meta": src_meta,
            "trailing_returns" : trailing_returns
        }

    def parse_funds_rating(self, response, symbol, src_meta):

        sharpe_text =  response.xpath(
             "//td[text()='3-Yr Sharpe Ratio']/following-sibling::td/text()") .get()

        beta_text = response.xpath(
            "//td[text()='3-Yr Beta']/following-sibling::td/text()").getall()

        alpha_text = response.xpath(
            "//td[text()='3-Yr Alpha']/following-sibling::td/text()").getall()

        data = {
            "symbol" : symbol,
            "src_meta": src_meta,
            "sharpe" : sharpe_text,
            "beta_standard": beta_text[0],
            "beta_best_fit": beta_text[1],
            "alpha_standard": alpha_text[0],
            "alpha_best_fit": alpha_text[1]
            }
        yield data

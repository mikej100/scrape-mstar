import scrapy
import re
import pandas as pd
import numpy as np
from os.path import exists
from . import investmentsbook as ib

"""Base Morningstar urls for the specific security types.
"""
url_funds = "https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id={sym}&tab={view}"
url_cefs = "https://tools.morningstar.co.uk/uk/cefreport/default.aspx?SecurityToken={sym}&tab={view}"
url_equities = "https://tools.morningstar.co.uk/uk/stockreport/default.aspx?tab=0{view}&SecurityToken={sym}%5d3%5d0%5dE0WWE$$ALL"
#url_equities = "https://tools.morningstar.co.uk/uk/stockreport/default.aspx?Site=uk{view}&id={sym}"

"""Spider for summary data of various security types.

    :yield: [description]
    :rtype: [type]
"""
class Funds1Spider(scrapy.Spider):
    name = "funds1"

    def start_requests(self):
        symbols = ib.Investmentsbook.get_ms_symbols()
        url_stem_equities = 'https://tools.morningstar.co.uk/uk/stockreport/default.aspx?Site=uk&id='
        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(
                url=url_funds.format(sym=symbol, view="0"),
                callback=self.parse_funds_summ,
                cb_kwargs=dict(symbol=symbol))

        for symbol in symbols['cef_symbols']:
            yield scrapy.Request(
                url=url_cefs.format(sym=symbol, view=""),
                callback=self.parse_cefs_summ,
                cb_kwargs=dict(symbol=symbol))

        for symbol in symbols['equity_symbols']:
            yield scrapy.Request(
                url=url_equities.format(sym=symbol, view=""),
                callback=self.parse_equities_summ,
                cb_kwargs=dict(symbol=symbol)
            )


    def parse_funds_summ(self, response, symbol):
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

        data = {
            "isin" : isin_text,
            "symbol": symbol,
            "name": name_text,
            "price": re.search(r"[0-9]+\.?[0-9]+",price_text).group(),
            "currency" : re.search("^.{3}", price_text).group(),
            "date": date_text,
            "asset_allocation": aa_data,
            "top_region": tr_data,
            "top_sectors": ts_data
            }
        yield data

    def parse_cefs_summ(self, response, symbol):
        time_text = response.xpath("//p[@id='Col0PriceTime']/text()").get()

        data = {
            "isin" : response.xpath("//tr[@id='KeyStatsIsin']/td/text()").get(),
            "symbol": symbol,
            "name": response.xpath("//span[@class='securityName']/text()").get(),
            "price": response.xpath("//span[@id='Col0Price']/text()").get(),
            "currency" : response.xpath("//span[@id='Col0Price']/text()").get(),
            "date": re.search(r"\d{2}/\d{2}/\d{4}", time_text).group()
            }
        yield data


    def parse_equities_summ(self, response, symbol):
        # Cannot fetch the following data from page
        # sector_text = response.xpath("//h3[text()='Sector']/parent::*/text()").getall()
        time_text = response.xpath("//p[@id='Col0PriceTime']/text()").get()
        isin_text =	response.xpath("//td[@id='Col0Isin']/text()").getall()[0]
        price_text = response.xpath("//span[@id='Col0Price']/text()").getall()[0]
        price_info_text = response.xpath("//p[@id='Col0PriceTime']/text()").getall()
        yield {
            "isin" : isin_text,
            "symbol": symbol,
            "name": response.xpath("//span[@class='securityName']/text()").get(),
            "price": price_text,
            "currency" : re.search(r"\|\s(\w{3})", price_info_text[2]).group(1),
            "date": re.search(r"\d{2}/\d{2}/\d{4}", price_info_text[0]).group()
        }



class Funds2Spider(scrapy.Spider):
    name = "funds2"

    def start_requests(self):
        symbols = ib.Investmentsbook.get_ms_symbols()
        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(
                url=url_funds.format(sym=symbol, view="1"),
                callback=self.parse_funds_perf,
                cb_kwargs=dict(symbol=symbol))

        for symbol in symbols['cef_symbols']:
            yield scrapy.Request(
                url=url_cefs.format(sym=symbol, view="1"),
                callback=self.parse_cef_perf,
                cb_kwargs=dict(symbol=symbol))

        for symbol in symbols['equity_symbols']:
            yield scrapy.Request(
                url=url_equities.format(sym=symbol, view="&vw=pf"),
                callback=self.parse_equities_perf,
                cb_kwargs=dict(symbol=symbol)
            )


    def parse_funds_perf(self, response, symbol):

        tr_ret_text =  response.xpath(
            "//table[contains(@class, 'returnsTrailingTable')]//td[contains(@class, 'col2')]//text()") \
            .getall()
        values = [item for item in tr_ret_text[1:9]]
        periods = [ '1d', '1w', '1m', '3m', '6m', 'ytd', '1y', '3y']
        trailing_returns = dict( zip( periods, values))

        data = {
            "symbol" : symbol,
            "trailing_returns" : trailing_returns
            }
        yield data

    def parse_cef_perf(self, response, symbol):
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
            "trailing_returns" : trailing_returns_price,
            "trailing_returns_cef_nav" : trailing_returns_nav
            }
        yield data


    def parse_equities_perf(self, response, symbol):
        tr_text = response.xpath(
            "//div[@id='TrailingReturns']//tr[@class='rowSecurity']//text()") .getall()

        periods = [ '1m', '3m', '1y', '3y', '5y', '10y', 'ytd']

        tr_values = [item for item in tr_text[1:8]]
        trailing_returns = dict( zip( periods, tr_values))

        yield {
            "symbol" : symbol,
            "trailing_returns" : trailing_returns
        }

class Funds3Spider(scrapy.Spider):
    """Scrape risk and ratings data from Morningstar website for funds.
    Write to funds3.json.

    :param scrapy: [description]
    :type scrapy: [type]
    :yield: [description]
    :rtype: [type]
    """
    name = "funds3"

    def start_requests(self):
        symbols = ib.Investmentsbook.get_ms_symbols()
                    # https://tools.morningstar.co.uk/uk/stockreport/default.aspx?tab=0&vw=pf&SecurityToken=0P0000004C%5d3%5d0%5dE0WWE
        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(
                url=url_funds.format(sym=symbol, view="2"),
                callback=self.parse_funds_rating,
                cb_kwargs=dict(symbol=symbol))


    def parse_funds_rating(self, response, symbol):

        sharpe_text =  response.xpath(
             "//td[text()='3-Yr Sharpe Ratio']/following-sibling::td/text()") .get()

        beta_text = response.xpath(
            "//td[text()='3-Yr Beta']/following-sibling::td/text()").getall()

        alpha_text = response.xpath(
            "//td[text()='3-Yr Alpha']/following-sibling::td/text()").getall()

        data = {
            "symbol" : symbol,
            "sharpe" : sharpe_text,
            "beta_standard": beta_text[0],
            "beta_best_fit": beta_text[1],
            "alpha_standard": alpha_text[0],
            "alpha_best_fit": alpha_text[1]

            }
        yield data


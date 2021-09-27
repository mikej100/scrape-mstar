import scrapy
import re
import pandas as pd
import numpy as np
from os.path import exists

class Funds1Spider(scrapy.Spider):
    name = "funds1"

    is_test_mode = False
    def start_requests(self):
        if self.is_test_mode:
            symbols = {
                "fund_symbols":[
                "0P0001HPYK"
            ],
            "equity_symobls":[]
            }
        else:
            symbols =  self.get_ms_symbols()

        url_stem_funds = 'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id='
        url_stem_funds_sustainability = 'https://www.morningstar.co.uk/Common/funds/snapshot/SustenabilitySAL.aspx?Site=uk'
        url_stem_equities = 'https://tools.morningstar.co.uk/uk/stockreport/default.aspx?Site=uk&id='


        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(url=url_stem_funds + symbol, callback=self.parse_funds)

        for symbol in symbols['equity_symbols']:
            yield scrapy.Request(url=url_stem_equities + symbol, callback=self.parse_equities)


    def parse_funds(self, response):
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
            "name": name_text,
            "currency" : re.search("^.{3}", price_text).group(),
            "price": re.search(r"[0-9]+\.?[0-9]+",price_text).group(),
            "date": date_text,
            "asset_allocation": aa_data,
            "top_region": tr_data,
            "top_sectors": ts_data
            }
        yield data



    def parse_equities(self, response):
        # Cannot fetch the following data from page
        # sector_text = response.xpath("//h3[text()='Sector']/parent::*/text()").getall()
        isin_text =	response.xpath("//td[@id='Col0Isin']/text()").getall()[0]
        price_text = response.xpath("//span[@id='Col0Price']/text()").getall()[0]
        currency_text = response.xpath("//p[@id='Col0PriceTime']/text()").getall()[2]
        yield {
            "isin" : isin_text,
            "currency" : re.search(r"\|\s(\w{3})", currency_text).group(1),
            "price": price_text,
        }

    def get_ms_symbols(self):
        inv_book_name = "../../../20210716 Investments book.xlsx"
        funds_sheet_name = "FundsBase"

        df =  pd.read_excel(inv_book_name, sheet_name = funds_sheet_name)


        funds = df\
            .pipe( lambda df_: df_[df_['Type'] == "Fund"])
        # funds = df[df['Type'] =='Fund']
        funds2 = funds[funds['Morningstar symbol'].apply(lambda s: isinstance(s, str))]
        fund_symbols = funds2['Morningstar symbol']

        equities = df\
            .pipe( lambda df_: df_[df_['Type'] == "Equity"])
        # funds = df[df['Type'] =='Fund']
        equities2 = equities[equities['Morningstar symbol'].apply(lambda s: isinstance(s, str))]
        equity_symbols = equities2['Morningstar symbol']
        symbols = {
            "fund_symbols": fund_symbols,
            "equity_symbols": equity_symbols
        }
        return symbols

        

import scrapy
import re
import pandas as pd
from os.path import exists

class Funds1Spider(scrapy.Spider):
    name = "funds1"

    def start_requests(self):
        # fund_symbols = [
        #     "0P0001HPYK"
        # ]
        symbols =  self.get_ms_symbols()

        url_stem_funds = 'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id='
        url_stem_equities = 'https://tools.morningstar.co.uk/uk/stockreport/default.aspx?Site=uk&id='

        for symbol in symbols['fund_symbols']:
            yield scrapy.Request(url=url_stem_funds + symbol, callback=self.parse_funds)

        for symbol in symbols['equity_symbols']:
            yield scrapy.Request(url=url_stem_equities + symbol, callback=self.parse_equities)


    def parse_funds(self, response):
        isin_text = response.xpath("//td[text()='ISIN']/following-sibling::*/text()").getall()[1]

        price_elems =  response.xpath("//td[text()='NAV']/following-sibling::*/text()").getall()
        if len(price_elems) > 1 :
            price_text = price_elems[1]
        else:
            # Some funds have Closing Price rather than NAV
            price_text =  response.xpath("//td[text()='Closing Price']/following-sibling::*/text()").getall()[1]

        yield {
            "isin" : isin_text,
            "currency" : re.search("^.{3}", price_text).group(),
            "price": re.search(r"[0-9]+\.?[0-9]+",price_text).group()
        }

    def parse_equities(self, response):
        isin_text =	response.xpath("//td[@id='Col0Isin']/text()").getall()[0]
        price_text = response.xpath("//span[@id='Col0Price']/text()").getall()[0]
        currency_text = response.xpath("//p[@id='Col0PriceTime']/text()").getall()[2]
        yield {
            "isin" : isin_text,
            "currency" : re.search(r"\|\s(\w{3})", currency_text).group(1),
            "price": price_text
        }

    def get_ms_symbols(self):
        inv_book_name = "../../../20210622 Investments book.xlsx"
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

        

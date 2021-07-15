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

        url_stem = 'https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id='

        for fund_symbol in symbols['fund_symbols']:
            yield scrapy.Request(url=url_stem + fund_symbol, callback=self.parse)

    def parse(self, response):
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

        

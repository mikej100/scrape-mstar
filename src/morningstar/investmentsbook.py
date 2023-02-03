import pandas as pd
import json
import os
import re
# TODO make into singleton so open book just once.

class Investmentsbook():
    """Manage interactions with investments workbook. The investments workbook 
    is  the source for securities ids to be processed. The location of the 
    workbook is specified by an invironment variable
    """

    def __init__(self, bookpath: str|None = None, sheetname = "SecBase"):
        if bookpath == None:
            inv_book_loc = os.environ['INVESTMENTS_BOOK_LOC']
            inv_book_name = os.environ['INVESTMENTS_BOOK_NAME']
            # Path envvar is Windows path, needs modifying for linux platform.
            #TODO replace with a reduce
            inv_book_loc = re.sub(r"\\", "/", inv_book_loc)
            inv_book_loc = re.sub(r"C", "c", inv_book_loc)
            inv_book_loc = re.sub(r":", "", inv_book_loc)
            bookpath = f"/mnt/{inv_book_loc}/{inv_book_name}"
        self.bookpath = bookpath
        self.sheetname = sheetname


    def get_ms_symbols(self):
        df = pd.read_excel(self.bookpath, sheet_name=self.sheetname)
        df_with_symbol = df[
            df['Morningstar symbol']
            .apply(lambda s: isinstance(s, str))
        ]
        fund_symbols = list(
            df_with_symbol[df_with_symbol['Type'] == "Fund"]
            ['Morningstar symbol']
        )

        cef_pattern = re.compile(r"cef:(.*)")
        cef_symbols = [re.match(cef_pattern, s).group(1)
                       for s in fund_symbols
                       if re.match(cef_pattern, s)]

        non_cef_symbols = [s
                           for s in fund_symbols
                           if not(re.match(cef_pattern, s))]

        equity_symbols = list(
            df_with_symbol[df_with_symbol['Type'] == "Equity"]
            ['Morningstar symbol']
        )

        self.symbols = {
            "fund_symbols": non_cef_symbols,
            "cef_symbols": cef_symbols,
            "equity_symbols": equity_symbols
        }
        return self.symbols

    def exists(self):
        return os.path.exists(self.bookpath)

    def write_symbols(self, fpath="data/symbols.json"):
        with open(fpath, "w") as outfile:
            outfile.write(json.dumps(self.symbols))
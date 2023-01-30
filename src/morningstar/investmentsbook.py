import pandas as pd
import os
import re
# TODO make into singleton so open book just once.

class Investmentsbook():
    is_test_mode = False

    def __init__(self, bookname):
        self.bookname = bookname


        """[Get Morningstar symbols from investments workbook]
        """
    def get_ms_symbols(self):

        if Investmentsbook.is_test_mode:
            symbols = {
                "fund_symbols":[
                      "F0000103JP"
                ],
                "cef_symbols":[
                       "F000000JUY"
                    ],
                "equity_symbols":[
                      "0P0000004C"
                ]
                }
        else:
            #inv_book_name = os.environ["INVESTMENTS_BOOK"]
            sec_sheet_name = "SecBase"

            df = pd.read_excel(self.bookname, sheet_name=sec_sheet_name)

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

            symbols = {
                "fund_symbols": non_cef_symbols,
                "cef_symbols": cef_symbols,
                "equity_symbols": equity_symbols
            }
        return symbols

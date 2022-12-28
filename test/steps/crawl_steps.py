import datetime
import pathlib
from behave import given, when, then
from hamcrest import *
import glob

from  morningstar.run_securities import run_securities

symbols_list = ""
crawl_id = ""

@given('scrapy modules are in same project as this test')
def step_implementation(context):
    pass

@given(u'symbols dataset 1')
def step_impl(context):
    symbols_list ='{"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}' 

@when(u'scrape-mstar is invoked')
def step_impl(context):
    symbols =  '{"fund_symbols": ["F000013G37"], "cef_symbols": [], "equity_symbols": ["0P0000004C"]}'
    crawl_id = "crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S') 
    run_securities(symbols, crawl_id)


@then(u'new securities_data file is created')
def step_impl(context):
    
    result = glob.glob("data/", f"*{crawl_id}*")
    raise NotImplementedError(u'STEP: Then new securities_data file is created')

#@given('symbols data json {"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}
#When scrape-mstar is invoked
#Then new securities_data file is created
 
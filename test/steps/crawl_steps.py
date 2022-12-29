import datetime
import pathlib
from behave import given, when, then
from hamcrest import *
import glob
import sys


@given('scrapy modules are in same project as this test')
def step_implementation(context):
    pass

@given(u'symbols dataset 1')
def step_impl(context):
    # context.symbols_list ='{"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}' 
    context.symbols ='{"fund_symbols": ["F000013G37"], "cef_symbols": [], "equity_symbols": ["0P0000004C"]}' 

@when(u'scrape-mstar is invoked')
def step_impl(context):
    context.crawl_id = "crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S') 
    from  src.morningstar.run_securities import run_securities
    run_securities(context.symbols, context.crawl_id)


@then(u'new securities_data file is created')
def step_impl(context):
    
    result = glob.glob(f"data/*{context.crawl_id}*")
    assert_that(len(result), is_(equal_to(1)), "Count matching crawl_id s")

#@given('symbols data json {"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}
#When scrape-mstar is invoked
#Then new securities_data file is created
 
from behave import given, when, then
from hamcrest import *

symbols_list = ""

@given('scrapy modules are in same project as this test')
def step_implementation(context):
    pass

@given(u'symbols dataset 1')
def step_impl(context):
    symbols_list ='{"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}' 

@when(u'scrape-mstar is invoked')
def step_impl(context):
    csrc/morningstar/run_securities.py
    raise NotImplementedError(u'STEP: When scrape-mstar is invoked')


@then(u'new securities_data file is created')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then new securities_data file is created')

#@given('symbols data json {"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}
#When scrape-mstar is invoked
#Then new securities_data file is created
 
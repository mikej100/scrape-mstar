import datetime
import glob
import os
import logging
import pathlib
import sys
import time

from behave import given, when, then
from hamcrest import *
from scrapyd_api import  ScrapydAPI


# logger = logging.getLogger(__name__j)
# file_handler = logging.FileHandler(f"{os.getcwd()}/logs/")

@given('scrapy modules are in same project as this test')
def step_implementation(context):
    pass

@given('symbols dataset 1')
def step_implementation(context):
    # context.symbols_l:ist ='{"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}' 
    context.symbols ='{"fund_symbols": ["F000013G37"], "cef_symbols": [], "equity_symbols": ["0P0000004C"]}' 
    pass

@when('scrape-mstar is invoked')
def step_impl(context):
    context.crawl_id = "crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S') 
    from  src.morningstar.run_securities import run_securities
    run_securities(context.symbols, context.crawl_id)


@then('new securities_data file is created')
def step_impl(context):
    
    result = glob.glob(f"data/*{context.crawl_id}*")
    assert_that(len(result), is_(equal_to(1)), "Count matching crawl_id s")

#@given('symbols data json {"fund_symbols": ["F000013G37"], "cef_symbols": ["F000011FTC"], "equity_symbols": ["0P0000004C"]}
#When scrape-mstar is invoked
#Then new securities_data file is created
@given('morningstar scapy module is deployed to local server')
def step_impl(context):
    context.scrapyd = ScrapydManager()
    assert_that( context.scrapyd.is_project_deployed(), is_(True), "project listed by scrapyd")


    

@when('a run request is submitted')
def step_impl(context):
    context.symbols ='{"fund_symbols": ["F000013G37"], "cef_symbols": [], "equity_symbols": ["0P0000004C"]}' 
    context.crawl_id = "crawl_" + datetime.datetime.now().strftime('%Y%m%dT%H%M%S') 
    context.feed_uri = f"{os.getcwd()}/data/scrapyd_{context.crawl_id}.json" 
    settings = {
        "FEED_URI": context.feed_uri
    }
    result = context.scrapyd.schedule( 
        context.scrapyd_project,
        context.scrapyd_spider, 
        settings=settings,
        symbols=context.symbols
        )
    assert_that(result, matches_regexp(r"\S{32}") )
    context.job_id = result

@then('a run_id is returned')
def step_impl(context):
    assert_that(context.job_id, matches_regexp(r"\S{32}") )

@then('the output file is produced within "{timeout_str}" seconds')
def step_impl(context,timeout_str):
    timeout = float(timeout_str)
    interval = 0.5

    timeleft = timeout
    result = False
    while timeleft > 0:
        if len(glob.glob(context.feed_uri)) == 1:
            result = True
            break
        timeleft = timeleft - interval
        time.sleep(interval)

    assert_that(result, is_(True))
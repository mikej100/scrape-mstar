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

from src.scrapyd_manager import ScrapydManager

@given(u'scrapyd is not running on localhost')
def step_impl(context):
    context.scrapyd = ScrapydManager()
    result = context.scrapyd.is_running()
    assert_that(result, is_(False))

@given(u'scrapyd is running on localhost')
def step_impl(context):
    context.scrapyd = ScrapydManager()
    result = context.scrapyd.start_service()
    assert_that(result, is_(True))


@when(u'scapyd is started on localhost')
def step_impl(context):
    result = context.scrapyd.start_service()
    a=2

@then(u'scrapyd on localhost responds to a request')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then scrapyd on localhost responds to a request')

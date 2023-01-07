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

@given('scrapyd is not running on localhost')
def step_impl(context):
    context.scrapyd = ScrapydManager()
    result = context.scrapyd.is_running()
    assert_that(result, is_(False))

@given('scrapyd is running on localhost')
def step_impl(context):
    context.scrapyd = ScrapydManager()
    assert_that(
        context.scrapyd.start_service(),
        is_(True)
        )

@given('default project is not deployed on scrapyd')
def step_impl(context):
    context.scrapyd.delete_project("default")
    assert_that(
        context.scrapyd.is_project_deployed("default"),
        is_(False)
    )

@when('scapyd is started on localhost')
def step_impl(context):
    assert_that(
        context.scrapyd.start_service(),
        is_(True)
        )

@when('default project is deployed to localhost')
def step_impl(context):
    assert_that(
        context.scrapyd.deploy_default(),
        is_(True)
        )

@then('scrapyd on localhost responds to a request')
def step_impl(context):
    result = context.scrapyd.is_running()
    assert_that(result, is_(True))

@then('default project is listed by scrapyd server')
def step_impl(context):
    result = context.scrapyd.is_project_deployed()
    assert_that( result, is_(True),  "projects listed by scrapyd")
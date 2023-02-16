import os
import logging
import subprocess
import time

from behave import given, when, then #pylint: disable=no-name-in-module
from hamcrest import *
from scrapyd_api import  ScrapydAPI

from scrapyd_manager import ScrapydManager

# pylint: disable=function-redefined
# pylint:  disable=missing-function-docstring

logger = logging.getLogger("managed_scrapy_steps")

@given('scrapyd is not running on localhost')
def step_impl(context):
    context.scrapyd = ScrapydManager()
    assert_that (
        context.scrapyd.stop_service(),
        is_(True),
        "Scrapyd stopped"
        )

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
    if not  hasattr(context, "scrapyd") :
        context.scrapyd = ScrapydManager()
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

@when('scrapyd service is stopped on localhost')
def step_impl(context):
    if not  hasattr(context, "scrapyd") :
        context.scrapyd = ScrapydManager()
    assert_that(
        context.scrapyd.stop_service(),
        is_(True),
        "Stopping scrapyd service"
    )

@when('scrapyd start and deploy script is run')
def step_impl(context):
    logger.info(f"Working directory before calling scrapyd_manager:\n{os.getcwd()}")
    run_process = subprocess.Popen("src/scrapyd-start-deploy")
    time.sleep(2)

@then('scrapyd on localhost responds to a request')
def step_impl(context):
    result = context.scrapyd.is_running()
    assert_that(result, is_(True))

@then('default project is listed by scrapyd server')
def step_impl(context):
    result = context.scrapyd.is_project_deployed()
    assert_that( result, is_(True),  "projects listed by scrapyd")


@then('scrapyd is not running on localhost')
def step_impl(context):
    assert_that(
        context.scrapyd.is_running(),
        is_(False), 
        "scrapyd service running."
    )

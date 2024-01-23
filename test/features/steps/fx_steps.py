import logging
from behave import given, when, then  # pylint: disable=no-name-in-module
import datetime
import dateutil.parser as dparser
from hamcrest import *

from src.dataman.fx import Fx

# pylint: disable=function-redefined
# pylint:  disable=missing-function-docstring
logger = logging.getLogger("fx_steps")


@given('a MongoDB Atlas cloud database with historic GBPUSD exchange rates')
def step_impl(context):
    fx = Fx()
    assert_that(fx, instance_of(Fx))
    context.fx = fx


# @when( 'the python conversion function is called with date "{date_string}"')
# def step_impl(context, date_string):
#     sdate = dparser.parse(date_string)
#     sdatetime = datetime.datetime.fromordinal(sdate.toordinal())
#     context.fx_result = context.fx.fx_by_pxtime(sdatetime)

@then('the conversion rate is "{fx_expected}"')
def step_impl(context, fx_expected):
    assert_that(
        context.fx_result,
        float(fx_expected)
    )


@when('integer "{px_value}" representing the date 2023-01-21 for conversion')
def step_impl(context, px_value):
    fx = Fx()
    context.mm_result = fx.posixtime_to_mm(int(px_value))


@then('the result is "{mm_value}"')
def step_impl(context, mm_value):
    assert_that(
        mm_value,
        context.mm_result
    )

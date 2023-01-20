import logging
from behave import given, when, then
from hamcrest import *

from src.dataman.fx import Fx

logger = logging.getLogger("fx_steps")

@given(u'a MongoDB Atlas cloud database with historic GBPUSD exchange rates')
def step_impl(context):
   fx = Fx()
   assert_that(fx, instance_of( Fx ) )


@when(u'the python conversion function is called with date "2020-09-23"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the python conversion function is called with date "2020-09-23"')


@then(u'the conversion rate is "1.21"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the conversion rate is "1.21"')
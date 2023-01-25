from hamcrest import *
import datetime
import dateutil.parser as dparser

from dataman import fx

def test_posixtimestamp_to_mm1():
    assert_that(
        fx.posixtimestamp_to_mm(1674259200),
        equal_to(12124800),
    )


        
def test_posixdtime_to_mm():
    test_dt = dparser.parse("2023-01-21")
    assert_that(
        fx.posixdtime_to_mm(test_dt),
        equal_to(12124800),
    )

def test_pydate_to_mm():
    test_datetime = dparser.parse("2023-01-21")
    test_date = test_datetime.date()
    assert_that(
        fx.pydate_to_mm(test_date),
        equal_to(12124800),
    )

def test_xldate_to_mm():
    xldate = 44947
    assert_that(
        fx.xldate_to_mm(xldate),
        equal_to(12124800),
    )

def test_xldate_to_pxdtime():
    xldate = 44947
    assert_that(
        fx.xldate_to_pxdtime(xldate),
        equal_to(dparser.parse("2023-01-21")),
    )
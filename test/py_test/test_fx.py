from hamcrest import *
import datetime
import dateutil.parser as dparser

from dataman import fx

def test_gpbusd():
    usd = fx.Fx()

    def test_date(date_string, expected):
        assert_that( usd.rate( dparser.parse(date_string)),
            close_to( expected, 0.008),
            f"for date {date_string}"
        )
                                     # Source of test value
    test_date("2020-09-23", 1.2724)  # www.exchangereates.org.uk
    test_date("2010-07-23", 1.536)  # www.exchangereates.org.uk

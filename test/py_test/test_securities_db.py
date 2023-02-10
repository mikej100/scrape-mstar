from hamcrest import *
from dataman import crawl_data as cd


def test_find_last_crawl():
    secdb = cd.SecuritiesDb()
    latest = secdb.get_latest_crawl()
    assert_that(latest, matches_regexp(r"crawl_") )

def test_get_all_last_crawl():
    secdb = cd.SecuritiesDb()
    latest = secdb.get_latest_crawl()
    all_data = secdb.get_crawl_all(latest)
    assert_that(all_data, has_length(greater_than(2)))

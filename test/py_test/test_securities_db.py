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

#   SLOW!!
def test_wait_for_crawl_fails_for_spurious_crawlid():
    secdb = cd.SecuritiesDb()
    timer = secdb.wait_for_crawl("spurious_crawl_id", timeout=1.5)
    assert_that(timer, less_than(0))

def test_wait_for_crawl_for_known_crawl():
    secdb = cd.SecuritiesDb()
    latest = secdb.get_latest_crawl()
    timer = secdb.wait_for_crawl(latest)
    assert_that(timer, greater_than_or_equal_to(0))

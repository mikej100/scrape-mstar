import logging
import os
import re
from functools import reduce
from behave import given, when, then #pylint: disable=no-name-in-module
from hamcrest import *

from morningstar.investmentsbook import Investmentsbook

# pylint: disable=function-redefined
# pylint:  disable=missing-function-docstring
@given('investment book file in financial analysis folder')
def step_impl(context):
    inv_book_loc = os.environ['INVESTMENTS_BOOK_LOC']
    inv_book_name = os.environ['INVESTMENTS_BOOK_NAME']
    #TODO replace with a reduce
    inv_book_loc = re.sub(r"\\", "/", inv_book_loc)
    inv_book_loc = re.sub(r"C", "c", inv_book_loc)
    inv_book_loc = re.sub(r":", "", inv_book_loc)

    inv_book_path = f"/mnt/{inv_book_loc}/{inv_book_name}"
    assert_that(os.path.exists(inv_book_path), is_(True), "Locating investments book")
    context.inv_book_path = inv_book_path

@when('the workbook is read')
def step_impl(context):
    book = Investmentsbook(context.inv_book_path)
    context.symbols = book.get_ms_symbols()


@then('the number of FundsBase entries is "{n_expected}"')
def step_impl(context, n_expected):
    n = reduce( lambda n, dict: n + len(dict), context.symbols, 0)
    assert_that(n,
        equal_to(int(n_expected)),
        "Expected number of symbols"
    )
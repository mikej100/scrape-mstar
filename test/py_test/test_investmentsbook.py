import datetime
from hamcrest import *
import json
import os
from morningstar.investmentsbook import Investmentsbook

def test_file_exists():
    book = Investmentsbook()
    assert_that( book.exists(), True, "Check book exists")

def test_file_does_not_exist():
    book = Investmentsbook("spurious path")
    assert_that( book.exists(), is_(False), "Check book exists")

def test_export_symbols():
    book = Investmentsbook()
    symbols = book.get_ms_symbols()
    symbols_fname ="data/symbols_test.json" 
    book.write_symbols((symbols_fname))

    f_time = os.path.getctime(symbols_fname)
    f_age = datetime.datetime.now().timestamp() - f_time
    assert_that(f_age, less_than(0.1), "Checking symbols file age in seconds")

def test_default_export_symbols():
    book = Investmentsbook()
    symbols = book.get_ms_symbols()
    symbols_fname ="data/symbols.json" 
    book.write_symbols()

    f_time = os.path.getctime(symbols_fname)
    f_age = datetime.datetime.now().timestamp() - f_time
    assert_that(f_age, less_than(0.1), "Checking symbols file age in seconds")
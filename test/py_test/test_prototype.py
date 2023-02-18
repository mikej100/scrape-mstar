from hamcrest import *
import logging
import logging.config
import yaml

logger = logging.getLogger(__name__)

from morningstar.prototype import Prototype

def test_prototype():
    inner = Prototype.outer()
    result = inner()
    logger.debug(f"inner:{result}")
    assert_that(result, not_none)
    
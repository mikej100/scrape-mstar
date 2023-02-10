from hamcrest import *
import logging
import logging.config
import yaml

with open("./logging.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.debug("Testing")

from morningstar.prototype import Prototype

def test_prototype():
    inner = Prototype.outer()
    result = inner()
    logger.debug(f"inner:{result}")
    assert_that(result, not_none)
    
import logging
import sys
def before_all(context):
    logger = logging.getLogger
    logger.debug("before_all")
    


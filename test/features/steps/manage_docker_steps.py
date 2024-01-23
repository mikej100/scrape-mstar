import os
import logging
import subprocess
import time
import sys

from behave import given, when, then #pylint: disable=no-name-in-module
from hamcrest import *
from scrapyd_api import  ScrapydAPI

from scrapyd_manager import ScrapydManager

# pylint: disable=function-redefined
# pylint:  disable=missing-function-docstring

logger = logging.getLogger("manage_docker_steps")


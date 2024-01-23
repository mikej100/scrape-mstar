import logging
import logging.config
import yaml
import sys

# Set up logging config
with open("./logging.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)

logger = logging.getLogger()
logger.debug("Message from scrape_utils")

# ping pong
# Add src to module import location searchsys
sys.path.append("./src")
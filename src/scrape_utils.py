import logging
import logging.config
import yaml


# Set up logging config
with open("./logging.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)
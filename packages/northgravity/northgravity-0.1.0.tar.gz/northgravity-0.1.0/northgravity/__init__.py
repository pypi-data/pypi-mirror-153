import logging
import sys

from .configuration import *
# Set logger with proper format for backend parsing to status page
from .constants import LOGGER_NAME

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.Logger(LOGGER_NAME)

logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(logger_handler)
config = configuration.Configuration()

# Import the methods
from .DatalakeHandler import *
from .TaskHandler import *
from .StatusHandler import *
from .Timeseries import *

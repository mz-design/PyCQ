# ---------------------------------------------------------------------------------------------
# Station_status.py - holds StationStatus variable
#
# Prerequisites: none
#
# initial release: 31.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import logging
import constants
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

StationStatus = 'offline'

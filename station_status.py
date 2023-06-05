# ---------------------------------------------------------------------------------------------
# Station_status.py - holds StationStatus class
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


class StationStatus:

    def __init__(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
        if status is not ('online' or 'offline'):
            logger.add_log_entry(logging.ERROR, f"Invalid station status {self.status} (valid are 'online'/'offline')")
        return self.status

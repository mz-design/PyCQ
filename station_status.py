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

    def __init__(self):
        self.status = None

    def get_status(self):
        return self.status

    def set_status(self, new_status):
        if new_status not in ('online', 'offline'):
            logger.add_log_entry(logging.ERROR, f"Invalid station status {self.status} (valid are 'online'/'offline')")
            return
        self.status = new_status
        return self.status


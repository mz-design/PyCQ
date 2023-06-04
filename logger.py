# -------------------------------------------------------------------------------------
# logger.py - defines common logging class 'Logger' using built-in 'logging' class
#
# Prerequisites: None
#
# initial release: 28.05.2023 - MichaelZ
# -------------------------------------------------------------------------------------


import logging


class Logger:
    def __init__(self, log_file, level=logging.INFO):
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)

        # Check if a handler is already added
        if not self.logger.handlers:
            self.logger.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler = logging.FileHandler(self.log_file)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)


    def add_log_entry(self, level, information):
        self.logger.log(level, information)


# TODO: Remove usage example below after debug
# Usage Example:
# Starting the module set the suggested '.log' file name and minimal display log entry severity:
# DEBUG (default) is lowest display severity ... CRITICAL is highest display severity
#
#   logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# Adding log entry to selected file:
#
#   logger.add_log_entry(logging.DEBUG, "This is a debug log entry.")
#   logger.add_log_entry(logging.INFO, 'This is an info log entry.')
#   logger.add_log_entry(logging.WARNING, 'This is a warning log entry.')
#   logger.add_log_entry(logging.ERROR, 'This is an error log entry.')
#   logger.add_log_entry(logging.CRITICAL, 'This is a critical log entry.')


# TODO: Any more functionalities here? - TBD

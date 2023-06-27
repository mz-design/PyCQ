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

# TODO: Any more functionalities here? - TBD

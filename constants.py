# ------------------------------------------------------------------------------------------------------
# constants.py -  Main project constants (like logging level, file names, port numbers etc.)
#
# Prerequisites: None
#
# initial release: 31.05.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import logging


# Logging

LOGGING_LEVEL = logging.DEBUG
LOG_FILE = 'PyCQ.log'
LOG_MAX_LINES = 1000

# Communications

HTTP_PORT = 8080
TCP_PORT = 1234
UDP_PORT = 50000
MAGIC = 'py1234cq'
ANNOUNCE_INTERVAL = 5
KEEP_ALIVE_INTERVAL = 30

# Audio

SAMPLERATE = 44100
CHANNELS = 2
REC_TIME = 5
AUDIO_TYPE = '.ogg'              # Supported file types are: '.wav', '.flac' and '.ogg' [default = '.ogg']

# Files and folders

MESSAGE_STORE = 'MsgStore'
HISTORY = 'history.csv'
HISTORY_MAX_ENTRIES = 100
MESSAGE_STORE_MAX_FILES = 100
STATIONS = 'stations.csv'




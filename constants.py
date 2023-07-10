# ------------------------------------------------------------------------------------------------------
# constants.py -  Main project constants (like logging level, file names, tcp_port numbers etc.)
#
# Prerequisites: None
#
# Beta release: 10.07.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import logging


# Logging

LOGGING_LEVEL = logging.DEBUG
LOG_FILE = 'PyCQ.log'
LOG_MAX_LINES = 1000
LOG_ROTATOR_COUNTER = 20        # Num of periodic register/keep-alive rounds before log is cleaned (1 round ~35-40 sec)

# Communications

HTTP_PORT = 8080
TCP_PORT = 1234
UDP_PORT = 50000
MAGIC = 'py1234cq'
ANNOUNCE_INTERVAL = 5
KEEP_ALIVE_INTERVAL = 30
STATION_REGISTER_INTERVAL = 30

# Audio

SAMPLERATE = 44100
CHANNELS = 2
REC_TIME = 5
AUDIO_TYPE = '.ogg'              # Supported file types are: '.wav', '.flac' and '.ogg' [default = '.ogg']
OUTPUT_VOLUME = -3.3             # Desired output audio device volume setting in dB (valid range -61.0 -0.0) default -3.3 (~80% of maximum)
PLAY_C2A = True                  # Play 'call to attention' preamble sound before playing new voice message [default = True]
C2A_FILE = 'c2a.ogg'
ALERT_SOUND = 'emergency_alarm.ogg'

# Files and folders

MESSAGE_STORE = 'MsgStore'
RESOURCE_FOLDER = 'resources'
HISTORY = 'history.csv'
HISTORY_MAX_ENTRIES = 100
MESSAGE_STORE_MAX_FILES = 100
STATIONS = 'stations.csv'

# GUI settings

TRAY_ICON = 'resources/icon.png'
TRANSPARENCY = 255                       # Default value
ENABLE_CHANGE_TRANSPARENCY = True        # When False slider popup transparency control in station will be disabled and user will be forced default value
ENABLE_CHANGE_VOLUME = True              # When False slider volume control in station will be disabled and user will be forced to OUTPUT_VOLUME value
ENABLE_EXIT = True                       # When False 'Exit' option in station disabled (user cannot exit application)
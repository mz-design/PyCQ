# ------------------------------------------------------------------------------------------------------
# constants.py -  Main project constants (like logging level, file names, tcp_port numbers etc.)
#
# Prerequisites: None
#
# Beta release: 10.07.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import logging


# Logging

LOGGING_LEVEL = logging.DEBUG   # Minimal desired logging level [default = DEBUG (maximal)]
LOG_FILE = 'PyCQ.log'           # Log file name
LOG_MAX_LINES = 1000            # Max number of log file lines after initial clean-up on application start
LOG_ROTATOR_COUNTER = 20        # Num of periodic register/keep-alive rounds before log is cleaned (1 round ~35-40 sec)

# Communications

HTTP_PORT = 8080                    # HTTP port (used by Caller HTTP server)
TCP_PORT = 1234                     # TCP port (used for Caller<->Station signalling)
UDP_PORT = 50000                    # UDP port (used by 'Announcer' module on caller and 'Listener' module on Station
MAGIC = 'py1234cq'                  # UDP 'magic' packet
ANNOUNCE_INTERVAL = 5               # Caller announcement interval [default = 5 sec]
KEEP_ALIVE_INTERVAL = 30            # "Station Keep-Alive" interval used by Caller [default = 30 sec]
STATION_REGISTER_INTERVAL = 30      # "Periodic Register" interval used by Station [default = 30 sec]

# Audio

SAMPLERATE = 44100               # Audio recording/playback samplerate [default = 44100 Hz]
CHANNELS = 2                     # number of audio playback channels [default = 2 (stereo)]
REC_TIME = 5                     # Voice Message recording length [default = 5 sec]
AUDIO_TYPE = '.ogg'              # Supported file types are: '.wav', '.flac' and '.ogg' [default = '.ogg']
OUTPUT_VOLUME = -3.3             # Desired output audio device volume setting in dB (valid range -61.0 -0.0) default -3.3 (~80% of maximum)
PLAY_C2A = True                  # Play "call to attention" preamble sound before playing new voice message [default = True]
C2A_FILE = 'c2a.ogg'             # "Call to attention" sound file
ALERT_SOUND = 'emergency_alarm.ogg'     # sound file for system alerts

# Files and folders

MESSAGE_STORE = 'MsgStore'       # Filestore directory (in case of standalone ".exe" precompiled in file)
RESOURCE_FOLDER = 'resources'    # Resources directory (in case of standalone ".exe" precompiled in file)
HISTORY = 'history.csv'          # message history database file (in case of standalone ".exe" precompiled in file)
HISTORY_MAX_ENTRIES = 100        # Max number of history entries after initial clean-up on Caller start
MESSAGE_STORE_MAX_FILES = 100    # Max number of stored audio files after initial clean-up on Caller start
STATIONS = 'stations.csv'

# GUI settings

TRAY_ICON = 'resources/icon.png'         # tray icon file for Station tray application
TRANSPARENCY = 255                       # Default value = 255 (non-transparent). May be changed through 'Change popup transparency' menu of tray icon
ENABLE_CHANGE_TRANSPARENCY = True        # When False slider popup transparency control in station will be disabled and user will be forced default value
ENABLE_CHANGE_VOLUME = True              # When False slider volume control in station will be disabled and user will be forced to OUTPUT_VOLUME value
ENABLE_EXIT = True                       # When False 'Exit' option in station disabled (user cannot exit application)


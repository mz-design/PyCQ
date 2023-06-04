# ---------------------------------------------------------------------------------------------------
# caller.py - 'Caller' procedures
#
# Prerequisites:
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

import constants
import threading
import logging
import socket
import time

import http_srv
import keep_alive
import announcer
import cleanup
import tcp_server
from logger import Logger


# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# perform cleanups on startup
cleanup.clean_log(constants.LOG_FILE, constants.LOG_MAX_LINES)
cleanup.clean_history(constants.HISTORY, constants.HISTORY_MAX_ENTRIES)
cleanup.clean_AudioFiles(f'{constants.MESSAGE_STORE}/', constants.MESSAGE_STORE_MAX_FILES)

# get configuration from constants
udp_port = constants.UDP_PORT
magic = constants.MAGIC                                     # UDP 'magic word'
announce_interval = constants.ANNOUNCE_INTERVAL
tcp_port = constants.TCP_PORT
keep_alive_interval = constants.KEEP_ALIVE_INTERVAL
http_port = constants.HTTP_PORT

# Start HTTP server
# http_srv = http_srv.start_http_server(http_port)

# Create thread objects for 'announce' and periodic keep alive
thread_http_srv = threading.Thread(target=http_srv.start_http_server, args=(http_port, ))
thread_tcp_server = threading.Thread(target=tcp_server.start_server, args=("localhost", tcp_port))
thread_announcer = threading.Thread(target=announcer.announce_service, args=(udp_port, magic, announce_interval))
thread_periodic_keep_alive = threading.Thread(target=keep_alive.run_periodically, args=(keep_alive_interval, ))

# Start threads
thread_http_srv.start()
thread_tcp_server.start()
thread_announcer.start()
time.sleep(0.1)
thread_periodic_keep_alive.start()





# ---------------------------------------------------------------------------------------------------
# station.py - 'Station' procedures
#
# Prerequisites:
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

import constants
import threading
import logging
from socket import socket, gethostbyname, gethostname
from time import sleep
import tcp_client
from tcp_message import TcpMessage
import http_srv
import keep_alive
import announcer
import cleanup
import listener
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
tcp_port = constants.TCP_PORT
http_port = constants.HTTP_PORT

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())

# Initially set station_status to OFFLINE
station_online = False
logger.add_log_entry(logging.WARNING,f"Station {my_hostname} {my_ip} is OFFLINE")


def register_to_service():
    # Wait for 'Caller announcement' and get 'Caller IP' and 'Caller HOSTNAME'
    caller_ip, caller_hostname = listener.listen_for_service(udp_port, magic)

    # encode 'REGISTER' message
    data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'REGISTER', ''))
    # send to 'Caller'
    tcp_client.start_client(caller_ip, constants.TCP_PORT, data)

# def check_online





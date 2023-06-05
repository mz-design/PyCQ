# ---------------------------------------------------------------------------------------------------
# station.py - 'Station' procedures
#
# Prerequisites:
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

import os
import constants
import threading
import logging
from socket import socket, gethostbyname, gethostname
import time
from station_status import StationStatus
import csv_ops
import tcp_client
from tcp_message import TcpMessage
import http_srv
# import keep_alive
# import announcer
import cleanup
import listener
import tcp_server
from logger import Logger

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# initialize data stores, check if exists and create when needed
directory = constants.MESSAGE_STORE
if not os.path.exists(directory):
    os.makedirs(directory)
if not os.path.exists(constants.HISTORY):
    csv_ops.open_csv_file(constants.HISTORY)

# perform cleanups on startup
cleanup.clean_log(constants.LOG_FILE, constants.LOG_MAX_LINES)
cleanup.clean_history(constants.HISTORY, constants.HISTORY_MAX_ENTRIES)
cleanup.clean_AudioFiles(f'{constants.MESSAGE_STORE}/', constants.MESSAGE_STORE_MAX_FILES)

# get configuration from constants
udp_port = constants.UDP_PORT
magic = constants.MAGIC  # UDP 'magic word'
tcp_port = constants.TCP_PORT
http_port = constants.HTTP_PORT

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())

# Initially set station_status to OFFLINE
StationStatus.set_status('offline')
logger.add_log_entry(logging.WARNING, f"Station {my_hostname} {my_ip} is OFFLINE")


def register_to_service():
    if not station_online:
        # Wait for 'Caller announcement' and get 'Caller IP' and 'Caller HOSTNAME'
        caller_ip, caller_hostname = listener.listen_for_service(udp_port, magic)
        # encode 'REGISTER' message
        data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'REGISTER', ''))
        # send to 'Caller'
        tcp_client.start_client(caller_ip, constants.TCP_PORT, data)


def run_periodically(interval):
    while True:
        print("periodic station register\n")
        register_to_service()
        time.sleep(interval)


# Create thread objects for TCP server, HTTP server and periodic register
thread_http_srv = threading.Thread(target=http_srv.start_http_server, args=(http_port,))
thread_tcp_server = threading.Thread(target=tcp_server.start_server, args=(my_hostname, tcp_port))
thread_periodic_register = threading.Thread(target=run_periodically, args=(constants.STATION_REGISTER_INTERVAL,))
# thread_announcer = threading.Thread(target=announcer.announce_service, args=(udp_port, magic, announce_interval))
# thread_periodic_keep_alive = threading.Thread(target=keep_alive.run_periodically, args=(keep_alive_interval, ))

# Start threads
thread_http_srv.start()
thread_tcp_server.start()
time.sleep(0.01)
thread_periodic_register.start()


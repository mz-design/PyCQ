# ---------------------------------------------------------------------------------------------------
# keep_alive.py - 'Caller' check stations are alive
#
# Prerequisites: None
#
# initial release: 01.06.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------
import csv
import logging
import time

import cleanup
import constants
import csv_ops
import tcp_client
from announcer import gethostbyname, gethostname
from logger import Logger
from tcp_message import TcpMessage

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())

# Initialize 'alive' variable
alive = False


def check_alive():
    global alive
    # open station list
    rows = csv_ops.open_csv_file(constants.STATIONS)
    # set 'alive' flag to False before check
    alive = False
    for row in rows:
        ip = row['IP']
        hostname = row['HOSTNAME']

        # Encode 'KEEP_ALIVE_REQ' signal
        data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'KEEP_ALIVE_REQ', ''))

        # send to remote station
        tcp_client.start_client(ip, constants.TCP_PORT, data)

        # wait a moment for 'alive' flag update...
        time.sleep(0.05)
        if not alive:       # check 'alive' failed - remove entry
            logger.add_log_entry(logging.INFO, f'Station {hostname} with IP: {ip} keep alive fail - remove entry')

            # remove this row from .csv
            rows = [r for r in rows if r != row]

    # Write changes to stations.csv file
    fieldnames = ['IP', 'HOSTNAME']
    with open(constants.STATIONS, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_periodically(interval):
    cleanup_counter = 0
    while True:
        logger.add_log_entry(logging.DEBUG, "Send periodic 'keep-alive' message")
        check_alive()

        # clean-up log file on caller periodically (kind of 'log rotator')
        if cleanup_counter == constants.LOG_ROTATOR_COUNTER:
            logger.add_log_entry(logging.INFO, f"Periodic clean-up on clean-up counter {cleanup_counter}")
            cleanup.clean_log(constants.LOG_FILE, constants.LOG_MAX_LINES)
            cleanup_counter = 0
        cleanup_counter += 1
        time.sleep(interval)


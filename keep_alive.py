# ---------------------------------------------------------------------------------------------------
# keep_alive.py - 'Caller' check stations are alive
#
# Prerequisites: None
#
# initial release: 01.06.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------
import csv
import constants
# import threading
import logging
import time
from ping3 import ping, verbose_ping
import csv_ops
import tcp_client
from tcp_message import TcpMessage
from announcer import gethostbyname, gethostname
# import cleanup
# import tcp_server
from logger import Logger

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())

alive = False


def send_ping(destination):
    response_time = ping(destination)
    if response_time is not None:
        print(f"Received response from {destination} in {response_time:.3f} ms")
        return True
    else:
        print(f"No response from {destination}")
        return False


def check_alive():
    # open station list
    rows = csv_ops.open_csv_file(constants.STATIONS)
    for row in rows:
        ip = row['IP']
        hostname = row['HOSTNAME']
        print(ip, hostname)
        if not send_ping(ip):
            # station offline - remove entry from the list
            logger.add_log_entry(logging.INFO, f'Station {hostname} with IP: {ip} keep alive false - remove entry')
            # remove this row from .csv
            rows = [r for r in rows if r != row]
        else:
            # Encode 'KEEP_ALIVE'
            data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'KEEP_ALIVE_REQ', ''))
            # send to remote station
            tcp_client.start_client(ip, constants.TCP_PORT, data)
            # wait a moment...
            time.sleep(0.1)
            # check 'alive' value if False - remove entry
            if not alive:
                logger.add_log_entry(logging.INFO, f'Station {hostname} with IP: {ip} keep alive false - remove entry')
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
    while True:
        print('periodic keep alive')
        check_alive()
        time.sleep(interval)

# ---------------------------------------------------------------------------------------------
# announcer.py - 'Caller' send announcement UDP packet on network broadcast (tcp_port: 50000)
#
# Prerequisites: none
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import logging
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from time import sleep

import constants
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# Define global variables on module level
my_ip = ''


def announce_service(port, magic, interval):
    global my_ip
    s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    try:
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # this is a broadcast socket
        my_ip = gethostbyname(gethostname())  # get our IP.
        # (be careful of multiple NW interfaces or IPs)
        logger.add_log_entry(logging.DEBUG, f"announcer UDP socket bind successful")
    except Exception as e:
        # print(f"announcer UDP socket bind error occurred: {e}")
        logger.add_log_entry(logging.ERROR, f"announcer UDP socket bind error occurred: {e}")

    try:
        while True:
            data = magic + my_ip + gethostname()
            s.sendto(data.encode('utf-8'), ('<broadcast>', port))
            # print("Sent service announcement")
            logger.add_log_entry(logging.DEBUG, f"Sent service announcement. Announcement interval is {interval}")
            sleep(interval)
    except Exception as e:
        # print(f"error occurred: {e}")
        logger.add_log_entry(logging.CRITICAL, f"announcement send error occurred: {e}")
        s.close()

# Usage Example:
# port = 50000
# magic = constants.MAGIC
# interval = constants.ANNOUNCE_INTERVAL
# announce_service(tcp_port, magic, interval)

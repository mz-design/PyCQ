# ---------------------------------------------------------------------------------------------
# announcer.py - 'Caller' send announcement UDP packet on network broadcast (port: 50000)
#
# Prerequisites: none
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import constants
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
import logging
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def announce_service(port, magic, interval):
    s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    s.bind(('', 0))
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # this is a broadcast socket
    my_ip = gethostbyname(gethostname())  # get our IP.
    # (be careful of multiple NW interfaces or IPs)

    try:
        while True:
            data = magic + my_ip + gethostname()
            s.sendto(data.encode('utf-8'), ('<broadcast>', port))
            print("Sent service announcement")
            logger.add_log_entry(logging.DEBUG, "Sent service announcement")
            sleep(interval)
    except Exception as e:
        print(f"error occurred: {e}")
        logger.add_log_entry(logging.CRITICAL, f"announcer - error occurred: {e}")
        s.close()

# TODO: remove after debug
# port = 50000
# magic = constants.MAGIC
# interval = constants.ANNOUNCE_INTERVAL
# announce_service(port, magic, interval)

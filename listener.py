# ---------------------------------------------------------------------------------------------
# listener.py - Station listen for 'Caller' announcement UDP packet on network broadcast (port: 50000)
#
# Prerequisites: none
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import constants
from socket import socket, AF_INET, SOCK_DGRAM
import logging
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def listen_for_service(udp_port, udp_magic):
    s = socket(AF_INET, SOCK_DGRAM)  # create UDP socket
    s.bind(('', udp_port))
    caller_ip = None
    caller_hostname = None

    while True:
        try:
            data, addr = s.recvfrom(1024)  # wait for a packet
        except Exception as e:
            print(f"Error receiving packet: {e}")
            logger.add_log_entry(logging.ERROR, f"Error receiving announcement packet: {e}")
            continue

        if data.decode('utf-8').startswith(udp_magic):
            caller_ip = addr[0]
            caller_hostname = data[len(magic)+len(caller_ip):].decode('utf-8')
            print(f"Got service announcement from {caller_ip} {caller_hostname}")
            logger.add_log_entry(logging.INFO, f"Got service announcement from {caller_ip} {caller_hostname}")
            break

    # close the listening UDP socket
    s.close()
    return caller_ip, caller_hostname

# TODO: Register to 'Caller PC'
# def register_to_service(caller_ip, tcp_port)


# port = constants.UDP_PORT
# magic = constants.MAGIC
# listen_for_service(port, magic)


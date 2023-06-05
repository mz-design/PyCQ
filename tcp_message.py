# ------------------------------------------------------------------------------------------------------
# tcp_message.py - provide TcpMessage class for creating and parsing data strings for TCP communication
#
# Prerequisites: None
#
# initial release: 31.05.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import logging
import constants

# Initialize log
from logger import Logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


class TcpMessage:
    def __init__(self, ip, hostname, message, asset):
        self.ip = ip
        self.hostname = hostname
        self.message = message
        self.asset = asset

    def create(self):
        data = f"IP: {self.ip}\n"
        data += f"Hostname: {self.hostname}\n"
        data += f"Message: {self.message}\n"
        data += f"Asset: {self.asset}"
        logger.add_log_entry(logging.DEBUG, f"TCP message {self.message} with {self.ip} and {self.hostname} successfully created")
        return data

    def __str__(self):
        return f"Sender IP: {self.ip}\nSender Hostname: {self.hostname}\nMessage: {self.message}\nAsset: {self.asset}"

    @classmethod
    def parse(cls, data_string):
        try:
            lines = data_string.split("\n")
            ip = lines[0].split(": ")[1]
            hostname = lines[1].split(": ")[1]
            message = lines[2].split(": ")[1]
            asset = lines[3].split(": ")[1]
            return cls(ip, hostname, message, asset)
        except (IndexError, ValueError) as e:
            logger.add_log_entry(logging.ERROR, f"TcpMessage - Error parsing data string: {e}")


# TODO: Remove usage examples below after debugging
# Usage examples of class:
# received_data_string = "Sender IP: 192.168.0.1\nSender Hostname: myhostname\nMessage: Hello, TCP!"
# received_message = TcpMessage.parse(received_data_string)
# # Now, you can access the individual attributes of the received message
# print(received_message.ip)  # Output: 192.168.0.1
# print(received_message.hostname)  # Output: myhostname
# print(received_message.message)  # Output: Hello, TCP!

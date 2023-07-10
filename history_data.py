# ---------------------------------------------------------------------------------------------
# history_data.py - holds HistoryData class
#
# Prerequisites: none
#
# Beta release: 10.07.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import ipaddress
import logging

import constants
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


class HistoryData:
    def __init__(self, time, hostname, ip, asset):
        if not isinstance(time, str):
            logger.add_log_entry(logging.ERROR, "class:HistoryData - 'time' must be a string")
            raise TypeError("time must be a string")
        if not isinstance(hostname, str):
            logger.add_log_entry(logging.ERROR, "class:HistoryData - 'hostname' must be a string")
            raise TypeError("hostname must be a string")
        if not isinstance(ip, str):
            logger.add_log_entry(logging.ERROR, "class:HistoryData - 'ip' must be a string")
            raise TypeError("ip must be a string")
        if not isinstance(asset, str):
            logger.add_log_entry(logging.ERROR, "class:HistoryData - 'item' must be a string")
            raise TypeError("item must be a string")
        self.time = time
        self.hostname = hostname
        self.ip = ip
        self.asset = asset

    def check_ip(self):
        try:
            ipaddress.IPv4Address(self.ip)
        except ipaddress.AddressValueError:
            logger.add_log_entry(logging.WARNING, f"invalid ip format: {self.ip} - use '0.0.0.0' instead")
            self.ip = '0.0.0.0'
        return self.ip

    def check_hostname(self):
        # if hostname not sent use IP as a 'hostname'
        if self.hostname == '':
            logger.add_log_entry(logging.WARNING, f"No 'HOSTNAME' received - use ip {self.ip} instead")
            self.hostname = self.ip
        return self.hostname

    def check_asset(self):
        # if 'item' not sent - indicate ERROR
        if self.asset == '':
            logger.add_log_entry(logging.WARNING, f"No 'ITEM' received - mark as 'ERROR'")
            self.asset = 'ERROR'
        return self.asset

    def get_data(self):
        return {"TIME": self.time, "HOSTNAME": HistoryData.check_hostname(self), "IP": HistoryData.check_ip(self), "ASSET": HistoryData.check_asset(self)}

    def get_time(self):
        return self.time

    def get_hostname(self):
        return self.hostname

    def get_ip(self):
        return self.ip

    def get_asset(self):
        return self.asset

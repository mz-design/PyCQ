# ---------------------------------------------------------------------------------------------
# history_data.py - holds HistoryData class
#
# Prerequisites: none
#
# initial release: 31.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import logging
import ipaddress
import constants
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


class HistoryData:
    def __init__(self, time, action, hostname, ip, asset):
        if not isinstance(time, str):
            logger.add_log_entry(logging.ERROR, "class:HistoryData - 'time' must be a string")
            raise TypeError("time must be a string")
        if not isinstance(action, str):
            logger.add_log_entry(logging.ERROR, "class:HistoryData - 'action' must be a string")
            raise TypeError("action must be a string")
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
        self.action = action
        self.hostname = hostname
        self.ip = ip
        self.asset = asset

    def check_action(self):
        possible_actions = ('Text', 'Voice', 'Alert')
        if self.action not in possible_actions:
            logger.add_log_entry(logging.WARNING, f"Unrecognized Action: {self.action} - mark as 'ERROR'")
            self.action = 'ERROR'
        return self.action

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

    def check_item(self):
        # if 'item' not sent - indicate ERROR
        if self.item == '':
            logger.add_log_entry(logging.WARNING, f"No 'ITEM' received - mark as 'ERROR'")
            self.item = 'ERROR'
        return self.item

    def get_data(self):
        return {"TIME": self.time, "ACTION": HistoryData.check_action(self), "HOSTNAME": HistoryData.check_hostname(self),
                "IP": HistoryData.check_ip(self), "Item": HistoryData.check_item}

    def get_time(self):
        return self.time

    def get_action(self):
        return self.action

    def get_hostname(self):
        return self.hostname

    def get_ip(self):
        return self.ip

    def get_asset(self):
        return self.asset

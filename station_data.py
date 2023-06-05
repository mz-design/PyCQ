# ---------------------------------------------------------------------------------------------
# Station_data.py - holds StationData class
#
# Prerequisites: none
#
# initial release: 31.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import ipaddress
import logging
import constants
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


class StationData:
    def __init__(self, ip, hostname):
        if not isinstance(ip, str):
            logger.add_log_entry(logging.ERROR, "class:StationData - 'ip' must be a string")
            raise TypeError("'ip' must be a string")
        if not isinstance(hostname, str):
            logger.add_log_entry(logging.ERROR, "class:StationData - 'hostname' must be a string")
            raise TypeError("'hostname' must be a string")
        self.ip = ip
        self.hostname = hostname

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

    def get_data(self):
        return {"IP": StationData.check_ip(self), "HOSTNAME": StationData.check_hostname(self)}

    def get_ip(self):
        return self.ip

    def get_hostname(self):
        return self.hostname

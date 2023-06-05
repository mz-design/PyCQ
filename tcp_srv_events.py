# ------------------------------------------------------------------------------------------------------
# tcp_srv_events.py -  server events logic - process incoming TCP message
#
# Prerequisites: None
#
# initial release: 31.05.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import constants
import csv_ops
import station
import tcp_client
from tcp_message import TcpMessage
from announcer import gethostname, gethostbyname
from station_data import StationData
import keep_alive
import logging
from logger import Logger

# Initialize log
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())


def process_message(data):

    # Parse received message
    ip = TcpMessage.parse(data)
    hostname = TcpMessage.parse(data).hostname
    message = TcpMessage.parse(data).message
    asset = TcpMessage.parse(data).asset

    if message == 'REGISTER':
        # Search for station in 'stations.csv' add new entry on when does not exist (Caller)
        rows = csv_ops.open_csv_file(constants.STATIONS)
        for row in rows:
            # find and remove duplicates
            if row.get('IP') == ip or row.get('HOSTNAME') == hostname:
                # found conflict - remove station entry
                logger.add_log_entry(logging.INFO, f'Found station with IP: {ip} and Hostname: '
                                                   f'{row.get("HOSTNAME")} - remove old entry')
                csv_ops.remove_csv_row(constants.STATIONS, row)
        # add new entry
        new_line = StationData(ip, hostname)
        csv_ops.append_to_csv(constants.STATIONS, StationData.get_data(new_line))
        # encode 'REGISTER_ACK' message
        data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'REGISTER_ACK', ''))
        # send to remote station
        tcp_client.start_client(ip, constants.TCP_PORT, data)
        logger.add_log_entry(logging.INFO, f"'REGISTER_ACK' sent to station {hostname}")

    elif message == 'REGISTER_ACK':
        # station_update_status(status='online')
        station.station_online = True
        logger.add_log_entry(logging.INFO, f"'REGISTER_ACK' received from 'Caller'")
        logger.add_log_entry(logging.INFO, "Station status set ONLINE")

    elif message == 'NEW_MESSAGE_IND':
        # station_retrieve_message(asset)
        # Process message retrieval (Station)
        # Encode 'NEW_MESSAGE_ACK'
        data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'NEW_MESSAGE_ACK', asset))
        # send to remote station
        tcp_client.start_client(ip, constants.TCP_PORT, data)

    # elif message == 'NEW_MESSAGE_ACK':
        # Process 'NEW_MESSAGE_ACK' (on Caller) - mark message as 'delivered'
        # caller_update_messge_status(status=read)

    elif message == 'KEEP_ALIVE_REQ':
        # Encode 'KEEP_ALIVE_ACK'
        data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'KEEP_ALIVE_ACK', asset))
        # send to remote station
        tcp_client.start_client(ip, constants.TCP_PORT, data)

    elif message == 'KEEP_ALIVE_ACK':
        # keep alive acknowledge received - update keep_alive.alive True
        keep_alive.alive = True
    else:
        # Unexpected message - process as "msg_not_recognized" ERROR
        print(f"ERROR - unexpected message type: {TcpMessage.parse(data).message}")


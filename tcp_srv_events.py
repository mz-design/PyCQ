# ------------------------------------------------------------------------------------------------------
# tcp_srv_events.py -  TCP server events logic - process incoming TCP message and generates actions
#                       and responses
# Prerequisites: None
#
# initial release: 31.05.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import constants
import csv
import csv_ops
import new_msg_rcv
import station
import tcp_client
from tcp_message import TcpMessage
from announcer import gethostname, gethostbyname
from station_data import StationData
from history_data import HistoryData
import keep_alive
import datetime
import logging
from logger import Logger

# Initialize log
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())


def process_message(data):
    # Parse received message
    ip = TcpMessage.parse(data).ip
    hostname = TcpMessage.parse(data).hostname
    message = TcpMessage.parse(data).message
    asset = TcpMessage.parse(data).asset

    if message == 'REGISTER':
        # Search for station in 'stations.csv' add new entry on when does not exist (Caller)
        rows = csv_ops.open_csv_file(constants.STATIONS)
        for row in rows:
            # find and remove duplicates
            if row.get('IP') == ip or row.get('HOSTNAME') == hostname:
                # we found conflict - remove station entry
                logger.add_log_entry(logging.INFO, f'Found station with IP: {ip} and Hostname: '
                                                   f'{row.get("HOSTNAME")} - remove old entry')
                # csv_ops.remove_csv_row(constants.STATIONS, row)
                rows = [r for r in rows if r != row]
                # Write changes to stations.csv file
                fieldnames = ['IP', 'HOSTNAME']
                with open(constants.STATIONS, 'w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for new_row in rows:
                        writer.writerow(new_row)

        # add new line entry to the file
        new_line = StationData(ip, hostname)
        csv_ops.append_to_csv(constants.STATIONS, StationData.get_data(new_line))

        # encode 'REGISTER_ACK' message
        data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'REGISTER_ACK', asset))

        # send to remote station
        tcp_client.start_client(ip, constants.TCP_PORT, data)
        logger.add_log_entry(logging.INFO, f"'REGISTER_ACK' sent to station {hostname}")

    elif message == 'REGISTER_ACK':
        # update station status to 'online'
        logger.add_log_entry(logging.INFO, f"'REGISTER_ACK' received from 'Caller' -  station status is ONLINE")

    elif message == 'NEW_MESSAGE_IND':
        # station_retrieve_message(asset)
        new_msg_rcv.receive_and_play_new_message(ip, asset)
        # Encode 'NEW_MESSAGE_ACK'
        data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'NEW_MESSAGE_ACK', asset))
        # send to remote station
        tcp_client.start_client(ip, constants.TCP_PORT, data)

    elif message == 'NEW_MESSAGE_ACK':
        # Add new entry to 'history.csv'
        time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        new_line = HistoryData(time, hostname, ip, asset)
        csv_ops.append_to_csv(constants.HISTORY, HistoryData.get_data(new_line))

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
        logger.add_log_entry(logging.ERROR, f"ERROR - unexpected message type: {TcpMessage.parse(data).message}")


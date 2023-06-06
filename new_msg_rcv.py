# ------------------------------------------------------------------------------------------------------
# new_msg_rcv.py -  Statio receive and play new message
#
# Prerequisites: requests
#
# initial release: 31.05.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import audio
import requests
import constants
import tcp_client
from socket import gethostname, gethostbyname
from tcp_message import TcpMessage
from station_data import StationData
import logging
from logger import Logger

# Initialize log
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())


def download_file(url, save_path):
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
        logger.add_log_entry(logging.INFO, f"New message file: {url} successfully downloaded to {save_path}")
    else:
        print("Error downloading file.")
        logger.add_log_entry(f"Error downloading file: {url}")


def receive_and_play_new_message(caller_ip, asset):
    # get message file from 'Caller' http
    url = f'http://{caller_ip}:{constants.HTTP_PORT}/{constants.MESSAGE_STORE}/{asset}'
    print(url)
    save_path = f'{constants.MESSAGE_STORE}/{asset}'
    print(save_path)
    download_file(url, save_path)

    # play audio message from file
    audio.voice_play(f'{constants.MESSAGE_STORE}/{asset}')

# def send_new_message_ack(asset):
    # here comes code

# receive_and_play_new_message('10.100.102.63', '2023-06-06_18-44-21.ogg')




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
import datetime
import threading
import custom_popup
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
    if asset.endswith(constants.AUDIO_TYPE):  # we deal with audio message - get message file from 'Caller' http
        url = f'http://{caller_ip}:{constants.HTTP_PORT}/{constants.MESSAGE_STORE}/{asset}'
        print(url)
        save_path = f'{constants.MESSAGE_STORE}/{asset}'
        print(save_path)
        download_file(url, save_path)
        # play 'call_2_attention' preamble sound
        if constants.PLAY_C2A:
            audio.voice_play(f'{constants.RESOURCE_FOLDER}/{constants.C2A_FILE}')
            # audio_file = f'{constants.RESOURCE_FOLDER}/{constants.C2A_FILE}'
            # audio_thread = threading.Thread(target=audio.voice_play, args=(audio_file,))
            # audio_thread.start()
        # audio.voice_play(f'{constants.MESSAGE_STORE}/{asset}')
        # show custom popup and play audio message from file
        custom_popup.show_custom_popup(f"New Voice Message    {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                                       'message-icon.png', asset)

    # elif asset == "text":
    #     pass
    #     # text message
    elif asset == "fire_alert":
        custom_popup.show_custom_popup(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\nFire alert - immediately proceed to emergency exit !!!", 'fire_alert.png', "emergency_alarm.ogg")

    elif asset == "earthquake_alert":
        custom_popup.show_custom_popup(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\nEarthquake - immediately leave the building !!!", 'earthquake_alert.png', "emergency_alarm.ogg")

    elif asset == "tsunami_alert":
        custom_popup.show_custom_popup(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\nTsunami - immediately proceed to evacuation !!!", 'tsunami_alert.png', "emergency_alarm.ogg")

    elif asset == "intruder_alert":
        custom_popup.show_custom_popup(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\nIntruder alert - follow security procedures !!!", 'intruder_alert.png', "emergency_alarm.ogg")

    elif asset == "missile_alert":
        custom_popup.show_custom_popup(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\nMissile alert - Go to shelter immediately!!!", 'rocket.png', "emergency_alarm.ogg")

    else:
        logger.add_log_entry(f'Unexpected MESSAGE TYPE: {asset}')

# def send_new_message_ack(asset):
# here comes code

# receive_and_play_new_message('10.100.102.63', '2023-06-06_18-44-21.ogg')

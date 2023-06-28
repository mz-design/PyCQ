# ------------------------------------------------------------------------------------------------------
# custom_popup.py -  used to show the customized alert popup to user
#
# Prerequisites: PySide6.QtWidgets, PySide6.QtCore, PySide6.QtGui
#
# initial release: 14.06.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

from PyQt6.QtWidgets import QApplication
import audio
from message_popup import RoundedMessageWindow
import threading
import multiprocessing
import constants
from logger import Logger
import logging
import os

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def create_custom_popup(message, image, sound_file):
    try:
        app = QApplication([])
        app.setStyle("fusion")

        image_path = f"{constants.RESOURCE_FOLDER}/{image}"
        if image == "message-icon.png":
            # new voice message
            audio_file_path = f"{constants.MESSAGE_STORE}/{sound_file}"
        else:
            # alarm message
            audio_file_path = f"{constants.RESOURCE_FOLDER}/{sound_file}"

        popup = RoundedMessageWindow(message, image_path, audio_file_path)

        # start playing audio in new thread
        audio_thread = threading.Thread(target=audio.voice_play, args=(audio_file_path,))
        audio_thread.start()

        # visual popup to user
        popup.show()
        app.exec()

    except Exception as e:
        print(f"Error: {e}")
        logger.add_log_entry(logging.ERROR, f"Exception: {e}")


def show_custom_popup(message, image, sound_file):
    popup_process = multiprocessing.Process(target=create_custom_popup, args=(message, image, sound_file))
    popup_process.start()
    popup_process.join()

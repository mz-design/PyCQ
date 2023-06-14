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
from alert_popup import RoundedAlertWindow
import threading
import constants
from logger import Logger
import logging
# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def show_custom_popup(message, image, sound_file):
    try:
        app = QApplication([])
        app.setStyle("fusion")

        image_path = f"{constants.RESOURCE_FOLDER}/{image}"
        if image == 'message-icon.png':
            audio_file_path = f"{constants.MESSAGE_STORE}/{sound_file}"
            popup = RoundedMessageWindow(message, image_path, audio_file_path)
        else:
            audio_file_path = f"{constants.RESOURCE_FOLDER}/{sound_file}"
            popup = RoundedAlertWindow(message, image_path)

        # start playing audio in new thread
        audio_thread = threading.Thread(target=audio.voice_play, args=(audio_file_path,))
        audio_thread.start()

        # visual popup to user
        popup.show()
        app.exec()
    except Exception as e:
        print(f"Error: {e}")
        logger.add_log_entry(logging.ERROR, f"Exception: {e}")


# show_custom_popup("New voice message", "message-icon.png", "emergency_alarm.ogg")
# show_custom_popup("Missile alert - Go to shelter immediately!!!", 'rocket.png', "emergency_alarm.ogg")
# show_custom_popup("Fire alert - immediately proceed to emergency exit !!!", 'fire_alert.png', "emergency_alarm.ogg")
# show_custom_popup("Earthquake - immediately leave the building !!!", 'earthquake_alert.png', "emergency_alarm.ogg")
# show_custom_popup("Tsunami - immediately proceed to evacuation !!!", 'tsunami_warning.png', "emergency_alarm.ogg")
# show_custom_popup("Red alert - immediately go to nearest shelter !!!", 'red_alert.png', "emergency_alarm.ogg")
# show_custom_popup("Intruder alert - follow security procedures !!!", 'intruder_alert.png', "emergency_alarm.ogg")
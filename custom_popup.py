# ------------------------------------------------------------------------------------------------------
# custom_popup.py -  used to show the customized alert popup to user
#
# Prerequisites: PySide6.QtWidgets, PySide6.QtCore, PySide6.QtGui
#
# initial release: 14.06.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

from PyQt6.QtWidgets import QApplication
import audio
from alert_popup import RoundedPopupWindow
import threading
import constants


def show_custom_popup(message, image, sound_file):
    image_path = f"{constants.RESOURCE_FOLDER}/{image}"
    audio_file = f"{constants.RESOURCE_FOLDER}/{sound_file}"
    # start playing audio in new thread
    audio_thread = threading.Thread(target=audio.voice_play, args=(audio_file,))
    audio_thread.start()

    # visual popup to user
    app = QApplication([])
    popup = RoundedPopupWindow(message, image_path)
    popup.show()

    app.exec()


# show_custom_popup("New voice message", 'message-icon.png', "emergency_alarm.ogg")
# show_custom_popup("Missile alert - Go to shelter immediately!!!", 'rocket.png', "emergency_alarm.ogg")
# show_custom_popup("Fire alert - immediately proceed to emergency exit !!!", 'fire_alert.png', "emergency_alarm.ogg")
# show_custom_popup("Earthquake - immediately leave the building !!!", 'earthquake_alert.png', "emergency_alarm.ogg")
# show_custom_popup("Tsunami - immediately proceed to evacuation !!!", 'tsunami_warning.png', "emergency_alarm.ogg")
# show_custom_popup("Red alert - immediately go to nearest shelter !!!", 'red_alert.png', "emergency_alarm.ogg")
# show_custom_popup("Intruder alert - follow security procedures !!!", 'intruder_alert.png', "emergency_alarm.ogg")
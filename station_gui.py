# ---------------------------------------------------------------------------------------------------
# station_gui.py - 'Station' GUI procedures
#
# Prerequisites: PySide6
#
# Beta release: 10.07.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

import json
import logging
import os
import sys
import threading
import time
from multiprocessing import Process, freeze_support
from socket import gethostbyname, gethostname

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, QSlider, QPushButton, QLabel

import audio
import cleanup
import constants
import listener
import tcp_client
import tcp_server
from app_context import get_qapp
from logger import Logger
from message_popup import RoundedMessageWindow
from tcp_message import TcpMessage

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# Initialize data store, check if exists and create when needed - not required for frozen distributable (.exe)
if not getattr(sys, 'frozen', False):
    directory = constants.MESSAGE_STORE
    if not os.path.exists(directory):
        os.makedirs(directory)


# Perform log cleanup on startup
cleanup.clean_log(constants.LOG_FILE, 0)

# Get configuration from constants
udp_port = constants.UDP_PORT
magic = constants.MAGIC
tcp_port = constants.TCP_PORT
http_port = constants.HTTP_PORT

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())


def register_to_service():
    caller_ip, caller_hostname = listener.listen_for_service(udp_port, magic)
    # print(caller_ip, caller_hostname)
    data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'REGISTER', ''))
    tcp_client.start_client(caller_ip, constants.TCP_PORT, data)
    logger.add_log_entry(logging.DEBUG, f"Sent 'REGISTER' message to {caller_hostname} with IP {caller_ip}")


def run_periodically(interval, exit_flag):
    cleanup_counter = 0
    while not exit_flag.is_set():
        logger.add_log_entry(logging.DEBUG, "Periodic station Register started")
        # print("periodic station register\n")
        # clean-up log file on station periodically (kind of 'log rotator')
        if cleanup_counter == constants.LOG_ROTATOR_COUNTER:
            logger.add_log_entry(logging.INFO, f"Periodic clean-up on clean-up counter {cleanup_counter}")
            cleanup.clean_log(constants.LOG_FILE, constants.LOG_MAX_LINES)
            cleanup_counter = 0
        cleanup_counter += 1
        register_to_service()
        time.sleep(interval)


def show_tray_message(tray):
    tray.showMessage("PyCQ Beta 1.0.0", "MZ-Design 2023")


def create_tray_icon(exit_flag):
    # Create the Application object
    app = get_qapp()

    # Create a system tray icon
    tray = QSystemTrayIcon()
    icon = QIcon(f"{constants.RESOURCE_FOLDER}/icon.png")
    tray.setIcon(icon)
    tray.setToolTip("PyCQ message client")

    # Create a context menu for the system tray
    menu = QMenu()
    action = QAction("About")
    action.triggered.connect(lambda: show_tray_message(tray))
    menu.addAction(action)

    # Add the transparency_value widget menu item
    transparency_action = QAction("Change popup transparency")
    transparency_action.triggered.connect(lambda: create_transparency_widget())
    menu.addAction(transparency_action)

    # Add the volume_value widget menu item
    volume_action = QAction("Change message volume")
    volume_action.triggered.connect(lambda: create_volume_widget())
    menu.addAction(volume_action)

    # Add exit action
    exit_action = QAction("Exit")
    exit_action.triggered.connect(lambda: exit_application(exit_flag, tray))  # Connect to the exit_application function
    menu.addAction(exit_action)
    if not constants.ENABLE_EXIT:
        exit_action.setEnabled(False)

    # Set the context menu for the system tray
    tray.setContextMenu(menu)

    # Show the system tray icon
    tray.show()

    # Create thread objects for TCP server and periodic register
    thread_tcp_server = threading.Thread(target=tcp_server.start_server, args=(my_hostname, tcp_port))
    thread_periodic_register = threading.Thread(target=run_periodically, args=(constants.STATION_REGISTER_INTERVAL, exit_flag))

    # Start the threads
    thread_tcp_server.start()
    thread_periodic_register.start()

    # Start the application event loop
    app.exec()


def exit_application(exit_flag, tray):
    # Hide the tray icon
    tray.hide()

    # Set the exit flag to stop the threads
    exit_flag.set()

    # Terminate all application processes
    os._exit(0)


def show_tray_icon():
    # # Create the exit flag as a global variable
    exit_flag = threading.Event()
    create_tray_icon(exit_flag)


def create_transparency_widget():

    # Load transparency_value value from a conf_file, or use a default value
    try:
        with open('transparency.json') as file:
            transparency_value = json.load(file)
    except FileNotFoundError:
        transparency_value = constants.TRANSPARENCY

    # Create the transparency_value widget
    widget = QWidget()
    widget.setWindowFlags(Qt.FramelessWindowHint)  # Remove window title
    widget.setAttribute(Qt.WA_StyledBackground)  # Enable styling for the widget

    # Create the label
    label = QLabel("Transparency                                                ")

    # Create the slider
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(255)
    slider.setValue(transparency_value)  # Set the initial value from the loaded transparency_value value
    # Disable slider programmatically in constants file - very useful option :))))
    if not constants.ENABLE_CHANGE_TRANSPARENCY:
        slider.setEnabled(False)
        label = QLabel("Transparency (Setting DISABLED by your system Administrator)")

    # Set the layout for the widget and add the slider
    layout = QVBoxLayout(widget)
    layout.addWidget(label)
    layout.addWidget(slider)

    # Function to update the transparency_value of the widget
    def update_widget_transparency(value):
        if value < 10:
            widget.setWindowOpacity((value + 10) / 255)
        else:
            widget.setWindowOpacity(value / 255)
        create_transparency_widget.transparency_value = value

        # Update the stored transparency_value value in the conf_file
        with open('transparency.json', 'w') as conf_file:
            json.dump(value, conf_file)

    # Connect the slider's valueChanged signal to update_widget_transparency
    slider.valueChanged.connect(update_widget_transparency)

    # Create the close button
    close_button = QPushButton("Close")
    close_button.setFixedSize(50, 20)

    # Function to handle the close button click event
    def close_widget():
        widget.hide()

    # Connect the close button's clicked signal to close_widget
    close_button.clicked.connect(close_widget)

    # Add the close button to the layout
    layout.addWidget(close_button)

    widget.show()

    # Get the current geometry of the widget
    geometry = widget.geometry()

    # Multiply the dimensions by ...
    new_width = int(geometry.width() * 1)
    new_height = int(geometry.height() * 1)

    # Resize the widget
    widget.resize(new_width, new_height)

    # Get the dimensions of the screen
    screen = get_qapp().primaryScreen()
    screen_geometry = screen.geometry()

    # Calculate the new position of the widget
    new_x = screen_geometry.right() - widget.width() - 50
    new_y = screen_geometry.bottom() - widget.height() - 40

    # Move the widget to the new position
    widget.move(new_x, new_y)

    # Set the initial opacity of the widget
    if transparency_value < 10:
        widget.setWindowOpacity((transparency_value + 10) / 255)
    else:
        widget.setWindowOpacity(transparency_value / 255)


def create_volume_widget():

    # Load volume_value value from a conf_file, or use a default value
    try:
        with open('volume.json') as file:
            volume_value = json.load(file)
    except FileNotFoundError:
        volume_value = constants.OUTPUT_VOLUME

    # Create the transparency_value widget
    widget = QWidget()
    widget.setWindowFlags(Qt.FramelessWindowHint)  # Remove window title
    widget.setAttribute(Qt.WA_StyledBackground)  # Enable styling for the widget

    # Create the label
    label = QLabel("Volume                                                          ")

    # Create the slider
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(-50)
    slider.setMaximum(0)
    slider.setValue(volume_value)  # Set the initial value from the loaded transparency_value value
    # Disable slider programmatically in constants file - very useful option :))))
    if not constants.ENABLE_CHANGE_VOLUME:
        slider.setEnabled(False)
        label = QLabel("Volume (Setting DISABLED by your system Administrator)          ")

    # Set the layout for the widget and add the slider
    layout = QVBoxLayout(widget)
    layout.addWidget(label)
    layout.addWidget(slider)

    # Function to update the volume
    def update_volume(value):
        # Update the stored transparency_value value in the conf_file
        with open('volume.json', 'w') as conf_file:
            json.dump(value, conf_file)

    # Connect the slider's valueChanged signal to update_volume
    slider.valueChanged.connect(update_volume)

    # Create the close button
    close_button = QPushButton("Close")
    close_button.setFixedSize(50, 20)

    # Function to handle the close button click event
    def close_widget():
        widget.hide()

    # Connect the close button's clicked signal to close_widget
    close_button.clicked.connect(close_widget)

    # Add the close button to the layout
    layout.addWidget(close_button)

    widget.show()

    # Get the current geometry of the widget
    geometry = widget.geometry()

    # Multiply the dimensions by ...
    new_width = int(geometry.width() * 1)
    new_height = int(geometry.height() * 1)

    # Resize the widget
    widget.resize(new_width, new_height)

    # Get the dimensions of the screen
    screen = get_qapp().primaryScreen()
    screen_geometry = screen.geometry()

    # Calculate the new position of the widget
    new_x = screen_geometry.right() - widget.width() - 50
    new_y = screen_geometry.bottom() - widget.height() - 130

    # Move the widget to the new position
    widget.move(new_x, new_y)


def create_custom_popup(message, image, sound_file):
    try:
        app = get_qapp()

        image_path = f"{constants.RESOURCE_FOLDER}/{image}"
        if image == "message-icon.png":
            # new voice message
            audio_file_path = f"{constants.MESSAGE_STORE}/{sound_file}"

        else:
            # alarm message
            audio_file_path = f"{constants.RESOURCE_FOLDER}/{sound_file}"

        # start playing audio in new thread
        audio_thread = threading.Thread(target=audio.voice_play, args=(audio_file_path,))
        audio_thread.start()

        popup = RoundedMessageWindow(message, image_path, audio_file_path)

        # visual popup to user
        popup.show()
        app.exec()

    except Exception as e:
        print(f"Error: {e}")
        logger.add_log_entry(logging.ERROR, f"Exception: {e}")


def show_custom_popup(message, image, sound_file):
    # create_custom_popup(message, image, sound_file)
    popup_process = Process(target=create_custom_popup, args=(message, image, sound_file))
    popup_process.start()
    popup_process.join()

    # delete audio file after message popup is closed
    audio_file_path = f"{constants.MESSAGE_STORE}/{sound_file}"
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)
        # print(f"File '{sound_file}' deleted from MsgStore.")
        logger.add_log_entry(logging.INFO, f"File '{sound_file}' deleted from MsgStore.")


if __name__ == '__main__':
    # This check needed for freezing support (pyinstaller)
    if getattr(sys, 'frozen', False):
        freeze_support()
        os.chdir(sys._MEIPASS)

    show_tray_icon()

# ---------------------------------------------------------------------------------------------------
# station.py - 'Station' procedures
#
# Prerequisites: PySide6
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

import os
import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, QSlider, QPushButton
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
import constants
import logging
from socket import socket, gethostbyname, gethostname
import time
import csv_ops
import tcp_client
from tcp_message import TcpMessage
import http_srv
import cleanup
import listener
import tcp_server
from logger import Logger
import threading
import multiprocessing
import json

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# Initialize data store, check if exists and create when needed
directory = constants.MESSAGE_STORE
if not os.path.exists(directory):
    os.makedirs(directory)
if not os.path.exists(constants.HISTORY):
    csv_ops.open_csv_file(constants.HISTORY)

# Perform cleanups on startup
cleanup.clean_log(constants.LOG_FILE, constants.LOG_MAX_LINES)
cleanup.clean_history(constants.HISTORY, constants.HISTORY_MAX_ENTRIES)
cleanup.clean_AudioFiles(f'{constants.MESSAGE_STORE}/', constants.MESSAGE_STORE_MAX_FILES)

# Get configuration from constants
udp_port = constants.UDP_PORT
magic = constants.MAGIC
tcp_port = constants.TCP_PORT
http_port = constants.HTTP_PORT

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())


# Initialize transparency variable as a multiprocessing.Value
transparency = multiprocessing.Value('i', constants.TRANSPARENCY)


def update_transparency(value):
    transparency.value = value


def register_to_service():
    # if station_status != 'online':
    caller_ip, caller_hostname = listener.listen_for_service(udp_port, magic)
    print(caller_ip, caller_hostname)
    data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'REGISTER', ''))
    tcp_client.start_client(caller_ip, constants.TCP_PORT, data)
    logger.add_log_entry(logging.DEBUG, f"Sent 'REGISTER' message to {caller_hostname} with IP {caller_ip}")


def run_periodically(interval, exit_flag):
    cleanup_counter = 0
    while not exit_flag.is_set():
        logger.add_log_entry(logging.DEBUG, "Periodic station Register started")
        print("periodic station register\n")
        if cleanup_counter == 100:
            logger.add_log_entry(logging.INFO, f"Periodic clean-up on clean-up counter {cleanup_counter}")
            cleanup.clean_log(constants.LOG_FILE, constants.LOG_MAX_LINES)
            cleanup.clean_history(constants.HISTORY, constants.HISTORY_MAX_ENTRIES)
            cleanup.clean_AudioFiles(f'{constants.MESSAGE_STORE}/', constants.MESSAGE_STORE_MAX_FILES)
            cleanup_counter = 0
        cleanup_counter += 1
        register_to_service()
        time.sleep(interval)


def show_tray_message(tray):
    tray.showMessage("PyCQ Beta 1.0.0", "MZ-Design 2023")


def create_tray_icon(exit_flag):
    # Create the Application object
    app = QApplication([])

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

    # Add the transparency widget menu item
    transparency_action = QAction("Change message popup transparency")
    transparency_action.triggered.connect(lambda: show_transparency_widget())
    menu.addAction(transparency_action)

    exit_action = QAction("Exit")
    exit_action.triggered.connect(lambda: exit_application(exit_flag, tray))  # Connect to the exit_application function
    menu.addAction(exit_action)

    # Set the context menu for the system tray
    tray.setContextMenu(menu)

    # Show the system tray icon
    tray.show()

    # Create thread objects for TCP server, HTTP server, and periodic register
    thread_http_srv = threading.Thread(target=http_srv.start_http_server, args=(http_port,))
    thread_tcp_server = threading.Thread(target=tcp_server.start_server, args=(my_hostname, tcp_port))
    thread_periodic_register = threading.Thread(target=run_periodically,
                                                args=(constants.STATION_REGISTER_INTERVAL, exit_flag))

    # Start the threads
    thread_http_srv.start()
    thread_tcp_server.start()
    thread_periodic_register.start()

    # Start the application event loop
    app.exec_()


def exit_application(exit_flag, tray):
    # Hide the tray icon
    tray.hide()

    # Set the exit flag to stop the threads
    exit_flag.set()

    # Terminate all application processes
    os._exit(0)


def show_tray_icon():
    # Create the exit flag as a global variable
    exit_flag = multiprocessing.Event()

    # Create a process for the tray icon and start it
    icon_process = multiprocessing.Process(target=create_tray_icon, args=(exit_flag,))
    icon_process.start()

    # Wait for the tray icon process to finish
    icon_process.join()


def show_transparency_widget():
    # Create a separate process for the transparency widget
    widget_process = multiprocessing.Process(target=create_transparency_widget, args=(transparency,))
    widget_process.start()


def create_transparency_widget(transparency):
    # Create the Application object
    app = QApplication([])

    # Load transparency value from a file, or use a default value
    try:
        with open('transparency.json') as file:
            transparency_value = json.load(file)
    except FileNotFoundError:
        transparency_value = constants.TRANSPARENCY

    # Create the transparency widget
    widget = QWidget()
    widget.setWindowFlags(Qt.FramelessWindowHint)  # Remove window title
    widget.setAttribute(Qt.WA_StyledBackground)  # Enable styling for the widget

    # Create the slider
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(255)
    slider.setValue(transparency_value)  # Set the initial value from the loaded transparency value

    # Set the layout for the widget and add the slider
    layout = QVBoxLayout(widget)
    layout.addWidget(slider)

    # Function to update the transparency of the widget
    def update_transparency(value):
        if value < 10:
            widget.setWindowOpacity((value + 10) / 255)
        else:
            widget.setWindowOpacity(value / 255)
        transparency.value = value

        # Update the stored transparency value in the file
        with open('transparency.json', 'w') as file:
            json.dump(value, file)

    # Connect the slider's valueChanged signal to update_transparency
    slider.valueChanged.connect(update_transparency)

    # Create the close button
    close_button = QPushButton("Close")
    close_button.setFixedSize(50, 20)

    # Function to handle the close button click event
    def close_widget():
        widget.close()

    # Connect the close button's clicked signal to close_widget
    close_button.clicked.connect(close_widget)

    # Add the close button to the layout
    layout.addWidget(close_button)

    widget.show()

    # Get the current geometry of the widget
    geometry = widget.geometry()

    # Multiply the dimensions by 3
    new_width = int(geometry.width() * 3)
    new_height = int(geometry.height() * 1)

    # Resize the widget
    widget.resize(new_width, new_height)

    # Get the dimensions of the screen
    screen = app.primaryScreen()
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

    # Start the application event loop for the transparency widget
    app.exec_()

if __name__ == '__main__':
    show_tray_icon()

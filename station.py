# ---------------------------------------------------------------------------------------------------
# station.py - 'Station' procedures
#
# Prerequisites: PySide6,
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

import os
import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QCoreApplication
import constants
import logging
from socket import socket, gethostbyname, gethostname
import time
import station_status
import csv_ops
import tcp_client
from tcp_message import TcpMessage
import http_srv
import cleanup
import listener
import tcp_server
from logger import Logger
import threading

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

# Initially set station_status to OFFLINE
station_status.StationStatus = 'offline'
logger.add_log_entry(logging.WARNING, f"Station {my_hostname} {my_ip} is OFFLINE")


def register_to_service():
    if station_status.StationStatus != 'online':
        caller_ip, caller_hostname = listener.listen_for_service(udp_port, magic)
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


def exit_application():
    # Close the tray icon
    tray.hide()
    # Terminate all application processes
    os._exit(0)



# Create the Application object
app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)  # Ensure the application doesn't exit when the main window is closed

# Create thread objects for TCP server, HTTP server, and periodic register
exit_flag = threading.Event()
thread_http_srv = threading.Thread(target=http_srv.start_http_server, args=(http_port,))
thread_tcp_server = threading.Thread(target=tcp_server.start_server, args=(my_hostname, tcp_port))
thread_periodic_register = threading.Thread(target=run_periodically, args=(constants.STATION_REGISTER_INTERVAL, exit_flag))

# Start the threads
thread_http_srv.start()
thread_tcp_server.start()
time.sleep(0.01)
thread_periodic_register.start()

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
exit_action = QAction("Exit")
exit_action.triggered.connect(exit_application)  # Connect to the exit_application function
menu.addAction(exit_action)

# Set the context menu for the system tray
tray.setContextMenu(menu)

# Show the system tray icon
tray.show()

# Start the application event loop
sys.exit(app.exec())

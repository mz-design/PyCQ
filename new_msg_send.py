# ------------------------------------------------------------------------------------------------------
# new_msg_send.py -  Caller record and send new message
#
# Prerequisites: None
#
# initial release: 31.05.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

import audio
import constants
import tcp_client
from announcer import gethostname, gethostbyname
from tcp_message import TcpMessage
from station_data import StationData
from time import sleep
import logging
from logger import Logger
import sys
from PySide6.QtWidgets import QApplication, QLabel, QRadioButton, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

# Initialize log
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

my_hostname = gethostname()
my_ip = gethostbyname(gethostname())


def record_and_send_new_message(cast, ip, ip_list):
    # Record new message
    print(f"Start Recording in 0.2 Sec !!! for {constants.REC_TIME} seconds") # it's just for debug
    logger.add_log_entry(logging.INFO, f"Start Recording for {constants.REC_TIME} seconds")
    sleep(0.2)   # it's just for debug
    try:
        asset = audio.voice_rec()
    except Exception as e:
        print(f"An error occurred: {e}")
        asset = None
    print(asset)

    # Encode 'NEW_MESSAGE_IND' message
    data = TcpMessage.create(TcpMessage(my_ip, my_hostname, 'NEW_MESSAGE_IND', asset))

    # Uni-cast case
    if cast == 'uni-cast':
        station_address = ip

        # Send 'NEW_MESSAGE_IND' to remote station
        tcp_client.start_client(station_address, constants.TCP_PORT, data)
        logger.add_log_entry(logging.INFO, f"'NEW_MESSAGE_IND' sent to station {station_address}")

    # Multicast case
    elif cast == 'multicast':
        # Send 'NEW_MESSAGE_IND' to remote stations
        for i in ip_list:
            station_address = ip_list[i]
            tcp_client.start_client(station_address, constants.TCP_PORT, data)
            logger.add_log_entry(logging.INFO, f"'NEW_MESSAGE_IND' sent to station {station_address}")



# GUI section
def record_and_send():
    cast = cast_var.get()
    ip = ip_entry.text()
    ip_list = ip_list_entry.text()
    # Record and send message with given parameters
    record_and_send_new_message(cast, ip, ip_list)


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Record and Send Message")

cast_label = QLabel("Cast Type:")
cast_var = "uni-cast"
cast_radio1 = QRadioButton("Uni-cast", checked=True)
cast_radio1.toggled.connect(lambda: setattr(cast_radio1, "isChecked", True) if cast_radio1.isChecked() else setattr(cast_radio2, "isChecked", True))
cast_radio2 = QRadioButton("Multicast")
cast_radio2.toggled.connect(lambda: setattr(cast_radio2, "isChecked", True) if cast_radio2.isChecked() else setattr(cast_radio1, "isChecked", True))

ip_label = QLabel("IP Address:")
ip_entry = QLineEdit()

ip_list_label = QLabel("IP List:")
ip_list_entry = QLineEdit()

record_button = QPushButton("Record and Send")
record_button.clicked.connect(record_and_send)

cast_layout = QHBoxLayout()
cast_layout.addWidget(cast_label)
cast_layout.addWidget(cast_radio1)
cast_layout.addWidget(cast_radio2)

ip_layout = QHBoxLayout()
ip_layout.addWidget(ip_label)
ip_layout.addWidget(ip_entry)

ip_list_layout = QHBoxLayout()
ip_list_layout.addWidget(ip_list_label)
ip_list_layout.addWidget(ip_list_entry)

button_layout = QHBoxLayout()
button_layout.addStretch()
button_layout.addWidget(record_button)
button_layout.addStretch()

layout = QVBoxLayout()
layout.addLayout(cast_layout)
layout.addLayout(ip_layout)
layout.addLayout(ip_list_layout)
layout.addStretch()
layout.addLayout(button_layout)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())

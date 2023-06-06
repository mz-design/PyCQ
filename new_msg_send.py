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
import tkinter as tk

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
    ip = ip_entry.get()
    ip_list = ip_list_entry.get()
    # Record and send message with given parameters
    record_and_send_new_message(cast, ip, ip_list)


# Create GUI window
window = tk.Tk()
window.title("Record and Send Message")

# Create GUI elements
cast_label = tk.Label(window, text="Cast Type:")
cast_var = tk.StringVar(value="uni-cast")
cast_radio1 = tk.Radiobutton(window, text="Uni-cast", variable=cast_var, value="uni-cast")
cast_radio2 = tk.Radiobutton(window, text="Multicast", variable=cast_var, value="multi-cast")

ip_label = tk.Label(window, text="IP Address:")
ip_entry = tk.Entry(window)

ip_list_label = tk.Label(window, text="IP List:")
ip_list_entry = tk.Entry(window)

record_button = tk.Button(window, text="Record and Send", command=record_and_send)

# Add elements to GUI window
cast_label.grid(row=0, column=0)
cast_radio1.grid(row=0, column=1)
cast_radio2.grid(row=0, column=2)

ip_label.grid(row=1, column=0)
ip_entry.grid(row=1, column=1)

ip_list_label.grid(row=2, column=0)
ip_list_entry.grid(row=2, column=1)

record_button.grid(row=3, column=1
                   )

# Start GUI main loop
window.mainloop()
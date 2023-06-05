# ---------------------------------------------------------------------------------------------
# tcp_client.py - Connect TCP socket on server, send message and close connection
#
# Prerequisites: none
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import constants
import socket
import logging
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def start_client(tcp_host, tcp_port, data):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((tcp_host, tcp_port))
        print(f"Connected to server at {tcp_host}:{tcp_port}")
        logger.add_log_entry(logging.INFO, f"Connected to server at {tcp_host}:{tcp_port}")

        # Send data to the server
        message = data
        client_socket.send(message.encode("utf-8"))

        # Receive the response from the server
        # response = client_socket.recv(1024)
        # received_message = response.decode("utf-8")
        # print(f"Received message: {received_message}")
        # logger.add_log_entry(logging.INFO, f"Received message: {received_message}")

    except socket.gaierror as e:
        print(f"Address-related error occurred: {str(e)}")
        logger.add_log_entry(logging.ERROR, f"Address-related error occurred: {str(e)}")
    except socket.error as e:
        print(f"Socket error occurred: {str(e)}")
        logger.add_log_entry(logging.ERROR, f"Socket error occurred: {str(e)}")
    except socket.timeout as e:
        print(f"Timeout error occurred: {str(e)}")
        logger.add_log_entry(logging.ERROR, f"Socket error occurred: {str(e)}")
    finally:
        # Close the client socket
        client_socket.close()
        print("Client socket closed")
        logger.add_log_entry(logging.INFO, "Client socket closed")


# TODO: remove this Example usage after debug:
# tcp_host = '10.100.102.63'
# tcp_port = 1234
# start_client(tcp_host, tcp_port, "Hello!")

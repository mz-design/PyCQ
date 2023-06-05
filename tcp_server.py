# ---------------------------------------------------------------------------------------------
# tcp_server.py - Accepts TCP clients connections, receive message and close connection
#
# Prerequisites: none
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import constants
import threading
import logging
import socket
import tcp_srv_events
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def handle_client(client_socket, client_address):
    # Exception handling with try-except block
    received_message = ""
    try:
        # Handle the client connection
        print(f"Accepted connection from: {client_address}")
        # logger.add_log_entry(logging.INFO, f"Accepted connection from: {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024)
        received_message = data.decode("utf-8")
        print(f"Received message:\n{received_message}")
        logger.add_log_entry(logging.INFO, f"Received message: {received_message}")

        # Process received message
        # tcp_srv_events.process_message(received_message)

        # Send a response back to the client
        response_message = tcp_srv_events.process_message(received_message)
        client_socket.send(response_message.encode("utf-8"))

    except Exception as e:
        print(f"Error handling connection from {client_address}: {e}")
        # logger.add_log_entry(logging.ERROR, f"Error handling connection from {client_address}: {e}")
    finally:
        # Close the client socket
        client_socket.close()
        print(f"Closed connection with: {client_address}")
        # logger.add_log_entry(logging.INFO, f"Closed connection with: {client_address}")
    # return received_message


def start_server(tcp_host, tcp_port):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific tcp_host and tcp_port
    server_socket.bind((tcp_host, tcp_port))

    # Listen for incoming connections
    server_socket.listen()
    print(f"Server listening on {tcp_host}:{tcp_port}")
    logger.add_log_entry(logging.INFO, f"Server start listening on {tcp_host}:{tcp_port}")

    while True:
        # Exception handling with try-except block
        try:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()

            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except Exception as e:
            print(f"Error accepting client connection: {e}")
            logger.add_log_entry(logging.ERROR, f"Error accepting client connection: {e}")


# TODO: remove this Example usage after debug
# host = "10.100.102.63"
# port = 1234
# start_server(host, port)

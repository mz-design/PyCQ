# ---------------------------------------------------------------------------------------------
# http_srv.py - creates basic HTTP server for file transfer @ 'Caller' PC
#
# Prerequisites: none
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import constants
import http.server
import socketserver
import logging
from logger import Logger

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def start_http_server(port):
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("serving at tcp_port", port)
            httpd.serve_forever()
            logger.add_log_entry(logging.INFO, f"HTTP server started on tcp_port {port}: success")
    except Exception as e:
        print(f"Error: {e}")
        logger.add_log_entry(logging.ERROR, f"HTTP server error: {e}")


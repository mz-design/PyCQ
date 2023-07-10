# ---------------------------------------------------------------------------------------------
# http_srv.py - creates basic HTTP server for file transfer
#
# Prerequisites: none
#
# Beta release: 10.07.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import os
import logging
import constants
from logger import Logger

from http.server import HTTPServer, BaseHTTPRequestHandler

# Initialize logging
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        root_dir = os.getcwd()  # Get the current working directory
        path = self.path.lstrip('/')  # Remove leading slashes from the path

        # Check if the requested path is a file or directory in the local directory
        file_path = os.path.join(root_dir, path)
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        content = file.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                except Exception as e:
                    logger.add_log_entry(logging.ERROR, f"Error while reading file: {e}")
            elif os.path.isdir(file_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.generate_directory_listing(file_path).encode())
            return

        # If the requested path doesn't match any file or directory, respond with a 404 error
        self.send_error(404)

    def generate_directory_listing(self, dir_path):
        files = os.listdir(dir_path)
        response = "<html><head><title>Directory Listing</title></head><body><h1>Directory: {dir}</h1><ul>".format(
            dir=dir_path
        )
        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                response += f"<li><a href=\"/{file_path}\">{file_name}</a></li>"
            elif os.path.isdir(file_path):
                response += f"<li><a href=\"/{file_path}/\">{file_name}/</a></li>"
        response += "</ul></body></html>"
        return response

    def log_message(self, format, *args):
        return


def start_http_server(port):
    try:
        httpd = HTTPServer(('', port), MyHandler)
        logger.add_log_entry(logging.INFO, f"HTTP server started on port {port}: success")
        httpd.serve_forever()
    except Exception as e:
        # print(f"Error: {e}")
        logger.add_log_entry(logging.ERROR, f"HTTP server error: {e}")


# def start_http_server(port):
#
#     logger.add_log_entry(logging.DEBUG, f"Starting HTTP server on port {port}")
#     Handler = http.server.SimpleHTTPRequestHandler
#     try:
#         with socketserver.TCPServer(("", port), Handler) as httpd:
#             logger.add_log_entry(logging.INFO, f"HTTP server started on tcp_port {port}: success")
#             time.sleep(0.1)
#             httpd.serve_forever()
#
#     except Exception as e:
#         print(f"Error: {e}")
#         logger.add_log_entry(logging.ERROR, f"HTTP server error: {e}")

# ---------------------------------------------------------------------------------------
# csv_ops.py - operations with '.csv' files
#               Open (create if not found) required .csv data stores, read lines to dict
#
# Prerequisites: csv
#
# Beta release: 10.07.2023 - MichaelZ
# ---------------------------------------------------------------------------------------

import csv
import logging

import constants
from logger import Logger

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def open_csv_file(filename):
    rows = []                      # Initialize the lines storage

    try:
        # Try opening the file in read mode
        with open(filename, 'r', newline='') as file:
            # Create a CSV reader object
            reader = csv.DictReader(file)

            # Read and process the contents of the CSV file
            for row in reader:
                # Process each row as needed
                rows.append(row)
            logger.add_log_entry(logging.DEBUG, f'Read data lines from {filename} success')
            # Perform further operations on the CSV file as needed
            # ...
    except FileNotFoundError:
        # If the file doesn't exist, create it and open in write mode, write correct header
        if filename == constants.STATIONS:
            fieldnames = 'IP', 'HOSTNAME'
        else:
            fieldnames = 'TIME', 'HOSTNAME', 'IP', 'ASSET'
        with open(filename, 'w', newline='') as file:
            # Perform initial setup or write default data if needed
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Example header row
            logger.add_log_entry(logging.INFO, f"Create empty '.csv' file {filename}")
    return rows

    # File is automatically closed when exiting the 'with' block


def append_to_csv(filename, data):
    fieldnames = data.keys()

    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writerow(data)
        logger.add_log_entry(logging.DEBUG, f"Append new entry {data} to {filename}")

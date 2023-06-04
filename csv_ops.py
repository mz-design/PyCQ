# ---------------------------------------------------------------------------------------
# csv_ops.py - operations with '.csv' files
#               Open (create if not found) required .csv data stores, read lines to dict
#
# Prerequisites: pandas
#
# initial release: 31.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------

import csv
import pandas as pd
import logging
import constants

# Initialize logger
from logger import Logger
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
            fieldnames = 'TIME', 'ACTION', 'ITEM'
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


# def remove_csv_row(filename, row_to_remove):
#     df = pd.read_csv(filename)                          # Read the CSV file into a dataframe
#
#     df.drop(index=row_to_remove, inplace=True)          # Remove line with specific index from dataframe
#     df.reset_index(drop=True, inplace=True)
#
#     df.to_csv(filename, index=False)                   # Save the modified DataFrame back to CSV

# def remove_csv_row(filename, row_to_remove):
#     rows = []
#
#     with open(filename, 'r') as file:
#         reader = csv.DictReader(file)
#         fieldnames = reader.fieldnames
#         for row in reader:
#             rows.append(row)
#
#     with open(filename, 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         for i, row in enumerate(rows):
#             if i != row_to_remove:
#                 writer.writerow(row)

# TODO: Remove usage Example below after debug
# rows = open_csv_file(constants.HISTORY)
# # for row in rows:
# print(rows)

# append_to_csv(constants.HISTORY, {'Time' : '2342342342342342', 'Action' : 'huyhuy', 'Item' : '12121'})
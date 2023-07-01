# ---------------------------------------------------------------------------------------------------
# cleanup.py - Cleanup the 'MsgStore' folder, 'history.csv' and 'PyCQ.log' file to prevent oversizing
#
# Prerequisites: pandas
#
# initial release: 30.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

import csv
import glob
import logging
import os

import constants
from logger import Logger

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


def clean_AudioFiles(folder_path, num_to_keep):
    try:
        # Get a list of all files in the folder
        files = glob.glob(os.path.join(folder_path, "*"))

        # Sort the files by modification time (most recent first)
        files.sort(key=os.path.getmtime, reverse=True)

        # Identify the files to be deleted
        files_to_delete = files[num_to_keep:]

        # Delete the extra files
        for file_path in files_to_delete:
            os.remove(file_path)

        logger.add_log_entry(logging.INFO, f'MsgStore cleanup: Keep {num_to_keep} latest messages')

    except Exception as e:
        logger.add_log_entry(logging.ERROR, e)


def clean_pdf_file(csv_file, num_to_keep):
    try:
        # Read the CSV file and get the rows
        rows = []
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                rows.append(row)

        # Check if the rows have enough entries to keep
        if len(rows) > num_to_keep:
            # Identify the entries to be deleted
            if num_to_keep > 0:
                entries_to_delete = rows[:-num_to_keep]
            else:
                entries_to_delete = [rows[0]]  # Keep only the header row

            # Save the desired entries back to the CSV file
            with open(csv_file, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(entries_to_delete)

            logger.add_log_entry(logging.INFO, f'History cleanup: Keep {num_to_keep} latest CSV entries')
        else:
            logger.add_log_entry(logging.INFO, 'No history cleanup needed. Not enough entries.')

    except FileNotFoundError as e:
        logger.add_log_entry(logging.ERROR, f'File not found: {csv_file} - error {e}')
    except Exception as e:
        logger.add_log_entry(logging.ERROR, f'Error during history cleanup: {str(e)}')


def clean_log(log_file, num_to_keep):
    try:
        # Read the log file and extract log entries
        with open(log_file, "r") as file:
            log_entries = file.readlines()

        # Identify the entries to be deleted
        last_entries = log_entries[-num_to_keep:]
        # Rewrite the log file with the desired entries
        with open(log_file, "w") as file:
            file.writelines(last_entries)

        logger.add_log_entry(logging.INFO, f'Logfile cleanup: Keep {num_to_keep} latest log entries')

    except Exception as e:
        logger.add_log_entry(logging.ERROR, f"Clean log file failed: {e}")

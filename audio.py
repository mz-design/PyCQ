# ---------------------------------------------------------------------------------------------
# audio.py - Sound recorder/player module. Record audio from default input_device and
#            play to default output_device using numpy arrays. The file saved with unique
#            name convention using creation date-time to [PyCQ_root_directory]\Audio\.. folder
#
# Prerequisites: sounddevice, soundfile, numpy
#
# initial release: 28.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import constants
import sounddevice as sd
import soundfile as sf
# from tkinter import *
import datetime
import os
import logging

import audio_dev
from logger import Logger

logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)


# TODO: Left for debug - remove after
# devices = sd.query_devices()
# print(devices)


def voice_rec():
    try:
        fs = constants.SAMPLERATE
        duration = constants.REC_TIME
        # find available input device (microphone)
        sd.default.device = audio_dev.find_input_device()
        # get current volume settings
        current_volume = audio_dev.get_volume(sd.default.device)
        # set desired volume for recording
        audio_dev.set_volume(sd.default.device, constants.INPUT_VOLUME)
        # record audio
        sd.default.samplerate = fs
        sd.default.channels = constants.CHANNELS
        recording = sd.rec(int(duration * fs))
        sd.wait()
        logger.add_log_entry(logging.DEBUG, f"Capturing {duration}s of {fs}Hz audio on {sd.default.device} - success ")
        # restore current volume settings
        audio_dev.set_volume(sd.default.device, current_volume)

        # Check for valid file storage - create new if not found
        directory = constants.MESSAGE_STORE
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Generate unique file name with date and time of recording
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + constants.AUDIO_TYPE

        # Save as audio file at correct sampling rate with selected filename
        sf.write(f'{constants.MESSAGE_STORE}/{filename}', recording, fs)
        logger.add_log_entry(logging.INFO, f"Save {filename} to {constants.MESSAGE_STORE} - success ")

    except Exception as e:
        print('An error occurred:', e)
        logger.add_log_entry(logging.ERROR, e)
    return filename


def voice_play(filename):
    try:
        # find available output device (speakers, headphones etc.)
        sd.default.device = audio_dev.find_output_device()
        # get current volume settings
        current_volume = audio_dev.get_volume(sd.default.device)
        # set desired volume for recording
        audio_dev.set_volume(sd.default.device, constants.OUTPUT_VOLUME)
        # play audio
        data, fs = sf.read(filename, dtype='float32')
        sd.play(data, samplerate=constants.SAMPLERATE)
        sd.wait()
        # restore current volume settings
        audio_dev.set_volume(sd.default.device, current_volume)

    except Exception as e:
        print('An error occurred:', e)
        logger.add_log_entry(logging.ERROR, e)
    return None


# TODO: Remove Tk() form after final debug - not required here
# master = Tk()
#
# Label(master, text="Voice REC/PLAY debug").grid(row=0, sticky=W, rowspan=5)
#
# rec_button = Button(master, text="Record", command=voice_rec)
# rec_button.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=5)
#
# play_button = Button(master, text="Play", command=voice_play)
# play_button.grid(row=2, column=2, columnspan=2, rowspan=2, padx=5, pady=5)
#
# mainloop()

# TODO: Any more functionalities here? - TBD

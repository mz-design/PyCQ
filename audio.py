# ---------------------------------------------------------------------------------------------
# audio.py - Sound recorder/player module. Record audio from default input_device and
#            play to default output_device using numpy arrays. The file saved with unique
#            name convention using creation date-time to [PyCQ_root_directory]\Audio\.. folder
#
# Prerequisites: sounddevice, soundfile, numpy
#
# initial release: 28.05.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------

import datetime
import logging
import os
import threading

import sounddevice as sd
import soundfile as sf

import audio_dev
import constants
from logger import Logger

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# Initialize variables
lock = threading.Lock()


def voice_rec():
    filename = ''
    try:
        fs = constants.SAMPLERATE
        duration = constants.REC_TIME
        # find available input device (microphone)
        sd.default.device = audio_dev.find_input_device()
        # record audio
        sd.default.samplerate = fs
        sd.default.channels = constants.CHANNELS
        recording = sd.rec(int(duration * fs))
        sd.wait()
        logger.add_log_entry(logging.DEBUG, f"Capturing {duration}s of {fs}Hz audio on {sd.default.device} - success ")
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
        # print('An error occurred:', e)
        logger.add_log_entry(logging.ERROR, e)
    return filename


def voice_play(filename):
    # this function should be locked since it can be called by different threads simultaneously - CRITICAL
    with lock:
        logger.add_log_entry(logging.DEBUG, "voice_play() function locked by thread")
        try:
            # find available output device (speakers, headphones etc.)
            sd.default.device = audio_dev.find_output_device()

            # get current volume settings
            audio_dev.spk_volume().SetMute(0, None)
            current_volume = audio_dev.spk_volume().GetMasterVolumeLevel()
            logger.add_log_entry(logging.DEBUG, f"Store current master volume level: {current_volume}")

            # mute all sound streams except the own one
            audio_dev.mute_all()
            logger.add_log_entry(logging.DEBUG, f"Mute all sound sources except my one")

            # set desired master volume for playback
            audio_dev.spk_volume().SetMasterVolumeLevel(constants.OUTPUT_VOLUME, None)
            logger.add_log_entry(logging.DEBUG, f"Set playback volume to {constants.OUTPUT_VOLUME}")

            # play audio
            logger.add_log_entry(logging.INFO, f"Playing audio file {filename}")
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, samplerate=constants.SAMPLERATE)
            sd.wait()

            # restore current master volume settings
            audio_dev.spk_volume().SetMasterVolumeLevel(current_volume, None)
            logger.add_log_entry(logging.DEBUG, f"Restore master volume to stored value: {current_volume}")

            # Remove mute back all sound streams
            audio_dev.unmute_all()
            logger.add_log_entry(logging.DEBUG, f"Un-mute all active sound sources")

        except Exception as e:
            # print('An error occurred:', e)
            logger.add_log_entry(logging.ERROR, f" voice_play function Error occurred: {e}")
        return None

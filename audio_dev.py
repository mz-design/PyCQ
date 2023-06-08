# -------------------------------------------------------------------------------------
# audio_dev.py - Search for available Windows Audio devices and set default input_device
#                 for audio recording and default output_device for audio playback
#
# Prerequisites: pyaudio
#
# initial release: 28.05.2023 - MichaelZ
# -------------------------------------------------------------------------------------

import constants
import pyaudio
import logging
from logger import Logger

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# Initialize audio
audio = pyaudio.PyAudio()


def find_input_device():
    input_device = -1
    dev_list = audio.get_device_count()

    logger.add_log_entry(logging.INFO, 'Start searching primary input audio device')

    # Look for "Primary Sound Capture Driver" - 1st priority
    device_names = ["primary sound capture driver"]
    for dev in range(dev_list):
        device = audio.get_device_info_by_index(dev)
        if device['maxInputChannels'] > 0 and any(name in device['name'].lower() for name in device_names):
            print(f"Input device found: {device['name']} with id {dev}")
            input_device = dev
            logger.add_log_entry(logging.INFO, f"Found audio input: {device['name']} with id {dev}")
            break
        else:
            logger.add_log_entry(logging.WARNING, f'"Primary Sound Capture Driver" not found on device id: {dev}')

    # Look for microphone devices - 2nd priority
    if input_device == -1:
        logger.add_log_entry(logging.INFO, 'Looking for microphone devices - select 1st instance')
        device_names = ["microphone", "mic"]
        for dev in range(dev_list):
            device = audio.get_device_info_by_index(dev)
            if device['maxInputChannels'] > 0 and any(name in device['name'].lower() for name in device_names):
                print(f"Input device found: {device['name']} with id {dev}")
                input_device = dev
                logger.add_log_entry(logging.INFO, f"Found audio input: {device['name']} with id {dev}")
                break
            else:
                logger.add_log_entry(logging.WARNING, f'Microphone device not found on device id: {dev}')

    if input_device >= 0:
        logger.add_log_entry(logging.INFO, f"Set input audio device id: {input_device}")
    else:
        logger.add_log_entry(logging.ERROR, 'Input Audio Device not found on this system')
        logger.add_log_entry(logging.CRITICAL, 'No Input Audio Device! - inform user, terminate main()')

    return input_device


def find_output_device():
    output_device = -1
    dev_list = audio.get_device_count()

    logger.add_log_entry(logging.INFO, 'Start searching primary output audio device')

    # Look for "Primary Sound Driver" - 1st priority
    device_names = ["primary sound driver"]
    for dev in range(dev_list):
        device = audio.get_device_info_by_index(dev)
        if device['maxOutputChannels'] > 0 and any(name in device['name'].lower() for name in device_names):
            print(f"Output device found: {device['name']} with id {dev}")
            output_device = dev
            logger.add_log_entry(logging.INFO, f"Found audio output: {device['name']} with id {dev}")
            break
        else:
            logger.add_log_entry(logging.WARNING, f'"Primary Sound Driver" not found on device id: {dev}')

    # Look for speaker devices - 2nd priority
    if output_device == -1:
        logger.add_log_entry(logging.INFO, 'Looking for speaker devices - select 1st instance')
        device_names = ["speaker"]
        for dev in range(dev_list):
            device = audio.get_device_info_by_index(dev)
            if device['maxOutputChannels'] > 0 and any(name in device['name'].lower() for name in device_names):
                print(f"Output device found: {device['name']} with id {dev}")
                output_device = dev
                logger.add_log_entry(logging.INFO, f"Found audio output: {device['name']} with id {dev}")
                break
            else:
                logger.add_log_entry(logging.WARNING, f'Speaker device not found on device id: {dev}')

    if output_device >= 0:
        logger.add_log_entry(logging.INFO, f"Set output audio device id: {output_device}")
    else:
        logger.add_log_entry(logging.ERROR, 'Output Audio Device not found on this system')
        logger.add_log_entry(logging.CRITICAL, 'No Output Audio Device! - inform user, terminate main()')

    return output_device


def get_volume(device_index):   # Valid volume range is (0.0 - 1.0)
    # audio = pyaudio.PyAudio()
    device_info = audio.get_device_info_by_index(device_index)
    volume = device_info['volume']
    logger.add_log_entry(logging.DEBUG, f"Current audio device {device_index} volume is: {volume * 100}%")
    audio.terminate()
    return volume


def set_volume(device_index, volume):   # Valid volume range is (0.0 - 1.0)
    # audio = pyaudio.PyAudio()
    device_info = audio.get_device_info_by_index(device_index)
    device_info['volume'] = volume
    logger.add_log_entry(logging.DEBUG, f"Setting audio device {device_index} volume to: {volume * 100}%")
    audio.terminate()

# TODO: remove these debug lines
# find_input_device()
# find_output_device()

# TODO: Any more functionalities here? - TBD

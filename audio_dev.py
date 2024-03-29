# -------------------------------------------------------------------------------------
# audio_dev.py - Search for available Windows Audio devices and set default input_device
#                 for audio recording and default output_device for audio playback
#
# Prerequisites: pyaudio, pycaw, (for volume control), pywin32 for pythoncom
#
# Beta release: 10.07.2023 - MichaelZ
# -------------------------------------------------------------------------------------

import logging

import pyaudio
import pythoncom
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import constants
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
            # print(f"Input device found: {device['name']} with id {dev}")
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
                # print(f"Input device found: {device['name']} with id {dev}")
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
            # print(f"Output device found: {device['name']} with id {dev}")
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
                # print(f"Output device found: {device['name']} with id {dev}")
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


def spk_volume():
    pythoncom.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    logger.add_log_entry(logging.DEBUG, f"Speaker is: {devices}")
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    pythoncom.CoUninitialize()
    return volume


def mute_all():                                 # Mute all audio streams except my own
    # pythoncom.CoInitialize()                  # Need only on 1-st pythoncom instance initialization
    sessions = AudioUtilities.GetAllSessions()                                  # Mute
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() in ("python.exe", "station.exe", "caller.exe"):
            volume.SetMute(0, None)
            volume.SetMasterVolume(1.0, None)
        else:                               # Mute all audio streams except my own
            volume.SetMasterVolume(0.0, None)
            volume.SetMute(1, None)
            # volume.SetMute(1, None)
    # pythoncom.CoUninitialize()                # Need only on 1-st pythoncom instance initialization


def unmute_all():                               # Unmute all
    # pythoncom.CoInitialize()                  # Need only on 1-st pythoncom instance initialization
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        volume.SetMute(0, None)
        volume.SetMasterVolume(1.0, None)
    # pythoncom.CoUninitialize()                # Need only on 1-st pythoncom instance initialization

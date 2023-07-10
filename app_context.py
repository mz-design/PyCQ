# ---------------------------------------------------------------------------------------------------
# app_context.py - Define QApplication context for 'Station' GUI procedures
#
# Prerequisites: PySide6
#
# Beta release: 10.07.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

from PyQt6.QtWidgets import QApplication

app = None


def get_qapp():
    global app
    if app is None:
        app = QApplication([])
        app.setStyle("fusion")
    return app

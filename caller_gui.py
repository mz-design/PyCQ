# ---------------------------------------------------------------------------------------------------
# caller_gui.py - 'Caller' procedures UI version
#
# Prerequisites: PyQt6 , PyQt6.QtWidgets
#
# initial release: 20.06.2023 - MichaelZ
# ---------------------------------------------------------------------------------------------------

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
import os
import time
import socket
import audio
import new_msg_send
import constants
import csv_ops
import http_srv
import tcp_server
import keep_alive
import announcer
import cleanup
import threading
import logging
from logger import Logger

# Initialize logger
logger = Logger(constants.LOG_FILE, level=constants.LOGGING_LEVEL)

# initialize data stores, check if exists and create when needed
directory = constants.MESSAGE_STORE
if not os.path.exists(directory):
    os.makedirs(directory)
if not os.path.exists(constants.STATIONS):
    csv_ops.open_csv_file(constants.STATIONS)
if not os.path.exists(constants.HISTORY):
    csv_ops.open_csv_file(constants.HISTORY)

# perform cleanups on startup
cleanup.clean_log(constants.LOG_FILE, constants.LOG_MAX_LINES)
cleanup.clean_history(constants.HISTORY, constants.HISTORY_MAX_ENTRIES)
cleanup.clean_AudioFiles(f'{constants.MESSAGE_STORE}/', constants.MESSAGE_STORE_MAX_FILES)

# get configuration from constants
udp_port = constants.UDP_PORT
magic = constants.MAGIC                                     # UDP 'magic word'
announce_interval = constants.ANNOUNCE_INTERVAL
tcp_port = constants.TCP_PORT
keep_alive_interval = constants.KEEP_ALIVE_INTERVAL
http_port = constants.HTTP_PORT

# Start HTTP server
# http_srv = http_srv.start_http_server(http_port)

# Create thread objects for 'announce' and periodic keep alive
thread_http_srv = threading.Thread(target=http_srv.start_http_server, args=(http_port,))
thread_tcp_server = threading.Thread(target=tcp_server.start_server, args=(socket.gethostname(), tcp_port))
thread_announcer = threading.Thread(target=announcer.announce_service, args=(udp_port, magic, announce_interval))
thread_periodic_keep_alive = threading.Thread(target=keep_alive.run_periodically, args=(keep_alive_interval, ))

# Start threads
thread_http_srv.start()
thread_tcp_server.start()
thread_announcer.start()
time.sleep(0.1)
thread_periodic_keep_alive.start()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        MainWindow.setAcceptDrops(False)
        MainWindow.setWindowTitle("PyCQ Caller Application")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip("")
        MainWindow.setStatusTip("")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        MainWindow.setWindowFilePath("")
        MainWindow.setIconSize(QtCore.QSize(16, 16))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setAnimated(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 811, 611))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setToolTip("")
        self.tabWidget.setStatusTip("")
        self.tabWidget.setWhatsThis("Alerts")
        self.tabWidget.setAccessibleName("")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.Alerts_tab = QtWidgets.QWidget()
        self.Alerts_tab.setToolTip("System Alerts")
        self.Alerts_tab.setObjectName("Alerts_tab")
        self.fire_alert_Button = QtWidgets.QPushButton(parent=self.Alerts_tab)
        self.fire_alert_Button.setGeometry(QtCore.QRect(40, 30, 191, 181))
        self.fire_alert_Button.setToolTip("Send Fire Alert")
        self.fire_alert_Button.setStatusTip("")
        self.fire_alert_Button.setWhatsThis("")
        self.fire_alert_Button.setAccessibleName("")
        self.fire_alert_Button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/fire_alert.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.fire_alert_Button.setIcon(icon1)
        self.fire_alert_Button.setIconSize(QtCore.QSize(135, 135))
        self.fire_alert_Button.setCheckable(False)
        self.fire_alert_Button.setAutoDefault(False)
        self.fire_alert_Button.setDefault(False)
        self.fire_alert_Button.setFlat(False)
        self.fire_alert_Button.setObjectName("fire_alert_Button")
        self.intruder_alert_Button = QtWidgets.QPushButton(parent=self.Alerts_tab)
        self.intruder_alert_Button.setGeometry(QtCore.QRect(300, 30, 191, 181))
        self.intruder_alert_Button.setToolTip("Send Intruder Alert")
        self.intruder_alert_Button.setStatusTip("")
        self.intruder_alert_Button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/intruder_alert.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.intruder_alert_Button.setIcon(icon2)
        self.intruder_alert_Button.setIconSize(QtCore.QSize(135, 135))
        self.intruder_alert_Button.setCheckable(False)
        self.intruder_alert_Button.setAutoDefault(False)
        self.intruder_alert_Button.setFlat(False)
        self.intruder_alert_Button.setObjectName("intruder_alert_Button")
        self.missile_alert_Button = QtWidgets.QPushButton(parent=self.Alerts_tab)
        self.missile_alert_Button.setGeometry(QtCore.QRect(550, 30, 191, 181))
        self.missile_alert_Button.setToolTip("Send Rocket Attack Alert")
        self.missile_alert_Button.setStatusTip("")
        self.missile_alert_Button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("resources/rocket.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.missile_alert_Button.setIcon(icon3)
        self.missile_alert_Button.setIconSize(QtCore.QSize(135, 135))
        self.missile_alert_Button.setCheckable(False)
        self.missile_alert_Button.setAutoDefault(False)
        self.missile_alert_Button.setFlat(False)
        self.missile_alert_Button.setObjectName("missile_alert_Button")
        self.earthquake_alert_Button = QtWidgets.QPushButton(parent=self.Alerts_tab)
        self.earthquake_alert_Button.setGeometry(QtCore.QRect(170, 280, 190, 190))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.earthquake_alert_Button.sizePolicy().hasHeightForWidth())
        self.earthquake_alert_Button.setSizePolicy(sizePolicy)
        self.earthquake_alert_Button.setToolTip("Send Earthquake Alert")
        self.earthquake_alert_Button.setStatusTip("")
        self.earthquake_alert_Button.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.earthquake_alert_Button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("resources/earthquake_alert.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.earthquake_alert_Button.setIcon(icon4)
        self.earthquake_alert_Button.setIconSize(QtCore.QSize(135, 135))
        self.earthquake_alert_Button.setCheckable(False)
        self.earthquake_alert_Button.setAutoDefault(False)
        self.earthquake_alert_Button.setFlat(False)
        self.earthquake_alert_Button.setObjectName("earthquake_alert_Button")
        self.tsunami_alert_Button = QtWidgets.QPushButton(parent=self.Alerts_tab)
        self.tsunami_alert_Button.setGeometry(QtCore.QRect(430, 280, 191, 191))
        self.tsunami_alert_Button.setToolTip("Send Tsunami Alert")
        self.tsunami_alert_Button.setStatusTip("")
        self.tsunami_alert_Button.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("resources/tsunami_alert.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tsunami_alert_Button.setIcon(icon5)
        self.tsunami_alert_Button.setIconSize(QtCore.QSize(135, 135))
        self.tsunami_alert_Button.setCheckable(False)
        self.tsunami_alert_Button.setAutoDefault(False)
        self.tsunami_alert_Button.setFlat(False)
        self.tsunami_alert_Button.setObjectName("tsunami_alert_Button")
        self.label = QtWidgets.QLabel(parent=self.Alerts_tab)
        self.label.setGeometry(QtCore.QRect(90, 220, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setToolTip("")
        self.label.setStatusTip("")
        self.label.setText("Fire Alert")
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.Alerts_tab)
        self.label_2.setGeometry(QtCore.QRect(340, 220, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setToolTip("")
        self.label_2.setStatusTip("")
        self.label_2.setText("Intruder Alert")
        self.label_2.setScaledContents(False)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.Alerts_tab)
        self.label_3.setGeometry(QtCore.QRect(560, 220, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setToolTip("")
        self.label_3.setStatusTip("")
        self.label_3.setText("Missile Attack Alert")
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.Alerts_tab)
        self.label_4.setGeometry(QtCore.QRect(190, 480, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setToolTip("")
        self.label_4.setStatusTip("")
        self.label_4.setText("Earthquake Alert")
        self.label_4.setScaledContents(False)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.Alerts_tab)
        self.label_5.setGeometry(QtCore.QRect(460, 480, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setToolTip("")
        self.label_5.setStatusTip("")
        self.label_5.setText("Tsunami Alert")
        self.label_5.setScaledContents(False)
        self.label_5.setObjectName("label_5")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("resources/alert-icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.Alerts_tab, icon6, "Alert Broadcast")
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.Alerts_tab), "Send Broadcast Alerts")
        self.Messages = QtWidgets.QWidget()
        self.Messages.setObjectName("Messages")
        self.send_message_Button = QtWidgets.QPushButton(parent=self.Messages)
        self.send_message_Button.setGeometry(QtCore.QRect(480, 70, 281, 431))
        self.send_message_Button.setToolTip("Record And Send new Message")
        self.send_message_Button.setStatusTip("")
        self.send_message_Button.setWhatsThis("")
        self.send_message_Button.setAccessibleName("")
        self.send_message_Button.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("resources/message-icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.send_message_Button.setIcon(icon7)
        self.send_message_Button.setIconSize(QtCore.QSize(250, 250))
        self.send_message_Button.setCheckable(False)
        self.send_message_Button.setAutoDefault(False)
        self.send_message_Button.setDefault(False)
        self.send_message_Button.setFlat(False)
        self.send_message_Button.setObjectName("send_message_Button")
        self.stations_tableWidget = QtWidgets.QTableWidget(parent=self.Messages)
        self.stations_tableWidget.setGeometry(QtCore.QRect(20, 70, 421, 431))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        self.stations_tableWidget.setFont(font)
        self.stations_tableWidget.setToolTip("Select Recipients")
        self.stations_tableWidget.setStatusTip("")
        self.stations_tableWidget.setWhatsThis("")
        self.stations_tableWidget.setAccessibleName("")
        self.stations_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.stations_tableWidget.setAlternatingRowColors(True)
        self.stations_tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.stations_tableWidget.setGridStyle(QtCore.Qt.PenStyle.NoPen)
        self.stations_tableWidget.setCornerButtonEnabled(False)
        self.stations_tableWidget.setObjectName("stations_tableWidget")
        self.stations_tableWidget.setColumnCount(0)
        self.stations_tableWidget.setRowCount(0)
        self.stations_tableWidget.horizontalHeader().setVisible(False)
        self.stations_tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.stations_tableWidget.horizontalHeader().setDefaultSectionSize(130)
        self.stations_tableWidget.horizontalHeader().setHighlightSections(False)
        self.stations_tableWidget.horizontalHeader().setMinimumSectionSize(30)
        self.stations_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.stations_tableWidget.verticalHeader().setVisible(False)
        self.stations_tableWidget.verticalHeader().setHighlightSections(False)
        self.stations_tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.label_6 = QtWidgets.QLabel(parent=self.Messages)
        self.label_6.setGeometry(QtCore.QRect(90, 10, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(26)
        font.setBold(True)
        font.setItalic(False)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.refresh_stations_button = QtWidgets.QPushButton(parent=self.Messages)
        self.refresh_stations_button.setGeometry(QtCore.QRect(130, 510, 191, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setKerning(False)
        self.refresh_stations_button.setFont(font)
        self.refresh_stations_button.setMouseTracking(False)
        self.refresh_stations_button.setToolTip("Refresh Active Station List")
        self.refresh_stations_button.setStatusTip("")
        self.refresh_stations_button.setWhatsThis("")
        self.refresh_stations_button.setStyleSheet("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("resources/refresh_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.refresh_stations_button.setIcon(icon8)
        self.refresh_stations_button.setIconSize(QtCore.QSize(30, 30))
        self.refresh_stations_button.setObjectName("refresh_stations_button")
        self.label_7 = QtWidgets.QLabel(parent=self.Messages)
        self.label_7.setGeometry(QtCore.QRect(610, 380, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setToolTip("")
        self.label_7.setStatusTip("")
        self.label_7.setText("Send Message")
        self.label_7.setScaledContents(False)
        self.label_7.setObjectName("label_7")
        self.tabWidget.addTab(self.Messages, icon7, "Voice Messages")
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.Messages), "Send Voice Messages")
        self.message_history = QtWidgets.QWidget()
        self.message_history.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.message_history.setObjectName("message_history")
        self.history_tableWidget = QtWidgets.QTableWidget(parent=self.message_history)
        self.history_tableWidget.setGeometry(QtCore.QRect(-55, 40, 971, 441))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setKerning(True)
        self.history_tableWidget.setFont(font)
        self.history_tableWidget.setToolTip("")
        self.history_tableWidget.setStatusTip("")
        self.history_tableWidget.setWhatsThis("")
        self.history_tableWidget.setAccessibleName("")
        self.history_tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.history_tableWidget.setAutoScrollMargin(50)
        self.history_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_tableWidget.setAlternatingRowColors(True)
        self.history_tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.history_tableWidget.setGridStyle(QtCore.Qt.PenStyle.NoPen)
        self.history_tableWidget.setWordWrap(False)
        self.history_tableWidget.setCornerButtonEnabled(False)
        self.history_tableWidget.setColumnCount(5)
        self.history_tableWidget.setObjectName("history_tableWidget")
        self.history_tableWidget.setRowCount(0)
        self.history_tableWidget.horizontalHeader().setVisible(False)
        self.history_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.history_tableWidget.horizontalHeader().setDefaultSectionSize(170)
        self.history_tableWidget.horizontalHeader().setHighlightSections(False)
        self.history_tableWidget.horizontalHeader().setMinimumSectionSize(30)
        self.history_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.history_tableWidget.horizontalHeader().setStretchLastSection(False)
        self.history_tableWidget.verticalHeader().setVisible(False)
        self.history_tableWidget.verticalHeader().setHighlightSections(False)
        self.history_tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.refresh_history_button = QtWidgets.QPushButton(parent=self.message_history)
        self.refresh_history_button.setGeometry(QtCore.QRect(10, 490, 191, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.refresh_history_button.setFont(font)
        self.refresh_history_button.setToolTip("Refresh Message History")
        self.refresh_history_button.setIcon(icon8)
        self.refresh_history_button.setIconSize(QtCore.QSize(40, 40))
        self.refresh_history_button.setObjectName("refresh_history_button")
        self.label_9 = QtWidgets.QLabel(parent=self.message_history)
        self.label_9.setGeometry(QtCore.QRect(140, 20, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(parent=self.message_history)
        self.label_10.setGeometry(QtCore.QRect(280, 20, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(parent=self.message_history)
        self.label_11.setGeometry(QtCore.QRect(470, 20, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(parent=self.message_history)
        self.label_12.setGeometry(QtCore.QRect(640, 20, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.replay_message_button = QtWidgets.QPushButton(parent=self.message_history)
        self.replay_message_button.setGeometry(QtCore.QRect(220, 490, 171, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.replay_message_button.setFont(font)
        self.replay_message_button.setToolTip("Playback selected Message")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("resources/Play.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.replay_message_button.setIcon(icon9)
        self.replay_message_button.setIconSize(QtCore.QSize(40, 40))
        self.replay_message_button.setObjectName("replay_message_button")
        self.delete_messages_button = QtWidgets.QPushButton(parent=self.message_history)
        self.delete_messages_button.setGeometry(QtCore.QRect(690, 490, 91, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        self.delete_messages_button.setFont(font)
        self.delete_messages_button.setToolTip("Delete All Messages in History")
        self.delete_messages_button.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("resources/remove-icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.delete_messages_button.setIcon(icon10)
        self.delete_messages_button.setIconSize(QtCore.QSize(60, 60))
        self.delete_messages_button.setObjectName("delete_messages_button")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("resources/history-icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.message_history, icon11, "")
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.message_history), "Message history")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label_6.setText(_translate("MainWindow", "Active Stations"))
        self.refresh_stations_button.setText(_translate("MainWindow", "Refresh Stations"))
        self.refresh_history_button.setText(_translate("MainWindow", "Refresh History"))
        self.label_9.setText(_translate("MainWindow", "Time"))
        self.label_10.setText(_translate("MainWindow", "Station Name"))
        self.label_11.setText(_translate("MainWindow", "Station IP"))
        self.label_12.setText(_translate("MainWindow", "Message"))
        self.replay_message_button.setText(_translate("MainWindow", "Play"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.message_history), _translate("MainWindow", "Message History"))


def get_broadcast_ip_list():
    rows = csv_ops.open_csv_file(constants.STATIONS)  # Get the rows from the CSV file
    ip_list = []

    # Extract data from the specified column (excluding the header row)
    for row in rows[0:]:
        if "IP" in row:
            ip_list.append(row["IP"])
    return ip_list


def get_selected_values(table_widget, column):
    selected_rows = []
    for row_idx in range(table_widget.rowCount()):
        checkbox_item = table_widget.cellWidget(row_idx, 0)
        checkbox = checkbox_item.findChild(QtWidgets.QCheckBox)
        if checkbox.isChecked():
            selected_rows.append(row_idx)

    values = []
    for row_idx in selected_rows:
        item = table_widget.item(row_idx, column)
        if item is not None:
            values.append(item.text())

    return values


class CallerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_stations_data()
        self.load_history_data()

        # Connect alert_Button's clicked signals to send_message function
        self.fire_alert_Button.clicked.connect(lambda: self.send_message("fire_alert"))
        self.intruder_alert_Button.clicked.connect(lambda: self.send_message("intruder_alert"))
        self.missile_alert_Button.clicked.connect(lambda: self.send_message("missile_alert"))
        self.earthquake_alert_Button.clicked.connect(lambda: self.send_message("earthquake_alert"))
        self.tsunami_alert_Button.clicked.connect(lambda: self.send_message("tsunami_alert"))

        # Connect send_message_Button's click signals to send_message function
        self.send_message_Button.clicked.connect(lambda: self.send_message("voice_message"))

        # Connect the refresh_stations_button's clicked signal to the refresh_table function
        self.refresh_stations_button.clicked.connect(self.refresh_stations)

        # Connect the refresh_history_button's clicked signal to the refresh_table function
        self.refresh_history_button.clicked.connect(self.refresh_history)

        # Connect the delete_messages_button's clicked signal to delete_history function
        self.delete_messages_button.clicked.connect(self.delete_history)

        # Connect the replay_message_button's clicked signal to replay_message function
        self.replay_message_button.clicked.connect(self.replay_message())


    def enforce_single_selection(self):
        sender_checkbox = self.sender()

        for row_idx in range(self.history_tableWidget.rowCount()):
            checkbox_item = self.history_tableWidget.cellWidget(row_idx, 0)
            checkbox = checkbox_item.findChild(QtWidgets.QCheckBox)

            if checkbox is not sender_checkbox:
                checkbox.setChecked(False)
    def load_stations_data(self):
        # Get the rows from the CSV file
        rows = csv_ops.open_csv_file(constants.STATIONS)

        # Get the number of rows and columns in the CSV data
        num_rows = len(rows)
        num_cols = len(rows[0]) if rows else 0

        # Set the number of rows and columns in the table widget
        self.stations_tableWidget.setRowCount(num_rows)
        self.stations_tableWidget.setColumnCount(num_cols + 1)  # Add 1 for the checkbox column

        # Populate the table with data from the CSV file
        for row_idx, row_data in enumerate(rows):
            # Create a cell widget for the checkbox
            checkbox_widget = QtWidgets.QWidget()
            checkbox_layout = QtWidgets.QHBoxLayout(checkbox_widget)
            checkbox_layout.setContentsMargins(10, 0, 0, 0)  # Set left margin to 10 pixels
            checkbox_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Add a checkbox to the cell widget
            checkbox = QtWidgets.QCheckBox()
            checkbox_layout.addWidget(checkbox)

            # Set the cell widget as the item in the first column of each row
            self.stations_tableWidget.setCellWidget(row_idx, 0, checkbox_widget)

            for col_idx, cell_data in enumerate(row_data.values(), start=1):
                item = QtWidgets.QTableWidgetItem(str(cell_data))
                self.stations_tableWidget.setItem(row_idx, col_idx, item)

    def load_history_data(self):
        # Open the CSV file
        rows = csv_ops.open_csv_file(constants.HISTORY)

        # Get the number of rows and columns in the CSV data
        num_rows = len(rows)
        num_cols = len(rows[0]) if rows else 0

        # Set the number of rows and columns in the table widget
        self.history_tableWidget.setRowCount(num_rows)
        self.history_tableWidget.setColumnCount(num_cols + 1)  # Add 1 for the checkbox column

        # Populate the table with data from the CSV file
        for row_idx, row_data in enumerate(rows):
            # Create a cell widget for the checkbox
            checkbox_widget = QtWidgets.QWidget()
            checkbox_layout = QtWidgets.QHBoxLayout(checkbox_widget)
            checkbox_layout.setContentsMargins(10, 0, 0, 0)  # Set left margin to 10 pixels
            checkbox_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Add a checkbox to the cell widget
            checkbox = QtWidgets.QCheckBox()
            checkbox_layout.addWidget(checkbox)

            # Set the cell widget as the item in the first column of each row
            self.history_tableWidget.setCellWidget(row_idx, 0, checkbox_widget)

            for col_idx, cell_data in enumerate(row_data.values(), start=1):
                item = QtWidgets.QTableWidgetItem(str(cell_data))
                self.history_tableWidget.setItem(row_idx, col_idx, item)

        # Connect the checkboxes' stateChanged signal to the enforce_single_selection function
        for row_idx in range(self.history_tableWidget.rowCount()):
            checkbox_item = self.history_tableWidget.cellWidget(row_idx, 0)
            checkbox = checkbox_item.findChild(QtWidgets.QCheckBox)
            checkbox.stateChanged.connect(self.enforce_single_selection)

    def refresh_stations(self):
        # Clear the existing table data
        self.stations_tableWidget.clearContents()

        # Re-read the CSV file contents and update the table
        self.load_stations_data()

    def refresh_history(self):
        # Clear the existing table data
        self.history_tableWidget.clearContents()

        # Re-read the CSV file contents and update the table
        self.load_history_data()

    def delete_history(self):
        if self.show_yes_no_popup("Confirmation", "Delete Message History?") == QMessageBox.StandardButton.Yes:
            cleanup.clean_history(constants.HISTORY, 0)
            cleanup.clean_AudioFiles(constants.MESSAGE_STORE, 0)
            self.refresh_history()
            logger.add_log_entry(logging.INFO, "Message history deleted by user")

    def replay_message(self):
        asset = get_selected_values(self.history_tableWidget, 5)
        if not asset:
            self.show_warning_popup("No messages selected\nPlease select message!")
        elif not asset[0].endswith(".ogg"): # not voice message
            self.show_warning_popup("Alert Broadcasts can not be replayed! ")
        else:
            audio.voice_play(asset[0])



    def send_message(self, asset):
        if asset in ("fire_alert", "earthquake_alert", "intruder_alert", "tsunami_alert", "missile_alert"):
            addr_list = get_broadcast_ip_list()
            if self.show_yes_no_popup("Confirmation", "Are you sure sending system broadcast?") == QMessageBox.StandardButton.No:
                return None
        else:
            addr_list = get_selected_values(self.stations_tableWidget, 1)
            if not addr_list:
                try:
                    self.show_warning_popup("No stations selected.")
                except Exception as e:
                    logger.add_log_entry(logging.ERROR, f"Exception {e} while generating warning popup")
                return None

        new_msg_send.record_and_send_new_message(addr_list, asset)

    def show_warning_popup(self, message):
        message_box = QMessageBox()
        message_box.setWindowIcon(QtGui.QIcon('resources/icon.png'))
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        message_box.setWindowTitle("Warning")
        message_box.setText(message)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()

    def show_yes_no_popup(self, title, message):
        reply = QMessageBox.question(self, title, message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        return reply

    def closeEvent(self, event):
        # Terminate the application
        QApplication.quit()
        # Terminate all application processes
        os._exit(0)

    # def refresh_history(self):
    #     # Clear the existing table data
    #     self.history_tableWidget.clearContents()
    #
    #     # Re-read the CSV file contents and update the table
    #     self.load_history_data()

def main():
    app = QApplication(sys.argv)
    form = CallerApp()
    form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

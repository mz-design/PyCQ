# ------------------------------------------------------------------------------------------------------
# message_popup.py -  Defines the RoundedMessageWindow class to use with system messages
#
# Prerequisites: PySide6.QtWidgets, PySide6.QtCore, PySide6.QtGui
#
# initial release: 14.06.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QIcon, QPixmap, QFont
import audio
import constants
import json


class RoundedMessageWindow(QWidget):
    def __init__(self, message, image_path, audio_filename):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.filename = audio_filename

        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)

        image_label = QLabel(self)
        self.setCustomImage(image_label, image_path)

        label = QLabel(message, self)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("color: black;")
        label.setAlignment(Qt.AlignCenter)

        close_button = CloseButton(self)

        image_layout = QHBoxLayout()
        image_layout.addSpacerItem(QSpacerItem(80, 1, QSizePolicy.Fixed, QSizePolicy.Fixed))
        image_layout.addWidget(image_label)
        image_layout.addWidget(close_button, alignment=Qt.AlignTop | Qt.AlignRight)

        layout.addLayout(image_layout)
        layout.addWidget(label)

        if image_path.endswith('message-icon.png'):
            # Voice message - provide 'replay' button
            replay_button = QPushButton("Replay", self)
            replay_button.clicked.connect(self.handleReplayButtonClick)
            replay_button.setStyleSheet(
                "QPushButton { background-color: green; color: white; border: none; border-radius: 5px; padding: 10px; }"
                "QPushButton:hover { background-color: darkgreen; }"
            )
            replay_button.setFont(QFont("Arial", 10, QFont.Bold))

            # Set the size of the replay button to 150 x 50
            replay_button.setFixedSize(250, 50)

            layout.addWidget(replay_button, 1, Qt.AlignCenter)

        self.setFixedSize(500, 500)

        self.drag_position = None

    def setCustomImage(self, label, image_path):
        image = QPixmap(image_path)
        scaled_image = image.scaledToHeight(300)

        label.setPixmap(scaled_image)
        label.setFixedSize(350, 350)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Load popup transparency value from a file, or use a default value
        try:
            with open('transparency.json') as file:
                transparency_value = json.load(file)
        except FileNotFoundError:
            transparency_value = constants.TRANSPARENCY

        background_color = QColor(255, 255, 255, transparency_value)
        painter.setBrush(QBrush(background_color))
        painter.setPen(Qt.NoPen)

        rect = self.rect()
        painter.drawEllipse(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_position:
                self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def handleReplayButtonClick(self):
        play_file(self.filename)


class CloseButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        close_icon = self.createCloseIcon()
        self.setIcon(QIcon(close_icon))
        self.setIconSize(QSize(30, 30))
        self.setStyleSheet(
            "QPushButton { background-color: red; border: none; border-radius: 15px; }"
            "QPushButton::hover { background-color: #ff4d4d; }"
        )
        self.clicked.connect(parent.close)
        self.setFixedSize(30, 30)

    def createCloseIcon(self):
        pixmap = QPixmap(30, 30)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Qt.GlobalColor.white, 2))

        painter.drawLine(8, 8, 22, 22)
        painter.drawLine(8, 22, 22, 8)

        painter.end()

        return pixmap


def play_file(filename):
    audio.voice_play(filename)
    print(f"Playing file: {filename}")

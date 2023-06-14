# ------------------------------------------------------------------------------------------------------
# message_popup.py -  Defines the RoundedMessageWindow class to use with system messages
#
# Prerequisites: PySide6.QtWidgets, PySide6.QtCore, PySide6.QtGui
#
# initial release: 14.06.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QIcon, QPixmap, QFont
import threading
import audio


class RoundedMessageWindow(QMainWindow):
    def __init__(self, message, image_path, audio_filename):
        super().__init__(flags=Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.filename = audio_filename

        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCustomImage(image_label, image_path)

        label = QLabel(message, self)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("color: black;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        replay_button = QPushButton("Replay", self)
        replay_button.clicked.connect(self.handleReplayButtonClick)
        replay_button.setStyleSheet(
            "QPushButton { background-color: green; color: white; border: none; border-radius: 5px; padding: 10px; }"
            "QPushButton:hover { background-color: darkgreen; }"
        )
        replay_button.setFont(QFont("Arial", 10, QFont.Bold))

        layout.addWidget(image_label)
        layout.addWidget(label)
        layout.addWidget(replay_button)

        self.setCentralWidget(container)
        self.setFixedSize(500, 500)

        self.close_button = CloseButton(self)
        self.close_button.move(455, 15)
        self.close_button.show()

        self.drag_position = None

    def setCustomImage(self, label, image_path):
        image = QPixmap(image_path)
        scaled_image = image.scaledToHeight(300)

        image_x = (self.width() - scaled_image.width()) // 2
        image_y = (self.height() - scaled_image.height() - 100) // 2

        label.setPixmap(scaled_image)
        label.setGeometry(image_x, image_y, scaled_image.width(), scaled_image.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        background_color = QColor(255, 255, 255, 200)
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
        # Call an external function to play the file with the given filename
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
    # Open thread for audio playback
    audio_thread = threading.Thread(target=audio.voice_play, args=(filename,))
    audio_thread.start()
    print(f"Playing file: {filename}")
    audio_thread.join()


# if __name__ == "__main__":
#     app = QApplication([])
#     app.setStyle("fusion")
#
#     audio_filename = f"{constants.MESSAGE_STORE}/2023-06-10_16-25-29.ogg"  # Replace with the actual filename
#     popup = RoundedMessageWindow(f"New Voice Message    {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
#                                f"{constants.RESOURCE_FOLDER}/message-icon.png", audio_filename)
#     popup.show()
#
#     app.exec()

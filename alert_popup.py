# ------------------------------------------------------------------------------------------------------
# alert_popup.py -  Defines the RoundedAlertWindow class to use with system messages
#
# Prerequisites: PySide6.QtWidgets, PySide6.QtCore, PySide6.QtGui
#
# initial release: 14.06.2023 - MichaelZ
# ------------------------------------------------------------------------------------------------------

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QPainter, QBrush, QColor, QPen, QIcon, QPixmap, QFont


class RoundedAlertWindow(QMainWindow):
    def __init__(self, message, image_path):
        super().__init__(flags=Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        container = QWidget(self)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 120)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCustomImage(image_label, image_path)

        label = QLabel(message, self)
        label.setFont(QFont("Arial", 12, QFont.Bold))  # Set the font size to 12, make it bold
        label.setStyleSheet("color: black;")  # Set the text color to black
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(label)

        self.setCentralWidget(container)
        self.setFixedSize(500, 500)

        self.close_button = CloseButton(self)
        self.close_button.move(455, 15)
        self.close_button.show()

        self.drag_position = None  # Store the position where the drag started

    def setCustomImage(self, label, image_path):
        image = QPixmap(image_path)
        scaled_image = image.scaledToHeight(300)  # Adjust the scaling factor as per your needs

        # Calculate the position to center the image within the circular area
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


# if __name__ == "__main__":
#     app = QApplication([])
#     app.setStyle("fusion")  # Set the application style to "fusion" for consistent look and feel
#
#     popup = RoundedPopupWindow("Custom Text", f"{constants.RESOURCE_FOLDER}/intruder_alert.png")  # Replace "image.png" with your own image path
#     popup.show()
#
#     app.exec()

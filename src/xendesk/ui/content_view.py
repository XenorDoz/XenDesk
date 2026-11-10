"""
Main content display area.

Responsible for displaying the currently active 
view selected through the sidebar.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


# Subclass to customize main window
class ContentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        background_color = self.palette()
        background_color.setColor(QPalette.ColorRole.Window, QColor("green"))       # TODO THEME to custom later
        self.setPalette(background_color)

class ConfigView(ContentView):
    def __init__(self):
        super().__init__()
        font = self.font()
        
        background_color = self.palette()
        background_color.setColor(QPalette.ColorRole.Window, QColor("dark purple"))       # TODO THEME to custom later
        self.setPalette(background_color)


        self.setLayout(QVBoxLayout())

        title_label = QLabel("Settings")
        font.setPointSize(40)
        title_label.setFont(font)

    pass

class WelcomeView(ContentView):
    def __init__(self):
        super().__init__()
        print("Showing Welcome View")

        background_color = self.palette()
        background_color.setColor(QPalette.ColorRole.Window, QColor("dark blue"))       # TODO THEME to custom later
        self.setPalette(background_color)

        font = self.font()

        self.setLayout(QVBoxLayout())


        welcome = QLabel("Welcome")
        welcome_font = font
        welcome_font.setPointSize(40)
        welcome.setFont(welcome_font)
        welcome.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        welcome2 = QLabel("to XenDesk!")
        welcome2_font = font
        welcome2_font.setPointSize(20)
        welcome2.setFont(welcome2_font)
        welcome2.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        logo = QLabel()
        pixmap = QPixmap("assets/logo/bwabwa.png") # type: ignore
        if pixmap.isNull():
            print("Can't load picture.")
        else:
            pixmap = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            print("Picture loaded")
        logo.setPixmap(pixmap)
        logo.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.layout().addStretch() # type: ignore
        self.layout().addWidget(welcome) # type: ignore
        self.layout().addWidget(welcome2) # type: ignore
        self.layout().addWidget(logo) # type: ignore
        self.layout().addStretch() # type: ignore

    pass


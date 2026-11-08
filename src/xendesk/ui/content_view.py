"""
Main content display area.

Responsible for displaying the currently active 
view selected through the sidebar.
"""

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget

# Subclass to customize main window
class ContentView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        background_color = self.palette()
        background_color.setColor(QPalette.ColorRole.Window, QColor("green"))       # TODO THEME to custom later
        self.setPalette(background_color)
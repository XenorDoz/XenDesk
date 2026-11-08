"""
Navigation sidebar component.

Responsible for displaying application 
entries and navigation controls.
"""


from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget

# Subclass to customize main window
class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        background_color = self.palette()
        background_color.setColor(QPalette.ColorRole.Window, QColor("red"))     # TODO THEME to custom later
        self.setPalette(background_color)
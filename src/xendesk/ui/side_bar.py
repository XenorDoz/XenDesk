"""
Navigation sidebar component

Responsible for displaying application
entries and navigation controls
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout


class SideBar(QWidget):
    def __init__(self):
        super().__init__()
        # Lets the stylesheet paint the background of a plain QWidget
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.my_layout = QVBoxLayout()
        self.setLayout(self.my_layout)
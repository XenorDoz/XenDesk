"""
Main application window.

Acts as the root UI Container of XenDesk 
and assemble the main interface components.
"""

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from ui.side_bar import SideBar
from ui.content_view import ContentView

# Subclass to customize main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ##########
        # Core elements
        ##########
        self.setWindowTitle("XenDesk")
        self.setMinimumSize(QSize(800,600))     # TODO SETTING to custom later

        ##########
        # Added stuff
        ##########
        main_layout = QHBoxLayout()

        main_side_bar = SideBar()
        main_side_bar.setFixedWidth(100)        # TODO SETTING to custom later
        
        main_content_view = ContentView()
        
        main_layout.addWidget(main_side_bar)
        main_layout.addWidget(main_content_view)

        ##########
        # Adding it to core window
        ##########
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
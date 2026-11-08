"""
Main application window.

Acts as the root UI Container of XenDesk 
and assemble the main interface components.
"""

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QPushButton, QStackedLayout

from ui.side_bar import SideBar
import ui.content_view as CV

from core.configManager import config

# Subclass to customize main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ##########
        # Core elements
        ##########

        self.setWindowTitle("XenDesk")
        self.setMinimumSize(QSize(config.main_window_size.width, config.main_window_size.height))

        
        # Grab every view

        self.welcome_view = CV.WelcomeView()
        self.config_view = CV.ConfigView()


        ##########
        # Added stuff
        ##########

        self.main_layout = QHBoxLayout()

        # Sidebar

        self.main_side_bar = SideBar()
        self.main_side_bar.setFixedWidth(config.main_sidebar_width)
        
        self.config_button = QPushButton("Config")
        self.config_button.setProperty("role", "system-button")
        self.config_button.clicked.connect(self.config_toggle)
        button_size = int(config.main_sidebar_width - .1 * config.main_sidebar_width)
        self.config_button.setFixedSize(button_size, button_size)                 
        self.config_button.setAutoFillBackground(True)          


        radius = button_size // 2
        margin = (config.main_sidebar_width - button_size) // 2
        self.main_side_bar.layout().setContentsMargins(margin, 0, margin, margin)  # type: ignore
        self.config_button.setStyleSheet(f"""
            background-color: blue;
            color: white;
            border-radius: {radius}px;
        """)                                                                        # TODO THEME to custom later


        self.main_side_bar.layout().addStretch() # type: ignore
        self.main_side_bar.layout().addWidget(self.config_button, alignment = Qt.AlignmentFlag.AlignHCenter) # type: ignore

        # Content view
        
        self.main_content_view = QWidget()
        self.main_content_view.setLayout(QStackedLayout())
        self.main_content_view.layout().addWidget(self.welcome_view) # type: ignore

        # Add everything
        
        self.main_layout.addWidget(self.main_side_bar)
        self.main_layout.addWidget(self.main_content_view)


        ##########
        # Adding it to core window
        ##########

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def config_toggle(self):
        
        print("Config toggle clicked")

# TODO don't load views in init, only load when needed
# Make show_view function to show view from a dict
# Make get_view function to get view and put it into dict 
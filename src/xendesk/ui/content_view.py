"""
Main content display area.

Responsible for displaying the currently active 
view selected through the sidebar.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton

from core.configManager import config

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
        self.important_stuff_spacing = 80
        self.parameter_spacing = 120


        self.title_font = self.font()
        self.title_font.setPointSize(40)
        self.parameter_font = self.font()
        self.parameter_font.setPointSize(14)
        self.setFont(self.parameter_font)


        background_color = self.palette()
        background_color.setColor(QPalette.ColorRole.Window, QColor("#333333"))       # TODO THEME to custom later
        self.setPalette(background_color)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Adding labels
        self.organising_parameters()

    def organising_parameters(self):
        self.main_layout.addSpacing(50)
        self.create_settings_title()
        self.main_layout.addSpacing(30)
        self.create_window_size_parameter()
        self.main_layout.addSpacing(10)
        self.create_sidebar_width_parameter()
        self.main_layout.addStretch() 
        self.create_save_button()
        self.main_layout.addSpacing(50)

    def create_settings_title(self):
        settings_label = QLabel("Settings")
        settings_label.setFont(self.title_font)
        settings_label.setContentsMargins(self.important_stuff_spacing,0,0,0)
        self.main_layout.addWidget(settings_label)
    def create_window_size_parameter(self):
        window_size_layout = QHBoxLayout()
        window_size_label = QLabel("Window size when starting app:")
        width = QLineEdit(str(config.main_window_size.width))
        width.editingFinished.connect(
            lambda: self.save_parameter(
                "main_window_size.width", width
            )
        )
        width.setFixedWidth(120)
        height = QLineEdit(str(config.main_window_size.height))
        height.editingFinished.connect(
            lambda: 
                self.save_parameter(
                "main_window_size.height", height
            )
        )
        height.setFixedWidth(120)

        window_size_layout.addSpacing(self.parameter_spacing)
        window_size_layout.addWidget(window_size_label)
        window_size_layout.addWidget(width)
        window_size_layout.addWidget(height)
        window_size_layout.addSpacing(self.parameter_spacing)
        self.main_layout.addLayout(window_size_layout)
    def create_save_button(self):
        layout = QHBoxLayout()
        
        button = QPushButton("Save")
        button.released.connect(config.save)

        layout.addStretch()
        layout.addWidget(button)
        layout.addSpacing(self.important_stuff_spacing)
        self.main_layout.addLayout(layout)
    def create_sidebar_width_parameter(self):
        sizebar_layout = QHBoxLayout()
        sizebar_label = QLabel("Sizebar size:")
        size = QLineEdit(str(config.main_sidebar_width))
        size.editingFinished.connect(
            lambda: self.save_parameter(
                "main_sidebar_width", size
            )
        )
        size.setFixedWidth(120)

        sizebar_layout.addSpacing(self.parameter_spacing)
        sizebar_layout.addWidget(sizebar_label)
        sizebar_layout.addStretch()
        sizebar_layout.addWidget(size)
        sizebar_layout.addSpacing(self.parameter_spacing)

        self.main_layout.addLayout(sizebar_layout)
    def save_parameter(self, parameter, widget):
        """
        Grabs the parameter changed and the widget
        Checks if it is the same type, and replace it and save
        """
        parts = parameter.split(".")
        target = config

        for part in parts[:-1]:
            target = getattr(target, part)

        attribute_name = parts[-1]
        old_value = getattr(target, attribute_name)

        try: new_value = type(old_value)(widget.text()) # Tries to set the attribute type to past attribute
        except (ValueError, TypeError):
            widget.setText(str(old_value))      # If not, restore to past attribute
            return

        setattr(target, attribute_name, new_value)
        config.save()

class WelcomeView(ContentView):
    def __init__(self):
        super().__init__()

        background_color = self.palette()
        background_color.setColor(QPalette.ColorRole.Window, QColor("dark blue"))       # TODO THEME to custom later
        self.setPalette(background_color)

        font = self.font()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)


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

        self.main_layout.addStretch() 
        self.main_layout.addWidget(welcome)
        self.main_layout.addWidget(welcome2) 
        self.main_layout.addWidget(logo)
        self.main_layout.addStretch() 

    pass


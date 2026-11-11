"""
Main content display area.

Responsible for displaying the currently active
view selected through the sidebar.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget

from core.config_manager import config
from core.theme_manager import PRESET_THEMES, theme_manager
from ui.color_dialog import ColorDialog

CUSTOMIZE = "__customize__"
CUSTOMIZE_LABEL = "Customize..."

# What each preset theme does on screen (to be filled later)
PRESET_ACTIONS = {
    "Dark": lambda: print("Dark theme"),
    "Light": lambda: print("Light theme"),
    "Ocean": lambda: print("Ocean theme"),
}


# Subclass to customize main window
class ContentView(QWidget):
    def __init__(self):
        super().__init__()
        # Lets the stylesheet paint the background of a plain QWidget
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

class ConfigView(ContentView):
    def __init__(self):
        super().__init__()
        self.setObjectName("config_view")
        self.important_stuff_spacing = 80
        self.parameter_spacing = 120

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Adding labels
        self.organising_parameters()

    def organising_parameters(self):
        self.main_layout.addSpacing(50)
        self.create_section_title("Settings", "title")
        self.main_layout.addSpacing(30)

        self.create_section_title("Graphics options", "title2")
        self.main_layout.addSpacing(10)
        self.create_window_size_parameter()
        self.main_layout.addSpacing(10)
        self.create_sidebar_width_parameter()
        self.main_layout.addSpacing(20)

        self.create_separator()
        self.main_layout.addSpacing(20)

        self.create_section_title("Appearance", "title2")
        self.main_layout.addSpacing(10)
        self.create_themes_row()

        self.main_layout.addStretch()
        self.create_save_button()
        self.main_layout.addSpacing(50)
    def create_section_title(self, text, role="title"):
        """
        Smaller title aligned with the settings title
        """
        label = QLabel(text)
        label.setProperty("role", role)
        label.setContentsMargins(self.important_stuff_spacing, 0, 0, 0)
        self.main_layout.addWidget(label)
    def create_separator(self):
        """
        Thin line in the buttons color, indented like the parameters
        """
        line = QFrame()
        line.setProperty("role", "separator")
        line.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        line.setFixedHeight(1)

        layout = QHBoxLayout()
        layout.addSpacing(self.parameter_spacing)
        layout.addWidget(line)
        layout.addSpacing(self.parameter_spacing)
        self.main_layout.addLayout(layout)
    def create_window_size_parameter(self):
        window_size_layout = QHBoxLayout()
        window_size_label = QLabel("Window size when starting app:")
        window_size_label.setWordWrap(True)

        width = QLineEdit(str(config.main_window_size.width))
        width.editingFinished.connect(
            lambda: self.save_parameter("main_window_size.width", width)
        )
        width.setFixedWidth(120)

        height = QLineEdit(str(config.main_window_size.height))
        height.editingFinished.connect(
            lambda: self.save_parameter("main_window_size.height", height)
        )
        height.setFixedWidth(120)

        window_size_layout.addSpacing(self.parameter_spacing)
        window_size_layout.addWidget(window_size_label)
        window_size_layout.addWidget(width)
        window_size_layout.addWidget(height)
        window_size_layout.addSpacing(self.parameter_spacing)
        self.main_layout.addLayout(window_size_layout)
    def create_sidebar_width_parameter(self):
        sidebar_layout = QHBoxLayout()
        sidebar_label = QLabel("Sidebar size:")

        size = QLineEdit(str(config.main_sidebar_width))
        size.editingFinished.connect(
            lambda: self.save_parameter("main_sidebar_width", size)
        )
        size.setFixedWidth(120)

        sidebar_layout.addSpacing(self.parameter_spacing)
        sidebar_layout.addWidget(sidebar_label)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(size)
        sidebar_layout.addSpacing(self.parameter_spacing)
        self.main_layout.addLayout(sidebar_layout)
    def create_save_button(self):
        layout = QHBoxLayout()

        button = QPushButton("Save")
        button.released.connect(config.save)

        layout.addStretch()
        layout.addWidget(button)
        layout.addSpacing(self.important_stuff_spacing)
        self.main_layout.addLayout(layout)
    def save_parameter(self, parameter, widget):
        """
        Sends the typed value to the core,
        restores the previous value if it is invalid
        """
        if not config.set_value(parameter, widget.text()):
            widget.setText(str(config.get_value(parameter)))

    def create_themes_row(self):
        self.selected_theme = theme_manager.active

        row = QHBoxLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.setFixedWidth(180)
        self.theme_combo.activated.connect(self.on_theme_activated)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_theme)

        row.addSpacing(self.parameter_spacing)
        row.addWidget(QLabel("Themes:"))
        row.addWidget(self.theme_combo)
        row.addStretch()
        row.addWidget(self.delete_button)
        row.addSpacing(self.parameter_spacing)

        self.main_layout.addLayout(row)
        self.refresh_themes()

    def refresh_themes(self):
        """
        Rebuilds the menu from the core's theme list
        """
        self.theme_combo.blockSignals(True)
        self.theme_combo.clear()

        for name in theme_manager.names():
            self.theme_combo.addItem(name, name)
        self.theme_combo.addItem(CUSTOMIZE_LABEL, CUSTOMIZE)

        index = self.theme_combo.findData(self.selected_theme)
        self.theme_combo.setCurrentIndex(index if index >= 0 else 0)
        self.theme_combo.blockSignals(False)

        self.delete_button.setVisible(theme_manager.is_custom(self.selected_theme))

    def on_theme_activated(self, index):
        value = self.theme_combo.itemData(index)

        if value == CUSTOMIZE:
            self.open_theme_editor()
            self.refresh_themes()  # if cancelled, restore the previous theme

        else:
            self.select_theme(value)

    def select_theme(self, name):
        self.selected_theme = name
        theme_manager.set_active(name)

        if theme_manager.is_preset(name):
            PRESET_ACTIONS[name]()

        self.window().apply_theme(name)  # type: ignore
        self.refresh_themes()

    def open_theme_editor(self):
        dialog = ColorDialog(parent=self)
        if not dialog.exec():  # Cancel: nothing is saved
            return

        name = dialog.selected_name()
        # Convert QColor to hexadecimal here, before entering the core
        colors = {role: color.name() for role, color in dialog.colors.items()}
        try:
            theme_manager.add_custom(name, colors)
        except ValueError as error:
            QMessageBox.warning(self, "Name already taken", str(error))
            return

        self.select_theme(name)

    def delete_theme(self):
        theme_manager.delete_custom(self.selected_theme)
        self.select_theme(PRESET_THEMES[0])


class WelcomeView(ContentView):
    def __init__(self):
        super().__init__()
        self.setObjectName("welcome_view")


        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        welcome = QLabel("Welcome")
        welcome.setProperty("role", "title")
        welcome.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        welcome2 = QLabel("to XenDesk!")
        welcome2.setProperty("role", "subtitle")
        welcome2.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        logo = QLabel()
        pixmap = QPixmap("assets/logo/bwabwa.png")  # type: ignore
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
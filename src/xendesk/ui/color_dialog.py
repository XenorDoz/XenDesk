from functools import partial

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QButtonGroup, QColorDialog, QDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

from core.theme_manager import theme_manager


class ColorDialog(QDialog):
    ROLES = ("primary", "secondary", "buttons", "text")
    LABELS = {"primary": "Primary", "secondary": "Secondary", "buttons": "Buttons", "text": "Text"}

    def __init__(self, colors=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose colors")

        # Starting colors: given colors, or the active theme's colors
        source = colors or theme_manager.colors(theme_manager.active)
        self.colors = {role: QColor(c) for role, c in source.items()}
        self.active_role = "primary"

        # Color picker, without its own OK/Cancel buttons
        self.picker = QColorDialog(self)
        self.picker.setOption(QColorDialog.ColorDialogOption.NoButtons, True)
        self.picker.setWindowFlags(Qt.WindowType.Widget)
        self.picker.currentColorChanged.connect(self._on_color_changed)

        # Role buttons: selectable, and painted with their current color
        self.role_buttons = {}
        group = QButtonGroup(self)
        group.setExclusive(True)
        for role in self.ROLES:
            btn = QPushButton(self.LABELS[role])
            btn.setCheckable(True)
            btn.clicked.connect(partial(self._select_role, role))
            group.addButton(btn)
            self.role_buttons[role] = btn
            self._paint(role)

        # Theme name and action buttons
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Theme name")

        self.apply_button = QPushButton("Apply")
        self.cancel_button = QPushButton("Cancel")
        self.apply_button.clicked.connect(self._on_apply)
        self.cancel_button.clicked.connect(self.reject)

        roles_row = QHBoxLayout()
        for role in self.ROLES:
            roles_row.addWidget(self.role_buttons[role])

        # Name on the left, buttons on the right
        actions_row = QHBoxLayout()
        actions_row.addWidget(self.name_edit)
        actions_row.addStretch()
        actions_row.addWidget(self.apply_button)
        actions_row.addWidget(self.cancel_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.picker)
        layout.addLayout(roles_row)
        layout.addLayout(actions_row)

        self._select_role("primary")

    def _select_role(self, role):
        self.active_role = role
        self.role_buttons[role].setChecked(True)

        # Show the color of the selected role in the picker
        self.picker.setCurrentColor(self.colors[role])

    def _on_color_changed(self, color):
        if not color.isValid():
            return
        self.colors[self.active_role] = color
        self._paint(self.active_role)

    def _paint(self, role):
        color = self.colors[role]

        # White text on dark backgrounds, black text on light ones
        text = "white" if color.lightness() < 128 else "black"
        self.role_buttons[role].setStyleSheet(
            f"background-color: {color.name()}; color: {text};"
        )

    def _on_apply(self):
        
        # A theme needs a name before it can be saved
        if not self.selected_name():
            self.name_edit.setFocus()
            return
        self.accept()

    def selected_name(self) -> str:
        return self.name_edit.text().strip()
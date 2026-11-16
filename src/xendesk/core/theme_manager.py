import json

from core.config_manager import config
from core.paths import ASSETS_DIR

PRESETS_PATH = ASSETS_DIR / "themes" / "themes.json"


class ThemeManager:
    """
    Manages themes
    """
    def __init__(self, config):
        self.config = config

    @property
    def active(self):
        return self.config.active_theme

    def add_custom(self, name, colors):
        """
        colors: dict {"primary": "#...", "secondary": "#...", "buttons": "#...", "text": "#..."}, already hexadecimal
        """

        if not name:
            raise ValueError("Theme name cannot be empty.")
        if self.exists(name):
            raise ValueError(f'Theme "{name}" already exists.')
        
        self.config.themes[name] = dict(colors)
        self.config.save()

    def colors(self, name):
        """
        Returns the colors of any theme, preset or custom
        """

        if name in PRESET_COLORS:
            return PRESET_COLORS[name]
        return self.config.themes[name]

    def delete_custom(self, name):
        self.config.themes.pop(name, None)
        self.config.save()

    def exists(self, name):
        return name in self.names()
    
    def is_preset(self, name):
        return name in PRESET_COLORS

    def is_custom(self, name):
        return name in self.config.themes

    def names(self):
        return [*PRESET_THEMES, *self.config.themes]
    
    def set_active(self, name):
        self.config.active_theme = name
        self.config.save()


def load_presets(path = PRESETS_PATH):   
    """
    Loads presets, only useful for outisde of tests
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)   # name -> {"primary": "#...", ...}, order kept

PRESET_COLORS = load_presets()
PRESET_THEMES = tuple(PRESET_COLORS)
theme_manager = ThemeManager(config)
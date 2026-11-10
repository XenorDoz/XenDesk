import json

from core.config_manager import config
from core.paths import ASSETS_DIR

PRESETS_PATH = ASSETS_DIR / "themes" / "themes.json"

with open(PRESETS_PATH, "r", encoding="utf-8") as file:
    PRESET_COLORS = json.load(file)   # name -> {"primary": "#...", ...}, order kept

PRESET_THEMES = tuple(PRESET_COLORS)


class ThemeManager:
    """
    Manages themes
    """

    @property
    def active(self):
        return config.active_theme

    def add_custom(self, name, colors):
        """
        colors: dict {"primary": "#...", "secondary": "#...", "buttons": "#...", "text": "#..."}, already hexadecimal
        """

        if not name:
            raise ValueError("Theme name cannot be empty.")
        if self.exists(name):
            raise ValueError(f'Theme "{name}" already exists.')
        
        config.themes[name] = dict(colors)
        config.save()

    def colors(self, name):
        """
        Returns the colors of any theme, preset or custom
        """

        if name in PRESET_COLORS:
            return PRESET_COLORS[name]
        return config.themes[name]

    def delete_custom(self, name):
        config.themes.pop(name, None)
        config.save()

    def exists(self, name):
        return name in self.names()
    
    def is_preset(self, name):
        return name in PRESET_COLORS

    def is_custom(self, name):
        return name in config.themes

    def names(self):
        return [*PRESET_THEMES, *config.themes]
    
    def set_active(self, name):
        config.active_theme = name
        config.save()



theme_manager = ThemeManager()
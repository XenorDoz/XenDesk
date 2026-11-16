import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from core.paths import CONFIG_PATH


@dataclass
class MainWindowSize:
    width: int
    height: int


@dataclass
class Config:
    next_global_id: int
    main_window_size: MainWindowSize
    main_sidebar_width: int
    active_theme: str = "Dark"
    themes: dict = field(default_factory=dict)  # name -> {"primary": "#...", ...}
    path: Path = CONFIG_PATH       # Where save() writes

    def save(self):
        data = {
            "main_window_size": asdict(self.main_window_size),
            "main_sidebar_width": self.main_sidebar_width,
            "next_global_id": self.next_global_id,
            "active_theme": self.active_theme,
            "themes": self.themes,
        }
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def _locate(self, path):
        """
        Returns (object, attribute_name) for a path like 'main_window_size.width'
        """
        *parents, name = path.split(".")
        target = self

        for part in parents:
            target = getattr(target, part)
        return target, name

    def get_value(self, path):
        target, name = self._locate(path)
        return getattr(target, name)

    def set_value(self, path, raw_text):
        """
        Converts raw_text to the current type of the value, then saves
        Returns False if the conversion fails and nothing is changed
        """
        target, name = self._locate(path)
        old_value = getattr(target, name)

        try:
            new_value = type(old_value)(raw_text)
        except (ValueError, TypeError):
            return False
        
        setattr(target, name, new_value)
        self.save()
        return True

def load_config(path = CONFIG_PATH):
    """
    Loads config, only useful for tests
    """
    with open(path, "r", encoding="utf-8") as file:
        raw_config = json.load(file)

    return Config(
        next_global_id=raw_config["next_global_id"],
        main_window_size=MainWindowSize(
            width=raw_config["main_window_size"]["width"],
            height=raw_config["main_window_size"]["height"],
        ),
        main_sidebar_width=raw_config["main_sidebar_width"],
        active_theme=raw_config.get("active_theme", "Dark"),
        themes=raw_config.get("themes", {}),
        path=path,
    )

config = load_config()
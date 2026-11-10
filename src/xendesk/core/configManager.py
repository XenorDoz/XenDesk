import json
from dataclasses import dataclass


@dataclass
class MainWindowSize:
    width: int
    height: int


@dataclass
class Config:
    next_global_id: int
    main_window_size: MainWindowSize
    main_sidebar_width: int
    
    def save(self):
        data = {
            "main_window_size": {
                "width": self.main_window_size.width,
                "height": self.main_window_size.height
            },
            "main_sidebar_width": self.main_sidebar_width,
            "next_global_id": self.next_global_id
        }

        with open("config/config.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        


with open("config/config.json", "r", encoding="utf-8") as file:
    raw_config = json.load(file)

config = Config(
    next_global_id=raw_config["next_global_id"],
    main_window_size=MainWindowSize(
        width=raw_config["main_window_size"]["width"],
        height=raw_config["main_window_size"]["height"]
    ),
    main_sidebar_width=raw_config["main_sidebar_width"]
)

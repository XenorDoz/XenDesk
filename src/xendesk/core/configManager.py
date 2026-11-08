import json
from dataclasses import dataclass


@dataclass
class MainWindowSize:
    width: int
    height: int


@dataclass
class Config:
    main_window_size: MainWindowSize
    main_sidebar_width: int


with open("config/config.json", "r", encoding="utf-8") as file:
    raw_config = json.load(file)

config = Config(
    main_window_size=MainWindowSize(
        width=raw_config["main_window_size"]["width"],
        height=raw_config["main_window_size"]["height"]
    ),
    main_sidebar_width=raw_config["main_sidebar_width"]
)
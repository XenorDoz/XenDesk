import json

import pytest

from core.config_manager import load_config
from core.theme_manager import PRESET_COLORS, ThemeManager


def make_theme_setup(tmp_path):
    """
    Creates a fresh config file and a ThemeManager using it
    """
    path = tmp_path/"config.json"
    data = {
        "main_window_size": {
            "width": 800,
            "height": 600
        },
        "main_sidebar_width": 80,
        "next_global_id": 1000,
        "active_theme": "Dark",
        "themes": {}
    }
    path.write_text(json.dumps(data), encoding = "utf-8")

    config = load_config(path)
    return path, config, ThemeManager(config)

COLORS = {
    "primary": "#111111",
    "secondary": "#222222",
    "buttons": "#333333",
    "text": "#eeeeee",
}

def test_set_active_changes_active_theme_and_saves(tmp_path):
    """
    Tests if choosing a theme puts it as active theme in config 
    """
    path, config, theme_manager = make_theme_setup(tmp_path)

    theme_manager.set_active("Light")
    assert theme_manager.get_active == "Light"
    saved = json.loads(path.read_text(encoding = "utf-8"))
    assert saved["active_theme"] == "Light"

def test_add_custom_theme_appears_in_name_and_saves(tmp_path):
    """
    Tests if creating a custom theme makes it appear in names
    """
    path, config, theme_manager = make_theme_setup(tmp_path)

    theme_manager.add_custom("Mine", COLORS)
    assert "Mine" in theme_manager.get_names()
    saved = json.loads(path.read_text(encoding = "utf-8"))
    assert saved["themes"]["Mine"] == COLORS


def test_add_custom_theme_refuses_empty_name(tmp_path):
    """
    Tests if adding a custom theme with an empty name is refused
    """
    path, config, theme_manager = make_theme_setup(tmp_path)

    with pytest.raises(ValueError):
        theme_manager.add_custom("", COLORS)

def test_add_custom_theme_refuses_duplicate_name(tmp_path):
    """
    Tests if adding a custom theme with a duplicate name is refused
    """
    path, config, theme_manager = make_theme_setup(tmp_path)
    theme_manager.add_custom("Mine", COLORS)

    with pytest.raises(ValueError):
        theme_manager.add_custom("Mine", COLORS)

def test_add_custom_theme_refuses_preset_name(tmp_path):
    """
    Tests if adding a custom theme with a preset name is refused
    """
    path, config, theme_manager = make_theme_setup(tmp_path)

    with pytest.raises(ValueError):
        theme_manager.add_custom("Dark", COLORS)

def test_get_colors_returns_preset_colors(tmp_path):
    """
    Tests if preset colors are returned correctly
    """
    path, config, theme_manager = make_theme_setup(tmp_path)

    assert theme_manager.get_colors("Dark") == PRESET_COLORS["Dark"]

def test_get_colors_returns_custom_colors(tmp_path):
    """
    Tests if custom colors are returned correctly
    """
    path, config, theme_manager = make_theme_setup(tmp_path)
    theme_manager.add_custom("Mine", COLORS)
    
    assert theme_manager.get_colors("Mine") == COLORS
    
def test_delete_custom_removes_theme_and_is_saved(tmp_path):
    """
    Tests if deleting custom theme removes it 
    """
    path, config, theme_manager = make_theme_setup(tmp_path)

    theme_manager.add_custom("Mine", COLORS)
    assert "Mine" in json.loads(path.read_text(encoding = "utf-8"))["themes"]
    theme_manager.delete_custom("Mine")

    assert "Mine" not in theme_manager.get_names()
    saved = json.loads(path.read_text(encoding = "utf-8"))
    assert "Mine" not in saved["themes"]

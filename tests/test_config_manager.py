import json

from core.config_manager import load_config

def make_config_file(tmp_path):
    """
    Creates a fresh config file with known values for testing
    """
    path = tmp_path/"config.json"
    data = {
        "main_window_size": {"width": 800, "height": 600},
        "main_sidebar_width": 80,
        "next_global_id": 1000,
        "active_theme": "Dark",
        "themes": {}
    }

    path.write_text(json.dumps(data), encoding = "utf-8")
    return path

def test_get_value_reads_nested_attribute(tmp_path):
    """
    Tests if we can read nested attributes using the _locate function
    """
    path = make_config_file(tmp_path)
    config = load_config(path)

    assert config.main_window_size.height == 600
    assert config.main_sidebar_width == 80

def test_set_value_accepts_valid_type_and_saves(tmp_path):
    """
    Tests if a valid value is accepted and saved in config
    """
    path = make_config_file(tmp_path)
    config = load_config(path)
    
    assert config.set_value("main_window_size.width", "1024")
    assert config.main_window_size.width == 1024

    saved = json.loads(path.read_text(encoding = "utf-8")) # Acts as a restart of the app
    assert saved["main_window_size"]["width"] == 1024

def test_set_value_refuses_wrong_type_and_changes_nothing(tmp_path):
    """
    Tests if a wrong value is refused and not saved in config
    """
    path = make_config_file(tmp_path)
    config = load_config(path)
    
    assert not config.set_value("main_window_size.width", "abc")
    assert config.main_window_size.width == 800

    saved = json.loads(path.read_text(encoding = "utf-8")) # Acts as a restart of the app
    assert saved["main_window_size"]["width"] == 800

    pass
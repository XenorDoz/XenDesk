import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    # Compiled .exe: config sits next to the executable
    BASE_DIR = Path(sys.executable).parent
    BUNDLE_DIR = Path(getattr(sys, "_MEIPASS"))  # set by PyInstaller at runtime
else:
    # core/paths.py -> core/xendesk/src/XenDesk
    BASE_DIR = Path(__file__).resolve().parents[3]
    BUNDLE_DIR = BASE_DIR

CONFIG_PATH = BASE_DIR/"config"/"config.json"
ASSETS_DIR = BUNDLE_DIR/"assets"
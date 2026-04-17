import os
from pathlib import Path

APPDATA = Path(os.environ["APPDATA"])

BASE_DIR = APPDATA / "HTR_AttendanceAuto"
CONFIG_DIR = BASE_DIR / "config"
FLAGS_DIR = BASE_DIR / "flags"
BIN_DIR = BASE_DIR / "bin"

USER_GAMES_FILE = CONFIG_DIR / "user_games.json"
SELECTED_FILE = CONFIG_DIR / "selected.json"
INSTALLED_EXE = BIN_DIR / "HTR_DA.exe"

STARTUP_DIR = APPDATA / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
STARTUP_VBS = STARTUP_DIR / "HTR_daily_attendance.vbs"
STARTUP_BAT_LEGACY = STARTUP_DIR / "HTR_daily_attendance.bat"

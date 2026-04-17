@echo off
setlocal
pyinstaller --onefile --noconsole --name HTR_DA --add-data "games.json;." --clean main.py
endlocal

@echo off
cd /d "%USERPROFILE%\Ziekte"
call venv\Scripts\activate.bat
python main.py
start "" http://localhost:5000
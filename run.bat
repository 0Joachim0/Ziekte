@echo off
setlocal enabledelayedexpansion

REM 1. Install Python silently if not already installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe -OutFile python_installer.exe"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python_installer.exe
)

REM 2. Create script folder
set "SCRIPT_FOLDER=%USERPROFILE%\Ziekte"
if not exist "!SCRIPT_FOLDER!" mkdir "!SCRIPT_FOLDER!"

REM 3. Download Python script
powershell -Command "Invoke-WebRequest -Uri https://pastebin.com/raw/your_raw_script_url -OutFile '!SCRIPT_FOLDER!\verzuim_tracker.py'"

REM 4. Create startup shortcut
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "BATCH_FILE=%STARTUP_FOLDER%\run_verzuim.bat"

(
    echo @echo off
    echo python "%SCRIPT_FOLDER%\verzuim_tracker.py"
) > "!BATCH_FILE!"

echo Setup complete. The tracker will now run at every startup.
pause
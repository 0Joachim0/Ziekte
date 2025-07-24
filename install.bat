@echo off
setlocal enabledelayedexpansion

REM 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python manually from https://www.python.org/ and ensure it is added to PATH.
    pause
    exit /b
)

REM 2. Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed or not in PATH.
    echo Please install Git from https://git-scm.com/download/win and ensure it is added to PATH.
    pause
    exit /b
)

REM 3. Set script/repo folder
set "SCRIPT_FOLDER=%USERPROFILE%\Ziekte"

REM 4. Clone or pull latest from GitHub repo
if exist "!SCRIPT_FOLDER!\.git" (
    echo Updating existing repository...
    pushd "!SCRIPT_FOLDER!"
    git pull
    popd
) else (
    echo Cloning repository...
    git clone https://github.com/0Joachim0/Ziekte.git "!SCRIPT_FOLDER!"
)

REM 5. Create virtual environment
set "VENV_PATH=!SCRIPT_FOLDER!\venv"
if not exist "!VENV_PATH!\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv "!VENV_PATH!"
)

REM 6. Install dependencies if requirements.txt exists
if exist "!SCRIPT_FOLDER!\requirements.txt" (
    echo Installing dependencies...
    call "!VENV_PATH!\Scripts\activate.bat"
    pip install --upgrade pip
    pip install -r "!SCRIPT_FOLDER!\requirements.txt"
)

REM 7. Create startup batch file
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "BATCH_FILE=%STARTUP_FOLDER%\run.bat"

(
    echo @echo off
    echo call "%SCRIPT_FOLDER%\venv\Scripts\activate.bat"
    echo python "%SCRIPT_FOLDER%\main.py"
) > "!BATCH_FILE!"

echo.
echo ✅ Setup complete. The tracker will run at startup.
pause
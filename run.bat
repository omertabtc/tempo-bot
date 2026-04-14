@echo off
REM Simple run script for Tempo Contract Analyzer Bot (Windows)

echo.
echo 🚀 Starting Tempo Contract Analyzer Bot...
echo.

REM Check if .env exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo 📝 Please copy .env.example to .env and add your Discord token:
    echo    copy .env.example .env
    echo    notepad .env
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Virtual environment not found. Creating...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📦 Installing dependencies...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Run the bot
echo ✅ Dependencies installed
echo 🤖 Starting bot...
echo.
python bot.py

pause

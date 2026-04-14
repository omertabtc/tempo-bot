@echo off
REM Simple script to start the bot with proper encoding

chcp 65001 > nul
echo.
echo ========================================================
echo   TEMPO CONTRACT ANALYZER BOT - Starting...
echo ========================================================
echo.

python bot.py

if errorlevel 1 (
    echo.
    echo ERROR: Bot stopped with an error!
    echo Check the output above for details.
    echo.
    pause
    exit /b 1
)

pause

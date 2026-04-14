@echo off
REM Installation automatique pour Tempo Contract Analyzer Bot
REM Double-clique sur ce fichier pour tout installer

echo.
echo ========================================================
echo   TEMPO CONTRACT ANALYZER BOT - Installation
echo ========================================================
echo.

echo [1/3] Verification de Python...
python --version
if errorlevel 1 (
    echo.
    echo ERREUR: Python n'est pas installe ou pas dans le PATH!
    echo Telecharge Python depuis: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Installation des dependances...
echo Cela peut prendre 1-2 minutes...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERREUR: L'installation a echoue!
    echo Essaye manuellement: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Test de la configuration...
echo.

python test_setup.py

echo.
echo ========================================================
echo   INSTALLATION TERMINEE !
echo ========================================================
echo.
echo Prochaines etapes :
echo   1. Assure-toi que ton token est dans .env (deja fait!)
echo   2. Lance le bot: python bot.py
echo   3. Teste sur Discord: /analyze-contract 0x...
echo.
echo IMPORTANT: Regenere ton token pour la securite!
echo Lis: IMPORTANT_SECURITY.md
echo.
pause

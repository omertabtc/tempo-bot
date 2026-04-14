@echo off
REM Script pour push le code vers GitHub (Windows)

echo ========================================
echo  Upload vers GitHub
echo ========================================
echo.

REM Vérifier si git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe!
    echo.
    echo Telecharge Git: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Vérifier si .env existe (ne doit PAS être push)
if exist .env (
    echo [OK] Fichier .env detecte
    echo [INFO] Il ne sera PAS envoye sur GitHub (deja dans .gitignore)
)

REM Initialiser git si nécessaire
if not exist .git (
    echo.
    echo [INIT] Premier push - initialisation...
    git init
    git branch -M main
    
    echo.
    echo Entre l'URL de ton repository GitHub:
    echo Exemple: https://github.com/ton_username/tempo-contract-analyzer.git
    set /p REPO_URL="URL: "
    
    git remote add origin %REPO_URL%
)

echo.
echo [1/3] Ajout des fichiers...
git add .

echo.
echo [2/3] Commit...
set /p COMMIT_MSG="Message du commit (ou Enter pour 'Update'): "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update

git commit -m "%COMMIT_MSG%"

echo.
echo [3/3] Push vers GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERREUR lors du push!
    echo.
    echo Solutions possibles:
    echo  1. Verifie que l'URL du repo est correcte
    echo  2. Authentifie-toi sur GitHub
    echo  3. Si premier push, fais: git push -u origin main --force
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SUCCESS! Code envoye sur GitHub
echo ========================================
echo.
echo Prochaines etapes:
echo  1. Va sur Railway.app
echo  2. Deploy from GitHub repo
echo  3. Choisis ton repository
echo  4. Ajoute les variables d'environnement
echo.
pause

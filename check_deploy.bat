@echo off
chcp 65001 > nul
echo ========================================
echo  PRE-DEPLOYMENT CHECK
echo ========================================
echo.

python pre_deploy_check.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Des problemes ont ete detectes!
    echo Corrige-les avant de deployer.
) else (
    echo.
    echo [SUCCESS] Pret pour le deploiement!
)

pause

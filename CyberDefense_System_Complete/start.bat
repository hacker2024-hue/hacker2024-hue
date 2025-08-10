@echo off
title CyberSec AI Assistant - Demarrage Rapide
color 0A

echo.
echo ================================================
echo  CyberSec AI Assistant - Demarrage Rapide
echo  Par Yao Kouakou Luc Annicet
echo ================================================
echo.

REM Verification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe !
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)

REM Creation/Activation environnement virtuel
if not exist "venv" (
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
)

echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installation dependances minimales
echo [INFO] Installation des dependances...
pip install --quiet fastapi uvicorn pydantic pydantic-settings loguru

REM Lancement de l'application
echo.
echo [INFO] Demarrage de CyberSec AI Assistant...
echo [INFO] Serveur accessible sur: http://localhost:8000
echo [INFO] Appuyez sur Ctrl+C pour arreter
echo.

python demo_launcher.py

pause
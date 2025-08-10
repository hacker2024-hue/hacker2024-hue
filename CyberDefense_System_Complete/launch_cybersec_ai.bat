@echo off
echo.
echo ========================================================================
echo   CyberSec AI Assistant - Lanceur Windows
echo   Version 1.0.0 - Developpe par Yao Kouakou Luc Annicet
echo ========================================================================
echo.

REM Configuration des couleurs
color 0A

REM Verification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou non disponible dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo [INFO] Python detecte...
python --version

REM Verification du repertoire
if not exist "%~dp0requirements.txt" (
    echo [ERREUR] Fichier requirements.txt non trouve
    echo Assurez-vous d'etre dans le repertoire du projet
    pause
    exit /b 1
)

echo [INFO] Repertoire du projet valide...

REM Creation de l'environnement virtuel s'il n'existe pas
if not exist "%~dp0venv" (
    echo [INFO] Creation de l'environnement virtuel Python...
    python -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [SUCCES] Environnement virtuel cree avec succes
)

REM Activation de l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

REM Installation des dependances
echo [INFO] Installation/Mise a jour des dependances...
pip install --upgrade pip
pip install fastapi uvicorn pydantic pydantic-settings httpx loguru scikit-learn numpy

REM Verification des modules critiques
echo [INFO] Verification des modules...
python -c "import fastapi, uvicorn, pydantic; print('Modules de base OK')"
if errorlevel 1 (
    echo [ERREUR] Certains modules critiques ne sont pas disponibles
    pause
    exit /b 1
)

echo.
echo [SUCCES] Environnement pret !
echo.

REM Menu principal
:MENU
echo ========================================================================
echo   MENU PRINCIPAL - CyberSec AI Assistant
echo ========================================================================
echo.
echo   1. Lancer le serveur principal (FastAPI)
echo   2. Lancer la demonstration simple
echo   3. Executer les tests de structure
echo   4. Installer toutes les dependances
echo   5. Ouvrir une console Python
echo   6. Afficher les informations systeme
echo   7. Quitter
echo.
set /p choice="Choisissez une option (1-7): "

if "%choice%"=="1" goto START_SERVER
if "%choice%"=="2" goto START_DEMO
if "%choice%"=="3" goto RUN_TESTS
if "%choice%"=="4" goto INSTALL_DEPS
if "%choice%"=="5" goto PYTHON_CONSOLE
if "%choice%"=="6" goto SYSTEM_INFO
if "%choice%"=="7" goto EXIT
echo Option invalide. Veuillez choisir entre 1 et 7.
goto MENU

:START_SERVER
echo.
echo [INFO] Demarrage du serveur CyberSec AI Assistant...
echo [INFO] Le serveur sera accessible sur http://localhost:8000
echo [INFO] Appuyez sur Ctrl+C pour arreter le serveur
echo.
python main.py
goto MENU

:START_DEMO
echo.
echo [INFO] Lancement de la demonstration CyberSec AI Assistant...
echo.
python demo_launcher.py
echo.
pause
goto MENU

:RUN_TESTS
echo.
echo [INFO] Execution des tests de structure...
echo.
python test_structure.py
echo.
pause
goto MENU

:INSTALL_DEPS
echo.
echo [INFO] Installation complete des dependances...
echo [ATTENTION] Certaines dependances peuvent echouer sur Python 3.13
echo.
pip install -r requirements.txt
echo.
pause
goto MENU

:PYTHON_CONSOLE
echo.
echo [INFO] Ouverture de la console Python interactive...
echo [INFO] Tapez 'exit()' pour revenir au menu
echo.
python
goto MENU

:SYSTEM_INFO
echo.
echo ========================================================================
echo   INFORMATIONS SYSTEME
echo ========================================================================
echo.
echo Version Python:
python --version
echo.
echo Version pip:
pip --version
echo.
echo Packages installes:
pip list | findstr -i "fastapi uvicorn pydantic loguru"
echo.
echo Repertoire de travail:
echo %CD%
echo.
echo Variables d'environnement Python:
echo PYTHONPATH=%PYTHONPATH%
echo.
pause
goto MENU

:EXIT
echo.
echo [INFO] Desactivation de l'environnement virtuel...
deactivate
echo [INFO] Merci d'avoir utilise CyberSec AI Assistant !
echo.
pause
exit /b 0
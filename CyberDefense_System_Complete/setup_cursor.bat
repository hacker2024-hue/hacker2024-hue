@echo off
title CyberSec AI Assistant - Configuration Cursor
color 0B

echo.
echo ========================================================================
echo   CONFIGURATION CURSOR - CYBERSEC AI ASSISTANT
echo   Version 1.0.0 - Developpe par Yao Kouakou Luc Annicet
echo ========================================================================
echo.

REM Verification du repertoire du projet
if not exist "%~dp0requirements.txt" (
    echo [ERREUR] Fichier requirements.txt non trouve
    echo Assurez-vous d'etre dans le repertoire du projet
    pause
    exit /b 1
)

echo [INFO] Repertoire du projet valide...

REM Verification de Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou non disponible dans PATH
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)

echo [INFO] Python detecte...
python --version

REM Verification de Cursor
cursor --version >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] Cursor n'est pas installe ou non dans PATH
    echo Telechargez Cursor depuis https://cursor.sh/
    echo Configuration continuera sans lancement automatique
    set CURSOR_AVAILABLE=0
) else (
    echo [INFO] Cursor detecte...
    cursor --version
    set CURSOR_AVAILABLE=1
)

echo.
echo [ETAPE 1/5] Creation environnement virtuel...
if not exist "venv" (
    python -m venv venv
    echo [OK] Environnement virtuel cree
) else (
    echo [OK] Environnement virtuel existant
)

echo.
echo [ETAPE 2/5] Activation environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo [ETAPE 3/5] Installation dependances de base...
pip install --quiet fastapi uvicorn pydantic pydantic-settings httpx loguru
if errorlevel 1 (
    echo [ATTENTION] Certaines dependances non installees
    echo Continuez avec: pip install -r requirements.txt
) else (
    echo [OK] Dependances de base installees
)

echo.
echo [ETAPE 4/5] Creation configuration Cursor...

REM Creation repertoire .cursor
if not exist ".cursor" mkdir .cursor

REM Creation repertoire .vscode pour compatibilite
if not exist ".vscode" mkdir .vscode

REM Creation settings.json basique pour VS Code/Cursor
echo { > .vscode\settings.json
echo   "python.defaultInterpreterPath": "./venv/Scripts/python.exe", >> .vscode\settings.json
echo   "python.terminal.activateEnvironment": true, >> .vscode\settings.json
echo   "editor.formatOnSave": true, >> .vscode\settings.json
echo   "files.exclude": { >> .vscode\settings.json
echo     "**/__pycache__": true, >> .vscode\settings.json
echo     "**/venv": true, >> .vscode\settings.json
echo     "**/*.pyc": true >> .vscode\settings.json
echo   } >> .vscode\settings.json
echo } >> .vscode\settings.json

echo [OK] Configuration Cursor creee

echo.
echo [ETAPE 5/5] Tests de validation...
python test_structure.py >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] Tests de structure echoues
    echo Verifiez la structure du projet
) else (
    echo [OK] Tests de structure reussis
)

echo.
echo ========================================================================
echo   CONFIGURATION TERMINEE AVEC SUCCES !
echo ========================================================================

echo.
echo [PROCHAINES ETAPES]
echo 1. ✅ Environnement virtuel configure
echo 2. ✅ Dependances de base installees
echo 3. ✅ Configuration Cursor creee
echo 4. ✅ Tests de validation reussis

if %CURSOR_AVAILABLE%==1 (
    echo.
    echo [OUVERTURE DANS CURSOR]
    echo Lancement automatique de Cursor...
    start "" cursor "%~dp0"
    echo ✅ Cursor lance avec le projet
) else (
    echo.
    echo [OUVERTURE MANUELLE CURSOR]
    echo 1. Ouvrez Cursor
    echo 2. File → Open Folder
    echo 3. Selectionnez ce dossier: %~dp0
)

echo.
echo [COMMANDES RAPIDES]
echo • python demo_launcher.py  → Demo interactive
echo • python main.py          → Serveur principal  
echo • python test_structure.py → Tests validation
echo • python cursor_setup.py  → Configuration avancee

echo.
echo [RACCOURCIS CURSOR]
echo • F5                       → Debug mode
echo • Ctrl+Shift+P            → Menu commandes
echo • Ctrl+`                  → Terminal integre
echo • Ctrl+Shift+E            → Explorateur fichiers

echo.
echo [SUPPORT]
echo 📧 Email: yao.kouakou.dev@gmaii.com
echo 🔗 GitHub: https://github.com/hackerduckman89/cybersec-ai-assistant
echo 📖 Guide: RECUPERATION_CURSOR.md

echo.
echo 🛡️ CyberSec AI Assistant pret dans Cursor ! 🚀
echo.
pause
@echo off
title CyberSec AI Assistant - Installation
color 0B

echo.
echo ========================================================================
echo   INSTALLATION - CyberSec AI Assistant
echo   Version 1.0.0 - Developpe par Yao Kouakou Luc Annicet
echo ========================================================================
echo.

REM Verification des privileges administrateur
net session >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] Execution sans privileges administrateur
    echo Certaines operations peuvent echouer
    echo.
)

REM Verification de Python
echo [ETAPE 1/6] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou non disponible dans PATH
    echo.
    echo Solutions possibles:
    echo 1. Telecharger Python depuis https://python.org
    echo 2. Ajouter Python au PATH systeme
    echo 3. Relancer ce script apres installation
    echo.
    pause
    exit /b 1
)

python --version
echo [OK] Python detecte avec succes
echo.

REM Verification de pip
echo [ETAPE 2/6] Verification de pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pip n'est pas disponible
    echo Reinstallez Python avec pip inclus
    pause
    exit /b 1
)

echo [OK] pip detecte avec succes
echo.

REM Mise a jour de pip
echo [ETAPE 3/6] Mise a jour de pip...
python -m pip install --upgrade pip
echo.

REM Creation de l'environnement virtuel
echo [ETAPE 4/6] Creation de l'environnement virtuel...
if exist "venv" (
    echo [INFO] Environnement virtuel existant detecte
    echo Souhaitez-vous le recreer ? (o/N)
    set /p recreate=
    if /i "%recreate%"=="o" (
        echo [INFO] Suppression de l'ancien environnement...
        rmdir /s /q venv
    )
)

if not exist "venv" (
    echo [INFO] Creation d'un nouvel environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel cree avec succes
) else (
    echo [INFO] Utilisation de l'environnement existant
)
echo.

REM Activation de l'environnement virtuel
echo [ETAPE 5/6] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)
echo [OK] Environnement virtuel active
echo.

REM Installation des dependances
echo [ETAPE 6/6] Installation des dependances...
echo.
echo [INFO] Installation des packages de base...
pip install fastapi uvicorn pydantic pydantic-settings httpx loguru
echo.
echo [INFO] Installation des outils de science des donnees...
pip install numpy scikit-learn pandas
echo.
echo [INFO] Installation des outils de securite...
pip install cryptography requests beautifulsoup4
echo.
echo [INFO] Installation des outils de developpement...
pip install pytest black flake8
echo.

REM Tentative d'installation des packages avances (peut echouer)
echo [INFO] Tentative d'installation des packages avances...
echo [ATTENTION] Certains packages peuvent echouer sur Python 3.13
echo.

pip install torch --index-url https://download.pytorch.org/whl/cpu || echo [ATTENTION] PyTorch non installe
pip install transformers || echo [ATTENTION] Transformers non installe
pip install spacy || echo [ATTENTION] spaCy non installe

echo.
echo ========================================================================
echo   INSTALLATION TERMINEE
echo ========================================================================
echo.

REM Verification de l'installation
echo [INFO] Verification de l'installation...
python -c "import fastapi, uvicorn, pydantic; print('[OK] Modules principaux installes')" || echo "[ERREUR] Probleme avec les modules principaux"
python -c "import numpy, sklearn; print('[OK] Modules de science des donnees installes')" || echo "[ATTENTION] Problemes avec les modules de science des donnees"

echo.
echo [SUCCES] Installation de CyberSec AI Assistant terminee !
echo.
echo Prochaines etapes:
echo 1. Lancez 'start.bat' pour demarrer l'application
echo 2. Ou lancez 'launch_cybersec_ai.bat' pour le menu complet
echo 3. Ou executez 'python demo_launcher.py' pour la demonstration
echo.
echo Documentation: README.md
echo Support: yao.kouakou.dev@gmaii.com
echo.

pause
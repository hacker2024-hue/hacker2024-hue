@echo off
chcp 65001 >nul
title Système Mondial de Détection et Protection contre les Cyberattaques - Yao Kouakou Luc Anicet

echo.
echo ================================================================
echo    🌐 SYSTÈME MONDIAL DE DÉTECTION ET PROTECTION CYBERNÉTIQUE
echo ================================================================
echo    Développé par: Yao Kouakou Luc Anicet
echo    Contact: hackerduckman89@gmail.com
echo    Contact: yao.kouakou.dev@gmail.com
echo    Version: 2.0.0 - Edition Mondiale
echo ================================================================
echo.

:: Vérification de Python
echo [1/8] 🔍 Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé. Veuillez installer Python 3.8+
    echo 📥 Téléchargez depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python détecté

:: Vérification de pip
echo [2/8] 📦 Vérification de pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip n'est pas installé
    pause
    exit /b 1
)
echo ✅ pip détecté

:: Installation des dépendances
echo [3/8] 📥 Installation des dépendances Python...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)
echo ✅ Dépendances installées

:: Vérification de Redis
echo [4/8] 🔍 Vérification de Redis...
redis-server --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Redis n'est pas installé. Tentative d'installation...
    echo 📥 Téléchargez Redis depuis: https://redis.io/download
    echo 💡 Ou utilisez: winget install Redis
    pause
) else (
    echo ✅ Redis détecté
)

:: Création des répertoires
echo [5/8] 📁 Création des répertoires...
if not exist "models" mkdir models
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "config" mkdir config
echo ✅ Répertoires créés

:: Création de la configuration
echo [6/8] ⚙️ Création de la configuration...
if not exist "config.json" (
    echo Création du fichier de configuration...
    python -c "
import json
config = {
    'system': {
        'name': 'CyberDefense Mondial - Yao Kouakou',
        'version': '2.0.0',
        'developer': 'Yao Kouakou Luc Anicet',
        'contact': {
            'primary': 'hackerduckman89@gmail.com',
            'secondary': 'yao.kouakou.dev@gmail.com'
        },
        'environment': 'production'
    },
    'redis': {
        'url': 'redis://localhost:6379',
        'max_connections': 100
    },
    'network': {
        'interface': 'eth0',
        'capture_enabled': True,
        'packet_filters': ['TCP', 'UDP', 'ICMP']
    },
    'ai': {
        'models_dir': 'models',
        'retrain_interval': 86400,
        'confidence_threshold': 0.7
    },
    'intelligence': {
        'feeds_enabled': True,
        'update_interval': 1800,
        'correlation_enabled': True
    },
    'protection': {
        'auto_response': True,
        'escalation_enabled': True,
        'learning_mode': False
    },
    'api': {
        'host': '0.0.0.0',
        'port': 8000,
        'cors_enabled': True
    },
    'world_map': {
        'enabled': True,
        'api_key': '',
        'update_interval': 300
    }
}
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
"
    echo ✅ Configuration créée
) else (
    echo ✅ Configuration existante
)

:: Démarrage de Redis
echo [7/8] 🚀 Démarrage de Redis...
start /B redis-server
timeout /t 3 /nobreak >nul
echo ✅ Redis démarré

:: Démarrage du système
echo [8/8] 🌐 Démarrage du système de défense cybernétique...
echo.
echo ================================================================
echo    🚀 LANCEMENT DU SYSTÈME MONDIAL
echo ================================================================
echo    Dashboard: http://localhost:8000
echo    API Docs:  http://localhost:8000/docs
echo    WebSocket: ws://localhost:8000/ws
echo    Carte Monde: http://localhost:8000/world-map
echo ================================================================
echo.

:: Lancement du système
python launch_cyber_defense.py

echo.
echo ================================================================
echo    ✅ SYSTÈME ARRÊTÉ
echo ================================================================
echo    Développé par: Yao Kouakou Luc Anicet
echo    Contact: hackerduckman89@gmail.com
echo    Contact: yao.kouakou.dev@gmail.com
echo ================================================================
pause
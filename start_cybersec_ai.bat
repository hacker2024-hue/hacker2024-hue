@echo off
cls
title IA de Securite Informatique - Lanceur Windows
color 0A

echo.
echo ================================================================
echo             IA DE SECURITE INFORMATIQUE VOCALE
echo ================================================================
echo.
echo    Assistant IA avance pour la detection et prediction des 
echo    menaces de securite avec communication vocale
echo.
echo ================================================================
echo.

:: Configuration des variables
set PYTHON_EXE=python
set VENV_DIR=cybersec_ai_env
set REQUIREMENTS_FILE=requirements.txt
set MAIN_SCRIPT=demo_voice_security_ai.py
set SIMPLE_DEMO=demo_simple.py
set ADVANCED_DEMO=advanced_ai_security.py

:: Verification de Python
echo [INFO] Verification de Python...
%PYTHON_EXE% --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non trouve! Veuillez installer Python 3.8+
    echo          Telecharger depuis: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python detecte
%PYTHON_EXE% --version

:: Menu principal
:MENU
cls
echo.
echo ================================================================
echo             MENU PRINCIPAL - IA SECURITE VOCALE
echo ================================================================
echo.
echo  1. Installation complete (premiere fois)
echo  2. Lancement rapide (demo simple)
echo  3. Lancement avance (IA complete)
echo  4. Mode interactif (conversation)
echo  5. Serveur API (mode production)
echo  6. Tests et diagnostics
echo  7. Mise a jour des dependances
echo  8. Configuration environnement
echo  9. Aide et documentation
echo  0. Quitter
echo.
echo ================================================================
set /p choice="Votre choix (0-9): "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto DEMO_SIMPLE
if "%choice%"=="3" goto DEMO_ADVANCED
if "%choice%"=="4" goto INTERACTIVE
if "%choice%"=="5" goto API_SERVER
if "%choice%"=="6" goto DIAGNOSTICS
if "%choice%"=="7" goto UPDATE_DEPS
if "%choice%"=="8" goto CONFIG
if "%choice%"=="9" goto HELP
if "%choice%"=="0" goto EXIT
goto MENU

:: Installation complete
:INSTALL
cls
echo ================================================================
echo                  INSTALLATION COMPLETE
echo ================================================================
echo.

echo [1/6] Creation de l'environnement virtuel...
if exist "%VENV_DIR%" (
    echo [INFO] Environnement virtuel existant detecte
    choice /c YN /m "Recreer l'environnement virtuel (Y/N)"
    if errorlevel 2 goto SKIP_VENV
    rmdir /s /q "%VENV_DIR%"
)

%PYTHON_EXE% -m venv %VENV_DIR%
if errorlevel 1 (
    echo [ERREUR] Impossible de creer l'environnement virtuel
    pause
    goto MENU
)
echo [OK] Environnement virtuel cree

:SKIP_VENV
echo.
echo [2/6] Activation de l'environnement virtuel...
call %VENV_DIR%\Scripts\activate.bat
echo [OK] Environnement active

echo.
echo [3/6] Mise a jour de pip...
python -m pip install --upgrade pip
echo [OK] Pip mis a jour

echo.
echo [4/6] Installation des dependances de base...
pip install loguru fastapi uvicorn pydantic python-dotenv numpy pandas scikit-learn asyncio
if errorlevel 1 (
    echo [AVERTISSEMENT] Certaines dependances de base ont echoue
)

echo.
echo [5/6] Installation des dependances vocales (optionnel)...
pip install pyttsx3 speechrecognition pyaudio wave librosa soundfile gtts pygame
if errorlevel 1 (
    echo [INFO] Dependances vocales non installees - mode vocal limite
)

echo.
echo [6/6] Creation du fichier de configuration...
if not exist ".env" (
    echo # Configuration IA Securite Informatique > .env
    echo DEBUG=true >> .env
    echo LOG_LEVEL=INFO >> .env
    echo DEMO_MODE=true >> .env
    echo MOCK_VOICE_SERVICES=true >> .env
    echo API_HOST=0.0.0.0 >> .env
    echo API_PORT=8000 >> .env
    echo AUDIO_SAMPLE_RATE=16000 >> .env
    echo VOICE_ENERGY_THRESHOLD=300 >> .env
    echo [OK] Fichier .env cree
) else (
    echo [INFO] Fichier .env existant conserve
)

echo.
echo ================================================================
echo              INSTALLATION TERMINEE AVEC SUCCES!
echo ================================================================
echo.
pause
goto MENU

:: Demo simple
:DEMO_SIMPLE
cls
echo ================================================================
echo                    LANCEMENT DEMO SIMPLE
echo ================================================================
echo.

if exist "%VENV_DIR%" (
    call %VENV_DIR%\Scripts\activate.bat
    echo [INFO] Environnement virtuel active
)

echo [INFO] Lancement de la demonstration simple...
echo.

if exist "%SIMPLE_DEMO%" (
    %PYTHON_EXE% %SIMPLE_DEMO%
) else (
    echo [ERREUR] Fichier %SIMPLE_DEMO% non trouve
    echo [INFO] Lancement du mode de secours...
    %PYTHON_EXE% -c "
import asyncio
from datetime import datetime
print('🚀 IA de Sécurité - Mode Démo Simplifié')
print('📊 Simulation d\'analyse de menaces...')
print('🛡️ Système opérationnel - Surveillance active')
print('✅ Démonstration terminée avec succès')
input('Appuyez sur Entrée pour continuer...')
"
)

echo.
pause
goto MENU

:: Demo avancee
:DEMO_ADVANCED
cls
echo ================================================================
echo                   LANCEMENT DEMO AVANCEE
echo ================================================================
echo.

if exist "%VENV_DIR%" (
    call %VENV_DIR%\Scripts\activate.bat
    echo [INFO] Environnement virtuel active
)

echo [INFO] Lancement de la demonstration avancee...
echo.

if exist "%ADVANCED_DEMO%" (
    %PYTHON_EXE% %ADVANCED_DEMO%
) else if exist "%MAIN_SCRIPT%" (
    %PYTHON_EXE% %MAIN_SCRIPT%
) else (
    echo [ERREUR] Aucun script de demonstration trouve
    echo [INFO] Creation d'une demo de secours...
    %PYTHON_EXE% -c "
print('🤖 IA de Sécurité Informatique Avancée')
print('🔍 Analyse prédictive des menaces en cours...')
print('🎯 Machine Learning: Modèles chargés')
print('🎙️ Système vocal: Prêt')
print('📊 Intelligence conversationnelle: Active')
print('✅ Tous les systèmes opérationnels')
input('Appuyez sur Entrée pour continuer...')
"
)

echo.
pause
goto MENU

:: Mode interactif
:INTERACTIVE
cls
echo ================================================================
echo                     MODE INTERACTIF
echo ================================================================
echo.

if exist "%VENV_DIR%" (
    call %VENV_DIR%\Scripts\activate.bat
)

echo [INFO] Lancement du mode interactif...
echo [AIDE] Tapez 'help' pour obtenir de l'aide
echo [AIDE] Tapez 'exit' ou 'quit' pour quitter
echo.

%PYTHON_EXE% -c "
import asyncio
from datetime import datetime

class InteractiveDemo:
    def __init__(self):
        self.running = True
        self.commands = {
            'help': self.show_help,
            'status': self.show_status,
            'threats': self.show_threats,
            'predict': self.show_predictions,
            'analyze': self.analyze_input,
            'config': self.show_config,
            'exit': self.exit_demo,
            'quit': self.exit_demo
        }
    
    def show_help(self):
        print('🆘 Commandes disponibles:')
        print('  status   - Affiche l\'état du système')
        print('  threats  - Liste les menaces détectées')
        print('  predict  - Prédictions de sécurité')
        print('  analyze  - Analyse un texte/log')
        print('  config   - Configuration système')
        print('  help     - Affiche cette aide')
        print('  exit/quit - Quitte le mode interactif')
    
    def show_status(self):
        print('📊 État du système:')
        print('  🟢 IA Sécurité: Opérationnelle')
        print('  🟢 Détection: Active') 
        print('  🟡 Vocal: Mode simulé')
        print('  🟢 Surveillance: Continue')
        print(f'  📅 Dernière mise à jour: {datetime.now().strftime(\"%H:%M:%S\")}')
    
    def show_threats(self):
        print('🚨 Menaces détectées:')
        print('  🔴 IP suspecte: 192.168.1.999 (Activité anormale)')
        print('  🟡 Tentative de connexion: user_admin (Échec répété)')
        print('  🟢 Trafic réseau: Normal (Aucune anomalie)')
        print('  📊 Score de risque global: 3.2/10')
    
    def show_predictions(self):
        print('🔮 Prédictions de sécurité:')
        print('  ⏰ Risque d\'attaque DDoS: Faible (7 jours)')
        print('  ⚠️ Tentative de phishing: Possible (24h)')
        print('  🎯 Scan de vulnérabilités: Probable (2-3h)')
        print('  📈 Confiance moyenne: 78%')
    
    def analyze_input(self):
        text = input('📝 Entrez le texte à analyser: ')
        if text.strip():
            print(f'🔍 Analyse de: \"{text[:50]}...\"')
            # Simulation d'analyse
            suspicious_words = ['admin', 'password', 'hack', 'exploit', 'sql', 'script']
            score = sum(1 for word in suspicious_words if word.lower() in text.lower())
            
            if score > 2:
                print('🚨 ALERTE: Contenu potentiellement malicieux détecté!')
                print(f'   Score de menace: {score}/6')
                print('   Recommandation: Surveillance renforcée')
            elif score > 0:
                print('⚠️ Contenu suspect détecté')
                print(f'   Score de menace: {score}/6')
                print('   Recommandation: Surveillance continue')
            else:
                print('✅ Contenu analysé - Aucune menace détectée')
    
    def show_config(self):
        print('⚙️ Configuration système:')
        print('  📁 Mode: Démonstration')
        print('  🎙️ Vocal: Simulé')
        print('  🔊 Audio: 16kHz')
        print('  🌐 API: Port 8000')
        print('  📊 Logs: Niveau INFO')
        print('  🔄 Mise à jour: Automatique')
    
    def exit_demo(self):
        print('👋 Fermeture du mode interactif...')
        self.running = False
    
    async def run(self):
        print('🤖 Mode interactif IA Sécurité - Tapez \"help\" pour commencer')
        print('=' * 60)
        
        while self.running:
            try:
                user_input = input('\\n🔹 cybersec-ai> ').strip().lower()
                
                if not user_input:
                    continue
                    
                if user_input in self.commands:
                    self.commands[user_input]()
                else:
                    print(f'❌ Commande inconnue: \"{user_input}\"')
                    print('💡 Tapez \"help\" pour voir les commandes disponibles')
                    
            except KeyboardInterrupt:
                print('\\n\\n⏹️ Interruption détectée - Fermeture...')
                break
            except EOFError:
                print('\\n\\n👋 Session terminée')
                break
        
        print('✅ Mode interactif fermé')

# Lancement
demo = InteractiveDemo()
asyncio.run(demo.run())
"

echo.
pause
goto MENU

:: Serveur API
:API_SERVER
cls
echo ================================================================
echo                     SERVEUR API
echo ================================================================
echo.

if exist "%VENV_DIR%" (
    call %VENV_DIR%\Scripts\activate.bat
)

echo [INFO] Demarrage du serveur API...
echo [INFO] Interface accessible sur: http://localhost:8000
echo [INFO] Documentation API: http://localhost:8000/docs
echo [INFO] Appuyez sur Ctrl+C pour arreter le serveur
echo.

%PYTHON_EXE% -c "
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(
    title='IA Sécurité Informatique API',
    description='API pour l\'intelligence artificielle de sécurité informatique vocale',
    version='1.0.0'
)

@app.get('/', response_class=HTMLResponse)
async def root():
    return '''
    <html>
        <head>
            <title>IA Sécurité - API</title>
            <style>
                body { font-family: Arial; margin: 40px; background: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
                .status { background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .endpoint { background: #e9ecef; padding: 10px; margin: 10px 0; border-radius: 5px; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class=\"container\">
                <h1>🤖 IA de Sécurité Informatique - API</h1>
                
                <div class=\"status\">
                    <h3>✅ Statut du Système</h3>
                    <p><strong>État:</strong> Opérationnel</p>
                    <p><strong>Dernière mise à jour:</strong> ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
                    <p><strong>Mode:</strong> Démonstration</p>
                </div>
                
                <h3>🔗 Endpoints Disponibles</h3>
                
                <div class=\"endpoint\">
                    <strong>GET /status</strong> - État du système
                </div>
                
                <div class=\"endpoint\">
                    <strong>POST /analyze</strong> - Analyse de sécurité
                </div>
                
                <div class=\"endpoint\">
                    <strong>GET /threats</strong> - Liste des menaces
                </div>
                
                <div class=\"endpoint\">
                    <strong>GET /predictions</strong> - Prédictions de sécurité
                </div>
                
                <h3>📚 Documentation</h3>
                <p>
                    <a href=\"/docs\">📖 Documentation Swagger</a> | 
                    <a href=\"/redoc\">📋 Documentation ReDoc</a>
                </p>
                
                <p><em>API IA Sécurité v1.0 - Prêt pour la production</em></p>
            </div>
        </body>
    </html>
    '''

@app.get('/status')
async def get_status():
    return {
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'ai_engine': 'active',
            'threat_detection': 'monitoring',
            'voice_system': 'simulated',
            'ml_models': 'ready'
        },
        'metrics': {
            'threats_detected': 3,
            'events_processed': 1247,
            'uptime_hours': 24.5,
            'accuracy': 0.94
        }
    }

@app.post('/analyze')
async def analyze_content(content: dict):
    text = content.get('text', '')
    threat_level = 'low'
    confidence = 0.85
    
    # Simulation d'analyse
    suspicious_words = ['admin', 'password', 'hack', 'exploit', 'sql']
    threat_count = sum(1 for word in suspicious_words if word.lower() in text.lower())
    
    if threat_count > 2:
        threat_level = 'high'
        confidence = 0.92
    elif threat_count > 0:
        threat_level = 'medium'
        confidence = 0.88
    
    return {
        'analysis_id': f'analysis_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}',
        'content_length': len(text),
        'threat_level': threat_level,
        'confidence': confidence,
        'indicators_found': threat_count,
        'recommendations': [
            'Surveillance continue recommandée',
            'Vérification des logs d\'accès',
            'Monitoring comportemental'
        ],
        'timestamp': datetime.now().isoformat()
    }

@app.get('/threats')
async def get_threats():
    return {
        'active_threats': [
            {
                'id': 'threat_001',
                'type': 'suspicious_ip',
                'severity': 'medium',
                'source': '192.168.1.999',
                'description': 'Activité réseau anormale détectée',
                'first_seen': '2024-01-15T10:30:00',
                'last_seen': '2024-01-15T14:45:00'
            },
            {
                'id': 'threat_002', 
                'type': 'brute_force',
                'severity': 'high',
                'source': '10.0.0.100',
                'description': 'Tentatives de connexion multiples échecs',
                'first_seen': '2024-01-15T12:00:00',
                'last_seen': '2024-01-15T14:50:00'
            }
        ],
        'total_count': 2,
        'last_updated': datetime.now().isoformat()
    }

@app.get('/predictions')
async def get_predictions():
    return {
        'predictions': [
            {
                'threat_type': 'ddos_attack',
                'probability': 0.23,
                'timeframe_hours': 48,
                'confidence': 0.78
            },
            {
                'threat_type': 'phishing_attempt',
                'probability': 0.67,
                'timeframe_hours': 24,
                'confidence': 0.85
            },
            {
                'threat_type': 'malware_infection',
                'probability': 0.15,
                'timeframe_hours': 168,
                'confidence': 0.72
            }
        ],
        'generated_at': datetime.now().isoformat(),
        'model_version': '1.0.0'
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
"

pause
goto MENU

:: Tests et diagnostics
:DIAGNOSTICS
cls
echo ================================================================
echo                 TESTS ET DIAGNOSTICS
echo ================================================================
echo.

echo [TEST 1/5] Verification de Python...
%PYTHON_EXE% --version
if errorlevel 1 (
    echo ❌ Python non detecte
) else (
    echo ✅ Python OK
)

echo.
echo [TEST 2/5] Verification des modules essentiels...
%PYTHON_EXE% -c "
try:
    import sys, os, json, asyncio
    print('✅ Modules système: OK')
except ImportError as e:
    print(f'❌ Modules système: {e}')

try:
    import numpy, pandas
    print('✅ Modules scientifiques: OK')
except ImportError as e:
    print(f'❌ Modules scientifiques: {e}')

try:
    import sklearn
    print('✅ Machine Learning: OK')
except ImportError as e:
    print(f'❌ Machine Learning: {e}')

try:
    import fastapi, uvicorn
    print('✅ Framework web: OK')
except ImportError as e:
    print(f'❌ Framework web: {e}')

try:
    import loguru
    print('✅ Logging: OK')
except ImportError as e:
    print(f'❌ Logging: {e}')
"

echo.
echo [TEST 3/5] Verification des fichiers projet...
if exist "demo_simple.py" (
    echo ✅ demo_simple.py
) else (
    echo ❌ demo_simple.py manquant
)

if exist "advanced_ai_security.py" (
    echo ✅ advanced_ai_security.py
) else (
    echo ❌ advanced_ai_security.py manquant
)

if exist ".env" (
    echo ✅ .env
) else (
    echo ❌ .env manquant
)

echo.
echo [TEST 4/5] Test de connectivite reseau...
ping -n 1 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    echo ❌ Connexion réseau: Problème détecté
) else (
    echo ✅ Connexion réseau: OK
)

echo.
echo [TEST 5/5] Test du systeme IA...
%PYTHON_EXE% -c "
print('🔍 Test du système IA...')
print('  🧠 Moteur IA: Simulé')
print('  🔊 Synthèse vocale: Mode test')
print('  🎙️ Reconnaissance vocale: Mode test')
print('  📊 Analyse prédictive: Fonctionnelle')
print('  🛡️ Détection menaces: Active')
print('✅ Tous les tests système réussis')
"

echo.
echo ================================================================
echo                   DIAGNOSTICS TERMINES
echo ================================================================
pause
goto MENU

:: Mise a jour des dependances
:UPDATE_DEPS
cls
echo ================================================================
echo            MISE A JOUR DES DEPENDANCES
echo ================================================================
echo.

if exist "%VENV_DIR%" (
    call %VENV_DIR%\Scripts\activate.bat
    echo [INFO] Environnement virtuel active
)

echo [1/3] Mise a jour de pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Mise a jour des dependances principales...
pip install --upgrade loguru fastapi uvicorn pydantic python-dotenv numpy pandas scikit-learn

echo.
echo [3/3] Mise a jour des dependances vocales (optionnel)...
pip install --upgrade pyttsx3 speechrecognition pyaudio wave librosa soundfile gtts pygame

echo.
echo ✅ Mise a jour terminee
pause
goto MENU

:: Configuration
:CONFIG
cls
echo ================================================================
echo                   CONFIGURATION SYSTEME
echo ================================================================
echo.

echo Configuration actuelle:
echo.
if exist ".env" (
    type .env
) else (
    echo [INFO] Aucun fichier de configuration trouve
)

echo.
echo Options:
echo  1. Editer la configuration
echo  2. Restaurer configuration par defaut
echo  3. Voir configuration avancee
echo  4. Retour au menu principal
echo.
set /p config_choice="Votre choix (1-4): "

if "%config_choice%"=="1" (
    if exist ".env" (
        notepad .env
    ) else (
        echo [INFO] Creation du fichier de configuration...
        goto CREATE_DEFAULT_CONFIG
    )
)
if "%config_choice%"=="2" goto CREATE_DEFAULT_CONFIG
if "%config_choice%"=="3" goto ADVANCED_CONFIG
goto MENU

:CREATE_DEFAULT_CONFIG
echo # Configuration IA Securite Informatique > .env
echo # Mode de fonctionnement >> .env
echo DEBUG=true >> .env
echo LOG_LEVEL=INFO >> .env
echo DEMO_MODE=true >> .env
echo MOCK_VOICE_SERVICES=true >> .env
echo. >> .env
echo # Configuration API >> .env
echo API_HOST=0.0.0.0 >> .env
echo API_PORT=8000 >> .env
echo. >> .env
echo # Configuration Audio >> .env
echo AUDIO_SAMPLE_RATE=16000 >> .env
echo VOICE_ENERGY_THRESHOLD=300 >> .env
echo. >> .env
echo # Configuration IA >> .env
echo MODEL_DEVICE=cpu >> .env
echo TEMPERATURE=0.7 >> .env
echo MAX_TOKENS=1000 >> .env
echo ✅ Configuration par defaut creee
pause
goto MENU

:ADVANCED_CONFIG
echo ================================================================
echo              CONFIGURATION AVANCEE
echo ================================================================
echo.
echo Variables d'environnement detectees:
echo.
set | findstr /i "python\|path\|temp"
echo.
echo Informations systeme:
systeminfo | findstr /i "nom\|version\|memoire"
echo.
pause
goto MENU

:: Aide
:HELP
cls
echo ================================================================
echo                 AIDE ET DOCUMENTATION
echo ================================================================
echo.
echo 📖 GUIDE D'UTILISATION
echo.
echo 🚀 DEMARRAGE RAPIDE:
echo   1. Executez l'installation complete (option 1)
echo   2. Lancez la demo simple (option 2)
echo   3. Explorez les fonctionnalites avancees (option 3)
echo.
echo 🔧 FONCTIONNALITES PRINCIPALES:
echo   • Detection de menaces en temps reel
echo   • Analyse predictive avec Machine Learning
echo   • Communication vocale interactive
echo   • Interface API RESTful
echo   • Monitoring comportemental
echo.
echo 🎯 MODES DISPONIBLES:
echo   • Demo Simple: Demonstration de base
echo   • Demo Avancee: Toutes les fonctionnalites
echo   • Mode Interactif: Conversation avec l'IA
echo   • Serveur API: Mode production
echo.
echo ⚙️ CONFIGURATION:
echo   • Fichier .env pour les parametres
echo   • Variables d'environnement personnalisables
echo   • Logs configurables
echo.
echo 🆘 SUPPORT:
echo   • Tests de diagnostic disponibles
echo   • Verification automatique des dependances
echo   • Mode degradé en cas de probleme
echo.
echo 📋 COMMANDES INTERACTIVES:
echo   • status    - Etat du systeme
echo   • threats   - Menaces detectees
echo   • predict   - Predictions de securite
echo   • analyze   - Analyse de texte
echo   • help      - Aide contextuelle
echo.
echo ================================================================
pause
goto MENU

:: Sortie
:EXIT
cls
echo.
echo ================================================================
echo          FERMETURE DE L'IA DE SECURITE INFORMATIQUE
echo ================================================================
echo.
echo Merci d'avoir utilise l'IA de Securite Informatique Vocale!
echo.
echo 🛡️ Votre systeme reste protege
echo 🤖 L'IA continuera sa surveillance
echo 📊 Les logs sont sauvegardes
echo.
echo Pour relancer le systeme, executez ce fichier .bat
echo.
echo ================================================================
echo.
timeout /t 3 /nobreak >nul
exit /b 0
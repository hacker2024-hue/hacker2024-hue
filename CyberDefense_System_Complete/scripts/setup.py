#!/usr/bin/env python3
"""
Script de configuration automatique
===================================

Configuration initiale de CyberSec AI Assistant.
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from loguru import logger
import secrets


def create_env_file():
    """Création du fichier .env avec des valeurs par défaut"""
    
    env_file = Path(".env")
    
    if env_file.exists():
        logger.info("Fichier .env existant trouvé")
        return
    
    logger.info("Création du fichier .env...")
    
    # Génération d'une clé secrète
    secret_key = secrets.token_urlsafe(32)
    
    env_content = f"""# Configuration CyberSec AI Assistant
# Généré automatiquement le {os.popen('date').read().strip()}

# Application
DEBUG=true
SECRET_KEY={secret_key}
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# Database Configuration (SQLite par défaut pour dev)
DATABASE_URL=sqlite:///./cybersec_ai.db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# IA Model Configuration
AI_MODEL=microsoft/DialoGPT-medium
MODEL_DEVICE=cpu
MAX_RESPONSE_LENGTH=512
AI_TEMPERATURE=0.7

# Authentication
ACCESS_TOKEN_EXPIRE=30
JWT_ALGORITHM=HS256

# Communication Configuration
MAX_CONVERSATION_HISTORY=50
RESPONSE_TIMEOUT=30

# Security Analysis Configuration
MALWARE_ANALYSIS=true
NETWORK_MONITORING=true
VULN_SCANNING=true
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    logger.success("Fichier .env créé avec succès")


def install_spacy_model():
    """Installation du modèle spaCy"""
    
    logger.info("Vérification du modèle spaCy...")
    
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            logger.success("Modèle spaCy déjà installé")
            return True
        except OSError:
            logger.info("Installation du modèle spaCy en_core_web_sm...")
            result = subprocess.run([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.success("Modèle spaCy installé avec succès")
                return True
            else:
                logger.error(f"Erreur lors de l'installation: {result.stderr}")
                return False
                
    except ImportError:
        logger.error("spaCy n'est pas installé")
        return False


def create_directories():
    """Création des répertoires nécessaires"""
    
    directories = [
        "logs",
        "data",
        "models",
        "reports",
        "uploads"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Répertoire créé: {directory}")
        else:
            logger.debug(f"Répertoire existant: {directory}")


def check_system_requirements():
    """Vérification des prérequis système"""
    
    logger.info("Vérification des prérequis système...")
    
    # Version Python
    python_version = sys.version_info
    if python_version < (3, 8):
        logger.error(f"Python 3.8+ requis, trouvé: {python_version.major}.{python_version.minor}")
        return False
    
    logger.success(f"Version Python OK: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Mémoire disponible
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        
        if memory_gb < 4:
            logger.warning(f"Mémoire limitée: {memory_gb:.1f}GB (4GB+ recommandés)")
        else:
            logger.success(f"Mémoire OK: {memory_gb:.1f}GB")
            
    except ImportError:
        logger.info("psutil non disponible, impossible de vérifier la mémoire")
    
    return True


async def test_installation():
    """Test de l'installation"""
    
    logger.info("Test de l'installation...")
    
    try:
        # Import des modules principaux
        from core.config import config
        from core.ai_engine import CyberSecAI
        
        logger.success("✅ Imports des modules principaux OK")
        
        # Test de configuration
        logger.info(f"Configuration chargée: {config.app_name} v{config.version}")
        
        # Test basique du moteur IA (sans initialisation complète)
        ai_engine = CyberSecAI()
        logger.success("✅ Moteur IA instancié")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        return False


def print_final_instructions():
    """Affichage des instructions finales"""
    
    print("\n" + "="*60)
    print("🎉 Configuration terminée avec succès!")
    print("="*60)
    print()
    print("📋 Prochaines étapes:")
    print("  1. Vérifiez le fichier .env et ajustez si nécessaire")
    print("  2. Lancez l'application avec: python main.py")
    print("  3. Accédez à l'interface: http://localhost:8000")
    print("  4. Documentation API: http://localhost:8000/docs")
    print()
    print("🛠️ Commandes utiles:")
    print("  • Installation GPU: pip install torch[cuda]")
    print("  • Mode production: pip install .[production]")
    print("  • Tests: pytest")
    print()
    print("📚 Aide et documentation:")
    print("  • GitHub: https://github.com/hacker2024-hue/cybersec-ai-assistant")
    print("  • Issues: https://github.com/hacker2024-hue/cybersec-ai-assistant/issues")
    print()


def main():
    """Fonction principale de configuration"""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           CyberSec AI Assistant - Configuration          ║
    ║                     Script de Setup                     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    logger.info("🚀 Démarrage de la configuration...")
    
    # Vérifications système
    if not check_system_requirements():
        logger.error("❌ Prérequis système non satisfaits")
        sys.exit(1)
    
    # Création des répertoires
    create_directories()
    
    # Création du fichier .env
    create_env_file()
    
    # Installation du modèle spaCy
    if not install_spacy_model():
        logger.warning("⚠️ Le modèle spaCy n'a pas pu être installé automatiquement")
        logger.info("Vous pouvez l'installer manuellement avec: python -m spacy download en_core_web_sm")
    
    # Test de l'installation
    if asyncio.run(test_installation()):
        logger.success("✅ Installation testée avec succès")
    else:
        logger.error("❌ Erreur lors du test d'installation")
        sys.exit(1)
    
    print_final_instructions()


if __name__ == "__main__":
    main()
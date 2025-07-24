#!/usr/bin/env python3
"""
CyberSec AI Assistant - Point d'entrée principal
===============================================

Démarrage de l'application de sécurité informatique avec IA.
"""

import sys
import asyncio
import uvicorn
from pathlib import Path
from loguru import logger

# Ajout du répertoire racine au path Python
sys.path.insert(0, str(Path(__file__).parent))

from core.config import config
from api.main import app


def setup_logging():
    """Configuration du système de logging"""
    
    # Suppression du logger par défaut
    logger.remove()
    
    # Configuration du format de log
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Logger console
    logger.add(
        sys.stderr,
        format=log_format,
        level=config.log_level,
        colorize=True
    )
    
    # Logger fichier si configuré
    if config.log_file:
        logger.add(
            config.log_file,
            format=log_format,
            level=config.log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )


def print_banner():
    """Affichage de la bannière de démarrage"""
    
    banner = """
    ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗    █████╗ ██╗
    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝   ██╔══██╗██║
    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██║        ███████║██║
    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║        ██╔══██║██║
    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗╚██████╗   ██║  ██║██║
     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝   ╚═╝  ╚═╝╚═╝
    """
    
    print("\033[96m" + banner + "\033[0m")
    print("\033[93m" + "🛡️  Assistant IA Avancé en Cybersécurité" + "\033[0m")
    print("\033[92m" + f"Version {config.version} - Développé par Yao Kouakou Luc Annicet" + "\033[0m")
    print("\033[94m" + "=" * 80 + "\033[0m")
    print()


def check_dependencies():
    """Vérification des dépendances requises"""
    
    logger.info("Vérification des dépendances...")
    
    required_packages = [
        "torch", "transformers", "fastapi", "uvicorn", 
        "spacy", "sklearn", "pandas", "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.debug(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"❌ {package} - MANQUANT")
    
    if missing_packages:
        logger.error(f"Packages manquants: {', '.join(missing_packages)}")
        logger.error("Installez les dépendances avec: pip install -r requirements.txt")
        return False
    
    logger.success("Toutes les dépendances sont installées")
    return True


def check_models():
    """Vérification des modèles requis"""
    
    logger.info("Vérification des modèles...")
    
    try:
        # Vérification du modèle spaCy
        import spacy
        try:
            spacy.load("en_core_web_sm")
            logger.success("✅ Modèle spaCy en_core_web_sm disponible")
        except OSError:
            logger.warning("⚠️ Modèle spaCy en_core_web_sm manquant")
            logger.info("Installez avec: python -m spacy download en_core_web_sm")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la vérification des modèles: {e}")
        return False


def print_system_info():
    """Affichage des informations système"""
    
    logger.info("Configuration système:")
    logger.info(f"  🖥️  Host: {config.api_host}:{config.api_port}")
    logger.info(f"  🧠  Modèle IA: {config.model_name}")
    logger.info(f"  💾  Device: {config.model_device}")
    logger.info(f"  🌡️  Température: {config.temperature}")
    logger.info(f"  🔧  Mode debug: {config.debug}")
    logger.info(f"  👥  Workers: {config.api_workers}")
    logger.info(f"  📊  Log level: {config.log_level}")


async def startup_checks():
    """Vérifications de démarrage"""
    
    logger.info("🔍 Exécution des vérifications de démarrage...")
    
    # Vérification des dépendances
    if not check_dependencies():
        logger.error("❌ Échec de la vérification des dépendances")
        return False
    
    # Vérification des modèles
    if not check_models():
        logger.warning("⚠️ Certains modèles sont manquants")
    
    # Test de connectivité (optionnel)
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://httpbin.org/status/200")
            if response.status_code == 200:
                logger.success("✅ Connectivité Internet OK")
    except Exception:
        logger.warning("⚠️ Connectivité Internet limitée")
    
    logger.success("✅ Vérifications de démarrage terminées")
    return True


def main():
    """Fonction principale"""
    
    print_banner()
    setup_logging()
    
    logger.info("🚀 Démarrage de CyberSec AI Assistant...")
    
    # Vérifications de démarrage
    if not asyncio.run(startup_checks()):
        logger.error("❌ Échec des vérifications de démarrage")
        sys.exit(1)
    
    print_system_info()
    
    # Configuration pour le démarrage
    uvicorn_config = {
        "app": app,
        "host": config.api_host,
        "port": config.api_port,
        "log_level": config.log_level.lower(),
        "reload": config.debug,
        "workers": 1 if config.debug else config.api_workers,
        "access_log": True,
        "use_colors": True,
    }
    
    logger.info("🌐 Démarrage du serveur web...")
    logger.info(f"📍 Interface disponible sur: http://{config.api_host}:{config.api_port}")
    logger.info(f"📚 Documentation API: http://{config.api_host}:{config.api_port}/docs")
    logger.info(f"🔧 Statut système: http://{config.api_host}:{config.api_port}/health")
    
    try:
        uvicorn.run(**uvicorn_config)
    except KeyboardInterrupt:
        logger.info("🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        sys.exit(1)
    finally:
        logger.info("👋 CyberSec AI Assistant arrêté")


if __name__ == "__main__":
    main()
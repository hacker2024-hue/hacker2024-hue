#!/usr/bin/env python3
"""
Script de Lancement du Système Mondial de Détection et Protection contre les Cyberattaques
========================================================================================

Ce script permet de démarrer facilement le système de défense cybernétique
avec différentes configurations et options.
"""

import asyncio
import argparse
import json
import logging
import sys
import os
from pathlib import Path
from typing import Dict, Any
import signal
import psutil

# Ajout du répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

from security.cyber_defense_system import CyberDefenseSystem, start_cyber_defense_system

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cyber_defense.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CyberDefenseLauncher:
    """Lanceur du système de défense cybernétique"""
    
    def __init__(self):
        self.system = None
        self.config = {}
        
    def load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Chargement de la configuration"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
                logger.info(f"Configuration chargée depuis {config_path}")
        else:
            # Configuration par défaut
            self.config = {
                "redis_url": "redis://localhost:6379",
                "network_interface": "eth0",
                "api_host": "0.0.0.0",
                "api_port": 8000,
                "websocket_enabled": True,
                "auto_response_enabled": True,
                "threat_feed_update_interval": 300,
                "metrics_collection_interval": 30,
                "alert_retention_days": 30,
                "max_concurrent_incidents": 100,
                "emergency_threshold": 10,
                "backup_enabled": True,
                "logging_level": "INFO",
                "capture_packets": True,
                "enable_ai_analysis": True,
                "enable_global_sharing": True,
                "enable_auto_mitigation": True
            }
            logger.info("Configuration par défaut utilisée")
        
        return self.config
    
    def check_prerequisites(self) -> bool:
        """Vérification des prérequis"""
        logger.info("🔍 Vérification des prérequis...")
        
        # Vérification de Redis
        try:
            import redis
            r = redis.Redis.from_url(self.config.get("redis_url", "redis://localhost:6379"))
            r.ping()
            logger.info("✅ Redis connecté")
        except Exception as e:
            logger.error(f"❌ Erreur connexion Redis: {e}")
            logger.error("Veuillez démarrer Redis: sudo systemctl start redis")
            return False
        
        # Vérification des permissions réseau
        try:
            import scapy
            logger.info("✅ Scapy disponible")
        except ImportError:
            logger.error("❌ Scapy non installé: pip install scapy")
            return False
        
        # Vérification des permissions root pour la capture de paquets
        if self.config.get("capture_packets", True):
            if os.geteuid() != 0:
                logger.warning("⚠️  Capture de paquets désactivée (nécessite les permissions root)")
                self.config["capture_packets"] = False
        
        # Vérification de l'interface réseau
        network_interface = self.config.get("network_interface", "eth0")
        if not os.path.exists(f"/sys/class/net/{network_interface}"):
            logger.warning(f"⚠️  Interface réseau {network_interface} non trouvée")
            # Tentative de détection automatique
            import psutil
            interfaces = psutil.net_if_addrs().keys()
            if interfaces:
                auto_interface = list(interfaces)[0]
                logger.info(f"🔧 Interface automatique détectée: {auto_interface}")
                self.config["network_interface"] = auto_interface
        
        logger.info("✅ Prérequis vérifiés")
        return True
    
    async def start_system(self) -> bool:
        """Démarrage du système"""
        try:
            logger.info("🚀 Démarrage du système de défense cybernétique...")
            
            # Création et initialisation du système
            self.system = CyberDefenseSystem(self.config)
            await self.system.initialize()
            
            logger.info("✅ Système démarré avec succès")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du démarrage: {e}")
            return False
    
    async def run_system(self):
        """Exécution du système"""
        if not self.system:
            logger.error("❌ Système non initialisé")
            return
        
        try:
            # Démarrage du serveur API
            host = self.config.get("api_host", "0.0.0.0")
            port = self.config.get("api_port", 8000)
            
            logger.info(f"🌐 Serveur API démarré sur http://{host}:{port}")
            logger.info("📊 Interface WebSocket disponible sur ws://localhost:8000/ws")
            logger.info("📚 Documentation API: http://localhost:8000/docs")
            
            # Démarrage du serveur
            self.system.run(host=host, port=port)
            
        except KeyboardInterrupt:
            logger.info("🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'exécution: {e}")
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Nettoyage et arrêt propre"""
        if self.system:
            logger.info("🛑 Arrêt du système...")
            await self.system.shutdown()
            logger.info("✅ Système arrêté proprement")
    
    def setup_signal_handlers(self):
        """Configuration des gestionnaires de signaux"""
        def signal_handler(signum, frame):
            logger.info(f"Signal {signum} reçu, arrêt en cours...")
            asyncio.create_task(self.cleanup())
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def print_banner(self):
        """Affichage de la bannière"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🌐 SYSTÈME MONDIAL DE DÉTECTION ET PROTECTION CONTRE LES CYBERATTAQUES   ║
║                                                                              ║
║    🛡️  Détection en temps réel • Protection proactive • Surveillance réseau ║
║    🧠 Intelligence artificielle • Corrélation globale • Réponse automatique ║
║                                                                              ║
║    Version: 1.0.0 | Sécurité Avancée | Protection Intelligente             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_status(self):
        """Affichage du statut du système"""
        if self.system:
            status = self.system.status.value
            print(f"\n📊 Statut du système: {status.upper()}")
            
            # Statistiques rapides
            try:
                import asyncio
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Ces appels seraient asynchrones dans un vrai contexte
                    print("📈 Métriques système disponibles via l'API")
            except:
                pass
        else:
            print("\n❌ Système non démarré")

def create_config_template():
    """Création d'un template de configuration"""
    template = {
        "redis_url": "redis://localhost:6379",
        "network_interface": "eth0",
        "api_host": "0.0.0.0",
        "api_port": 8000,
        "websocket_enabled": True,
        "auto_response_enabled": True,
        "threat_feed_update_interval": 300,
        "metrics_collection_interval": 30,
        "alert_retention_days": 30,
        "max_concurrent_incidents": 100,
        "emergency_threshold": 10,
        "backup_enabled": True,
        "logging_level": "INFO",
        "capture_packets": True,
        "enable_ai_analysis": True,
        "enable_global_sharing": True,
        "enable_auto_mitigation": True,
        "threat_feeds": [
            "https://api.abuseipdb.com/api/v2/blacklist",
            "https://api.threatfox.abuse.ch/export/csv/",
            "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/"
        ],
        "monitoring": {
            "enable_network_monitoring": True,
            "enable_threat_detection": True,
            "enable_protection": True,
            "enable_correlation": True
        },
        "notifications": {
            "email_enabled": False,
            "slack_enabled": False,
            "webhook_enabled": False,
            "sms_enabled": False
        }
    }
    
    with open("cyber_defense_config.json", "w") as f:
        json.dump(template, f, indent=2)
    
    print("📄 Template de configuration créé: cyber_defense_config.json")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Système Mondial de Détection et Protection contre les Cyberattaques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python launch_cyber_defense.py                    # Démarrage avec config par défaut
  python launch_cyber_defense.py -c config.json    # Démarrage avec config personnalisée
  python launch_cyber_defense.py --create-config   # Créer un template de configuration
  python launch_cyber_defense.py --check-only      # Vérifier les prérequis uniquement
        """
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Chemin vers le fichier de configuration JSON"
    )
    
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Créer un template de configuration"
    )
    
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Vérifier les prérequis uniquement"
    )
    
    parser.add_argument(
        "--no-capture",
        action="store_true",
        help="Désactiver la capture de paquets"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Mode debug avec logs détaillés"
    )
    
    args = parser.parse_args()
    
    # Affichage de la bannière
    launcher = CyberDefenseLauncher()
    launcher.print_banner()
    
    # Création de template de configuration
    if args.create_config:
        create_config_template()
        return
    
    # Configuration du niveau de log
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Mode debug activé")
    
    # Chargement de la configuration
    config = launcher.load_config(args.config)
    
    # Désactivation de la capture si demandé
    if args.no_capture:
        config["capture_packets"] = False
        logger.info("📡 Capture de paquets désactivée")
    
    # Vérification des prérequis
    if not launcher.check_prerequisites():
        logger.error("❌ Prérequis non satisfaits")
        sys.exit(1)
    
    # Arrêt si vérification uniquement
    if args.check_only:
        logger.info("✅ Prérequis vérifiés avec succès")
        return
    
    # Configuration des gestionnaires de signaux
    launcher.setup_signal_handlers()
    
    # Démarrage du système
    async def run():
        if await launcher.start_system():
            await launcher.run_system()
        else:
            logger.error("❌ Impossible de démarrer le système")
            sys.exit(1)
    
    # Exécution
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        logger.info("🛑 Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
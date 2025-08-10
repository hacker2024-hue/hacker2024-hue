#!/usr/bin/env python3
"""
Script de Lancement du Système de Défense Cybernétique
=====================================================

Lancement simplifié du système avec protection par mot de passe.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

# Import du système principal
from security.cyber_defense_system import CyberDefenseSystem

async def main():
    """Fonction principale de lancement"""
    
    print("🔐 Système Mondial de Défense Cybernétique")
    print("=" * 50)
    print("👨‍💻 Développé par: Yao Kouakou Luc Anicet")
    print("📞 Téléphone: +225 014094507")
    print("📧 Email: hackerduckman89@gmail.com")
    print("🔐 Licence: CI-CYBER-2024-001")
    print("🔑 Mot de passe: AZ12ER34")
    print("=" * 50)
    
    try:
        # Charger la configuration
        config_path = Path("config.json")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            print("❌ Fichier de configuration config.json non trouvé")
            return
        
        # Créer et initialiser le système
        print("🚀 Initialisation du système...")
        system = CyberDefenseSystem(config)
        
        # Démarrer le système
        print("🌐 Démarrage du serveur web...")
        await system.initialize()
        
        # Lancer le serveur
        print("✅ Système prêt !")
        print("🌐 Dashboard: http://localhost:8000/auth")
        print("🔐 Mot de passe: AZ12ER34")
        print("📊 API: http://localhost:8000/api/")
        print("🗺️ Carte mondiale: http://localhost:8000/world-map")
        print("=" * 50)
        
        # Lancer le serveur
        system.run(host="0.0.0.0", port=8000)
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du système...")
        if 'system' in locals():
            await system.shutdown()
        print("✅ Système arrêté")
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
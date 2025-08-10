#!/usr/bin/env python3
"""
Lancement Simple du Système de Défense Cybernétique
==================================================

Script de lancement simplifié sans dépendances problématiques.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

# Imports directs des modules nécessaires
from security.access_protection import AccessProtection, access_protection
from security.auth_interface import AuthInterface
from security.dashboard_interface import DashboardInterface
from security.notification_system import NotificationSystem
from security.license_system import LicenseSystem
from security.payment_system import PaymentSystem
from security.world_map_monitor import WorldMapMonitor

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

async def create_simple_system():
    """Créer un système simplifié"""
    
    # Créer l'application FastAPI
    app = FastAPI(
        title="Système de Défense Cybernétique",
        description="Système mondial de détection et protection contre les cyberattaques",
        version="3.0.0"
    )
    
    # Ajouter CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Initialiser les composants
    print("🔐 Initialisation du système de protection...")
    await access_protection.initialize()
    
    print("🌐 Initialisation du dashboard...")
    dashboard = DashboardInterface(app)
    
    print("📧 Initialisation des notifications...")
    notification_system = NotificationSystem()
    await notification_system.initialize()
    
    print("🔐 Initialisation du système de licences...")
    license_system = LicenseSystem()
    await license_system.initialize()
    
    print("💳 Initialisation du système de paiements...")
    payment_system = PaymentSystem()
    await payment_system.initialize()
    
    print("🗺️ Initialisation de la carte mondiale...")
    world_map = WorldMapMonitor()
    await world_map.initialize()
    
    print("🔐 Initialisation de l'authentification...")
    auth_interface = AuthInterface(app)
    
    # Routes de base
    @app.get("/")
    async def root():
        return {
            "message": "Système de Défense Cybernétique",
            "version": "3.0.0 - Edition Commerciale",
            "developer": "Yao Kouakou Luc Anicet",
            "contact": "+225 014094507",
            "license": "CI-CYBER-2024-001",
            "status": "Opérationnel"
        }
    
    @app.get("/status")
    async def status():
        return {
            "status": "running",
            "components": {
                "protection": "active",
                "dashboard": "active",
                "notifications": "active",
                "licenses": "active",
                "payments": "active",
                "world_map": "active"
            }
        }
    
    @app.get("/developer")
    async def developer_info():
        return {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license": "CI-CYBER-2024-001",
            "version": "3.0.0 - Edition Commerciale Europe & Côte d'Ivoire"
        }
    
    return app

async def main():
    """Fonction principale"""
    
    print("🔐 Système Mondial de Défense Cybernétique")
    print("=" * 50)
    print("👨‍💻 Développé par: Yao Kouakou Luc Anicet")
    print("📞 Téléphone: +225 014094507")
    print("📧 Email: hackerduckman89@gmail.com")
    print("🔐 Licence: CI-CYBER-2024-001")
    print("🔑 Mot de passe: AZ12ER34")
    print("=" * 50)
    
    try:
        # Créer le système
        print("🚀 Création du système...")
        app = await create_simple_system()
        
        print("✅ Système prêt !")
        print("🌐 Dashboard: http://localhost:8000/auth")
        print("🔐 Mot de passe: AZ12ER34")
        print("📊 API: http://localhost:8000/api/")
        print("🗺️ Carte mondiale: http://localhost:8000/world-map")
        print("📋 Statut: http://localhost:8000/status")
        print("👨‍💻 Développeur: http://localhost:8000/developer")
        print("=" * 50)
        
        # Lancer le serveur
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du système...")
        print("✅ Système arrêté")
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
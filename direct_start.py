#!/usr/bin/env python3
"""
Lancement Direct du Système de Défense Cybernétique
==================================================

Script de lancement qui importe directement les modules.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

# Imports directs sans passer par __init__.py
sys.path.insert(0, str(Path(__file__).parent / "security"))

# Imports directs des modules
import access_protection
import auth_interface
import dashboard_interface
import notification_system
import license_system
import payment_system
import world_map_monitor

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

async def create_direct_system():
    """Créer un système avec imports directs"""
    
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
    await access_protection.access_protection.initialize()
    
    print("🌐 Initialisation du dashboard...")
    dashboard = dashboard_interface.DashboardInterface(app)
    
    print("📧 Initialisation des notifications...")
    notification_sys = notification_system.NotificationSystem()
    await notification_sys.initialize()
    
    print("🔐 Initialisation du système de licences...")
    license_sys = license_system.LicenseSystem()
    await license_sys.initialize()
    
    print("💳 Initialisation du système de paiements...")
    payment_sys = payment_system.PaymentSystem()
    await payment_sys.initialize()
    
    print("🗺️ Initialisation de la carte mondiale...")
    world_map = world_map_monitor.WorldMapMonitor()
    await world_map.initialize()
    
    print("🔐 Initialisation de l'authentification...")
    auth_interface.AuthInterface(app)
    
    # Routes de base
    @app.get("/")
    async def root():
        return {
            "message": "Système de Défense Cybernétique",
            "version": "3.0.0 - Edition Commerciale",
            "developer": "Yao Kouakou Luc Anicet",
            "contact": "+225 014094507",
            "license": "CI-CYBER-2024-001",
            "status": "Opérationnel",
            "password": "AZ12ER34"
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
            },
            "developer": {
                "name": "Yao Kouakou Luc Anicet",
                "phone": "+225 014094507",
                "email": "hackerduckman89@gmail.com",
                "license": "CI-CYBER-2024-001"
            }
        }
    
    @app.get("/developer")
    async def developer_info():
        return {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license": "CI-CYBER-2024-001",
            "version": "3.0.0 - Edition Commerciale Europe & Côte d'Ivoire",
            "ivoirian_license": {
                "number": "CI-CYBER-2024-001",
                "type": "Licence de Vente de Logiciels de Sécurité",
                "authority": "Ministère du Commerce et de l'Industrie de Côte d'Ivoire",
                "validity": "5 ans (2024-2029)"
            }
        }
    
    @app.get("/test")
    async def test_endpoint():
        return {
            "message": "Test réussi !",
            "system": "Opérationnel",
            "protection": "Active",
            "password": "AZ12ER34"
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
        app = await create_direct_system()
        
        print("✅ Système prêt !")
        print("🌐 Dashboard: http://localhost:8000/auth")
        print("🔐 Mot de passe: AZ12ER34")
        print("📊 API: http://localhost:8000/api/")
        print("🗺️ Carte mondiale: http://localhost:8000/world-map")
        print("📋 Statut: http://localhost:8000/status")
        print("👨‍💻 Développeur: http://localhost:8000/developer")
        print("🧪 Test: http://localhost:8000/test")
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
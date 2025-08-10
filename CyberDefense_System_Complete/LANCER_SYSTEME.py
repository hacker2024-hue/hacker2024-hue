#!/usr/bin/env python3
"""
🔐 LANCEMENT DU SYSTÈME DE DÉFENSE CYBERNÉTIQUE
===============================================

Script de lancement final pour le système de défense cybernétique
développé par Yao Kouakou Luc Anicet.

MOT DE PASSE: AZ12ER34
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_banner():
    """Afficher la bannière du système"""
    print("🔐" + "=" * 58 + "🔐")
    print("🌐 SYSTÈME MONDIAL DE DÉFENSE CYBERNÉTIQUE")
    print("=" * 60)
    print("👨‍💻 Développé par: Yao Kouakou Luc Anicet")
    print("📞 Téléphone: +225 014094507")
    print("📧 Email: hackerduckman89@gmail.com")
    print("📧 Email: yao.kouakou.dev@gmail.com")
    print("🔐 Licence: CI-CYBER-2024-001")
    print("🔑 Mot de passe: AZ12ER34")
    print("🌍 Édition: Commerciale Europe & Côte d'Ivoire")
    print("🔐" + "=" * 58 + "🔐")

def check_environment():
    """Vérifier l'environnement"""
    print("\n🔍 Vérification de l'environnement...")
    
    # Vérifier Python
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python: {result.stdout.strip()}")
        else:
            print("❌ Python non disponible")
            return False
    except Exception as e:
        print(f"❌ Erreur Python: {e}")
        return False
    
    # Vérifier l'environnement virtuel
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Environnement virtuel: Actif")
    else:
        print("⚠️ Environnement virtuel: Non détecté")
    
    # Vérifier les fichiers nécessaires
    required_files = [
        "minimal_start.py",
        "config.json",
        "requirements.txt"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}: Présent")
        else:
            print(f"❌ {file}: Manquant")
            return False
    
    return True

def install_dependencies():
    """Installer les dépendances"""
    print("\n📦 Installation des dépendances...")
    
    try:
        # Installer les dépendances de base
        packages = [
            "fastapi",
            "uvicorn",
            "redis",
            "requests",
            "jinja2",
            "plotly",
            "pandas",
            "numpy",
            "cryptography",
            "qrcode",
            "pillow",
            "aiohttp",
            "websockets",
            "python-multipart",
            "psutil",
            "scapy",
            "folium",
            "geopy",
            "loguru",
            "httpx"
        ]
        
        for package in packages:
            print(f"📦 Installation de {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package}: Installé")
            else:
                print(f"⚠️ {package}: Erreur d'installation")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def start_redis():
    """Démarrer Redis"""
    print("\n🔴 Démarrage de Redis...")
    
    try:
        # Vérifier si Redis est déjà en cours d'exécution
        result = subprocess.run(["redis-cli", "ping"], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0 and "PONG" in result.stdout:
            print("✅ Redis: Déjà en cours d'exécution")
            return True
        
        # Démarrer Redis
        print("🚀 Démarrage de Redis...")
        subprocess.Popen(["redis-server", "--daemonize", "yes"])
        time.sleep(2)
        
        # Vérifier que Redis fonctionne
        result = subprocess.run(["redis-cli", "ping"], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0 and "PONG" in result.stdout:
            print("✅ Redis: Démarré avec succès")
            return True
        else:
            print("❌ Redis: Impossible de démarrer")
            return False
            
    except Exception as e:
        print(f"⚠️ Redis: {e}")
        print("ℹ️ Le système peut fonctionner sans Redis")
        return True

def launch_system():
    """Lancer le système"""
    print("\n🚀 Lancement du système...")
    
    try:
        # Lancer le système
        print("🌐 Démarrage du serveur web...")
        process = subprocess.Popen([
            sys.executable, "minimal_start.py"
        ])
        
        # Attendre que le système démarre
        print("⏳ Attente du démarrage...")
        time.sleep(8)
        
        # Tester le système
        print("🧪 Test du système...")
        result = subprocess.run([
            sys.executable, "test_system_live.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Système lancé avec succès !")
            print("\n" + "=" * 60)
            print("🎉 SYSTÈME OPÉRATIONNEL")
            print("=" * 60)
            
            print("\n🌐 Accès au système:")
            print("   🌐 Accueil: http://localhost:8000/")
            print("   📋 Statut: http://localhost:8000/status")
            print("   👨‍💻 Développeur: http://localhost:8000/developer")
            print("   🔐 Licence: http://localhost:8000/license")
            print("   💰 Prix: http://localhost:8000/pricing")
            print("   🛡️ Sécurité: http://localhost:8000/security")
            print("   🧪 Test: http://localhost:8000/test")
            
            print("\n🔐 Informations de sécurité:")
            print("   🔑 Mot de passe: AZ12ER34")
            print("   📞 Contact: +225 014094507")
            print("   📧 Email: hackerduckman89@gmail.com")
            print("   🔐 Licence: CI-CYBER-2024-001")
            
            print("\n✅ Fonctionnalités actives:")
            print("   ✅ Protection par mot de passe")
            print("   ✅ Blocage GitHub")
            print("   ✅ Licence ivoirienne")
            print("   ✅ Tarification commerciale")
            print("   ✅ API sécurisée")
            print("   ✅ Serveur web opérationnel")
            
            print("\n" + "=" * 60)
            print("✅ Système prêt à l'utilisation !")
            print("=" * 60)
            
            return process
            
        else:
            print("❌ Erreur lors du test du système")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return None

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifier l'environnement
    if not check_environment():
        print("❌ Environnement non compatible")
        return
    
    # Installer les dépendances
    if not install_dependencies():
        print("❌ Impossible d'installer les dépendances")
        return
    
    # Démarrer Redis
    start_redis()
    
    # Lancer le système
    process = launch_system()
    
    if process:
        try:
            print("\n🔄 Système en cours d'exécution...")
            print("🛑 Appuyez sur Ctrl+C pour arrêter")
            
            # Attendre l'interruption
            process.wait()
            
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du système...")
            process.terminate()
            process.wait()
            print("✅ Système arrêté")
        
        except Exception as e:
            print(f"❌ Erreur: {e}")
            if process:
                process.terminate()
    else:
        print("❌ Impossible de lancer le système")

if __name__ == "__main__":
    main()
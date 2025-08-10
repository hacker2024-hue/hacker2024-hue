#!/usr/bin/env python3
"""
🔐 Lanceur Unifié - Système Mondial de Défense Cybernétique
Dossier Complet - Yao Kouakou Luc Anicet
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

class DossierCompletLauncher:
    def __init__(self):
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "secondary_email": "yao.kouakou.dev@gmail.com",
            "license": "CI-CYBER-2024-001"
        }
        self.system_info = {
            "name": "Système Mondial de Défense Cybernétique",
            "version": "3.0.0 - Edition Commerciale Europe & Côte d'Ivoire",
            "password": "AZ12ER34"
        }
        self.current_dir = Path(__file__).parent
        self.venv_path = self.current_dir / "cyberdefense_env"
        
    def print_banner(self):
        """Affiche la bannière du système"""
        print("=" * 80)
        print("🔐 SYSTÈME MONDIAL DE DÉFENSE CYBERNÉTIQUE")
        print("📁 DOSSIER COMPLET - LANCEUR UNIFIÉ")
        print("=" * 80)
        print(f"👨‍💻 Développé par: {self.developer_info['name']}")
        print(f"📞 Téléphone: {self.developer_info['phone']}")
        print(f"📧 Email Principal: {self.developer_info['email']}")
        print(f"📧 Email Secondaire: {self.developer_info['secondary_email']}")
        print(f"🔐 Licence Ivoirienne: {self.developer_info['license']}")
        print(f"🚀 Version: {self.system_info['version']}")
        print(f"🔑 Mot de passe: {self.system_info['password']}")
        print("=" * 80)
        print()
        
    def check_environment(self):
        """Vérifie l'environnement Python"""
        print("🔍 Vérification de l'environnement...")
        
        # Vérifier Python
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ requis")
            return False
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} détecté")
        
        # Vérifier l'environnement virtuel
        if self.venv_path.exists():
            print("✅ Environnement virtuel détecté")
            return True
        else:
            print("⚠️  Environnement virtuel non trouvé")
            return self.create_venv()
            
    def create_venv(self):
        """Crée l'environnement virtuel"""
        print("🔧 Création de l'environnement virtuel...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
            print("✅ Environnement virtuel créé")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de la création de l'environnement virtuel")
            return False
            
    def install_dependencies(self):
        """Installe les dépendances"""
        print("📦 Installation des dépendances...")
        
        # Activer l'environnement virtuel
        if os.name == 'nt':  # Windows
            pip_path = self.venv_path / "Scripts" / "pip"
            python_path = self.venv_path / "Scripts" / "python"
        else:  # Linux/Mac
            pip_path = self.venv_path / "bin" / "pip"
            python_path = self.venv_path / "bin" / "python"
            
        if not pip_path.exists():
            print("❌ Pip non trouvé dans l'environnement virtuel")
            return False
            
        # Installer les packages essentiels
        packages = [
            "fastapi", "uvicorn", "redis", "aiohttp", "requests",
            "jinja2", "plotly", "pandas", "numpy", "cryptography",
            "qrcode", "pillow", "psutil", "scapy", "folium", "geopy"
        ]
        
        for package in packages:
            try:
                print(f"📦 Installation de {package}...")
                subprocess.run([str(pip_path), "install", package], check=True, capture_output=True)
                print(f"✅ {package} installé")
            except subprocess.CalledProcessError:
                print(f"⚠️  Erreur lors de l'installation de {package}")
                
        return True
        
    def start_redis(self):
        """Démarre Redis"""
        print("🔴 Démarrage de Redis...")
        try:
            # Vérifier si Redis est déjà en cours d'exécution
            result = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True)
            if result.returncode == 0 and "PONG" in result.stdout:
                print("✅ Redis déjà en cours d'exécution")
                return True
        except FileNotFoundError:
            pass
            
        try:
            # Essayer de démarrer Redis
            subprocess.Popen(["redis-server"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            print("✅ Redis démarré")
            return True
        except FileNotFoundError:
            print("⚠️  Redis non trouvé - le système fonctionnera sans cache")
            return False
            
    def launch_system(self):
        """Lance le système principal"""
        print("🚀 Lancement du système...")
        
        # Activer l'environnement virtuel
        if os.name == 'nt':  # Windows
            python_path = self.venv_path / "Scripts" / "python"
        else:  # Linux/Mac
            python_path = self.venv_path / "bin" / "python"
            
        if not python_path.exists():
            print("❌ Python non trouvé dans l'environnement virtuel")
            return None
            
        try:
            # Lancer le système minimal
            process = subprocess.Popen([
                str(python_path), "minimal_start.py"
            ], cwd=self.current_dir)
            
            print("✅ Système lancé avec succès!")
            return process
        except Exception as e:
            print(f"❌ Erreur lors du lancement: {e}")
            return None
            
    def test_system(self):
        """Teste le système"""
        print("🧪 Test du système...")
        time.sleep(3)  # Attendre que le système démarre
        
        try:
            # Activer l'environnement virtuel
            if os.name == 'nt':  # Windows
                python_path = self.venv_path / "Scripts" / "python"
            else:  # Linux/Mac
                python_path = self.venv_path / "bin" / "python"
                
            # Lancer le test
            result = subprocess.run([
                str(python_path), "test_system_live.py"
            ], cwd=self.current_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Test du système réussi!")
                print(result.stdout)
            else:
                print("⚠️  Test du système avec avertissements:")
                print(result.stdout)
                print(result.stderr)
                
        except Exception as e:
            print(f"⚠️  Erreur lors du test: {e}")
            
    def show_access_info(self):
        """Affiche les informations d'accès"""
        print("\n" + "=" * 80)
        print("🌐 ACCÈS AU SYSTÈME")
        print("=" * 80)
        print(f"🔑 Mot de passe: {self.system_info['password']}")
        print()
        print("📱 URLs d'accès:")
        print("   • Accueil: http://localhost:8000/")
        print("   • Dashboard: http://localhost:8000/dashboard")
        print("   • Authentification: http://localhost:8000/auth")
        print("   • API Status: http://localhost:8000/status")
        print("   • Développeur: http://localhost:8000/developer")
        print("   • Licences: http://localhost:8000/license")
        print("   • Tarification: http://localhost:8000/pricing")
        print()
        print("📞 Support:")
        print(f"   • Téléphone: {self.developer_info['phone']}")
        print(f"   • Email: {self.developer_info['email']}")
        print(f"   • Licence: {self.developer_info['license']}")
        print("=" * 80)
        
    def show_menu(self):
        """Affiche le menu principal"""
        print("\n📋 MENU PRINCIPAL")
        print("1. 🚀 Lancer le système complet")
        print("2. 🧪 Tester le système")
        print("3. 📊 Voir les informations d'accès")
        print("4. 🔧 Installer les dépendances")
        print("5. 📚 Voir la documentation")
        print("6. 🛑 Quitter")
        print()
        
        choice = input("Choisissez une option (1-6): ").strip()
        return choice
        
    def show_documentation(self):
        """Affiche la documentation"""
        print("\n📚 DOCUMENTATION DISPONIBLE")
        print("=" * 50)
        docs = [
            ("README_PRINCIPAL.md", "Guide principal du dossier complet"),
            ("README_LANCEMENT.md", "Guide de lancement"),
            ("SECURITE_ACCES.md", "Documentation sécurité"),
            ("LICENCE_VENTE_IVOIRIENNE.md", "Licence commerciale ivoirienne"),
            ("COMMERCIAL_PRICING.md", "Tarification commerciale"),
            ("README_FINAL.md", "Documentation complète")
        ]
        
        for i, (doc, desc) in enumerate(docs, 1):
            if (self.current_dir / doc).exists():
                print(f"{i}. ✅ {doc} - {desc}")
            else:
                print(f"{i}. ❌ {doc} - {desc}")
                
        print("\n💡 Pour ouvrir un fichier:")
        print("   • Windows: notepad nom_du_fichier.md")
        print("   • Linux/Mac: nano nom_du_fichier.md")
        
    def run(self):
        """Exécute le lanceur principal"""
        self.print_banner()
        
        if not self.check_environment():
            print("❌ Environnement non compatible")
            return
            
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                # Lancer le système
                if self.install_dependencies():
                    self.start_redis()
                    process = self.launch_system()
                    if process:
                        self.show_access_info()
                        print("\n🔄 Système en cours d'exécution...")
                        print("🛑 Appuyez sur Ctrl+C pour arrêter")
                        try:
                            process.wait()
                        except KeyboardInterrupt:
                            print("\n🛑 Arrêt du système...")
                            process.terminate()
                            process.wait()
                            print("✅ Système arrêté")
                            
            elif choice == "2":
                # Tester le système
                self.test_system()
                
            elif choice == "3":
                # Informations d'accès
                self.show_access_info()
                
            elif choice == "4":
                # Installer les dépendances
                self.install_dependencies()
                
            elif choice == "5":
                # Documentation
                self.show_documentation()
                
            elif choice == "6":
                # Quitter
                print("👋 Au revoir!")
                break
                
            else:
                print("❌ Option invalide")
                
            input("\nAppuyez sur Entrée pour continuer...")

def main():
    """Fonction principale"""
    launcher = DossierCompletLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
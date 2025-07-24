#!/usr/bin/env python3
"""
Script de Configuration Cursor - CyberSec AI Assistant
====================================================

Configuration automatique de l'environnement de développement Cursor
pour le projet CyberSec AI Assistant.

Auteur: Yao Kouakou Luc Annicet
Email: yao.kouakou.dev@gmaii.com
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path

class CursorSetup:
    def __init__(self):
        self.project_name = "CyberSec AI Assistant"
        self.version = "1.0.0"
        self.author = "Yao Kouakou Luc Annicet"
        self.email = "yao.kouakou.dev@gmaii.com"
        self.github = "https://github.com/hackerduckman89/cybersec-ai-assistant"
        
        self.current_dir = Path.cwd()
        self.cursor_dir = self.current_dir / ".cursor"
        
    def print_banner(self):
        """Affiche la bannière de configuration"""
        print("\n" + "="*60)
        print("🎯 CONFIGURATION CURSOR - CYBERSEC AI ASSISTANT")
        print("="*60)
        print(f"📁 Projet: {self.project_name}")
        print(f"👨‍💻 Auteur: {self.author}")
        print(f"📧 Email: {self.email}")
        print(f"🔗 GitHub: {self.github}")
        print("="*60 + "\n")
    
    def check_cursor_installation(self):
        """Vérifie si Cursor est installé"""
        try:
            result = subprocess.run(['cursor', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Cursor est installé:", result.stdout.strip())
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        print("❌ Cursor n'est pas installé ou non accessible")
        print("📥 Téléchargez Cursor: https://cursor.sh/")
        return False
    
    def create_cursor_directories(self):
        """Crée les répertoires nécessaires pour Cursor"""
        try:
            self.cursor_dir.mkdir(exist_ok=True)
            print(f"✅ Répertoire Cursor créé: {self.cursor_dir}")
            return True
        except Exception as e:
            print(f"❌ Erreur création répertoire: {e}")
            return False
    
    def check_project_structure(self):
        """Vérifie la structure du projet"""
        required_files = [
            'README.md',
            'requirements.txt',
            'main.py',
            'demo_launcher.py',
            'core/',
            'api/',
            'security/',
            'communication/'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.current_dir / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print("❌ Fichiers manquants:", ', '.join(missing_files))
            return False
        
        print("✅ Structure du projet validée")
        return True
    
    def setup_python_environment(self):
        """Configure l'environnement Python"""
        print("\n🐍 Configuration environnement Python...")
        
        # Vérification Python
        python_version = sys.version_info
        if python_version < (3, 8):
            print(f"❌ Python {python_version.major}.{python_version.minor} trop ancien")
            print("📥 Installez Python 3.8+ depuis https://python.org")
            return False
        
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Création environnement virtuel si nécessaire
        venv_path = self.current_dir / "venv"
        if not venv_path.exists():
            print("📦 Création environnement virtuel...")
            try:
                subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
                print("✅ Environnement virtuel créé")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur création venv: {e}")
                return False
        else:
            print("✅ Environnement virtuel existant")
        
        return True
    
    def install_dependencies(self):
        """Installe les dépendances Python"""
        print("\n📦 Installation des dépendances...")
        
        # Chemin vers pip dans venv
        if platform.system() == "Windows":
            pip_path = self.current_dir / "venv" / "Scripts" / "pip.exe"
        else:
            pip_path = self.current_dir / "venv" / "bin" / "pip"
        
        if not pip_path.exists():
            print("❌ pip non trouvé dans l'environnement virtuel")
            return False
        
        requirements_file = self.current_dir / "requirements.txt"
        if not requirements_file.exists():
            print("❌ Fichier requirements.txt non trouvé")
            return False
        
        try:
            # Installation des dépendances de base
            basic_deps = [
                'fastapi>=0.104.0',
                'uvicorn>=0.24.0',
                'pydantic>=2.4.0',
                'pydantic-settings>=2.0.0',
                'httpx>=0.25.0',
                'loguru>=0.7.0'
            ]
            
            for dep in basic_deps:
                print(f"📥 Installation {dep}...")
                result = subprocess.run([str(pip_path), 'install', dep], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"⚠️ Attention: {dep} non installé ({result.stderr.strip()})")
                else:
                    print(f"✅ {dep} installé")
            
            print("✅ Dépendances de base installées")
            return True
            
        except Exception as e:
            print(f"❌ Erreur installation: {e}")
            return False
    
    def open_in_cursor(self):
        """Ouvre le projet dans Cursor"""
        print("\n🚀 Ouverture dans Cursor...")
        
        try:
            # Tentative d'ouverture avec cursor
            subprocess.Popen(['cursor', str(self.current_dir)])
            print("✅ Cursor lancé avec le projet")
            return True
        except FileNotFoundError:
            print("❌ Impossible de lancer Cursor automatiquement")
            print(f"💡 Ouvrez manuellement: cursor {self.current_dir}")
            return False
    
    def create_vscode_settings(self):
        """Crée les paramètres compatibles VS Code/Cursor"""
        vscode_dir = self.current_dir / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
        
        # Settings.json pour VS Code/Cursor
        settings = {
            "python.defaultInterpreterPath": "./venv/bin/python",
            "python.terminal.activateEnvironment": True,
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "python.formatting.provider": "black",
            "editor.formatOnSave": True,
            "files.exclude": {
                "**/__pycache__": True,
                "**/venv": True,
                "**/*.pyc": True,
                "**/.git": True
            }
        }
        
        settings_file = vscode_dir / "settings.json"
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        
        print(f"✅ Paramètres VS Code/Cursor créés: {settings_file}")
    
    def run_tests(self):
        """Exécute les tests de validation"""
        print("\n🧪 Tests de validation...")
        
        test_file = self.current_dir / "test_structure.py"
        if not test_file.exists():
            print("❌ Fichier de test non trouvé")
            return False
        
        try:
            # Exécution du test de structure
            if platform.system() == "Windows":
                python_path = self.current_dir / "venv" / "Scripts" / "python.exe"
            else:
                python_path = self.current_dir / "venv" / "bin" / "python"
            
            if python_path.exists():
                result = subprocess.run([str(python_path), str(test_file)], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("✅ Tests de structure réussis")
                    return True
                else:
                    print(f"❌ Tests échoués: {result.stderr}")
                    return False
            else:
                # Fallback avec python système
                result = subprocess.run([sys.executable, str(test_file)], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("✅ Tests de structure réussis")
                    return True
                else:
                    print(f"❌ Tests échoués: {result.stderr}")
                    return False
                    
        except subprocess.TimeoutExpired:
            print("❌ Tests interrompus (timeout)")
            return False
        except Exception as e:
            print(f"❌ Erreur tests: {e}")
            return False
    
    def setup_complete_message(self):
        """Affiche le message de fin de configuration"""
        print("\n" + "🎉" + "="*58 + "🎉")
        print("🎉 CONFIGURATION CURSOR TERMINÉE AVEC SUCCÈS ! 🎉")
        print("="*60)
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. ✅ Cursor est configuré pour votre projet")
        print("2. 🚀 Utilisez F5 pour débugger")
        print("3. 🔧 Ctrl+Shift+P pour accéder aux tâches")
        print("4. 💬 Testez l'IA avec @ pour du contexte projet")
        print("\n📖 COMMANDES RAPIDES:")
        print("• python demo_launcher.py  → Démo interactive")
        print("• python main.py          → Serveur principal")
        print("• python test_structure.py → Tests validation")
        print("\n🎯 GUIDE COMPLET: CURSOR_INTEGRATION.md")
        print("💌 Support: yao.kouakou.dev@gmaii.com")
        print("\n" + "🛡️" + "="*56 + "🛡️" + "\n")
    
    def run(self):
        """Exécute la configuration complète"""
        self.print_banner()
        
        # Vérifications préalables
        if not self.check_project_structure():
            return False
        
        if not self.create_cursor_directories():
            return False
        
        # Configuration environnement
        if not self.setup_python_environment():
            return False
        
        if not self.install_dependencies():
            print("⚠️ Certaines dépendances n'ont pas pu être installées")
            print("💡 Exécutez manuellement: pip install -r requirements.txt")
        
        # Configuration Cursor/VS Code
        self.create_vscode_settings()
        
        # Tests validation
        if not self.run_tests():
            print("⚠️ Tests de validation échoués")
            print("💡 Vérifiez la configuration et réessayez")
        
        # Vérification et lancement Cursor
        if self.check_cursor_installation():
            self.open_in_cursor()
        
        # Message final
        self.setup_complete_message()
        return True

def main():
    """Point d'entrée principal"""
    try:
        setup = CursorSetup()
        success = setup.run()
        
        if success:
            sys.exit(0)
        else:
            print("\n❌ Configuration incomplète")
            print("💡 Consultez CURSOR_INTEGRATION.md pour aide")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Configuration interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
🧪 Testeur Unifié - Système Mondial de Défense Cybernétique
Dossier Complet - Yao Kouakou Luc Anicet
"""

import os
import sys
import subprocess
import time
import json
import requests
from pathlib import Path
from typing import Dict, Any, List

class DossierCompletTester:
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
        self.base_url = "http://localhost:8000"
        self.test_results = []
        
    def print_banner(self):
        """Affiche la bannière du testeur"""
        print("=" * 80)
        print("🧪 TESTEUR UNIFIÉ - SYSTÈME DE DÉFENSE CYBERNÉTIQUE")
        print("📁 DOSSIER COMPLET - VALIDATION COMPLÈTE")
        print("=" * 80)
        print(f"👨‍💻 Développé par: {self.developer_info['name']}")
        print(f"📞 Téléphone: {self.developer_info['phone']}")
        print(f"📧 Email: {self.developer_info['email']}")
        print(f"🔐 Licence: {self.developer_info['license']}")
        print(f"🚀 Version: {self.system_info['version']}")
        print("=" * 80)
        print()
        
    def test_file_structure(self) -> Dict[str, Any]:
        """Teste la structure des fichiers"""
        print("📁 Test de la structure des fichiers...")
        result = {
            "test": "Structure des fichiers",
            "status": "PASS",
            "details": []
        }
        
        required_dirs = [
            "security", "core", "api", "templates", "config",
            "data", "logs", "models", "scripts", "communication"
        ]
        
        required_files = [
            "minimal_start.py", "test_system_live.py", "config.json",
            "requirements.txt", "README_PRINCIPAL.md", "SECURITE_ACCES.md"
        ]
        
        # Vérifier les dossiers
        for dir_name in required_dirs:
            dir_path = self.current_dir / dir_name
            if dir_path.exists():
                result["details"].append(f"✅ Dossier {dir_name} trouvé")
            else:
                result["details"].append(f"❌ Dossier {dir_name} manquant")
                result["status"] = "FAIL"
                
        # Vérifier les fichiers
        for file_name in required_files:
            file_path = self.current_dir / file_name
            if file_path.exists():
                result["details"].append(f"✅ Fichier {file_name} trouvé")
            else:
                result["details"].append(f"❌ Fichier {file_name} manquant")
                result["status"] = "FAIL"
                
        return result
        
    def test_python_environment(self) -> Dict[str, Any]:
        """Teste l'environnement Python"""
        print("🐍 Test de l'environnement Python...")
        result = {
            "test": "Environnement Python",
            "status": "PASS",
            "details": []
        }
        
        # Vérifier Python
        if sys.version_info >= (3, 8):
            result["details"].append(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} compatible")
        else:
            result["details"].append(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} incompatible")
            result["status"] = "FAIL"
            
        # Vérifier l'environnement virtuel
        venv_path = self.current_dir / "cyberdefense_env"
        if venv_path.exists():
            result["details"].append("✅ Environnement virtuel trouvé")
        else:
            result["details"].append("⚠️  Environnement virtuel non trouvé")
            
        return result
        
    def test_dependencies(self) -> Dict[str, Any]:
        """Teste les dépendances"""
        print("📦 Test des dépendances...")
        result = {
            "test": "Dépendances Python",
            "status": "PASS",
            "details": []
        }
        
        required_packages = [
            "fastapi", "uvicorn", "redis", "aiohttp", "requests",
            "jinja2", "plotly", "pandas", "numpy", "cryptography"
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                result["details"].append(f"✅ {package} disponible")
            except ImportError:
                result["details"].append(f"❌ {package} manquant")
                result["status"] = "FAIL"
                
        return result
        
    def test_redis_connection(self) -> Dict[str, Any]:
        """Teste la connexion Redis"""
        print("🔴 Test de la connexion Redis...")
        result = {
            "test": "Connexion Redis",
            "status": "PASS",
            "details": []
        }
        
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            result["details"].append("✅ Redis connecté et opérationnel")
        except Exception as e:
            result["details"].append(f"⚠️  Redis non disponible: {e}")
            result["status"] = "WARNING"
            
        return result
        
    def test_system_endpoints(self) -> Dict[str, Any]:
        """Teste les endpoints du système"""
        print("🌐 Test des endpoints du système...")
        result = {
            "test": "Endpoints du système",
            "status": "PASS",
            "details": []
        }
        
        endpoints = [
            ("/", "Accueil"),
            ("/status", "Statut API"),
            ("/developer", "Informations développeur"),
            ("/license", "Licences"),
            ("/pricing", "Tarification"),
            ("/security", "Sécurité")
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    result["details"].append(f"✅ {name} ({endpoint}) - OK")
                else:
                    result["details"].append(f"⚠️  {name} ({endpoint}) - Status {response.status_code}")
                    result["status"] = "WARNING"
            except requests.exceptions.RequestException as e:
                result["details"].append(f"❌ {name} ({endpoint}) - Erreur: {e}")
                result["status"] = "FAIL"
                
        return result
        
    def test_security_features(self) -> Dict[str, Any]:
        """Teste les fonctionnalités de sécurité"""
        print("🔐 Test des fonctionnalités de sécurité...")
        result = {
            "test": "Fonctionnalités de sécurité",
            "status": "PASS",
            "details": []
        }
        
        # Test du mot de passe
        if self.system_info["password"] == "AZ12ER34":
            result["details"].append("✅ Mot de passe principal configuré")
        else:
            result["details"].append("❌ Mot de passe principal incorrect")
            result["status"] = "FAIL"
            
        # Test des fichiers de sécurité
        security_files = [
            "security/access_protection.py",
            "security/auth_interface.py",
            "SECURITE_ACCES.md"
        ]
        
        for file_path in security_files:
            full_path = self.current_dir / file_path
            if full_path.exists():
                result["details"].append(f"✅ {file_path} trouvé")
            else:
                result["details"].append(f"❌ {file_path} manquant")
                result["status"] = "FAIL"
                
        return result
        
    def test_commercial_features(self) -> Dict[str, Any]:
        """Teste les fonctionnalités commerciales"""
        print("💼 Test des fonctionnalités commerciales...")
        result = {
            "test": "Fonctionnalités commerciales",
            "status": "PASS",
            "details": []
        }
        
        # Test des fichiers commerciaux
        commercial_files = [
            "security/license_system.py",
            "security/payment_system.py",
            "license_manager.py",
            "LICENCE_VENTE_IVOIRIENNE.md",
            "COMMERCIAL_PRICING.md"
        ]
        
        for file_path in commercial_files:
            full_path = self.current_dir / file_path
            if full_path.exists():
                result["details"].append(f"✅ {file_path} trouvé")
            else:
                result["details"].append(f"❌ {file_path} manquant")
                result["status"] = "FAIL"
                
        # Test de la licence ivoirienne
        if self.developer_info["license"] == "CI-CYBER-2024-001":
            result["details"].append("✅ Licence ivoirienne configurée")
        else:
            result["details"].append("❌ Licence ivoirienne incorrecte")
            result["status"] = "FAIL"
            
        return result
        
    def test_developer_info(self) -> Dict[str, Any]:
        """Teste les informations du développeur"""
        print("👨‍💻 Test des informations du développeur...")
        result = {
            "test": "Informations du développeur",
            "status": "PASS",
            "details": []
        }
        
        # Vérifier les informations de contact
        if self.developer_info["name"] == "Yao Kouakou Luc Anicet":
            result["details"].append("✅ Nom du développeur correct")
        else:
            result["details"].append("❌ Nom du développeur incorrect")
            result["status"] = "FAIL"
            
        if self.developer_info["phone"] == "+225 014094507":
            result["details"].append("✅ Téléphone correct")
        else:
            result["details"].append("❌ Téléphone incorrect")
            result["status"] = "FAIL"
            
        if self.developer_info["email"] == "hackerduckman89@gmail.com":
            result["details"].append("✅ Email principal correct")
        else:
            result["details"].append("❌ Email principal incorrect")
            result["status"] = "FAIL"
            
        return result
        
    def run_all_tests(self):
        """Exécute tous les tests"""
        self.print_banner()
        
        print("🧪 DÉMARRAGE DES TESTS COMPLETS")
        print("=" * 60)
        
        # Liste des tests à exécuter
        tests = [
            self.test_file_structure,
            self.test_python_environment,
            self.test_dependencies,
            self.test_redis_connection,
            self.test_system_endpoints,
            self.test_security_features,
            self.test_commercial_features,
            self.test_developer_info
        ]
        
        # Exécuter les tests
        for test_func in tests:
            try:
                result = test_func()
                self.test_results.append(result)
                print(f"\n📊 {result['test']}: {result['status']}")
                for detail in result['details']:
                    print(f"   {detail}")
            except Exception as e:
                error_result = {
                    "test": test_func.__name__,
                    "status": "ERROR",
                    "details": [f"❌ Erreur lors du test: {e}"]
                }
                self.test_results.append(error_result)
                print(f"\n❌ {test_func.__name__}: ERROR")
                print(f"   ❌ Erreur lors du test: {e}")
                
        # Afficher le résumé
        self.show_summary()
        
    def show_summary(self):
        """Affiche le résumé des tests"""
        print("\n" + "=" * 80)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed_tests = sum(1 for r in self.test_results if r["status"] == "FAIL")
        warning_tests = sum(1 for r in self.test_results if r["status"] == "WARNING")
        error_tests = sum(1 for r in self.test_results if r["status"] == "ERROR")
        
        print(f"📈 Total des tests: {total_tests}")
        print(f"✅ Tests réussis: {passed_tests}")
        print(f"⚠️  Tests avec avertissements: {warning_tests}")
        print(f"❌ Tests échoués: {failed_tests}")
        print(f"💥 Tests en erreur: {error_tests}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"📊 Taux de réussite: {success_rate:.1f}%")
        
        print("\n📋 Détail par test:")
        for result in self.test_results:
            status_icon = {
                "PASS": "✅",
                "FAIL": "❌",
                "WARNING": "⚠️",
                "ERROR": "💥"
            }.get(result["status"], "❓")
            
            print(f"{status_icon} {result['test']}: {result['status']}")
            
        print("\n" + "=" * 80)
        
        if failed_tests == 0 and error_tests == 0:
            print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
            print("🚀 Le système est prêt pour la production !")
        elif failed_tests == 0:
            print("⚠️  Tests terminés avec des avertissements")
            print("🔧 Vérifiez les détails ci-dessus")
        else:
            print("❌ Certains tests ont échoué")
            print("🔧 Corrigez les problèmes avant la production")
            
        print("=" * 80)
        
        # Informations de contact
        print(f"\n📞 Support:")
        print(f"   • Développeur: {self.developer_info['name']}")
        print(f"   • Téléphone: {self.developer_info['phone']}")
        print(f"   • Email: {self.developer_info['email']}")
        print(f"   • Licence: {self.developer_info['license']}")

def main():
    """Fonction principale"""
    tester = DossierCompletTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
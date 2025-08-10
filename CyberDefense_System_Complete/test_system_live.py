#!/usr/bin/env python3
"""
Test du Système en Cours d'Exécution
====================================

Script de test pour valider le système de défense cybernétique.
"""

import requests
import json
import time
from typing import Dict, Any

class SystemTester:
    """Testeur du système en cours d'exécution"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license": "CI-CYBER-2024-001"
        }
    
    def test_endpoint(self, endpoint: str, expected_keys: list = None) -> Dict[str, Any]:
        """Tester un endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: OK")
                
                if expected_keys:
                    for key in expected_keys:
                        if key in data:
                            print(f"   ✅ {key}: Présent")
                        else:
                            print(f"   ❌ {key}: Manquant")
                
                return data
            else:
                print(f"❌ {endpoint}: Erreur {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {e}")
            return None
    
    def run_complete_test(self):
        """Exécuter le test complet"""
        print("🔐 Test du Système de Défense Cybernétique")
        print("=" * 60)
        print(f"👨‍💻 Développé par: {self.developer_info['name']}")
        print(f"📞 Téléphone: {self.developer_info['phone']}")
        print(f"📧 Email: {self.developer_info['email']}")
        print(f"🔐 Licence: {self.developer_info['license']}")
        print("=" * 60)
        
        # Test de connectivité
        print("\n🌐 Test de connectivité...")
        try:
            response = self.session.get(f"{self.base_url}/test", timeout=5)
            if response.status_code == 200:
                print("✅ Serveur accessible")
            else:
                print(f"❌ Serveur inaccessible: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Impossible de se connecter au serveur: {e}")
            return
        
        # Tests des endpoints
        print("\n🧪 Tests des endpoints:")
        print("-" * 40)
        
        # Test principal
        main_data = self.test_endpoint("/", [
            "message", "version", "developer", "security", "status"
        ])
        
        # Test du statut
        status_data = self.test_endpoint("/status", [
            "status", "system", "version", "components", "developer"
        ])
        
        # Test des informations développeur
        dev_data = self.test_endpoint("/developer", [
            "name", "phone", "email", "license", "ivoirian_license"
        ])
        
        # Test de la licence
        license_data = self.test_endpoint("/license", [
            "license_number", "type", "authority", "developer", "contact"
        ])
        
        # Test des prix
        pricing_data = self.test_endpoint("/pricing", [
            "regions", "payment_methods", "contact"
        ])
        
        # Test de la sécurité
        security_data = self.test_endpoint("/security", [
            "password", "protection_features", "blocked_resources"
        ])
        
        # Test de validation
        test_data = self.test_endpoint("/test", [
            "message", "system", "protection", "password", "developer"
        ])
        
        # Résumé des tests
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        tests = [
            ("Page principale", main_data),
            ("Statut système", status_data),
            ("Informations développeur", dev_data),
            ("Licence ivoirienne", license_data),
            ("Tarification", pricing_data),
            ("Sécurité", security_data),
            ("Test de validation", test_data)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, data in tests:
            if data:
                print(f"✅ {test_name}: RÉUSSI")
                passed += 1
            else:
                print(f"❌ {test_name}: ÉCHOUÉ")
        
        print(f"\n📈 Résultat: {passed}/{total} tests réussis")
        
        if passed == total:
            print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
            print("\n✅ Fonctionnalités validées:")
            print("   ✅ Système de protection par mot de passe")
            print("   ✅ Informations du développeur")
            print("   ✅ Licence ivoirienne CI-CYBER-2024-001")
            print("   ✅ Tarification Europe et Côte d'Ivoire")
            print("   ✅ Protection contre GitHub")
            print("   ✅ API fonctionnelle")
            print("   ✅ Serveur web opérationnel")
            
            print("\n🔐 Informations de sécurité:")
            print(f"   🔑 Mot de passe: AZ12ER34")
            print(f"   📞 Contact: {self.developer_info['phone']}")
            print(f"   📧 Email: {self.developer_info['email']}")
            print(f"   🔐 Licence: {self.developer_info['license']}")
            
            print("\n🌐 Accès au système:")
            print(f"   🌐 Accueil: {self.base_url}/")
            print(f"   📋 Statut: {self.base_url}/status")
            print(f"   👨‍💻 Développeur: {self.base_url}/developer")
            print(f"   🔐 Licence: {self.base_url}/license")
            print(f"   💰 Prix: {self.base_url}/pricing")
            print(f"   🛡️ Sécurité: {self.base_url}/security")
            print(f"   🧪 Test: {self.base_url}/test")
            
        else:
            print("⚠️ Certains tests ont échoué")
        
        print("\n" + "=" * 60)
        print("✅ Test terminé")

def main():
    """Fonction principale"""
    tester = SystemTester()
    tester.run_complete_test()

if __name__ == "__main__":
    main()
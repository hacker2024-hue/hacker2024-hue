#!/usr/bin/env python3
"""
Script de Test du Système de Défense Cybernétique
=================================================

Ce script permet de tester et valider le fonctionnement du système
de détection et protection contre les cyberattaques.
"""

import asyncio
import json
import time
import requests
import websockets
import logging
from datetime import datetime
from typing import Dict, Any, List
import sys
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CyberDefenseTester:
    """Testeur du système de défense cybernétique"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.websocket_url = base_url.replace("http", "ws") + "/ws"
        self.test_results = []
        
    async def run_all_tests(self):
        """Exécution de tous les tests"""
        logger.info("🧪 Démarrage des tests du système de défense cybernétique")
        
        # Tests de connectivité
        await self.test_connectivity()
        
        # Tests de l'API REST
        await self.test_rest_api()
        
        # Tests WebSocket
        await self.test_websocket()
        
        # Tests de simulation de menaces
        await self.test_threat_simulation()
        
        # Tests de performance
        await self.test_performance()
        
        # Affichage des résultats
        self.print_results()
    
    async def test_connectivity(self):
        """Test de connectivité"""
        logger.info("🔗 Test de connectivité...")
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.add_result("Connectivité API", "SUCCESS", "API accessible")
            else:
                self.add_result("Connectivité API", "FAILED", f"Code: {response.status_code}")
        except Exception as e:
            self.add_result("Connectivité API", "FAILED", str(e))
        
        try:
            response = requests.get(f"{self.base_url}/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "unknown")
                self.add_result("Statut Système", "SUCCESS", f"Status: {status}")
            else:
                self.add_result("Statut Système", "FAILED", f"Code: {response.status_code}")
        except Exception as e:
            self.add_result("Statut Système", "FAILED", str(e))
    
    async def test_rest_api(self):
        """Test de l'API REST"""
        logger.info("🔌 Test de l'API REST...")
        
        endpoints = [
            ("/threats", "GET"),
            ("/threats/statistics", "GET"),
            ("/incidents", "GET"),
            ("/protection/status", "GET"),
            ("/network/statistics", "GET"),
            ("/network/flows", "GET"),
            ("/network/anomalies", "GET"),
            ("/alerts", "GET"),
            ("/metrics", "GET")
        ]
        
        for endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                
                if response.status_code == 200:
                    self.add_result(f"API {endpoint}", "SUCCESS", "Endpoint accessible")
                else:
                    self.add_result(f"API {endpoint}", "FAILED", f"Code: {response.status_code}")
            except Exception as e:
                self.add_result(f"API {endpoint}", "FAILED", str(e))
    
    async def test_websocket(self):
        """Test WebSocket"""
        logger.info("📡 Test WebSocket...")
        
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                # Test de connexion
                self.add_result("WebSocket Connexion", "SUCCESS", "Connexion établie")
                
                # Test d'envoi de message
                test_message = {"type": "get_status"}
                await websocket.send(json.dumps(test_message))
                
                # Test de réception
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(response)
                
                if data.get("type") == "system_status":
                    self.add_result("WebSocket Communication", "SUCCESS", "Communication fonctionnelle")
                else:
                    self.add_result("WebSocket Communication", "FAILED", "Réponse inattendue")
                    
        except Exception as e:
            self.add_result("WebSocket", "FAILED", str(e))
    
    async def test_threat_simulation(self):
        """Test de simulation de menaces"""
        logger.info("🚨 Test de simulation de menaces...")
        
        # Test 1: Simulation d'attaque DDoS
        ddos_threat = {
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "source_port": 12345,
            "destination_port": 80,
            "protocol": "tcp",
            "payload_size": 1500,
            "threat_score": 0.9,
            "attack_type": "ddos"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/threats/simulate",
                json=ddos_threat,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.add_result("Simulation DDoS", "SUCCESS", f"Threat ID: {data.get('threat_id')}")
                else:
                    self.add_result("Simulation DDoS", "FAILED", data.get("message", "Échec simulation"))
            else:
                self.add_result("Simulation DDoS", "FAILED", f"Code: {response.status_code}")
        except Exception as e:
            self.add_result("Simulation DDoS", "FAILED", str(e))
        
        # Test 2: Simulation d'attaque APT
        apt_threat = {
            "source_ip": "203.0.113.1",
            "destination_ip": "10.0.0.1",
            "source_port": 12345,
            "destination_port": 22,
            "protocol": "tcp",
            "threat_score": 0.8,
            "attack_type": "apt"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/threats/simulate",
                json=apt_threat,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.add_result("Simulation APT", "SUCCESS", f"Threat ID: {data.get('threat_id')}")
                else:
                    self.add_result("Simulation APT", "FAILED", data.get("message", "Échec simulation"))
            else:
                self.add_result("Simulation APT", "FAILED", f"Code: {response.status_code}")
        except Exception as e:
            self.add_result("Simulation APT", "FAILED", str(e))
        
        # Test 3: Simulation d'attaque Malware
        malware_threat = {
            "source_ip": "198.51.100.1",
            "destination_ip": "10.0.0.1",
            "source_port": 12345,
            "destination_port": 443,
            "protocol": "tcp",
            "threat_score": 0.7,
            "attack_type": "malware"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/threats/simulate",
                json=malware_threat,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.add_result("Simulation Malware", "SUCCESS", f"Threat ID: {data.get('threat_id')}")
                else:
                    self.add_result("Simulation Malware", "FAILED", data.get("message", "Échec simulation"))
            else:
                self.add_result("Simulation Malware", "FAILED", f"Code: {response.status_code}")
        except Exception as e:
            self.add_result("Simulation Malware", "FAILED", str(e))
    
    async def test_performance(self):
        """Test de performance"""
        logger.info("⚡ Test de performance...")
        
        # Test de latence API
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/status", timeout=5)
            latency = (time.time() - start_time) * 1000  # ms
            
            if latency < 100:  # Moins de 100ms
                self.add_result("Latence API", "SUCCESS", f"{latency:.2f}ms")
            elif latency < 500:  # Moins de 500ms
                self.add_result("Latence API", "WARNING", f"{latency:.2f}ms (lent)")
            else:
                self.add_result("Latence API", "FAILED", f"{latency:.2f}ms (trop lent)")
        except Exception as e:
            self.add_result("Latence API", "FAILED", str(e))
        
        # Test de charge (simulation de plusieurs requêtes)
        try:
            start_time = time.time()
            responses = []
            
            for i in range(10):
                response = requests.get(f"{self.base_url}/threats", timeout=5)
                responses.append(response.status_code)
            
            total_time = time.time() - start_time
            success_count = sum(1 for code in responses if code == 200)
            
            if success_count == 10:
                self.add_result("Test de Charge", "SUCCESS", f"10/10 requêtes réussies en {total_time:.2f}s")
            elif success_count >= 8:
                self.add_result("Test de Charge", "WARNING", f"{success_count}/10 requêtes réussies")
            else:
                self.add_result("Test de Charge", "FAILED", f"{success_count}/10 requêtes réussies")
        except Exception as e:
            self.add_result("Test de Charge", "FAILED", str(e))
    
    def add_result(self, test_name: str, status: str, message: str):
        """Ajout d'un résultat de test"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        # Affichage immédiat
        status_icon = {
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "FAILED": "❌"
        }.get(status, "❓")
        
        logger.info(f"{status_icon} {test_name}: {message}")
    
    def print_results(self):
        """Affichage des résultats finaux"""
        print("\n" + "="*80)
        print("📊 RÉSULTATS DES TESTS - SYSTÈME DE DÉFENSE CYBERNÉTIQUE")
        print("="*80)
        
        # Statistiques
        total_tests = len(self.test_results)
        success_count = sum(1 for r in self.test_results if r["status"] == "SUCCESS")
        warning_count = sum(1 for r in self.test_results if r["status"] == "WARNING")
        failed_count = sum(1 for r in self.test_results if r["status"] == "FAILED")
        
        print(f"\n📈 Statistiques:")
        print(f"   Total des tests: {total_tests}")
        print(f"   ✅ Succès: {success_count}")
        print(f"   ⚠️  Avertissements: {warning_count}")
        print(f"   ❌ Échecs: {failed_count}")
        
        # Score de réussite
        success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0
        print(f"   📊 Taux de réussite: {success_rate:.1f}%")
        
        # Résultats détaillés
        print(f"\n📋 Résultats détaillés:")
        print("-" * 80)
        
        for result in self.test_results:
            status_icon = {
                "SUCCESS": "✅",
                "WARNING": "⚠️",
                "FAILED": "❌"
            }.get(result["status"], "❓")
            
            print(f"{status_icon} {result['test']}")
            print(f"   Message: {result['message']}")
            print(f"   Timestamp: {result['timestamp']}")
            print()
        
        # Recommandations
        print("💡 Recommandations:")
        if failed_count == 0 and warning_count == 0:
            print("   🎉 Tous les tests sont passés avec succès!")
            print("   Le système de défense cybernétique fonctionne correctement.")
        elif failed_count == 0:
            print("   ⚠️  Le système fonctionne mais quelques optimisations sont recommandées.")
        else:
            print("   ❌ Des problèmes ont été détectés. Vérifiez la configuration et les logs.")
            print("   Consultez la documentation pour le dépannage.")
        
        print("="*80)

async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test du système de défense cybernétique")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="URL de base du système (défaut: http://localhost:8000)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout en secondes pour les tests (défaut: 30)"
    )
    
    args = parser.parse_args()
    
    # Vérification que le système est accessible
    try:
        response = requests.get(args.url, timeout=5)
        if response.status_code != 200:
            logger.error(f"❌ Le système n'est pas accessible à {args.url}")
            logger.error("Veuillez démarrer le système avec: python launch_cyber_defense.py")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Impossible de se connecter à {args.url}: {e}")
        logger.error("Veuillez démarrer le système avec: python launch_cyber_defense.py")
        sys.exit(1)
    
    # Création et exécution des tests
    tester = CyberDefenseTester(args.url)
    
    try:
        await asyncio.wait_for(tester.run_all_tests(), timeout=args.timeout)
    except asyncio.TimeoutError:
        logger.error(f"⏰ Tests interrompus après {args.timeout} secondes")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("🛑 Tests interrompus par l'utilisateur")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
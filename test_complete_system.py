#!/usr/bin/env python3
"""
Test Complet du Système Mondial de Défense Cybernétique
=======================================================

Script de test complet pour toutes les fonctionnalités du système
développé par Yao Kouakou Luc Anicet.
"""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import aiohttp
import websockets
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteSystemTester:
    """
    Testeur complet du système de défense cybernétique
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.websocket_url = base_url.replace("http", "ws") + "/ws"
        self.session = None
        self.websocket = None
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "contacts": {
                "primary": "hackerduckman89@gmail.com",
                "secondary": "yao.kouakou.dev@gmail.com"
            },
            "version": "2.0.0 - Edition Mondiale"
        }
        
    async def initialize(self):
        """Initialisation du testeur"""
        logger.info("🚀 Initialisation du testeur complet du système")
        logger.info(f"👨‍💻 Développé par: {self.developer_info['name']}")
        logger.info(f"📧 Contact: {self.developer_info['contacts']['primary']}")
        
        # Création de la session HTTP
        self.session = aiohttp.ClientSession()
        
        # Connexion WebSocket
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            logger.info("✅ Connexion WebSocket établie")
        except Exception as e:
            logger.error(f"❌ Erreur connexion WebSocket: {e}")
    
    async def cleanup(self):
        """Nettoyage des ressources"""
        if self.session:
            await self.session.close()
        if self.websocket:
            await self.websocket.close()
    
    async def test_system_status(self):
        """Test du statut du système"""
        logger.info("🔍 Test du statut du système")
        
        try:
            async with self.session.get(f"{self.base_url}/status") as response:
                if response.status == 200:
                    status_data = await response.json()
                    logger.info(f"✅ Statut système: {status_data.get('status', 'N/A')}")
                    logger.info(f"📊 Uptime: {status_data.get('uptime', 'N/A')}")
                    return True
                else:
                    logger.error(f"❌ Erreur statut: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test statut: {e}")
            return False
    
    async def test_developer_info(self):
        """Test des informations du développeur"""
        logger.info("👨‍💻 Test des informations du développeur")
        
        try:
            async with self.session.get(f"{self.base_url}/developer/info") as response:
                if response.status == 200:
                    dev_info = await response.json()
                    logger.info(f"✅ Développeur: {dev_info.get('name', 'N/A')}")
                    logger.info(f"📧 Contact: {dev_info.get('contacts', {}).get('primary', 'N/A')}")
                    logger.info(f"🔄 Version: {dev_info.get('version', 'N/A')}")
                    return True
                else:
                    logger.error(f"❌ Erreur infos développeur: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test infos développeur: {e}")
            return False
    
    async def test_world_map(self):
        """Test de la carte mondiale"""
        logger.info("🌍 Test de la carte mondiale")
        
        try:
            async with self.session.get(f"{self.base_url}/world-map") as response:
                if response.status == 200:
                    html_content = await response.text()
                    if "Yao Kouakou" in html_content and "hackerduckman89@gmail.com" in html_content:
                        logger.info("✅ Carte mondiale générée avec succès")
                        logger.info("📍 Informations du développeur présentes")
                        return True
                    else:
                        logger.warning("⚠️ Carte générée mais informations manquantes")
                        return False
                else:
                    logger.error(f"❌ Erreur carte mondiale: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test carte mondiale: {e}")
            return False
    
    async def test_world_statistics(self):
        """Test des statistiques mondiales"""
        logger.info("📊 Test des statistiques mondiales")
        
        try:
            async with self.session.get(f"{self.base_url}/world-map/statistics") as response:
                if response.status == 200:
                    stats = await response.json()
                    logger.info(f"✅ Menaces totales: {stats.get('total_threats', 0)}")
                    logger.info(f"📈 Risque global: {stats.get('global_risk_level', 'N/A')}")
                    logger.info(f"⚡ Attaques actives: {stats.get('active_attacks', 0)}")
                    return True
                else:
                    logger.error(f"❌ Erreur statistiques: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test statistiques: {e}")
            return False
    
    async def test_ai_models(self):
        """Test des modèles IA"""
        logger.info("🧠 Test des modèles IA")
        
        try:
            async with self.session.get(f"{self.base_url}/ai/models") as response:
                if response.status == 200:
                    models_data = await response.json()
                    logger.info(f"✅ Modèles IA: {models_data.get('total_models', 0)}")
                    logger.info(f"🔮 Prédictions: {models_data.get('total_predictions', 0)}")
                    logger.info(f"📈 Confiance moyenne: {models_data.get('average_confidence', 0):.2f}")
                    return True
                else:
                    logger.error(f"❌ Erreur modèles IA: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test modèles IA: {e}")
            return False
    
    async def test_intelligence_sharing(self):
        """Test du partage d'intelligence"""
        logger.info("🌐 Test du partage d'intelligence")
        
        try:
            async with self.session.get(f"{self.base_url}/intelligence/statistics") as response:
                if response.status == 200:
                    intel_stats = await response.json()
                    logger.info(f"✅ Intelligence totale: {intel_stats.get('total_intelligence', 0)}")
                    logger.info(f"📡 Flux actifs: {intel_stats.get('active_feeds', 0)}")
                    return True
                else:
                    logger.error(f"❌ Erreur intelligence: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test intelligence: {e}")
            return False
    
    async def test_threat_simulation(self):
        """Test de simulation de menaces"""
        logger.info("🎭 Test de simulation de menaces")
        
        # Simulation d'une menace mondiale
        world_threat = {
            "threat_type": "apt_worldwide",
            "source_ip": "203.0.113.45",
            "destination_ip": "192.168.1.100",
            "threat_level": "critical",
            "description": "Attaque APT mondiale simulée pour test",
            "indicators": ["T1055", "T1071", "T1027"],
            "metadata": {
                "simulation": True,
                "developer": self.developer_info["name"],
                "contact": self.developer_info["contacts"]["primary"]
            }
        }
        
        try:
            async with self.session.post(f"{self.base_url}/threats/simulate", 
                                        json=world_threat) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"✅ Simulation menace: {result.get('message', 'N/A')}")
                    return True
                else:
                    logger.error(f"❌ Erreur simulation: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test simulation: {e}")
            return False
    
    async def test_network_monitoring(self):
        """Test de la surveillance réseau"""
        logger.info("📊 Test de la surveillance réseau")
        
        try:
            async with self.session.get(f"{self.base_url}/network/statistics") as response:
                if response.status == 200:
                    network_stats = await response.json()
                    logger.info(f"✅ Paquets capturés: {network_stats.get('packets_captured', 0)}")
                    logger.info(f"📈 Flux analysés: {network_stats.get('flows_analyzed', 0)}")
                    return True
                else:
                    logger.error(f"❌ Erreur statistiques réseau: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test réseau: {e}")
            return False
    
    async def test_protection_system(self):
        """Test du système de protection"""
        logger.info("🛡️ Test du système de protection")
        
        try:
            async with self.session.get(f"{self.base_url}/protection/status") as response:
                if response.status == 200:
                    protection_status = await response.json()
                    logger.info(f"✅ Statut protection: {protection_status.get('status', 'N/A')}")
                    logger.info(f"🔒 IPs bloquées: {protection_status.get('blocked_ips_count', 0)}")
                    return True
                else:
                    logger.error(f"❌ Erreur statut protection: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Erreur test protection: {e}")
            return False
    
    async def test_websocket_notifications(self):
        """Test des notifications WebSocket"""
        logger.info("🔌 Test des notifications WebSocket")
        
        if not self.websocket:
            logger.error("❌ WebSocket non disponible")
            return False
        
        try:
            # Écoute des notifications pendant 10 secondes
            start_time = time.time()
            notification_count = 0
            
            while time.time() - start_time < 10:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    notification_count += 1
                    
                    notification_type = data.get('type', 'unknown')
                    logger.info(f"📡 Notification #{notification_count}: {notification_type}")
                    
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"❌ Erreur réception WebSocket: {e}")
                    break
            
            logger.info(f"✅ {notification_count} notifications reçues")
            return notification_count > 0
        
        except Exception as e:
            logger.error(f"❌ Erreur test WebSocket: {e}")
            return False
    
    async def test_api_endpoints(self):
        """Test de tous les endpoints API"""
        logger.info("🔗 Test de tous les endpoints API")
        
        endpoints = [
            ("/", "Dashboard principal"),
            ("/status", "Statut système"),
            ("/threats", "Menaces actives"),
            ("/incidents", "Incidents"),
            ("/network/statistics", "Statistiques réseau"),
            ("/network/flows", "Flux réseau"),
            ("/network/anomalies", "Anomalies réseau"),
            ("/ai/models", "Modèles IA"),
            ("/ai/predictions", "Prédictions IA"),
            ("/intelligence/search", "Recherche intelligence"),
            ("/intelligence/statistics", "Statistiques intelligence"),
            ("/intelligence/history", "Historique intelligence"),
            ("/world-map/statistics", "Statistiques mondiales"),
            ("/world-map/threats", "Menaces mondiales"),
            ("/developer/info", "Infos développeur"),
            ("/alerts", "Alertes"),
            ("/metrics", "Métriques")
        ]
        
        results = {}
        
        for endpoint, description in endpoints:
            try:
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    if response.status == 200:
                        logger.info(f"✅ {description}: OK")
                        results[endpoint] = True
                    else:
                        logger.warning(f"⚠️ {description}: {response.status}")
                        results[endpoint] = False
            except Exception as e:
                logger.error(f"❌ {description}: {e}")
                results[endpoint] = False
        
        success_rate = sum(results.values()) / len(results) * 100
        logger.info(f"📊 Taux de succès API: {success_rate:.1f}%")
        
        return success_rate > 80
    
    async def run_complete_test(self):
        """Exécution du test complet"""
        logger.info("🎬 Démarrage du test complet du système")
        logger.info("=" * 60)
        
        test_results = {}
        
        try:
            await self.initialize()
            
            # Attente que le système soit prêt
            logger.info("⏳ Attente que le système soit prêt...")
            await asyncio.sleep(5)
            
            # Tests individuels
            tests = [
                ("Statut Système", self.test_system_status),
                ("Infos Développeur", self.test_developer_info),
                ("Carte Mondiale", self.test_world_map),
                ("Statistiques Mondiales", self.test_world_statistics),
                ("Modèles IA", self.test_ai_models),
                ("Partage Intelligence", self.test_intelligence_sharing),
                ("Simulation Menaces", self.test_threat_simulation),
                ("Surveillance Réseau", self.test_network_monitoring),
                ("Système Protection", self.test_protection_system),
                ("Notifications WebSocket", self.test_websocket_notifications),
                ("Endpoints API", self.test_api_endpoints)
            ]
            
            for test_name, test_func in tests:
                logger.info(f"\n🧪 Test: {test_name}")
                logger.info("-" * 40)
                
                try:
                    result = await test_func()
                    test_results[test_name] = result
                    
                    if result:
                        logger.info(f"✅ {test_name}: SUCCÈS")
                    else:
                        logger.warning(f"⚠️ {test_name}: ÉCHEC")
                
                except Exception as e:
                    logger.error(f"❌ {test_name}: ERREUR - {e}")
                    test_results[test_name] = False
                
                await asyncio.sleep(1)
            
            # Résumé final
            logger.info("\n" + "=" * 60)
            logger.info("📋 RÉSUMÉ DES TESTS")
            logger.info("=" * 60)
            
            successful_tests = sum(test_results.values())
            total_tests = len(test_results)
            success_rate = (successful_tests / total_tests) * 100
            
            for test_name, result in test_results.items():
                status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
                logger.info(f"{test_name}: {status}")
            
            logger.info(f"\n📊 Résultat Global: {successful_tests}/{total_tests} ({success_rate:.1f}%)")
            
            if success_rate >= 90:
                logger.info("🎉 SYSTÈME FONCTIONNEL À 100%")
            elif success_rate >= 80:
                logger.info("✅ SYSTÈME FONCTIONNEL")
            elif success_rate >= 60:
                logger.warning("⚠️ SYSTÈME PARTIELLEMENT FONCTIONNEL")
            else:
                logger.error("❌ SYSTÈME NON FONCTIONNEL")
            
            # Informations de contact
            logger.info("\n" + "=" * 60)
            logger.info("👨‍💻 INFORMATIONS DU DÉVELOPPEUR")
            logger.info("=" * 60)
            logger.info(f"Nom: {self.developer_info['name']}")
            logger.info(f"Contact Principal: {self.developer_info['contacts']['primary']}")
            logger.info(f"Contact Secondaire: {self.developer_info['contacts']['secondary']}")
            logger.info(f"Version: {self.developer_info['version']}")
            
            logger.info("\n🌐 Accès au système:")
            logger.info(f"Dashboard: {self.base_url}")
            logger.info(f"API Docs: {self.base_url}/docs")
            logger.info(f"Carte Monde: {self.base_url}/world-map")
            logger.info(f"WebSocket: {self.websocket_url}")
            
        except Exception as e:
            logger.error(f"❌ Erreur fatale du test: {e}")
        
        finally:
            await self.cleanup()
            logger.info("\n✅ Test complet terminé")

async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test complet du système de défense cybernétique")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="URL du système de défense cybernétique")
    
    args = parser.parse_args()
    
    # Création et exécution du testeur
    tester = CompleteSystemTester(args.url)
    
    try:
        await tester.run_complete_test()
    except KeyboardInterrupt:
        logger.info("🛑 Test interrompu par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    asyncio.run(main())
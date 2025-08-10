#!/usr/bin/env python3
"""
Démonstration des Fonctionnalités Avancées
==========================================

Ce script démontre les nouvelles fonctionnalités avancées du système
de défense cybernétique : IA, partage d'intelligence, etc.
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

class AdvancedFeaturesDemo:
    """
    Démonstration des fonctionnalités avancées
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.websocket_url = base_url.replace("http", "ws") + "/ws"
        self.session = None
        self.websocket = None
        
    async def initialize(self):
        """Initialisation de la démonstration"""
        logger.info("🚀 Initialisation de la démonstration des fonctionnalités avancées")
        
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
    
    async def demo_ai_analysis(self):
        """Démonstration de l'analyse IA"""
        logger.info("🧠 Démonstration de l'analyse IA")
        
        # Test des statistiques des modèles
        try:
            async with self.session.get(f"{self.base_url}/ai/models") as response:
                if response.status == 200:
                    models_data = await response.json()
                    logger.info(f"📊 Modèles IA: {json.dumps(models_data, indent=2)}")
                else:
                    logger.error(f"❌ Erreur récupération modèles: {response.status}")
        except Exception as e:
            logger.error(f"❌ Erreur test modèles IA: {e}")
        
        # Test de l'historique des prédictions
        try:
            async with self.session.get(f"{self.base_url}/ai/predictions") as response:
                if response.status == 200:
                    predictions = await response.json()
                    logger.info(f"🔮 Prédictions IA: {len(predictions)} prédictions trouvées")
                    
                    if predictions:
                        latest_prediction = predictions[-1]
                        logger.info(f"📈 Dernière prédiction: {latest_prediction.get('predicted_category', 'N/A')} "
                                  f"(Confiance: {latest_prediction.get('confidence_score', 0):.2f})")
                else:
                    logger.error(f"❌ Erreur récupération prédictions: {response.status}")
        except Exception as e:
            logger.error(f"❌ Erreur test prédictions IA: {e}")
    
    async def demo_intelligence_sharing(self):
        """Démonstration du partage d'intelligence"""
        logger.info("🌐 Démonstration du partage d'intelligence")
        
        # Test des statistiques d'intelligence
        try:
            async with self.session.get(f"{self.base_url}/intelligence/statistics") as response:
                if response.status == 200:
                    intel_stats = await response.json()
                    logger.info(f"📊 Statistiques intelligence: {json.dumps(intel_stats, indent=2)}")
                else:
                    logger.error(f"❌ Erreur récupération statistiques: {response.status}")
        except Exception as e:
            logger.error(f"❌ Erreur test statistiques intelligence: {e}")
        
        # Test de recherche d'intelligence
        search_queries = ["malware", "phishing", "192.168.1.1", "example.com"]
        
        for query in search_queries:
            try:
                async with self.session.get(f"{self.base_url}/intelligence/search", 
                                          params={"query": query}) as response:
                    if response.status == 200:
                        results = await response.json()
                        logger.info(f"🔍 Recherche '{query}': {len(results)} résultats")
                        
                        if results:
                            first_result = results[0]
                            logger.info(f"   Premier résultat: {first_result.get('value', 'N/A')} "
                                      f"({first_result.get('type', 'N/A')})")
                    else:
                        logger.error(f"❌ Erreur recherche '{query}': {response.status}")
            except Exception as e:
                logger.error(f"❌ Erreur test recherche '{query}': {e}")
        
        # Test de l'historique d'intelligence
        try:
            async with self.session.get(f"{self.base_url}/intelligence/history") as response:
                if response.status == 200:
                    history = await response.json()
                    logger.info(f"📚 Historique intelligence: {len(history)} entrées")
                    
                    if history:
                        # Analyse par type
                        type_counts = {}
                        for entry in history:
                            intel_type = entry.get('type', 'unknown')
                            type_counts[intel_type] = type_counts.get(intel_type, 0) + 1
                        
                        logger.info(f"   Répartition par type: {type_counts}")
                else:
                    logger.error(f"❌ Erreur récupération historique: {response.status}")
        except Exception as e:
            logger.error(f"❌ Erreur test historique intelligence: {e}")
    
    async def demo_websocket_notifications(self):
        """Démonstration des notifications WebSocket"""
        logger.info("🔌 Démonstration des notifications WebSocket")
        
        if not self.websocket:
            logger.error("❌ WebSocket non disponible")
            return
        
        try:
            # Écoute des notifications pendant 30 secondes
            logger.info("👂 Écoute des notifications WebSocket (30 secondes)...")
            
            start_time = time.time()
            notification_count = 0
            
            while time.time() - start_time < 30:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    
                    notification_type = data.get('type', 'unknown')
                    notification_count += 1
                    
                    logger.info(f"📡 Notification #{notification_count}: {notification_type}")
                    
                    # Affichage détaillé selon le type
                    if notification_type == 'ai_prediction':
                        prediction = data.get('prediction', {})
                        logger.info(f"   🧠 Prédiction: {prediction.get('predicted_category', 'N/A')} "
                                  f"(Confiance: {prediction.get('confidence_score', 0):.2f})")
                    
                    elif notification_type == 'threat_intelligence':
                        intelligence = data.get('intelligence', {})
                        logger.info(f"   🌐 Intelligence: {intelligence.get('value', 'N/A')} "
                                  f"({intelligence.get('type', 'N/A')})")
                    
                    elif notification_type == 'threat_detected':
                        threat = data.get('threat', {})
                        logger.info(f"   ⚠️ Menace: {threat.get('threat_type', 'N/A')} "
                                  f"(Niveau: {threat.get('threat_level', 'N/A')})")
                    
                    elif notification_type == 'network_anomaly':
                        anomaly = data.get('anomaly', {})
                        logger.info(f"   📊 Anomalie: {anomaly.get('anomaly_type', 'N/A')} "
                                  f"(Score: {anomaly.get('anomaly_score', 0):.2f})")
                
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"❌ Erreur réception WebSocket: {e}")
                    break
            
            logger.info(f"✅ {notification_count} notifications reçues")
        
        except Exception as e:
            logger.error(f"❌ Erreur démonstration WebSocket: {e}")
    
    async def demo_threat_simulation_advanced(self):
        """Démonstration de simulation de menaces avancées"""
        logger.info("🎭 Démonstration de simulation de menaces avancées")
        
        # Simulation d'une attaque APT sophistiquée
        apt_threat = {
            "threat_type": "apt",
            "source_ip": "203.0.113.45",
            "destination_ip": "192.168.1.100",
            "threat_level": "critical",
            "description": "Attaque APT sophistiquée avec techniques d'évasion avancées",
            "indicators": [
                "T1055: Process Injection",
                "T1071: Application Layer Protocol",
                "T1027: Obfuscated Files or Information",
                "T1036: Masquerading"
            ],
            "payload": {
                "entropy": 7.8,
                "size": 2048576,
                "type": "executable",
                "signatures": ["malware_family_apt_2024"]
            },
            "timeline": {
                "initial_access": "2024-01-15T10:30:00Z",
                "persistence": "2024-01-15T10:35:00Z",
                "privilege_escalation": "2024-01-15T10:40:00Z",
                "lateral_movement": "2024-01-15T11:00:00Z"
            }
        }
        
        try:
            async with self.session.post(f"{self.base_url}/threats/simulate", 
                                        json=apt_threat) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"🎭 Simulation APT: {result.get('message', 'N/A')}")
                else:
                    logger.error(f"❌ Erreur simulation APT: {response.status}")
        except Exception as e:
            logger.error(f"❌ Erreur test simulation APT: {e}")
        
        # Simulation d'un malware polymorphe
        polymorphic_malware = {
            "threat_type": "polymorphic_malware",
            "source_ip": "198.51.100.123",
            "destination_ip": "192.168.1.50",
            "threat_level": "high",
            "description": "Malware polymorphe avec capacités d'auto-modification",
            "indicators": [
                "T1059: Command and Scripting Interpreter",
                "T1027.002: Software Packing",
                "T1055: Process Injection",
                "T1070: Indicator Removal"
            ],
            "payload": {
                "entropy": 8.2,
                "size": 1048576,
                "type": "polymorphic_executable",
                "signatures": ["polymorphic_engine_v2", "obfuscation_layer"]
            },
            "behavior": {
                "self_modification": True,
                "anti_analysis": True,
                "network_communication": True,
                "file_operations": True
            }
        }
        
        try:
            async with self.session.post(f"{self.base_url}/threats/simulate", 
                                        json=polymorphic_malware) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"🎭 Simulation Malware Polymorphe: {result.get('message', 'N/A')}")
                else:
                    logger.error(f"❌ Erreur simulation Malware: {response.status}")
        except Exception as e:
            logger.error(f"❌ Erreur test simulation Malware: {e}")
        
        # Simulation d'une campagne de phishing ciblée
        targeted_phishing = {
            "threat_type": "targeted_phishing",
            "source_ip": "203.0.113.67",
            "destination_ip": "192.168.1.25",
            "threat_level": "medium",
            "description": "Campagne de phishing ciblée contre les employés",
            "indicators": [
                "T1566: Phishing",
                "T1071.003: Web Protocols",
                "T1059.005: Visual Basic",
                "T1204.002: User Execution"
            ],
            "payload": {
                "entropy": 6.5,
                "size": 512000,
                "type": "phishing_kit",
                "signatures": ["phishing_template_2024", "credential_harvester"]
            },
            "targets": [
                "finance@company.com",
                "hr@company.com",
                "admin@company.com"
            ],
            "techniques": [
                "spear_phishing",
                "credential_harvesting",
                "session_hijacking"
            ]
        }
        
        try:
            async with self.session.post(f"{self.base_url}/threats/simulate", 
                                        json=targeted_phishing) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"🎭 Simulation Phishing Ciblé: {result.get('message', 'N/A')}")
                else:
                    logger.error(f"❌ Erreur simulation Phishing: {response.status}")
        except Exception as e:
            logger.error(f"❌ Erreur test simulation Phishing: {e}")
    
    async def demo_performance_analysis(self):
        """Démonstration de l'analyse de performance"""
        logger.info("📈 Démonstration de l'analyse de performance")
        
        # Test de latence des API
        endpoints = [
            "/status",
            "/threats",
            "/incidents",
            "/network/statistics",
            "/ai/models",
            "/intelligence/statistics"
        ]
        
        performance_results = {}
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    end_time = time.time()
                    latency = (end_time - start_time) * 1000  # en millisecondes
                    
                    performance_results[endpoint] = {
                        "latency_ms": round(latency, 2),
                        "status": response.status,
                        "success": response.status == 200
                    }
                    
                    logger.info(f"⏱️ {endpoint}: {latency:.2f}ms (Status: {response.status})")
            except Exception as e:
                logger.error(f"❌ Erreur test performance {endpoint}: {e}")
                performance_results[endpoint] = {
                    "latency_ms": -1,
                    "status": -1,
                    "success": False,
                    "error": str(e)
                }
        
        # Analyse des résultats
        successful_requests = [r for r in performance_results.values() if r["success"]]
        if successful_requests:
            avg_latency = sum(r["latency_ms"] for r in successful_requests) / len(successful_requests)
            max_latency = max(r["latency_ms"] for r in successful_requests)
            min_latency = min(r["latency_ms"] for r in successful_requests)
            
            logger.info(f"📊 Performance moyenne: {avg_latency:.2f}ms")
            logger.info(f"📊 Latence min/max: {min_latency:.2f}ms / {max_latency:.2f}ms")
            logger.info(f"📊 Taux de succès: {len(successful_requests)}/{len(endpoints)} ({len(successful_requests)/len(endpoints)*100:.1f}%)")
        
        return performance_results
    
    async def demo_integration_scenarios(self):
        """Démonstration de scénarios d'intégration"""
        logger.info("🔗 Démonstration de scénarios d'intégration")
        
        # Scénario 1: Détection → IA → Intelligence → Protection
        logger.info("🔄 Scénario 1: Pipeline complet de sécurité")
        
        # 1. Simulation d'une menace
        threat_data = {
            "threat_type": "suspicious_connection",
            "source_ip": "203.0.113.100",
            "destination_ip": "192.168.1.10",
            "threat_level": "medium",
            "description": "Connexion suspecte détectée"
        }
        
        try:
            # Simulation de la menace
            async with self.session.post(f"{self.base_url}/threats/simulate", 
                                        json=threat_data) as response:
                if response.status == 200:
                    logger.info("✅ 1. Menace simulée avec succès")
                    
                    # 2. Vérification de la détection
                    await asyncio.sleep(2)
                    async with self.session.get(f"{self.base_url}/threats") as response:
                        if response.status == 200:
                            threats = await response.json()
                            if threats:
                                logger.info(f"✅ 2. Menace détectée: {len(threats)} menaces actives")
                            else:
                                logger.warning("⚠️ 2. Aucune menace détectée")
                        else:
                            logger.error(f"❌ 2. Erreur récupération menaces: {response.status}")
                    
                    # 3. Vérification de l'analyse IA
                    await asyncio.sleep(2)
                    async with self.session.get(f"{self.base_url}/ai/predictions") as response:
                        if response.status == 200:
                            predictions = await response.json()
                            if predictions:
                                logger.info(f"✅ 3. Analyse IA: {len(predictions)} prédictions générées")
                            else:
                                logger.warning("⚠️ 3. Aucune prédiction IA générée")
                        else:
                            logger.error(f"❌ 3. Erreur récupération prédictions: {response.status}")
                    
                    # 4. Vérification de l'intelligence
                    await asyncio.sleep(2)
                    async with self.session.get(f"{self.base_url}/intelligence/search", 
                                              params={"query": "203.0.113.100"}) as response:
                        if response.status == 200:
                            intelligence = await response.json()
                            logger.info(f"✅ 4. Intelligence: {len(intelligence)} résultats trouvés")
                        else:
                            logger.error(f"❌ 4. Erreur recherche intelligence: {response.status}")
                    
                    # 5. Vérification de la protection
                    await asyncio.sleep(2)
                    async with self.session.get(f"{self.base_url}/protection/status") as response:
                        if response.status == 200:
                            protection_status = await response.json()
                            logger.info(f"✅ 5. Protection: {protection_status.get('status', 'N/A')}")
                        else:
                            logger.error(f"❌ 5. Erreur statut protection: {response.status}")
                
                else:
                    logger.error(f"❌ 1. Erreur simulation menace: {response.status}")
        
        except Exception as e:
            logger.error(f"❌ Erreur scénario d'intégration: {e}")
    
    async def run_complete_demo(self):
        """Exécution de la démonstration complète"""
        logger.info("🎬 Démarrage de la démonstration complète des fonctionnalités avancées")
        
        try:
            await self.initialize()
            
            # Attente que le système soit prêt
            logger.info("⏳ Attente que le système soit prêt...")
            await asyncio.sleep(5)
            
            # Démonstrations
            await self.demo_ai_analysis()
            await asyncio.sleep(2)
            
            await self.demo_intelligence_sharing()
            await asyncio.sleep(2)
            
            await self.demo_threat_simulation_advanced()
            await asyncio.sleep(2)
            
            await self.demo_performance_analysis()
            await asyncio.sleep(2)
            
            await self.demo_integration_scenarios()
            await asyncio.sleep(2)
            
            # Démonstration WebSocket en parallèle
            logger.info("🔌 Démarrage de l'écoute WebSocket...")
            await self.demo_websocket_notifications()
            
            logger.info("✅ Démonstration complète terminée avec succès")
        
        except Exception as e:
            logger.error(f"❌ Erreur démonstration: {e}")
        
        finally:
            await self.cleanup()

async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Démonstration des fonctionnalités avancées")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="URL du système de défense cybernétique")
    parser.add_argument("--timeout", type=int, default=30,
                       help="Timeout pour les tests (secondes)")
    
    args = parser.parse_args()
    
    # Création et exécution de la démonstration
    demo = AdvancedFeaturesDemo(args.url)
    
    try:
        await demo.run_complete_demo()
    except KeyboardInterrupt:
        logger.info("🛑 Démonstration interrompue par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    asyncio.run(main())
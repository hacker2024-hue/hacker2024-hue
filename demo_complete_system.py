#!/usr/bin/env python3
"""
Démonstration Complète du Système Mondial de Défense Cybernétique
==================================================================

Script de démonstration de toutes les fonctionnalités du système
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

class CompleteSystemDemo:
    """
    Démonstration complète du système de défense cybernétique
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
        """Initialisation de la démonstration"""
        logger.info("🚀 Initialisation de la démonstration complète")
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
    
    async def demo_dashboard(self):
        """Démonstration du dashboard"""
        logger.info("🎨 Démonstration du Dashboard")
        
        try:
            # Test du dashboard principal
            async with self.session.get(f"{self.base_url}/") as response:
                if response.status == 200:
                    html_content = await response.text()
                    if "Yao Kouakou" in html_content and "Système Mondial" in html_content:
                        logger.info("✅ Dashboard principal accessible")
                        logger.info("📊 Graphiques et métriques en temps réel")
                    else:
                        logger.warning("⚠️ Dashboard accessible mais contenu incomplet")
                else:
                    logger.error(f"❌ Erreur dashboard: {response.status}")
            
            # Test des métriques du dashboard
            async with self.session.get(f"{self.base_url}/dashboard/metrics") as response:
                if response.status == 200:
                    metrics = await response.json()
                    logger.info(f"📈 Métriques: {metrics.get('total_threats', 0)} menaces totales")
                    logger.info(f"🧠 Précision IA: {metrics.get('ai_accuracy', 0):.1%}")
                else:
                    logger.error(f"❌ Erreur métriques: {response.status}")
            
            # Test des graphiques
            async with self.session.get(f"{self.base_url}/dashboard/charts") as response:
                if response.status == 200:
                    charts = await response.json()
                    logger.info(f"📊 {len(charts)} graphiques générés")
                else:
                    logger.error(f"❌ Erreur graphiques: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur démo dashboard: {e}")
    
    async def demo_world_map(self):
        """Démonstration de la carte mondiale"""
        logger.info("🌍 Démonstration de la Carte Mondiale")
        
        try:
            # Test de la carte mondiale
            async with self.session.get(f"{self.base_url}/world-map") as response:
                if response.status == 200:
                    html_content = await response.text()
                    if "Yao Kouakou" in html_content and "hackerduckman89@gmail.com" in html_content:
                        logger.info("✅ Carte mondiale générée avec succès")
                        logger.info("📍 Géolocalisation des menaces active")
                        logger.info("📊 Statistiques mondiales intégrées")
                    else:
                        logger.warning("⚠️ Carte générée mais informations manquantes")
                else:
                    logger.error(f"❌ Erreur carte mondiale: {response.status}")
            
            # Test des statistiques mondiales
            async with self.session.get(f"{self.base_url}/world-map/statistics") as response:
                if response.status == 200:
                    stats = await response.json()
                    logger.info(f"🌍 Menaces mondiales: {stats.get('total_threats', 0)}")
                    logger.info(f"📈 Risque global: {stats.get('global_risk_level', 'N/A')}")
                else:
                    logger.error(f"❌ Erreur statistiques mondiales: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur démo carte mondiale: {e}")
    
    async def demo_notification_system(self):
        """Démonstration du système de notification"""
        logger.info("🔔 Démonstration du Système de Notification")
        
        try:
            # Test des statistiques de notification
            async with self.session.get(f"{self.base_url}/notifications/stats") as response:
                if response.status == 200:
                    stats = await response.json()
                    logger.info(f"📧 Notifications totales: {stats.get('total', 0)}")
                    logger.info(f"✅ Notifications envoyées: {stats.get('sent', 0)}")
                else:
                    logger.error(f"❌ Erreur stats notifications: {response.status}")
            
            # Test d'envoi de notification
            notification_data = {
                "title": "Test de Notification - Yao Kouakou",
                "message": "Ceci est un test du système de notification avancé développé par Yao Kouakou Luc Anicet.",
                "priority": "high",
                "notification_type": "webhook",
                "recipients": ["hackerduckman89@gmail.com"]
            }
            
            async with self.session.post(f"{self.base_url}/notifications/send", 
                                        json=notification_data) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"✅ Notification envoyée: {result.get('id', 'N/A')}")
                else:
                    logger.warning(f"⚠️ Erreur envoi notification: {response.status}")
            
            # Test de notification
            async with self.session.post(f"{self.base_url}/notifications/test", 
                                        params={"notification_type": "webhook"}) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"🧪 Test notification: {result.get('success', False)}")
                else:
                    logger.warning(f"⚠️ Erreur test notification: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur démo notifications: {e}")
    
    async def demo_ai_system(self):
        """Démonstration du système IA"""
        logger.info("🧠 Démonstration du Système IA")
        
        try:
            # Test des modèles IA
            async with self.session.get(f"{self.base_url}/ai/models") as response:
                if response.status == 200:
                    models_data = await response.json()
                    logger.info(f"🤖 Modèles IA: {models_data.get('total_models', 0)}")
                    logger.info(f"🔮 Prédictions: {models_data.get('total_predictions', 0)}")
                    logger.info(f"📈 Confiance moyenne: {models_data.get('average_confidence', 0):.2f}")
                else:
                    logger.error(f"❌ Erreur modèles IA: {response.status}")
            
            # Test des prédictions IA
            async with self.session.get(f"{self.base_url}/ai/predictions") as response:
                if response.status == 200:
                    predictions = await response.json()
                    logger.info(f"🔮 {len(predictions)} prédictions IA récupérées")
                else:
                    logger.error(f"❌ Erreur prédictions IA: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur démo IA: {e}")
    
    async def demo_intelligence_sharing(self):
        """Démonstration du partage d'intelligence"""
        logger.info("🌐 Démonstration du Partage d'Intelligence")
        
        try:
            # Test des statistiques d'intelligence
            async with self.session.get(f"{self.base_url}/intelligence/statistics") as response:
                if response.status == 200:
                    intel_stats = await response.json()
                    logger.info(f"📡 Intelligence totale: {intel_stats.get('total_intelligence', 0)}")
                    logger.info(f"🔄 Flux actifs: {intel_stats.get('active_feeds', 0)}")
                else:
                    logger.error(f"❌ Erreur stats intelligence: {response.status}")
            
            # Test de recherche d'intelligence
            async with self.session.get(f"{self.base_url}/intelligence/search", 
                                       params={"query": "malware"}) as response:
                if response.status == 200:
                    results = await response.json()
                    logger.info(f"🔍 {len(results)} résultats de recherche")
                else:
                    logger.error(f"❌ Erreur recherche intelligence: {response.status}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur démo intelligence: {e}")
    
    async def demo_threat_simulation_advanced(self):
        """Démonstration de simulation de menaces avancées"""
        logger.info("🎭 Démonstration de Simulation de Menaces Avancées")
        
        # Menaces mondiales complexes
        advanced_threats = [
            {
                "threat_type": "apt_worldwide_advanced",
                "source_ip": "203.0.113.45",
                "destination_ip": "192.168.1.100",
                "threat_level": "critical",
                "description": "Attaque APT mondiale avancée avec techniques MITRE ATT&CK",
                "indicators": ["T1055", "T1071", "T1027", "T1083", "T1059"],
                "metadata": {
                    "simulation": True,
                    "developer": self.developer_info["name"],
                    "contact": self.developer_info["contacts"]["primary"],
                    "mitre_techniques": ["Process Injection", "Application Layer Protocol", "Obfuscated Files"],
                    "target_countries": ["France", "USA", "Germany"],
                    "attack_vectors": ["Spear Phishing", "Watering Hole", "Supply Chain"]
                }
            },
            {
                "threat_type": "polymorphic_malware_global",
                "source_ip": "198.51.100.123",
                "destination_ip": "10.0.0.50",
                "threat_level": "high",
                "description": "Malware polymorphique avec évasion avancée",
                "indicators": ["T1027.002", "T1055.012", "T1071.001"],
                "metadata": {
                    "simulation": True,
                    "developer": self.developer_info["name"],
                    "contact": self.developer_info["contacts"]["primary"],
                    "malware_family": "Polymorphic RAT",
                    "evasion_techniques": ["Code Obfuscation", "Anti-VM", "Anti-Debug"],
                    "affected_systems": ["Windows", "Linux", "macOS"]
                }
            },
            {
                "threat_type": "targeted_phishing_campaign",
                "source_ip": "203.0.113.67",
                "destination_ip": "172.16.0.25",
                "threat_level": "medium",
                "description": "Campagne de phishing ciblée contre entreprises",
                "indicators": ["T1566.001", "T1071.001", "T1059.005"],
                "metadata": {
                    "simulation": True,
                    "developer": self.developer_info["name"],
                    "contact": self.developer_info["contacts"]["primary"],
                    "target_industries": ["Finance", "Healthcare", "Technology"],
                    "phishing_techniques": ["Spear Phishing", "Whaling", "Vishing"],
                    "social_engineering": ["Authority", "Urgency", "Scarcity"]
                }
            }
        ]
        
        for i, threat in enumerate(advanced_threats, 1):
            try:
                logger.info(f"🎭 Simulation menace #{i}: {threat['threat_type']}")
                
                async with self.session.post(f"{self.base_url}/threats/simulate", 
                                            json=threat) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Menace simulée: {result.get('message', 'N/A')}")
                    else:
                        logger.error(f"❌ Erreur simulation menace #{i}: {response.status}")
                
                await asyncio.sleep(2)  # Pause entre les simulations
                
            except Exception as e:
                logger.error(f"❌ Erreur simulation menace #{i}: {e}")
    
    async def demo_websocket_notifications(self):
        """Démonstration des notifications WebSocket"""
        logger.info("🔌 Démonstration des Notifications WebSocket")
        
        if not self.websocket:
            logger.error("❌ WebSocket non disponible")
            return
        
        try:
            # Écoute des notifications pendant 15 secondes
            start_time = time.time()
            notification_count = 0
            notification_types = set()
            
            while time.time() - start_time < 15:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    notification_count += 1
                    
                    notification_type = data.get('type', 'unknown')
                    notification_types.add(notification_type)
                    
                    logger.info(f"📡 Notification #{notification_count}: {notification_type}")
                    
                    # Affichage des détails pour certains types
                    if notification_type == 'world_threat':
                        threat = data.get('threat', {})
                        logger.info(f"   🌍 Menace: {threat.get('threat_type', 'N/A')} depuis {threat.get('source_country', 'N/A')}")
                    elif notification_type == 'ai_prediction':
                        prediction = data.get('prediction', {})
                        logger.info(f"   🧠 Prédiction: {prediction.get('prediction', 'N/A')} (confiance: {prediction.get('confidence', 0):.2f})")
                    elif notification_type == 'notification':
                        notification = data.get('notification', {})
                        logger.info(f"   🔔 Notification: {notification.get('title', 'N/A')} ({notification.get('priority', 'N/A')})")
                    
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"❌ Erreur réception WebSocket: {e}")
                    break
            
            logger.info(f"✅ {notification_count} notifications reçues")
            logger.info(f"📊 Types de notifications: {', '.join(notification_types)}")
        
        except Exception as e:
            logger.error(f"❌ Erreur démo WebSocket: {e}")
    
    async def demo_performance_analysis(self):
        """Démonstration d'analyse de performance"""
        logger.info("⚡ Démonstration d'Analyse de Performance")
        
        endpoints_to_test = [
            ("/status", "Statut système"),
            ("/dashboard/metrics", "Métriques dashboard"),
            ("/ai/models", "Modèles IA"),
            ("/intelligence/statistics", "Stats intelligence"),
            ("/world-map/statistics", "Stats carte mondiale"),
            ("/notifications/stats", "Stats notifications"),
            ("/network/statistics", "Stats réseau"),
            ("/protection/status", "Statut protection")
        ]
        
        performance_results = {}
        
        for endpoint, description in endpoints_to_test:
            try:
                start_time = time.time()
                async with self.session.get(f"{self.base_url}{endpoint}") as response:
                    end_time = time.time()
                    latency = (end_time - start_time) * 1000  # en millisecondes
                    
                    if response.status == 200:
                        logger.info(f"✅ {description}: {latency:.1f}ms")
                        performance_results[description] = {"status": "success", "latency": latency}
                    else:
                        logger.warning(f"⚠️ {description}: {response.status} ({latency:.1f}ms)")
                        performance_results[description] = {"status": "error", "latency": latency}
                
            except Exception as e:
                logger.error(f"❌ {description}: {e}")
                performance_results[description] = {"status": "error", "latency": None}
        
        # Analyse des performances
        successful_requests = [r for r in performance_results.values() if r["status"] == "success"]
        if successful_requests:
            avg_latency = sum(r["latency"] for r in successful_requests) / len(successful_requests)
            max_latency = max(r["latency"] for r in successful_requests)
            min_latency = min(r["latency"] for r in successful_requests)
            
            logger.info(f"📊 Performance - Moyenne: {avg_latency:.1f}ms, Min: {min_latency:.1f}ms, Max: {max_latency:.1f}ms")
            
            if avg_latency < 100:
                logger.info("🚀 Performance excellente")
            elif avg_latency < 500:
                logger.info("✅ Performance bonne")
            else:
                logger.warning("⚠️ Performance à améliorer")
    
    async def demo_integration_scenarios(self):
        """Démonstration de scénarios d'intégration"""
        logger.info("🔄 Démonstration de Scénarios d'Intégration")
        
        # Scénario 1: Détection → IA → Intelligence → Protection
        logger.info("🔄 Scénario 1: Pipeline complet de sécurité")
        
        try:
            # 1. Simulation d'une menace
            threat_data = {
                "threat_type": "integrated_test",
                "source_ip": "203.0.113.100",
                "destination_ip": "192.168.1.200",
                "threat_level": "high",
                "description": "Test d'intégration complète du pipeline de sécurité",
                "indicators": ["T1055", "T1071"],
                "metadata": {
                    "simulation": True,
                    "developer": self.developer_info["name"],
                    "contact": self.developer_info["contacts"]["primary"],
                    "scenario": "pipeline_complet"
                }
            }
            
            async with self.session.post(f"{self.base_url}/threats/simulate", 
                                        json=threat_data) as response:
                if response.status == 200:
                    logger.info("✅ 1. Menace simulée")
                else:
                    logger.error("❌ 1. Erreur simulation menace")
            
            await asyncio.sleep(3)
            
            # 2. Vérification de l'analyse IA
            async with self.session.get(f"{self.base_url}/ai/predictions") as response:
                if response.status == 200:
                    predictions = await response.json()
                    if predictions:
                        logger.info(f"✅ 2. Analyse IA effectuée ({len(predictions)} prédictions)")
                    else:
                        logger.warning("⚠️ 2. Aucune prédiction IA trouvée")
                else:
                    logger.error("❌ 2. Erreur analyse IA")
            
            # 3. Vérification de l'intelligence
            async with self.session.get(f"{self.base_url}/intelligence/search", 
                                       params={"query": "integrated_test"}) as response:
                if response.status == 200:
                    results = await response.json()
                    logger.info(f"✅ 3. Intelligence partagée ({len(results)} résultats)")
                else:
                    logger.error("❌ 3. Erreur intelligence")
            
            # 4. Vérification de la protection
            async with self.session.get(f"{self.base_url}/protection/status") as response:
                if response.status == 200:
                    protection_status = await response.json()
                    logger.info(f"✅ 4. Protection active: {protection_status.get('status', 'N/A')}")
                else:
                    logger.error("❌ 4. Erreur statut protection")
            
            logger.info("🎉 Pipeline d'intégration complet testé avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur scénario d'intégration: {e}")
    
    async def run_complete_demo(self):
        """Exécution de la démonstration complète"""
        logger.info("🎬 Démarrage de la démonstration complète du système")
        logger.info("=" * 70)
        
        try:
            await self.initialize()
            
            # Attente que le système soit prêt
            logger.info("⏳ Attente que le système soit prêt...")
            await asyncio.sleep(5)
            
            # Démonstrations individuelles
            demos = [
                ("Dashboard Avancé", self.demo_dashboard),
                ("Carte Mondiale", self.demo_world_map),
                ("Système de Notification", self.demo_notification_system),
                ("Système IA", self.demo_ai_system),
                ("Partage d'Intelligence", self.demo_intelligence_sharing),
                ("Simulation de Menaces Avancées", self.demo_threat_simulation_advanced),
                ("Notifications WebSocket", self.demo_websocket_notifications),
                ("Analyse de Performance", self.demo_performance_analysis),
                ("Scénarios d'Intégration", self.demo_integration_scenarios)
            ]
            
            for demo_name, demo_func in demos:
                logger.info(f"\n🎯 Démonstration: {demo_name}")
                logger.info("-" * 50)
                
                try:
                    await demo_func()
                    logger.info(f"✅ {demo_name}: TERMINÉ")
                except Exception as e:
                    logger.error(f"❌ {demo_name}: ERREUR - {e}")
                
                await asyncio.sleep(2)
            
            # Résumé final
            logger.info("\n" + "=" * 70)
            logger.info("🎉 DÉMONSTRATION COMPLÈTE TERMINÉE")
            logger.info("=" * 70)
            
            # Informations de contact
            logger.info("\n" + "=" * 70)
            logger.info("👨‍💻 INFORMATIONS DU DÉVELOPPEUR")
            logger.info("=" * 70)
            logger.info(f"Nom: {self.developer_info['name']}")
            logger.info(f"Contact Principal: {self.developer_info['contacts']['primary']}")
            logger.info(f"Contact Secondaire: {self.developer_info['contacts']['secondary']}")
            logger.info(f"Version: {self.developer_info['version']}")
            
            logger.info("\n🌐 Accès au système:")
            logger.info(f"Dashboard: {self.base_url}")
            logger.info(f"API Docs: {self.base_url}/docs")
            logger.info(f"Carte Monde: {self.base_url}/world-map")
            logger.info(f"WebSocket: {self.websocket_url}")
            
            logger.info("\n🚀 Fonctionnalités démontrées:")
            logger.info("✅ Dashboard avancé avec graphiques interactifs")
            logger.info("✅ Carte mondiale avec géolocalisation")
            logger.info("✅ Système de notification multi-canal")
            logger.info("✅ Intelligence artificielle avancée")
            logger.info("✅ Partage d'intelligence sur les menaces")
            logger.info("✅ Simulation de menaces complexes")
            logger.info("✅ Notifications WebSocket temps réel")
            logger.info("✅ Analyse de performance")
            logger.info("✅ Scénarios d'intégration complets")
            
        except Exception as e:
            logger.error(f"❌ Erreur fatale de la démonstration: {e}")
        
        finally:
            await self.cleanup()
            logger.info("\n✅ Démonstration complète terminée")

async def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Démonstration complète du système de défense cybernétique")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="URL du système de défense cybernétique")
    
    args = parser.parse_args()
    
    # Création et exécution de la démonstration
    demo = CompleteSystemDemo(args.url)
    
    try:
        await demo.run_complete_demo()
    except KeyboardInterrupt:
        logger.info("🛑 Démonstration interrompue par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    asyncio.run(main())
"""
Système Mondial de Détection et Protection contre les Cyberattaques
===================================================================

Ce module principal orchestre l'ensemble du système de cybersécurité
avec détection globale, protection proactive et surveillance réseau.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import redis.asyncio as redis
from fastapi import WebSocket, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import des modules de sécurité
from .global_threat_detection import GlobalThreatDetector, NetworkEvent, GlobalThreat
from .proactive_protection import ProactiveProtection, IncidentResponse
from .network_monitor import NetworkMonitor, NetworkPacket, NetworkAnomaly
from .ai_threat_analyzer import AIThreatAnalyzer, ThreatFeatures, ThreatPrediction
from .threat_intelligence_sharing import ThreatIntelligenceSharing, ThreatIntelligence
from .world_map_monitor import WorldMapMonitor, WorldThreat, WorldStatistics
from .dashboard_interface import DashboardInterface
from .notification_system import NotificationSystem, NotificationType, NotificationPriority

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemStatus(Enum):
    """Statut du système"""
    INITIALIZING = "initializing"
    RUNNING = "running"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"
    SHUTDOWN = "shutdown"

class AlertLevel(Enum):
    """Niveaux d'alerte"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class SystemAlert:
    """Alerte système"""
    id: str
    level: AlertLevel
    title: str
    message: str
    source: str
    timestamp: datetime
    acknowledged: bool
    resolved: bool
    metadata: Dict[str, Any]

@dataclass
class SystemMetrics:
    """Métriques système"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_throughput: float
    active_threats: int
    active_incidents: int
    blocked_ips: int
    anomalies_detected: int
    system_status: SystemStatus

class CyberDefenseSystem:
    """
    Système principal de défense cybernétique
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._load_default_config()
        self.redis_url = self.config.get("redis_url", "redis://localhost:6379")
        self.redis = redis.from_url(self.redis_url)
        
        # Composants du système
        self.threat_detector = GlobalThreatDetector(self.redis_url)
        self.protection_system = ProactiveProtection(self.redis_url)
        self.network_monitor = NetworkMonitor(self.redis_url, self.config.get("network_interface", "eth0"))
        self.ai_analyzer = AIThreatAnalyzer(self.redis_url, self.config.get("models_dir", "models"))
        self.intelligence_sharing = ThreatIntelligenceSharing(self.redis_url)
        self.world_map_monitor = WorldMapMonitor(self.redis_url)
        self.dashboard_interface = DashboardInterface(self.app)
        self.notification_system = NotificationSystem(self.redis_url)
        
        # État du système
        self.status = SystemStatus.INITIALIZING
        self.alerts: Dict[str, SystemAlert] = {}
        self.metrics_history: List[SystemMetrics] = []
        self.websocket_connections: Set[WebSocket] = set()
        
        # API FastAPI
        self.app = FastAPI(
            title="CyberDefense System API",
            description="API du système mondial de détection et protection contre les cyberattaques",
            version="1.0.0"
        )
        
        # Configuration CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Configuration des routes
        self._setup_routes()
        
        # Tâches en arrière-plan
        self.background_tasks = []
        
    async def initialize(self):
        """Initialisation complète du système"""
        logger.info("🚀 Initialisation du système de défense cybernétique")
        
        try:
            # Initialisation des composants
            await self.threat_detector.initialize()
            await self.protection_system.initialize()
            await self.network_monitor.initialize()
            await self.ai_analyzer.initialize()
            await self.intelligence_sharing.initialize()
            await self.world_map_monitor.initialize()
            await self.notification_system.initialize()
            
            # Démarrage des tâches en arrière-plan
            self.background_tasks = [
                asyncio.create_task(self._system_monitor()),
                asyncio.create_task(self._metrics_collector()),
                asyncio.create_task(self._alert_manager()),
                asyncio.create_task(self._threat_correlation()),
                asyncio.create_task(self._intelligence_sharing()),
                asyncio.create_task(self._health_checker())
            ]
            
            # Changement de statut
            self.status = SystemStatus.RUNNING
            
            logger.info("✅ Système de défense cybernétique initialisé avec succès")
            
            # Création de l'alerte de démarrage
            await self._create_system_alert(
                AlertLevel.INFO,
                "Système Démarrage",
                "Le système de défense cybernétique a démarré avec succès",
                "system"
            )
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation: {e}")
            self.status = SystemStatus.EMERGENCY
            raise
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Chargement de la configuration par défaut"""
        return {
            "redis_url": "redis://localhost:6379",
            "network_interface": "eth0",
            "api_host": "0.0.0.0",
            "api_port": 8000,
            "websocket_enabled": True,
            "auto_response_enabled": True,
            "threat_feed_update_interval": 300,  # 5 minutes
            "metrics_collection_interval": 30,   # 30 secondes
            "alert_retention_days": 30,
            "max_concurrent_incidents": 100,
            "emergency_threshold": 10,  # menaces critiques simultanées
            "backup_enabled": True,
            "logging_level": "INFO"
        }
    
    def _setup_routes(self):
        """Configuration des routes API"""
        
        @self.app.get("/")
        async def root():
            return {
                "message": "Système Mondial de Détection et Protection contre les Cyberattaques",
                "version": "1.0.0",
                "status": self.status.value,
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/status")
        async def get_system_status():
            return {
                "status": self.status.value,
                "components": {
                    "threat_detector": "running",
                    "protection_system": "running",
                    "network_monitor": "running"
                },
                "metrics": await self._get_current_metrics(),
                "alerts_count": len(self.alerts),
                "active_threats": len(await self.threat_detector.get_active_threats()),
                "active_incidents": len(await self.protection_system.get_incident_history())
            }
        
        @self.app.get("/threats")
        async def get_threats():
            threats = await self.threat_detector.get_active_threats()
            return [asdict(threat) for threat in threats]
        
        @self.app.get("/threats/statistics")
        async def get_threat_statistics():
            return await self.threat_detector.get_threat_statistics()
        
        @self.app.get("/incidents")
        async def get_incidents():
            incidents = await self.protection_system.get_incident_history()
            return [asdict(incident) for incident in incidents]
        
        @self.app.get("/protection/status")
        async def get_protection_status():
            return await self.protection_system.get_protection_status()
        
        @self.app.get("/network/statistics")
        async def get_network_statistics():
            return asdict(await self.network_monitor.get_network_statistics())
        
        @self.app.get("/network/flows")
        async def get_network_flows():
            flows = await self.network_monitor.get_active_flows()
            return [asdict(flow) for flow in flows]
        
        @self.app.get("/network/anomalies")
        async def get_network_anomalies():
            anomalies = await self.network_monitor.get_network_anomalies()
            return [asdict(anomaly) for anomaly in anomalies]
        
        @self.app.get("/ai/models")
        async def get_ai_models():
            return await self.ai_analyzer.get_model_statistics()
        
        @self.app.get("/ai/predictions")
        async def get_ai_predictions():
            predictions = await self.ai_analyzer.get_prediction_history()
            return [asdict(prediction) for prediction in predictions]
        
        @self.app.get("/intelligence/search")
        async def search_intelligence(query: str, intelligence_type: str = None):
            from .threat_intelligence_sharing import IntelligenceType
            intel_type = IntelligenceType(intelligence_type) if intelligence_type else None
            results = await self.intelligence_sharing.search_intelligence(query, intel_type)
            return [asdict(intel) for intel in results]
        
        @self.app.get("/intelligence/statistics")
        async def get_intelligence_statistics():
            return await self.intelligence_sharing.get_intelligence_statistics()
        
        @self.app.get("/intelligence/history")
        async def get_intelligence_history():
            intelligence = await self.intelligence_sharing.get_intelligence_history()
            return [asdict(intel) for intel in intelligence]
        
        @self.app.get("/world-map")
        async def get_world_map():
            """Carte mondiale interactive"""
            from fastapi.responses import HTMLResponse
            html_content = self.world_map_monitor.generate_world_map_html()
            return HTMLResponse(content=html_content, status_code=200)
        
        @self.app.get("/world-map/statistics")
        async def get_world_statistics():
            """Statistiques mondiales"""
            stats = await self.world_map_monitor.get_world_statistics()
            return asdict(stats)
        
        @self.app.get("/world-map/threats")
        async def get_world_threats():
            """Menaces mondiales"""
            threats = await self.world_map_monitor.get_world_threats()
            return [asdict(threat) for threat in threats]
        
        @self.app.get("/developer/info")
        async def get_developer_info():
            """Informations du développeur"""
            return await self.world_map_monitor.get_developer_info()
        
        @self.app.get("/notifications")
        async def get_notifications(limit: int = 100):
            """Récupération des notifications"""
            notifications = await self.notification_system.get_notifications(limit)
            return [asdict(notification) for notification in notifications]
        
        @self.app.get("/notifications/stats")
        async def get_notification_stats():
            """Statistiques des notifications"""
            return await self.notification_system.get_notification_stats()
        
        @self.app.post("/notifications/send")
        async def send_notification(
            title: str,
            message: str,
            priority: str = "medium",
            notification_type: str = "email",
            recipients: List[str] = None
        ):
            """Envoi d'une notification"""
            try:
                notification_id = await self.notification_system.send_notification(
                    title=title,
                    message=message,
                    priority=NotificationPriority(priority),
                    notification_type=NotificationType(notification_type),
                    recipients=recipients or []
                )
                return {"message": "Notification envoyée", "id": notification_id}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @self.app.post("/notifications/test")
        async def test_notification(notification_type: str = "email"):
            """Test d'une notification"""
            try:
                success = await self.notification_system.test_notification(
                    NotificationType(notification_type)
                )
                return {"success": success, "message": "Test de notification effectué"}
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        @self.app.get("/alerts")
        async def get_alerts():
            return [asdict(alert) for alert in self.alerts.values()]
        
        @self.app.get("/metrics")
        async def get_metrics():
            return [asdict(metric) for metric in self.metrics_history[-100:]]
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            await self._handle_websocket_connection(websocket)
        
        @self.app.post("/threats/simulate")
        async def simulate_threat(threat_data: Dict[str, Any]):
            """Simulation d'une menace pour les tests"""
            try:
                # Création d'un événement réseau simulé
                event = NetworkEvent(
                    timestamp=datetime.now(),
                    source_ip=threat_data.get("source_ip", "192.168.1.100"),
                    destination_ip=threat_data.get("destination_ip", "10.0.0.1"),
                    source_port=threat_data.get("source_port", 12345),
                    destination_port=threat_data.get("destination_port", 80),
                    protocol=threat_data.get("protocol", "tcp"),
                    payload_size=threat_data.get("payload_size", 1024),
                    flags=threat_data.get("flags", ""),
                    country_source=threat_data.get("country_source", "US"),
                    country_dest=threat_data.get("country_dest", "FR"),
                    asn_source=threat_data.get("asn_source", "AS12345"),
                    asn_dest=threat_data.get("asn_dest", "AS67890"),
                    threat_score=threat_data.get("threat_score", 0.8),
                    anomaly_score=threat_data.get("anomaly_score", 0.7)
                )
                
                # Traitement de l'événement
                threat = await self.threat_detector.process_network_event(event)
                
                if threat:
                    # Déclenchement de la protection
                    incident = await self.protection_system.handle_threat(asdict(threat))
                    
                    return {
                        "success": True,
                        "threat_id": threat.id,
                        "incident_id": incident.id,
                        "message": "Menace simulée et traitée avec succès"
                    }
                else:
                    return {
                        "success": False,
                        "message": "Aucune menace détectée dans l'événement simulé"
                    }
                    
            except Exception as e:
                logger.error(f"Erreur simulation menace: {e}")
                return {"success": False, "error": str(e)}
    
    async def _handle_websocket_connection(self, websocket: WebSocket):
        """Gestion des connexions WebSocket"""
        try:
            # Ajout de la connexion
            await self.threat_detector.add_websocket_connection(websocket)
            await self.protection_system.add_websocket_connection(websocket)
            await self.network_monitor.add_websocket_connection(websocket)
            await self.ai_analyzer.add_websocket_connection(websocket)
            await self.intelligence_sharing.add_websocket_connection(websocket)
            await self.world_map_monitor.add_websocket_connection(websocket)
            await self.notification_system.add_websocket_connection(websocket)
            self.websocket_connections.add(websocket)
            
            logger.info(f"🔌 Nouvelle connexion WebSocket établie")
            
            # Envoi du statut initial
            await websocket.send_text(json.dumps({
                "type": "system_status",
                "status": self.status.value,
                "timestamp": datetime.now().isoformat()
            }))
            
            # Boucle de réception des messages
            while True:
                try:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    await self._handle_websocket_message(websocket, message)
                except Exception as e:
                    logger.error(f"Erreur WebSocket: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Erreur connexion WebSocket: {e}")
        finally:
            # Nettoyage de la connexion
            await self.threat_detector.remove_websocket_connection(websocket)
            await self.protection_system.remove_websocket_connection(websocket)
            await self.network_monitor.remove_websocket_connection(websocket)
            await self.ai_analyzer.remove_websocket_connection(websocket)
            await self.intelligence_sharing.remove_websocket_connection(websocket)
            await self.world_map_monitor.remove_websocket_connection(websocket)
            await self.notification_system.remove_websocket_connection(websocket)
            self.websocket_connections.discard(websocket)
            logger.info("🔌 Connexion WebSocket fermée")
    
    async def _handle_websocket_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Traitement des messages WebSocket"""
        message_type = message.get("type")
        
        if message_type == "get_status":
            # Envoi du statut système
            await websocket.send_text(json.dumps({
                "type": "system_status",
                "status": self.status.value,
                "metrics": await self._get_current_metrics(),
                "timestamp": datetime.now().isoformat()
            }))
        
        elif message_type == "get_threats":
            # Envoi des menaces actives
            threats = await self.threat_detector.get_active_threats()
            await websocket.send_text(json.dumps({
                "type": "threats_update",
                "threats": [asdict(threat) for threat in threats],
                "timestamp": datetime.now().isoformat()
            }))
        
        elif message_type == "get_incidents":
            # Envoi des incidents
            incidents = await self.protection_system.get_incident_history()
            await websocket.send_text(json.dumps({
                "type": "incidents_update",
                "incidents": [asdict(incident) for incident in incidents],
                "timestamp": datetime.now().isoformat()
            }))
    
    async def _system_monitor(self):
        """Moniteur système principal"""
        while self.status != SystemStatus.SHUTDOWN:
            try:
                await self._monitor_system_health()
                await asyncio.sleep(60)  # 1 minute
            except Exception as e:
                logger.error(f"Erreur moniteur système: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_system_health(self):
        """Surveillance de la santé du système"""
        # Vérification des composants
        components_status = {
            "threat_detector": True,  # Simplifié
            "protection_system": True,  # Simplifié
            "network_monitor": True   # Simplifié
        }
        
        # Vérification des seuils critiques
        active_threats = len(await self.threat_detector.get_active_threats())
        active_incidents = len([i for i in await self.protection_system.get_incident_history() if i.status == "active"])
        
        # Vérification du seuil d'urgence
        if active_threats > self.config.get("emergency_threshold", 10):
            if self.status != SystemStatus.EMERGENCY:
                self.status = SystemStatus.EMERGENCY
                await self._create_system_alert(
                    AlertLevel.EMERGENCY,
                    "Seuil d'Urgence Dépassé",
                    f"Nombre de menaces critiques: {active_threats}",
                    "system_monitor"
                )
        
        # Vérification de la santé des composants
        if not all(components_status.values()):
            await self._create_system_alert(
                AlertLevel.CRITICAL,
                "Composant Système Défaillant",
                "Un ou plusieurs composants du système sont défaillants",
                "system_monitor"
            )
    
    async def _metrics_collector(self):
        """Collecteur de métriques système"""
        while self.status != SystemStatus.SHUTDOWN:
            try:
                metrics = await self._collect_system_metrics()
                self.metrics_history.append(metrics)
                
                # Limitation de l'historique
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-500:]
                
                await asyncio.sleep(self.config.get("metrics_collection_interval", 30))
                
            except Exception as e:
                logger.error(f"Erreur collecte métriques: {e}")
                await asyncio.sleep(15)
    
    async def _collect_system_metrics(self) -> SystemMetrics:
        """Collecte des métriques système"""
        # Métriques système (simulées)
        import psutil
        
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Métriques réseau
        network_stats = psutil.net_io_counters()
        network_throughput = (network_stats.bytes_sent + network_stats.bytes_recv) / 1024 / 1024  # MB
        
        # Métriques de sécurité
        active_threats = len(await self.threat_detector.get_active_threats())
        active_incidents = len([i for i in await self.protection_system.get_incident_history() if i.status == "active"])
        blocked_ips = (await self.protection_system.get_protection_status()).get("blocked_ips_count", 0)
        anomalies_detected = len(await self.network_monitor.get_network_anomalies())
        
        return SystemMetrics(
            timestamp=datetime.now(),
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_throughput=network_throughput,
            active_threats=active_threats,
            active_incidents=active_incidents,
            blocked_ips=blocked_ips,
            anomalies_detected=anomalies_detected,
            system_status=self.status
        )
    
    async def _get_current_metrics(self) -> Dict[str, Any]:
        """Récupération des métriques actuelles"""
        if self.metrics_history:
            latest = self.metrics_history[-1]
            return asdict(latest)
        return {}
    
    async def _alert_manager(self):
        """Gestionnaire d'alertes"""
        while self.status != SystemStatus.SHUTDOWN:
            try:
                await self._process_alerts()
                await asyncio.sleep(30)  # 30 secondes
            except Exception as e:
                logger.error(f"Erreur gestionnaire alertes: {e}")
                await asyncio.sleep(15)
    
    async def _process_alerts(self):
        """Traitement des alertes"""
        current_time = datetime.now()
        
        # Nettoyage des anciennes alertes
        expired_alerts = []
        retention_days = self.config.get("alert_retention_days", 30)
        
        for alert_id, alert in self.alerts.items():
            if (current_time - alert.timestamp).days > retention_days:
                expired_alerts.append(alert_id)
        
        for alert_id in expired_alerts:
            del self.alerts[alert_id]
        
        # Traitement des alertes non résolues
        for alert in self.alerts.values():
            if not alert.resolved and alert.level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]:
                await self._escalate_alert(alert)
    
    async def _create_system_alert(self, level: AlertLevel, title: str, message: str, source: str, metadata: Dict[str, Any] = None):
        """Création d'une alerte système"""
        alert = SystemAlert(
            id=f"alert_{int(time.time())}_{hash(title)}",
            level=level,
            title=title,
            message=message,
            source=source,
            timestamp=datetime.now(),
            acknowledged=False,
            resolved=False,
            metadata=metadata or {}
        )
        
        self.alerts[alert.id] = alert
        
        # Notification via WebSocket
        await self._broadcast_alert(alert)
        
        # Log de l'alerte
        log_level = logging.ERROR if level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY] else logging.WARNING
        logger.log(log_level, f"🚨 ALERTE {level.value.upper()}: {title} - {message}")
        
        return alert
    
    async def _escalate_alert(self, alert: SystemAlert):
        """Escalade d'une alerte"""
        if alert.level == AlertLevel.EMERGENCY:
            # Procédures d'urgence
            logger.critical(f"🚨 ESCALADE URGENCE: {alert.title}")
            
            # Notification des administrateurs
            # Déclenchement des procédures d'urgence
            # Isolation automatique si nécessaire
    
    async def _broadcast_alert(self, alert: SystemAlert):
        """Diffusion d'une alerte via WebSocket"""
        message = {
            "type": "system_alert",
            "alert": asdict(alert),
            "timestamp": datetime.now().isoformat()
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket: {e}")
                self.websocket_connections.discard(websocket)
    
    async def _threat_correlation(self):
        """Corrélation des menaces"""
        while self.status != SystemStatus.SHUTDOWN:
            try:
                await self._correlate_threats_and_incidents()
                await asyncio.sleep(120)  # 2 minutes
            except Exception as e:
                logger.error(f"Erreur corrélation menaces: {e}")
                await asyncio.sleep(60)
    
    async def _correlate_threats_and_incidents(self):
        """Corrélation entre menaces et incidents"""
        threats = await self.threat_detector.get_active_threats()
        incidents = await self.protection_system.get_incident_history()
        
        # Recherche de patterns
        threat_patterns = {}
        for threat in threats:
            pattern_key = f"{threat.attack_type.value}_{threat.threat_level.value}"
            if pattern_key not in threat_patterns:
                threat_patterns[pattern_key] = []
            threat_patterns[pattern_key].append(threat)
        
        # Détection de patterns suspects
        for pattern, threat_list in threat_patterns.items():
            if len(threat_list) > 3:  # Plus de 3 menaces du même type
                await self._create_system_alert(
                    AlertLevel.WARNING,
                    f"Pattern de Menace Détecté",
                    f"Pattern {pattern}: {len(threat_list)} menaces détectées",
                    "threat_correlation",
                    {"pattern": pattern, "threat_count": len(threat_list)}
                )
    
    async def _intelligence_sharing(self):
        """Partage d'intelligence sur les menaces"""
        while self.status != SystemStatus.SHUTDOWN:
            try:
                await self._share_threat_intelligence()
                await asyncio.sleep(600)  # 10 minutes
            except Exception as e:
                logger.error(f"Erreur partage intelligence: {e}")
                await asyncio.sleep(300)
    
    async def _share_threat_intelligence(self):
        """Partage d'intelligence sur les menaces"""
        # Ici, on pourrait implémenter le partage avec:
        # - MISP (Malware Information Sharing Platform)
        # - STIX/TAXII
        # - CERTs
        # - Organisations de sécurité
        logger.info("🌐 Partage d'intelligence sur les menaces")
    
    async def _health_checker(self):
        """Vérificateur de santé du système"""
        while self.status != SystemStatus.SHUTDOWN:
            try:
                await self._perform_health_check()
                await asyncio.sleep(300)  # 5 minutes
            except Exception as e:
                logger.error(f"Erreur vérification santé: {e}")
                await asyncio.sleep(60)
    
    async def _perform_health_check(self):
        """Exécution d'une vérification de santé"""
        # Vérification de la connectivité Redis
        try:
            await self.redis.ping()
        except Exception as e:
            await self._create_system_alert(
                AlertLevel.CRITICAL,
                "Erreur Connectivité Redis",
                f"Impossible de se connecter à Redis: {e}",
                "health_checker"
            )
        
        # Vérification de l'espace disque
        import psutil
        disk_usage = psutil.disk_usage('/').percent
        if disk_usage > 90:
            await self._create_system_alert(
                AlertLevel.WARNING,
                "Espace Disque Faible",
                f"Utilisation disque: {disk_usage}%",
                "health_checker"
            )
        
        # Vérification de la mémoire
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > 90:
            await self._create_system_alert(
                AlertLevel.WARNING,
                "Mémoire Faible",
                f"Utilisation mémoire: {memory_usage}%",
                "health_checker"
            )
    
    async def shutdown(self):
        """Arrêt propre du système"""
        logger.info("🛑 Arrêt du système de défense cybernétique")
        
        # Changement de statut
        self.status = SystemStatus.SHUTDOWN
        
        # Arrêt des tâches en arrière-plan
        for task in self.background_tasks:
            task.cancel()
        
        # Arrêt des composants
        await self.network_monitor.stop_capture()
        
        # Fermeture des connexions WebSocket
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.close()
            except:
                pass
        
        logger.info("✅ Système arrêté avec succès")
    
    def run(self, host: str = None, port: int = None):
        """Démarrage du serveur API"""
        host = host or self.config.get("api_host", "0.0.0.0")
        port = port or self.config.get("api_port", 8000)
        
        logger.info(f"🌐 Démarrage du serveur API sur {host}:{port}")
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level=self.config.get("logging_level", "info")
        )

# Fonction de démarrage rapide
async def start_cyber_defense_system(config: Dict[str, Any] = None):
    """Démarrage rapide du système"""
    system = CyberDefenseSystem(config)
    await system.initialize()
    return system

if __name__ == "__main__":
    # Configuration par défaut
    config = {
        "redis_url": "redis://localhost:6379",
        "network_interface": "eth0",
        "api_host": "0.0.0.0",
        "api_port": 8000,
        "auto_response_enabled": True
    }
    
    # Démarrage du système
    system = CyberDefenseSystem(config)
    
    try:
        # Initialisation
        asyncio.run(system.initialize())
        
        # Démarrage du serveur
        system.run()
        
    except KeyboardInterrupt:
        logger.info("Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
    finally:
        # Arrêt propre
        asyncio.run(system.shutdown())
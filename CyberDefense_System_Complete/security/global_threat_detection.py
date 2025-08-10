"""
Système Mondial de Détection des Cyberattaques en Temps Réel
============================================================

Ce module implémente un système de détection globale des menaces cybernétiques
avec corrélation en temps réel, partage d'intelligence et protection proactive.
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
from fastapi import WebSocket
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import hashlib
import ipaddress
import re

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLevel(Enum):
    """Niveaux de menace"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

class AttackType(Enum):
    """Types d'attaques"""
    DDoS = "ddos"
    MALWARE = "malware"
    PHISHING = "phishing"
    RANSOMWARE = "ransomware"
    APT = "apt"
    ZERO_DAY = "zero_day"
    INSIDER = "insider"
    SUPPLY_CHAIN = "supply_chain"
    IOT = "iot"
    CLOUD = "cloud"

@dataclass
class ThreatIndicator:
    """Indicateur de menace"""
    id: str
    type: str
    value: str
    confidence: float
    first_seen: datetime
    last_seen: datetime
    sources: List[str]
    tags: List[str]
    threat_level: ThreatLevel
    description: str
    mitigation: str

@dataclass
class GlobalThreat:
    """Menace globale détectée"""
    id: str
    name: str
    attack_type: AttackType
    threat_level: ThreatLevel
    indicators: List[ThreatIndicator]
    affected_regions: List[str]
    affected_sectors: List[str]
    first_detected: datetime
    last_updated: datetime
    status: str
    description: str
    impact_score: float
    confidence: float
    mitigation_steps: List[str]
    ioc_count: int
    victim_count: int

@dataclass
class NetworkEvent:
    """Événement réseau"""
    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    payload_size: int
    flags: str
    country_source: str
    country_dest: str
    asn_source: str
    asn_dest: str
    threat_score: float
    anomaly_score: float

class GlobalThreatDetector:
    """
    Détecteur global de menaces en temps réel
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.active_threats: Dict[str, GlobalThreat] = {}
        self.threat_indicators: Dict[str, ThreatIndicator] = {}
        self.network_events: List[NetworkEvent] = []
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.websocket_connections: Set[WebSocket] = set()
        self.threat_feeds = [
            "https://api.abuseipdb.com/api/v2/blacklist",
            "https://api.threatfox.abuse.ch/export/csv/",
            "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/",
            "https://api.cybercure.ai/feed"
        ]
        self.correlation_rules = self._load_correlation_rules()
        self.mitigation_strategies = self._load_mitigation_strategies()
        
    async def initialize(self):
        """Initialisation du système"""
        logger.info("🚀 Initialisation du système de détection globale des menaces")
        
        # Chargement des données historiques
        await self._load_historical_data()
        
        # Démarrage des tâches en arrière-plan
        asyncio.create_task(self._threat_feed_monitor())
        asyncio.create_task(self._correlation_engine())
        asyncio.create_task(self._anomaly_detection_loop())
        asyncio.create_task(self._threat_intelligence_sharing())
        
        logger.info("✅ Système de détection globale initialisé")
    
    async def process_network_event(self, event: NetworkEvent) -> Optional[GlobalThreat]:
        """
        Traitement d'un événement réseau en temps réel
        """
        try:
            # Ajout à la liste des événements
            self.network_events.append(event)
            
            # Limitation de la taille de la liste
            if len(self.network_events) > 10000:
                self.network_events = self.network_events[-5000:]
            
            # Analyse de l'événement
            threat_score = await self._analyze_network_event(event)
            
            if threat_score > 0.7:
                # Détection de menace potentielle
                threat = await self._create_threat_from_event(event, threat_score)
                await self._notify_threat_detection(threat)
                return threat
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'événement réseau: {e}")
            return None
    
    async def _analyze_network_event(self, event: NetworkEvent) -> float:
        """
        Analyse d'un événement réseau pour détecter des menaces
        """
        threat_score = 0.0
        
        # Vérification des indicateurs connus
        for indicator in self.threat_indicators.values():
            if self._match_indicator(event, indicator):
                threat_score += indicator.confidence * 0.3
        
        # Analyse géographique
        if event.country_source in ["CN", "RU", "KP", "IR"]:
            threat_score += 0.2
        
        # Analyse des ports suspects
        suspicious_ports = {22, 23, 3389, 445, 1433, 3306, 5432}
        if event.destination_port in suspicious_ports:
            threat_score += 0.15
        
        # Analyse du volume de trafic
        if event.payload_size > 1000000:  # 1MB
            threat_score += 0.1
        
        # Analyse comportementale
        anomaly_score = await self._calculate_anomaly_score(event)
        threat_score += anomaly_score * 0.25
        
        return min(threat_score, 1.0)
    
    async def _calculate_anomaly_score(self, event: NetworkEvent) -> float:
        """
        Calcul du score d'anomalie pour un événement
        """
        try:
            # Préparation des features
            features = [
                event.payload_size,
                event.source_port,
                event.destination_port,
                hash(event.source_ip) % 1000,
                hash(event.destination_ip) % 1000
            ]
            
            # Normalisation
            features_scaled = self.scaler.fit_transform([features])
            
            # Détection d'anomalie
            anomaly_score = self.anomaly_detector.decision_function(features_scaled)[0]
            
            # Normalisation du score entre 0 et 1
            return max(0, min(1, (anomaly_score + 0.5) * 2))
            
        except Exception as e:
            logger.error(f"Erreur calcul anomalie: {e}")
            return 0.0
    
    def _match_indicator(self, event: NetworkEvent, indicator: ThreatIndicator) -> bool:
        """
        Vérification si un événement correspond à un indicateur
        """
        if indicator.type == "ip":
            return (event.source_ip == indicator.value or 
                   event.destination_ip == indicator.value)
        elif indicator.type == "port":
            return (event.source_port == int(indicator.value) or 
                   event.destination_port == int(indicator.value))
        elif indicator.type == "domain":
            # Logique de correspondance de domaine
            return False
        return False
    
    async def _create_threat_from_event(self, event: NetworkEvent, threat_score: float) -> GlobalThreat:
        """
        Création d'une menace à partir d'un événement
        """
        threat_id = f"threat_{int(time.time())}_{hash(event.source_ip)}"
        
        # Détermination du type d'attaque
        attack_type = self._determine_attack_type(event)
        
        # Détermination du niveau de menace
        threat_level = self._determine_threat_level(threat_score)
        
        # Création de l'indicateur
        indicator = ThreatIndicator(
            id=f"ind_{threat_id}",
            type="ip",
            value=event.source_ip,
            confidence=threat_score,
            first_seen=event.timestamp,
            last_seen=event.timestamp,
            sources=["network_monitor"],
            tags=[attack_type.value],
            threat_level=threat_level,
            description=f"Activité suspecte détectée depuis {event.source_ip}",
            mitigation="Bloquer l'IP source et surveiller le trafic"
        )
        
        threat = GlobalThreat(
            id=threat_id,
            name=f"Menace réseau - {event.source_ip}",
            attack_type=attack_type,
            threat_level=threat_level,
            indicators=[indicator],
            affected_regions=[event.country_source],
            affected_sectors=["network"],
            first_detected=event.timestamp,
            last_updated=event.timestamp,
            status="active",
            description=f"Activité suspecte détectée depuis {event.source_ip} vers {event.destination_ip}",
            impact_score=threat_score,
            confidence=threat_score,
            mitigation_steps=["Bloquer l'IP source", "Surveiller le trafic", "Analyser les logs"],
            ioc_count=1,
            victim_count=1
        )
        
        # Stockage de la menace
        self.active_threats[threat_id] = threat
        self.threat_indicators[indicator.id] = indicator
        
        return threat
    
    def _determine_attack_type(self, event: NetworkEvent) -> AttackType:
        """
        Détermination du type d'attaque basé sur l'événement
        """
        if event.destination_port in [80, 443, 8080]:
            return AttackType.PHISHING
        elif event.destination_port in [22, 23, 3389]:
            return AttackType.APT
        elif event.payload_size > 1000000:
            return AttackType.DDoS
        else:
            return AttackType.MALWARE
    
    def _determine_threat_level(self, threat_score: float) -> ThreatLevel:
        """
        Détermination du niveau de menace basé sur le score
        """
        if threat_score >= 0.9:
            return ThreatLevel.EMERGENCY
        elif threat_score >= 0.7:
            return ThreatLevel.CRITICAL
        elif threat_score >= 0.5:
            return ThreatLevel.HIGH
        elif threat_score >= 0.3:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    async def _notify_threat_detection(self, threat: GlobalThreat):
        """
        Notification de la détection d'une menace
        """
        logger.warning(f"🚨 MENACE DÉTECTÉE: {threat.name} (Niveau: {threat.threat_level.name})")
        
        # Notification via WebSocket
        await self._broadcast_threat(threat)
        
        # Stockage en base
        await self._store_threat(threat)
        
        # Escalade si critique
        if threat.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.EMERGENCY]:
            await self._escalate_threat(threat)
    
    async def _broadcast_threat(self, threat: GlobalThreat):
        """
        Diffusion d'une menace via WebSocket
        """
        message = {
            "type": "threat_detected",
            "threat": asdict(threat),
            "timestamp": datetime.now().isoformat()
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket: {e}")
                self.websocket_connections.discard(websocket)
    
    async def _store_threat(self, threat: GlobalThreat):
        """
        Stockage d'une menace en base de données
        """
        try:
            await self.redis.hset(
                f"threat:{threat.id}",
                mapping=asdict(threat)
            )
            await self.redis.expire(f"threat:{threat.id}", 86400)  # 24h
        except Exception as e:
            logger.error(f"Erreur stockage menace: {e}")
    
    async def _escalate_threat(self, threat: GlobalThreat):
        """
        Escalade d'une menace critique
        """
        logger.critical(f"🚨 ESCALADE: Menace critique {threat.id} - {threat.name}")
        
        # Notification aux administrateurs
        # Intégration avec les systèmes de sécurité
        # Déclenchement des procédures d'urgence
    
    async def _threat_feed_monitor(self):
        """
        Surveillance des flux de menaces externes
        """
        while True:
            try:
                for feed_url in self.threat_feeds:
                    await self._process_threat_feed(feed_url)
                await asyncio.sleep(300)  # 5 minutes
            except Exception as e:
                logger.error(f"Erreur surveillance flux menaces: {e}")
                await asyncio.sleep(60)
    
    async def _process_threat_feed(self, feed_url: str):
        """
        Traitement d'un flux de menaces
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(feed_url) as response:
                    if response.status == 200:
                        data = await response.text()
                        indicators = self._parse_threat_feed(data, feed_url)
                        
                        for indicator in indicators:
                            if indicator.id not in self.threat_indicators:
                                self.threat_indicators[indicator.id] = indicator
                                logger.info(f"📊 Nouvel indicateur ajouté: {indicator.value}")
        
        except Exception as e:
            logger.error(f"Erreur traitement flux {feed_url}: {e}")
    
    def _parse_threat_feed(self, data: str, source: str) -> List[ThreatIndicator]:
        """
        Parsing d'un flux de menaces
        """
        indicators = []
        
        try:
            # Parsing basique (à adapter selon le format du flux)
            lines = data.strip().split('\n')
            
            for line in lines:
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) >= 2:
                        value = parts[0].strip()
                        description = parts[1].strip() if len(parts) > 1 else ""
                        
                        indicator = ThreatIndicator(
                            id=hashlib.md5(f"{source}:{value}".encode()).hexdigest(),
                            type="ip" if self._is_ip(value) else "domain",
                            value=value,
                            confidence=0.8,
                            first_seen=datetime.now(),
                            last_seen=datetime.now(),
                            sources=[source],
                            tags=["external_feed"],
                            threat_level=ThreatLevel.MEDIUM,
                            description=description,
                            mitigation="Surveiller et bloquer si nécessaire"
                        )
                        indicators.append(indicator)
        
        except Exception as e:
            logger.error(f"Erreur parsing flux: {e}")
        
        return indicators
    
    def _is_ip(self, value: str) -> bool:
        """
        Vérification si une valeur est une IP
        """
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False
    
    async def _correlation_engine(self):
        """
        Moteur de corrélation des menaces
        """
        while True:
            try:
                await self._correlate_threats()
                await asyncio.sleep(60)  # 1 minute
            except Exception as e:
                logger.error(f"Erreur corrélation: {e}")
                await asyncio.sleep(30)
    
    async def _correlate_threats(self):
        """
        Corrélation des menaces actives
        """
        threats = list(self.active_threats.values())
        
        for i, threat1 in enumerate(threats):
            for threat2 in threats[i+1:]:
                correlation_score = self._calculate_correlation(threat1, threat2)
                
                if correlation_score > 0.8:
                    # Fusion des menaces corrélées
                    merged_threat = await self._merge_threats(threat1, threat2, correlation_score)
                    logger.info(f"🔄 Menaces corrélées fusionnées: {threat1.id} + {threat2.id}")
    
    def _calculate_correlation(self, threat1: GlobalThreat, threat2: GlobalThreat) -> float:
        """
        Calcul du score de corrélation entre deux menaces
        """
        score = 0.0
        
        # Corrélation par type d'attaque
        if threat1.attack_type == threat2.attack_type:
            score += 0.3
        
        # Corrélation par région
        common_regions = set(threat1.affected_regions) & set(threat2.affected_regions)
        if common_regions:
            score += 0.2
        
        # Corrélation temporelle
        time_diff = abs((threat1.first_detected - threat2.first_detected).total_seconds())
        if time_diff < 3600:  # 1 heure
            score += 0.3
        
        # Corrélation par indicateurs
        indicators1 = {ind.value for ind in threat1.indicators}
        indicators2 = {ind.value for ind in threat2.indicators}
        common_indicators = indicators1 & indicators2
        if common_indicators:
            score += 0.2
        
        return score
    
    async def _merge_threats(self, threat1: GlobalThreat, threat2: GlobalThreat, correlation_score: float) -> GlobalThreat:
        """
        Fusion de deux menaces corrélées
        """
        # Création de la menace fusionnée
        merged_threat = GlobalThreat(
            id=f"merged_{threat1.id}_{threat2.id}",
            name=f"Menace corrélée: {threat1.name} + {threat2.name}",
            attack_type=threat1.attack_type,
            threat_level=max(threat1.threat_level, threat2.threat_level),
            indicators=threat1.indicators + threat2.indicators,
            affected_regions=list(set(threat1.affected_regions + threat2.affected_regions)),
            affected_sectors=list(set(threat1.affected_sectors + threat2.affected_sectors)),
            first_detected=min(threat1.first_detected, threat2.first_detected),
            last_updated=datetime.now(),
            status="active",
            description=f"Menace corrélée (score: {correlation_score:.2f})",
            impact_score=max(threat1.impact_score, threat2.impact_score),
            confidence=correlation_score,
            mitigation_steps=threat1.mitigation_steps + threat2.mitigation_steps,
            ioc_count=threat1.ioc_count + threat2.ioc_count,
            victim_count=threat1.victim_count + threat2.victim_count
        )
        
        # Suppression des anciennes menaces
        del self.active_threats[threat1.id]
        del self.active_threats[threat2.id]
        
        # Ajout de la menace fusionnée
        self.active_threats[merged_threat.id] = merged_threat
        
        return merged_threat
    
    async def _anomaly_detection_loop(self):
        """
        Boucle de détection d'anomalies
        """
        while True:
            try:
                if len(self.network_events) > 100:
                    await self._detect_anomalies()
                await asyncio.sleep(30)  # 30 secondes
            except Exception as e:
                logger.error(f"Erreur détection anomalies: {e}")
                await asyncio.sleep(15)
    
    async def _detect_anomalies(self):
        """
        Détection d'anomalies dans les événements réseau
        """
        try:
            # Préparation des données
            features = []
            for event in self.network_events[-1000:]:  # Derniers 1000 événements
                features.append([
                    event.payload_size,
                    event.source_port,
                    event.destination_port,
                    hash(event.source_ip) % 1000,
                    hash(event.destination_ip) % 1000
                ])
            
            if len(features) < 10:
                return
            
            # Normalisation
            features_scaled = self.scaler.fit_transform(features)
            
            # Détection d'anomalies
            anomalies = self.anomaly_detector.predict(features_scaled)
            
            # Traitement des anomalies détectées
            for i, is_anomaly in enumerate(anomalies):
                if is_anomaly == -1:  # Anomalie détectée
                    event = self.network_events[-(1000-i)]
                    logger.warning(f"🚨 Anomalie détectée: {event.source_ip} -> {event.destination_ip}")
                    
                    # Création d'une menace basée sur l'anomalie
                    threat = await self._create_threat_from_event(event, 0.8)
                    await self._notify_threat_detection(threat)
        
        except Exception as e:
            logger.error(f"Erreur détection anomalies: {e}")
    
    async def _threat_intelligence_sharing(self):
        """
        Partage d'intelligence sur les menaces
        """
        while True:
            try:
                await self._share_threat_intelligence()
                await asyncio.sleep(600)  # 10 minutes
            except Exception as e:
                logger.error(f"Erreur partage intelligence: {e}")
                await asyncio.sleep(300)
    
    async def _share_threat_intelligence(self):
        """
        Partage d'intelligence sur les menaces avec d'autres systèmes
        """
        # Simulation du partage d'intelligence
        logger.info("🌐 Partage d'intelligence sur les menaces")
        
        # Ici, on pourrait implémenter l'intégration avec:
        # - MISP (Malware Information Sharing Platform)
        # - STIX/TAXII
        # - API de partage d'intelligence
        # - Systèmes de CERT
    
    def _load_correlation_rules(self) -> Dict[str, Any]:
        """
        Chargement des règles de corrélation
        """
        return {
            "time_window": 3600,  # 1 heure
            "geographic_threshold": 0.7,
            "temporal_threshold": 0.8,
            "indicator_threshold": 0.6
        }
    
    def _load_mitigation_strategies(self) -> Dict[str, List[str]]:
        """
        Chargement des stratégies de mitigation
        """
        return {
            "ddos": [
                "Activer la protection DDoS",
                "Rediriger le trafic",
                "Augmenter la bande passante"
            ],
            "malware": [
                "Isoler l'endpoint",
                "Scanner avec antivirus",
                "Restaurer depuis sauvegarde"
            ],
            "phishing": [
                "Bloquer les domaines",
                "Former les utilisateurs",
                "Mettre à jour les filtres"
            ],
            "apt": [
                "Investigation approfondie",
                "Isolation du réseau",
                "Audit de sécurité"
            ]
        }
    
    async def _load_historical_data(self):
        """
        Chargement des données historiques
        """
        logger.info("📊 Chargement des données historiques")
        
        # Chargement depuis Redis
        try:
            keys = await self.redis.keys("threat:*")
            for key in keys:
                data = await self.redis.hgetall(key)
                if data:
                    # Reconstruction de l'objet Threat
                    # (simplifié pour l'exemple)
                    pass
        except Exception as e:
            logger.error(f"Erreur chargement données historiques: {e}")
    
    async def add_websocket_connection(self, websocket: WebSocket):
        """
        Ajout d'une connexion WebSocket
        """
        self.websocket_connections.add(websocket)
    
    async def remove_websocket_connection(self, websocket: WebSocket):
        """
        Suppression d'une connexion WebSocket
        """
        self.websocket_connections.discard(websocket)
    
    async def get_active_threats(self) -> List[GlobalThreat]:
        """
        Récupération des menaces actives
        """
        return list(self.active_threats.values())
    
    async def get_threat_statistics(self) -> Dict[str, Any]:
        """
        Statistiques des menaces
        """
        threats = list(self.active_threats.values())
        
        return {
            "total_threats": len(threats),
            "threats_by_level": {
                level.name: len([t for t in threats if t.threat_level == level])
                for level in ThreatLevel
            },
            "threats_by_type": {
                attack_type.value: len([t for t in threats if t.attack_type == attack_type])
                for attack_type in AttackType
            },
            "total_indicators": len(self.threat_indicators),
            "total_events": len(self.network_events)
        }
"""
Module d'Intelligence de Sécurité Avancée
=========================================

Analyse de menaces en temps réel, détection d'anomalies et réponse 
intelligente aux incidents de sécurité.
"""

import asyncio
import json
import re
import hashlib
import ipaddress
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from transformers import pipeline
import spacy
from loguru import logger

from .config import config
from .ai_engine import SecurityAlert


class ThreatLevel(Enum):
    """Niveaux de menace"""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"


class AttackVector(Enum):
    """Vecteurs d'attaque"""
    MALWARE = "malware"
    PHISHING = "phishing"
    RANSOMWARE = "ransomware"
    APT = "apt"
    DDOS = "ddos"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DATA_EXFILTRATION = "data_exfiltration"
    INSIDER_THREAT = "insider_threat"
    SOCIAL_ENGINEERING = "social_engineering"
    ZERO_DAY = "zero_day"


class ResponseAction(Enum):
    """Actions de réponse"""
    MONITOR = "monitor"
    ALERT = "alert"
    BLOCK = "block"
    ISOLATE = "isolate"
    QUARANTINE = "quarantine"
    EMERGENCY_SHUTDOWN = "emergency_shutdown"
    FORENSIC_CAPTURE = "forensic_capture"
    USER_NOTIFICATION = "user_notification"


@dataclass
class ThreatIndicator:
    """Indicateur de menace"""
    indicator_type: str  # ip, domain, hash, url, email, etc.
    value: str
    confidence: float
    threat_types: List[AttackVector]
    source: str
    first_seen: datetime
    last_seen: datetime
    reputation_score: float
    geographic_info: Optional[Dict[str, Any]] = None
    related_campaigns: List[str] = None


@dataclass
class SecurityIncident:
    """Incident de sécurité détecté"""
    incident_id: str
    threat_level: ThreatLevel
    attack_vector: AttackVector
    title: str
    description: str
    indicators: List[ThreatIndicator]
    affected_assets: List[str]
    attack_timeline: List[Dict[str, Any]]
    recommended_actions: List[ResponseAction]
    confidence_score: float
    created_at: datetime
    updated_at: datetime
    status: str = "new"  # new, investigating, contained, resolved


@dataclass
class NetworkEvent:
    """Événement réseau"""
    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    bytes_transferred: int
    packets_count: int
    duration: float
    status: str
    user_agent: Optional[str] = None
    http_method: Optional[str] = None
    uri: Optional[str] = None


class SecurityIntelligenceEngine:
    """
    Moteur d'Intelligence de Sécurité Avancée
    
    Fonctionnalités:
    - Analyse de menaces en temps réel
    - Détection d'anomalies comportementales
    - Corrélation d'événements de sécurité
    - Analyse prédictive des menaces
    - Réponse automatisée aux incidents
    - Communication vocale des alertes critiques
    """
    
    def __init__(self):
        self.is_initialized = False
        
        # Modèles d'IA
        self.anomaly_detector = None
        self.threat_classifier = None
        self.nlp_model = None
        self.malware_classifier = None
        
        # Bases de données de menaces
        self.threat_intel_db = {}
        self.indicators_cache = {}
        self.behavioral_baselines = {}
        
        # Historique et contexte
        self.incidents_history: List[SecurityIncident] = []
        self.network_events: List[NetworkEvent] = []
        self.active_threats: Dict[str, SecurityIncident] = {}
        
        # Configuration
        self.detection_thresholds = {
            ThreatLevel.LOW: 0.3,
            ThreatLevel.MEDIUM: 0.5,
            ThreatLevel.HIGH: 0.7,
            ThreatLevel.CRITICAL: 0.85,
            ThreatLevel.CATASTROPHIC: 0.95
        }
        
        # Patterns de détection
        self.malicious_patterns = self._load_malicious_patterns()
        self.behavioral_anomalies = {}
        
        # Callbacks pour communication
        self.alert_callback = None
        self.voice_callback = None
        
    async def initialize(self):
        """Initialisation du moteur d'intelligence"""
        if self.is_initialized:
            return
            
        logger.info("Initialisation du moteur d'intelligence de sécurité...")
        
        try:
            # Chargement des modèles d'IA
            await self._load_ai_models()
            
            # Initialisation des bases de données de menaces
            await self._initialize_threat_databases()
            
            # Chargement des patterns de détection
            await self._load_detection_patterns()
            
            # Initialisation des analyses comportementales
            await self._initialize_behavioral_analysis()
            
            self.is_initialized = True
            logger.success("Moteur d'intelligence initialisé")
            
        except Exception as e:
            logger.error(f"Erreur initialisation: {e}")
            raise
    
    async def _load_ai_models(self):
        """Chargement des modèles d'IA"""
        try:
            # Modèle de détection d'anomalies
            self.anomaly_detector = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
            
            # Classificateur de menaces (transformers)
            self.threat_classifier = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium",
                device=0 if tf.config.list_physical_devices('GPU') else -1
            )
            
            # Modèle NLP pour analyse de logs
            self.nlp_model = spacy.load("en_core_web_sm")
            
            logger.success("Modèles d'IA chargés")
            
        except Exception as e:
            logger.error(f"Erreur chargement modèles: {e}")
            raise
    
    async def _initialize_threat_databases(self):
        """Initialisation des bases de données de menaces"""
        try:
            # Base de données d'indicateurs de menaces
            self.threat_intel_db = {
                "malicious_ips": set(),
                "malicious_domains": set(),
                "malware_hashes": set(),
                "phishing_urls": set(),
                "suspicious_patterns": []
            }
            
            # Chargement des feeds de threat intelligence
            await self._load_threat_feeds()
            
            logger.success("Bases de données de menaces initialisées")
            
        except Exception as e:
            logger.error(f"Erreur initialisation BD menaces: {e}")
            raise
    
    async def _load_threat_feeds(self):
        """Chargement des flux de threat intelligence"""
        try:
            # Simulation de chargement de feeds externes
            # En production, ceci se connecterait à des feeds réels
            
            # IPs malicieuses simulées
            malicious_ips = [
                "192.168.1.100", "10.0.0.50", "172.16.0.10",
                "185.220.100.240", "185.220.101.1"
            ]
            self.threat_intel_db["malicious_ips"].update(malicious_ips)
            
            # Domaines malicieux simulés
            malicious_domains = [
                "malware-example.com", "phishing-site.org",
                "trojan-download.net", "botnet-command.ru"
            ]
            self.threat_intel_db["malicious_domains"].update(malicious_domains)
            
            # Hashes de malware simulés
            malware_hashes = [
                "d41d8cd98f00b204e9800998ecf8427e",
                "5d41402abc4b2a76b9719d911017c592",
                "098f6bcd4621d373cade4e832627b4f6"
            ]
            self.threat_intel_db["malware_hashes"].update(malware_hashes)
            
            logger.info(f"Chargé {len(malicious_ips)} IPs malicieuses")
            logger.info(f"Chargé {len(malicious_domains)} domaines malicieux")
            logger.info(f"Chargé {len(malware_hashes)} hashes de malware")
            
        except Exception as e:
            logger.error(f"Erreur chargement feeds: {e}")
    
    def _load_malicious_patterns(self) -> Dict[str, List[str]]:
        """Chargement des patterns malicieux"""
        return {
            "sql_injection": [
                r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
                r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))",
                r"union.*select",
                r"insert.*into",
                r"delete.*from",
                r"drop.*table"
            ],
            "xss": [
                r"<script[^>]*>.*?</script>",
                r"javascript:",
                r"on\w+\s*=",
                r"<iframe[^>]*>.*?</iframe>",
                r"document\.cookie",
                r"window\.location"
            ],
            "command_injection": [
                r";\s*(ls|dir|cat|type|more|less)",
                r"&\s*(ls|dir|cat|type|more|less)",
                r"\|\s*(ls|dir|cat|type|more|less)",
                r"(`|\\$\\()",
                r"(nc|netcat|wget|curl)"
            ],
            "suspicious_activity": [
                r"password.*brute.*force",
                r"failed.*login.*attempts",
                r"privilege.*escalation",
                r"lateral.*movement",
                r"data.*exfiltration",
                r"backdoor.*access"
            ]
        }
    
    async def _load_detection_patterns(self):
        """Chargement des patterns de détection"""
        try:
            self.malicious_patterns = self._load_malicious_patterns()
            logger.success(f"Chargé {len(self.malicious_patterns)} catégories de patterns")
            
        except Exception as e:
            logger.error(f"Erreur chargement patterns: {e}")
    
    async def _initialize_behavioral_analysis(self):
        """Initialisation de l'analyse comportementale"""
        try:
            # Baselines comportementales par défaut
            self.behavioral_baselines = {
                "normal_login_hours": (8, 18),  # 8h-18h
                "max_failed_logins": 3,
                "normal_data_transfer_mb": 100,
                "max_concurrent_sessions": 5,
                "normal_geo_locations": ["FR", "EU"],
                "suspicious_user_agents": [
                    "sqlmap", "nikto", "nmap", "masscan", "zap"
                ]
            }
            
            logger.success("Analyse comportementale initialisée")
            
        except Exception as e:
            logger.error(f"Erreur initialisation analyse comportementale: {e}")
    
    async def analyze_network_traffic(self, events: List[NetworkEvent]) -> List[SecurityIncident]:
        """Analyse du trafic réseau pour détecter des menaces"""
        if not self.is_initialized:
            await self.initialize()
        
        incidents = []
        
        try:
            # Mise à jour de l'historique
            self.network_events.extend(events)
            
            # Analyse des événements
            for event in events:
                # Vérification contre les IOCs connus
                threat_indicators = await self._check_threat_indicators(event)
                
                if threat_indicators:
                    incident = await self._create_incident_from_network_event(
                        event, threat_indicators
                    )
                    incidents.append(incident)
                
                # Détection d'anomalies comportementales
                anomalies = await self._detect_behavioral_anomalies(event)
                
                if anomalies:
                    incident = await self._create_incident_from_anomalies(
                        event, anomalies
                    )
                    incidents.append(incident)
            
            # Analyse de corrélation
            correlated_incidents = await self._correlate_events(events)
            incidents.extend(correlated_incidents)
            
            # Traitement des incidents détectés
            for incident in incidents:
                await self._process_security_incident(incident)
            
            return incidents
            
        except Exception as e:
            logger.error(f"Erreur analyse trafic réseau: {e}")
            return []
    
    async def _check_threat_indicators(self, event: NetworkEvent) -> List[ThreatIndicator]:
        """Vérification des indicateurs de menaces"""
        indicators = []
        
        try:
            # Vérification IP source
            if event.source_ip in self.threat_intel_db["malicious_ips"]:
                indicator = ThreatIndicator(
                    indicator_type="ip",
                    value=event.source_ip,
                    confidence=0.9,
                    threat_types=[AttackVector.MALWARE],
                    source="threat_intel_db",
                    first_seen=event.timestamp,
                    last_seen=event.timestamp,
                    reputation_score=0.1
                )
                indicators.append(indicator)
            
            # Vérification IP destination
            if event.destination_ip in self.threat_intel_db["malicious_ips"]:
                indicator = ThreatIndicator(
                    indicator_type="ip",
                    value=event.destination_ip,
                    confidence=0.8,
                    threat_types=[AttackVector.DATA_EXFILTRATION],
                    source="threat_intel_db",
                    first_seen=event.timestamp,
                    last_seen=event.timestamp,
                    reputation_score=0.2
                )
                indicators.append(indicator)
            
            # Vérification patterns dans URI
            if event.uri:
                malicious_patterns = await self._check_malicious_patterns(event.uri)
                for pattern_type, confidence in malicious_patterns:
                    attack_vector_map = {
                        "sql_injection": AttackVector.SQL_INJECTION,
                        "xss": AttackVector.XSS,
                        "command_injection": AttackVector.PRIVILEGE_ESCALATION
                    }
                    
                    indicator = ThreatIndicator(
                        indicator_type="url_pattern",
                        value=event.uri,
                        confidence=confidence,
                        threat_types=[attack_vector_map.get(pattern_type, AttackVector.MALWARE)],
                        source="pattern_detection",
                        first_seen=event.timestamp,
                        last_seen=event.timestamp,
                        reputation_score=1.0 - confidence
                    )
                    indicators.append(indicator)
            
            return indicators
            
        except Exception as e:
            logger.error(f"Erreur vérification indicateurs: {e}")
            return []
    
    async def _check_malicious_patterns(self, text: str) -> List[Tuple[str, float]]:
        """Vérification des patterns malicieux dans le texte"""
        detected_patterns = []
        
        try:
            for pattern_type, patterns in self.malicious_patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    if matches:
                        # Calcul de confiance basé sur le nombre et la qualité des matches
                        match_count = len(list(matches))
                        confidence = min(0.9, 0.3 + (match_count * 0.2))
                        detected_patterns.append((pattern_type, confidence))
                        break  # Un pattern par type suffit
            
            return detected_patterns
            
        except Exception as e:
            logger.error(f"Erreur vérification patterns: {e}")
            return []
    
    async def _detect_behavioral_anomalies(self, event: NetworkEvent) -> List[str]:
        """Détection d'anomalies comportementales"""
        anomalies = []
        
        try:
            # Analyse temporelle
            hour = event.timestamp.hour
            if hour < self.behavioral_baselines["normal_login_hours"][0] or \
               hour > self.behavioral_baselines["normal_login_hours"][1]:
                anomalies.append("activity_outside_normal_hours")
            
            # Analyse de volume de données
            if event.bytes_transferred > self.behavioral_baselines["normal_data_transfer_mb"] * 1024 * 1024:
                anomalies.append("excessive_data_transfer")
            
            # Analyse géographique (simulation)
            source_geo = await self._get_ip_geolocation(event.source_ip)
            if source_geo and source_geo not in self.behavioral_baselines["normal_geo_locations"]:
                anomalies.append("suspicious_geographic_location")
            
            # Analyse User-Agent
            if event.user_agent:
                for suspicious_ua in self.behavioral_baselines["suspicious_user_agents"]:
                    if suspicious_ua.lower() in event.user_agent.lower():
                        anomalies.append("suspicious_user_agent")
                        break
            
            # Analyse de fréquence
            recent_events = self._get_recent_events_from_ip(event.source_ip, minutes=5)
            if len(recent_events) > 50:  # Plus de 50 requêtes en 5 minutes
                anomalies.append("high_frequency_requests")
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Erreur détection anomalies: {e}")
            return []
    
    async def _get_ip_geolocation(self, ip: str) -> Optional[str]:
        """Obtention de la géolocalisation d'une IP (simulation)"""
        try:
            # Simulation de géolocalisation
            ip_obj = ipaddress.ip_address(ip)
            
            if ip_obj.is_private:
                return "PRIVATE"
            elif ip.startswith("185.220"):  # Exemple d'IPs suspectes
                return "RU"
            else:
                return "FR"  # Par défaut
                
        except Exception:
            return None
    
    def _get_recent_events_from_ip(self, ip: str, minutes: int = 5) -> List[NetworkEvent]:
        """Récupération des événements récents d'une IP"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            event for event in self.network_events[-1000:]  # Derniers 1000 événements
            if event.source_ip == ip and event.timestamp > cutoff_time
        ]
    
    async def _create_incident_from_network_event(
        self, 
        event: NetworkEvent, 
        indicators: List[ThreatIndicator]
    ) -> SecurityIncident:
        """Création d'un incident à partir d'un événement réseau"""
        
        # Détermination du niveau de menace
        max_confidence = max(indicator.confidence for indicator in indicators)
        threat_level = self._calculate_threat_level(max_confidence)
        
        # Détermination du vecteur d'attaque principal
        attack_vectors = []
        for indicator in indicators:
            attack_vectors.extend(indicator.threat_types)
        
        primary_vector = max(set(attack_vectors), key=attack_vectors.count) if attack_vectors else AttackVector.MALWARE
        
        # Création de l'incident
        incident = SecurityIncident(
            incident_id=f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hash(event.source_ip) % 10000:04d}",
            threat_level=threat_level,
            attack_vector=primary_vector,
            title=f"Activité suspecte détectée depuis {event.source_ip}",
            description=self._generate_incident_description(event, indicators),
            indicators=indicators,
            affected_assets=[event.destination_ip],
            attack_timeline=[{
                "timestamp": event.timestamp.isoformat(),
                "event": "Network event detected",
                "details": asdict(event)
            }],
            recommended_actions=self._generate_recommended_actions(threat_level, primary_vector),
            confidence_score=max_confidence,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return incident
    
    async def _create_incident_from_anomalies(
        self, 
        event: NetworkEvent, 
        anomalies: List[str]
    ) -> SecurityIncident:
        """Création d'un incident à partir d'anomalies comportementales"""
        
        # Calcul de la confiance basé sur le nombre d'anomalies
        confidence = min(0.9, len(anomalies) * 0.2)
        threat_level = self._calculate_threat_level(confidence)
        
        # Création d'indicateurs d'anomalie
        indicators = []
        for anomaly in anomalies:
            indicator = ThreatIndicator(
                indicator_type="behavioral_anomaly",
                value=anomaly,
                confidence=confidence,
                threat_types=[AttackVector.INSIDER_THREAT],
                source="behavioral_analysis",
                first_seen=event.timestamp,
                last_seen=event.timestamp,
                reputation_score=1.0 - confidence
            )
            indicators.append(indicator)
        
        incident = SecurityIncident(
            incident_id=f"ANO-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hash(event.source_ip) % 10000:04d}",
            threat_level=threat_level,
            attack_vector=AttackVector.INSIDER_THREAT,
            title=f"Anomalies comportementales détectées pour {event.source_ip}",
            description=f"Anomalies détectées: {', '.join(anomalies)}",
            indicators=indicators,
            affected_assets=[event.source_ip, event.destination_ip],
            attack_timeline=[{
                "timestamp": event.timestamp.isoformat(),
                "event": "Behavioral anomalies detected",
                "anomalies": anomalies
            }],
            recommended_actions=self._generate_recommended_actions(threat_level, AttackVector.INSIDER_THREAT),
            confidence_score=confidence,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return incident
    
    def _calculate_threat_level(self, confidence: float) -> ThreatLevel:
        """Calcul du niveau de menace basé sur la confiance"""
        if confidence >= self.detection_thresholds[ThreatLevel.CATASTROPHIC]:
            return ThreatLevel.CATASTROPHIC
        elif confidence >= self.detection_thresholds[ThreatLevel.CRITICAL]:
            return ThreatLevel.CRITICAL
        elif confidence >= self.detection_thresholds[ThreatLevel.HIGH]:
            return ThreatLevel.HIGH
        elif confidence >= self.detection_thresholds[ThreatLevel.MEDIUM]:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW
    
    def _generate_incident_description(
        self, 
        event: NetworkEvent, 
        indicators: List[ThreatIndicator]
    ) -> str:
        """Génération d'une description d'incident"""
        
        description_parts = [
            f"Événement réseau suspect détecté à {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}.",
            f"Source: {event.source_ip}:{event.source_port}",
            f"Destination: {event.destination_ip}:{event.destination_port}",
            f"Protocole: {event.protocol}",
            f"Données transférées: {event.bytes_transferred} bytes"
        ]
        
        if event.uri:
            description_parts.append(f"URI: {event.uri}")
        
        if event.user_agent:
            description_parts.append(f"User-Agent: {event.user_agent}")
        
        if indicators:
            description_parts.append("\nIndicateurs de menace détectés:")
            for indicator in indicators:
                description_parts.append(
                    f"- {indicator.indicator_type}: {indicator.value} "
                    f"(confiance: {indicator.confidence:.2f})"
                )
        
        return "\n".join(description_parts)
    
    def _generate_recommended_actions(
        self, 
        threat_level: ThreatLevel, 
        attack_vector: AttackVector
    ) -> List[ResponseAction]:
        """Génération d'actions recommandées"""
        
        actions = [ResponseAction.MONITOR, ResponseAction.ALERT]
        
        if threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL, ThreatLevel.CATASTROPHIC]:
            actions.extend([ResponseAction.BLOCK, ResponseAction.FORENSIC_CAPTURE])
        
        if threat_level in [ThreatLevel.CRITICAL, ThreatLevel.CATASTROPHIC]:
            actions.extend([ResponseAction.ISOLATE, ResponseAction.USER_NOTIFICATION])
        
        if threat_level == ThreatLevel.CATASTROPHIC:
            actions.append(ResponseAction.EMERGENCY_SHUTDOWN)
        
        # Actions spécifiques par vecteur d'attaque
        if attack_vector == AttackVector.MALWARE:
            actions.append(ResponseAction.QUARANTINE)
        elif attack_vector == AttackVector.DATA_EXFILTRATION:
            actions.append(ResponseAction.BLOCK)
        elif attack_vector == AttackVector.RANSOMWARE:
            actions.extend([ResponseAction.ISOLATE, ResponseAction.EMERGENCY_SHUTDOWN])
        
        return list(set(actions))  # Suppression des doublons
    
    async def _correlate_events(self, events: List[NetworkEvent]) -> List[SecurityIncident]:
        """Corrélation d'événements pour détecter des campagnes d'attaque"""
        correlated_incidents = []
        
        try:
            # Regroupement par IP source
            ip_groups = {}
            for event in events:
                if event.source_ip not in ip_groups:
                    ip_groups[event.source_ip] = []
                ip_groups[event.source_ip].append(event)
            
            # Analyse des groupes
            for source_ip, ip_events in ip_groups.items():
                if len(ip_events) > 10:  # Plus de 10 événements de la même IP
                    # Analyse temporelle
                    time_span = max(e.timestamp for e in ip_events) - min(e.timestamp for e in ip_events)
                    
                    if time_span.total_seconds() < 300:  # Moins de 5 minutes
                        # Possible attaque coordonnée
                        incident = await self._create_coordinated_attack_incident(source_ip, ip_events)
                        correlated_incidents.append(incident)
            
            return correlated_incidents
            
        except Exception as e:
            logger.error(f"Erreur corrélation événements: {e}")
            return []
    
    async def _create_coordinated_attack_incident(
        self, 
        source_ip: str, 
        events: List[NetworkEvent]
    ) -> SecurityIncident:
        """Création d'un incident d'attaque coordonnée"""
        
        # Analyse des patterns d'attaque
        unique_destinations = set(e.destination_ip for e in events)
        total_bytes = sum(e.bytes_transferred for e in events)
        
        confidence = min(0.8, len(events) / 20)  # Confiance basée sur le volume
        threat_level = self._calculate_threat_level(confidence)
        
        # Détermination du type d'attaque
        if len(unique_destinations) > 5:
            attack_vector = AttackVector.DDOS
            title = f"Attaque DDoS détectée depuis {source_ip}"
        elif total_bytes > 100 * 1024 * 1024:  # Plus de 100MB
            attack_vector = AttackVector.DATA_EXFILTRATION
            title = f"Exfiltration de données potentielle depuis {source_ip}"
        else:
            attack_vector = AttackVector.APT
            title = f"Activité APT suspecte depuis {source_ip}"
        
        # Création des indicateurs
        indicators = [
            ThreatIndicator(
                indicator_type="coordinated_attack",
                value=f"{source_ip}_campaign",
                confidence=confidence,
                threat_types=[attack_vector],
                source="correlation_analysis",
                first_seen=min(e.timestamp for e in events),
                last_seen=max(e.timestamp for e in events),
                reputation_score=0.1
            )
        ]
        
        incident = SecurityIncident(
            incident_id=f"CAM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hash(source_ip) % 10000:04d}",
            threat_level=threat_level,
            attack_vector=attack_vector,
            title=title,
            description=f"Campagne d'attaque coordonnée détectée: {len(events)} événements "
                       f"vers {len(unique_destinations)} destinations en "
                       f"{(max(e.timestamp for e in events) - min(e.timestamp for e in events)).total_seconds():.0f} secondes",
            indicators=indicators,
            affected_assets=list(unique_destinations),
            attack_timeline=[{
                "timestamp": e.timestamp.isoformat(),
                "event": f"Request to {e.destination_ip}:{e.destination_port}",
                "bytes": e.bytes_transferred
            } for e in events[:10]],  # Premiers 10 événements
            recommended_actions=self._generate_recommended_actions(threat_level, attack_vector),
            confidence_score=confidence,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return incident
    
    async def _process_security_incident(self, incident: SecurityIncident):
        """Traitement d'un incident de sécurité"""
        try:
            # Ajout à l'historique
            self.incidents_history.append(incident)
            self.active_threats[incident.incident_id] = incident
            
            # Notification via callback
            if self.alert_callback:
                await self.alert_callback(incident)
            
            # Communication vocale pour les incidents critiques
            if incident.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.CATASTROPHIC]:
                await self._voice_alert(incident)
            
            # Log de l'incident
            logger.warning(
                f"Incident de sécurité détecté: {incident.title} "
                f"(Niveau: {incident.threat_level.value}, "
                f"Confiance: {incident.confidence_score:.2f})"
            )
            
        except Exception as e:
            logger.error(f"Erreur traitement incident: {e}")
    
    async def _voice_alert(self, incident: SecurityIncident):
        """Alerte vocale pour les incidents critiques"""
        try:
            if not self.voice_callback:
                return
            
            # Adaptation du message selon le niveau de menace
            if incident.threat_level == ThreatLevel.CATASTROPHIC:
                message = f"ALERTE CRITIQUE MAXIMALE! {incident.title}. Réponse immédiate requise!"
                tone = "urgent"
            elif incident.threat_level == ThreatLevel.CRITICAL:
                message = f"ALERTE CRITIQUE! {incident.title}. Action immédiate nécessaire."
                tone = "urgent"
            else:
                message = f"Alerte de sécurité: {incident.title}"
                tone = "concerned"
            
            # Appel du callback vocal
            await self.voice_callback(message, tone, incident)
            
        except Exception as e:
            logger.error(f"Erreur alerte vocale: {e}")
    
    async def analyze_text_input(self, text: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse d'un input textuel pour détecter des menaces ou questions de sécurité"""
        try:
            # Analyse NLP du texte
            doc = self.nlp_model(text)
            
            # Extraction d'entités liées à la sécurité
            security_entities = []
            for ent in doc.ents:
                if ent.label_ in ["ORG", "GPE", "PERSON", "URL", "EMAIL"]:
                    security_entities.append({
                        "text": ent.text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char
                    })
            
            # Détection de patterns malicieux dans le texte
            malicious_patterns = await self._check_malicious_patterns(text)
            
            # Classification du type de requête
            intent = await self._classify_security_intent(text)
            
            # Évaluation du risque
            risk_score = await self._calculate_text_risk_score(text, malicious_patterns, intent)
            
            analysis_result = {
                "text": text,
                "security_entities": security_entities,
                "malicious_patterns": malicious_patterns,
                "intent": intent,
                "risk_score": risk_score,
                "timestamp": datetime.now().isoformat(),
                "user_context": user_context,
                "recommendations": await self._generate_text_recommendations(intent, risk_score)
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Erreur analyse texte: {e}")
            return {"error": str(e)}
    
    async def _classify_security_intent(self, text: str) -> str:
        """Classification de l'intention de sécurité"""
        security_keywords = {
            "incident_report": ["incident", "breach", "compromis", "attaque", "malware"],
            "vulnerability_inquiry": ["vulnérabilité", "faille", "CVE", "patch", "mise à jour"],
            "threat_intelligence": ["menace", "IOC", "indicateur", "campagne", "APT"],
            "policy_question": ["politique", "procédure", "conformité", "audit", "règle"],
            "technical_support": ["aide", "problème", "erreur", "configuration", "dépannage"],
            "general_security": ["sécurité", "protection", "prévention", "formation"]
        }
        
        text_lower = text.lower()
        intent_scores = {}
        
        for intent, keywords in security_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores.items(), key=lambda x: x[1])[0]
        else:
            return "general_inquiry"
    
    async def _calculate_text_risk_score(
        self, 
        text: str, 
        malicious_patterns: List[Tuple[str, float]], 
        intent: str
    ) -> float:
        """Calcul du score de risque d'un texte"""
        
        base_risk = 0.0
        
        # Risque basé sur les patterns malicieux
        if malicious_patterns:
            pattern_risk = max(confidence for _, confidence in malicious_patterns)
            base_risk += pattern_risk * 0.6
        
        # Risque basé sur l'intention
        intent_risk_map = {
            "incident_report": 0.3,
            "vulnerability_inquiry": 0.2,
            "threat_intelligence": 0.1,
            "technical_support": 0.1,
            "general_inquiry": 0.0
        }
        base_risk += intent_risk_map.get(intent, 0.0)
        
        # Facteurs additionnels
        suspicious_terms = [
            "backdoor", "rootkit", "exploit", "zero-day", "pwned",
            "botnet", "ransomware", "keylogger", "phishing"
        ]
        
        text_lower = text.lower()
        suspicious_count = sum(1 for term in suspicious_terms if term in text_lower)
        base_risk += min(0.3, suspicious_count * 0.1)
        
        return min(1.0, base_risk)
    
    async def _generate_text_recommendations(self, intent: str, risk_score: float) -> List[str]:
        """Génération de recommandations basées sur l'analyse du texte"""
        recommendations = []
        
        if risk_score > 0.7:
            recommendations.append("Escalade vers l'équipe de sécurité recommandée")
            recommendations.append("Investigation approfondie nécessaire")
        elif risk_score > 0.4:
            recommendations.append("Surveillance renforcée recommandée")
            recommendations.append("Vérification des logs d'activité")
        
        intent_recommendations = {
            "incident_report": [
                "Documenter tous les détails de l'incident",
                "Isoler les systèmes affectés si nécessaire",
                "Préserver les preuves numériques"
            ],
            "vulnerability_inquiry": [
                "Vérifier les derniers bulletins de sécurité",
                "Planifier les mises à jour critiques",
                "Évaluer l'exposition de l'infrastructure"
            ],
            "threat_intelligence": [
                "Corréler avec les feeds de threat intelligence",
                "Mettre à jour les règles de détection",
                "Partager avec la communauté de sécurité"
            ]
        }
        
        recommendations.extend(intent_recommendations.get(intent, []))
        
        return recommendations
    
    async def get_threat_summary(self) -> Dict[str, Any]:
        """Résumé de l'état des menaces"""
        try:
            active_incidents = len(self.active_threats)
            
            # Répartition par niveau de menace
            threat_distribution = {}
            for level in ThreatLevel:
                count = sum(1 for incident in self.active_threats.values() 
                           if incident.threat_level == level)
                threat_distribution[level.value] = count
            
            # Vecteurs d'attaque les plus fréquents
            attack_vectors = {}
            for incident in self.incidents_history[-100:]:  # 100 derniers incidents
                vector = incident.attack_vector.value
                attack_vectors[vector] = attack_vectors.get(vector, 0) + 1
            
            # Tendances temporelles (dernières 24h)
            last_24h = datetime.now() - timedelta(hours=24)
            recent_incidents = [
                incident for incident in self.incidents_history
                if incident.created_at > last_24h
            ]
            
            summary = {
                "active_incidents": active_incidents,
                "total_incidents_24h": len(recent_incidents),
                "threat_distribution": threat_distribution,
                "top_attack_vectors": dict(sorted(attack_vectors.items(), 
                                                key=lambda x: x[1], reverse=True)[:5]),
                "threat_intelligence_indicators": {
                    "malicious_ips": len(self.threat_intel_db["malicious_ips"]),
                    "malicious_domains": len(self.threat_intel_db["malicious_domains"]),
                    "malware_hashes": len(self.threat_intel_db["malware_hashes"])
                },
                "last_updated": datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Erreur génération résumé: {e}")
            return {"error": str(e)}
    
    def set_alert_callback(self, callback):
        """Configuration du callback d'alerte"""
        self.alert_callback = callback
    
    def set_voice_callback(self, callback):
        """Configuration du callback vocal"""
        self.voice_callback = callback
    
    async def update_threat_intelligence(self, indicators: List[ThreatIndicator]):
        """Mise à jour de la threat intelligence"""
        try:
            for indicator in indicators:
                if indicator.indicator_type == "ip":
                    self.threat_intel_db["malicious_ips"].add(indicator.value)
                elif indicator.indicator_type == "domain":
                    self.threat_intel_db["malicious_domains"].add(indicator.value)
                elif indicator.indicator_type == "hash":
                    self.threat_intel_db["malware_hashes"].add(indicator.value)
                
                # Mise en cache
                self.indicators_cache[indicator.value] = indicator
            
            logger.info(f"Mis à jour {len(indicators)} indicateurs de menace")
            
        except Exception as e:
            logger.error(f"Erreur mise à jour threat intelligence: {e}")
    
    def cleanup(self):
        """Nettoyage des ressources"""
        try:
            # Limitation de l'historique
            max_history = 10000
            if len(self.incidents_history) > max_history:
                self.incidents_history = self.incidents_history[-max_history:]
            
            if len(self.network_events) > max_history:
                self.network_events = self.network_events[-max_history:]
            
            # Nettoyage des menaces inactives (plus de 24h)
            cutoff_time = datetime.now() - timedelta(hours=24)
            inactive_threats = [
                incident_id for incident_id, incident in self.active_threats.items()
                if incident.updated_at < cutoff_time
            ]
            
            for incident_id in inactive_threats:
                del self.active_threats[incident_id]
            
            logger.info(f"Nettoyage effectué: {len(inactive_threats)} menaces inactives supprimées")
            
        except Exception as e:
            logger.error(f"Erreur nettoyage: {e}")
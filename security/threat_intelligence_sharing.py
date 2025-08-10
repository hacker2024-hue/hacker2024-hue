"""
Partage d'Intelligence sur les Menaces
======================================

Ce module implémente un système de partage d'intelligence sur les menaces
avec intégration MISP, STIX/TAXII et autres plateformes de partage.
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
import hashlib
import base64
import hmac
import requests
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import yaml
import csv
import io

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntelligenceSource(Enum):
    """Sources d'intelligence"""
    MISP = "misp"
    TAXII = "taxii"
    ALIENVAULT = "alienvault"
    VIRUSTOTAL = "virustotal"
    ABUSEIPDB = "abuseipdb"
    THREATFOX = "threatfox"
    CENSYS = "censys"
    SHODAN = "shodan"
    CUSTOM = "custom"

class IntelligenceType(Enum):
    """Types d'intelligence"""
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    HASH = "hash"
    EMAIL = "email"
    MALWARE = "malware"
    VULNERABILITY = "vulnerability"
    ATTACK_PATTERN = "attack_pattern"
    CAMPAIGN = "campaign"
    THREAT_ACTOR = "threat_actor"

class ConfidenceLevel(Enum):
    """Niveaux de confiance"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ThreatIntelligence:
    """Intelligence sur les menaces"""
    id: str
    type: IntelligenceType
    value: str
    source: IntelligenceSource
    confidence: ConfidenceLevel
    first_seen: datetime
    last_seen: datetime
    tags: List[str]
    description: str
    threat_level: str
    country: str
    asn: str
    category: str
    metadata: Dict[str, Any]
    raw_data: Dict[str, Any]

@dataclass
class IntelligenceFeed:
    """Flux d'intelligence"""
    id: str
    name: str
    source: IntelligenceSource
    url: str
    api_key: str
    enabled: bool
    update_interval: int
    last_update: datetime
    total_indicators: int
    format: str
    headers: Dict[str, str]
    filters: Dict[str, Any]

@dataclass
class STIXObject:
    """Objet STIX"""
    id: str
    type: str
    created: datetime
    modified: datetime
    name: str
    description: str
    labels: List[str]
    pattern: str
    valid_from: datetime
    valid_until: datetime
    confidence: int
    threat_level: str
    raw_data: Dict[str, Any]

class ThreatIntelligenceSharing:
    """
    Système de partage d'intelligence sur les menaces
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.intelligence_cache: Dict[str, ThreatIntelligence] = {}
        self.feeds: Dict[str, IntelligenceFeed] = {}
        self.stix_objects: Dict[str, STIXObject] = {}
        self.websocket_connections: Set[WebSocket] = set()
        
        # Configuration des sources d'intelligence
        self.intelligence_sources = {
            IntelligenceSource.MISP: {
                "base_url": "https://www.misp-project.org/",
                "api_version": "2.4",
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            },
            IntelligenceSource.TAXII: {
                "base_url": "https://taxii.example.com/",
                "version": "2.1",
                "headers": {
                    "Content-Type": "application/taxii+json;version=2.1",
                    "Accept": "application/taxii+json;version=2.1"
                }
            },
            IntelligenceSource.VIRUSTOTAL: {
                "base_url": "https://www.virustotal.com/vtapi/v2/",
                "headers": {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            },
            IntelligenceSource.ABUSEIPDB: {
                "base_url": "https://api.abuseipdb.com/api/v2/",
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            }
        }
        
        # Chargement des flux par défaut
        self._load_default_feeds()
        
    async def initialize(self):
        """Initialisation du système de partage d'intelligence"""
        logger.info("🌐 Initialisation du système de partage d'intelligence")
        
        # Chargement des flux depuis la base
        await self._load_feeds_from_db()
        
        # Démarrage des tâches en arrière-plan
        asyncio.create_task(self._feed_monitor())
        asyncio.create_task(self._intelligence_correlator())
        asyncio.create_task(self._stix_processor())
        asyncio.create_task(self._cache_cleaner())
        
        logger.info("✅ Système de partage d'intelligence initialisé")
    
    def _load_default_feeds(self):
        """Chargement des flux par défaut"""
        default_feeds = [
            IntelligenceFeed(
                id="misp_default",
                name="MISP Default Feed",
                source=IntelligenceSource.MISP,
                url="https://www.misp-project.org/feeds/",
                api_key="",
                enabled=True,
                update_interval=3600,  # 1 heure
                last_update=datetime.now(),
                total_indicators=0,
                format="json",
                headers={"Content-Type": "application/json"},
                filters={"tags": ["malware", "phishing", "apt"]}
            ),
            IntelligenceFeed(
                id="abuseipdb",
                name="AbuseIPDB Blacklist",
                source=IntelligenceSource.ABUSEIPDB,
                url="https://api.abuseipdb.com/api/v2/blacklist",
                api_key="",
                enabled=True,
                update_interval=1800,  # 30 minutes
                last_update=datetime.now(),
                total_indicators=0,
                format="json",
                headers={"Accept": "application/json"},
                filters={"confidenceMinimum": 90}
            ),
            IntelligenceFeed(
                id="threatfox",
                name="ThreatFox Malware Feed",
                source=IntelligenceSource.THREATFOX,
                url="https://threatfox-api.abuse.ch/export/csv/",
                api_key="",
                enabled=True,
                update_interval=7200,  # 2 heures
                last_update=datetime.now(),
                total_indicators=0,
                format="csv",
                headers={},
                filters={"malware_type": "all"}
            )
        ]
        
        for feed in default_feeds:
            self.feeds[feed.id] = feed
    
    async def _load_feeds_from_db(self):
        """Chargement des flux depuis la base de données"""
        try:
            keys = await self.redis.keys("feed:*")
            for key in keys:
                data = await self.redis.hgetall(key)
                if data:
                    # Reconstruction de l'objet IntelligenceFeed
                    # (simplifié pour l'exemple)
                    pass
        except Exception as e:
            logger.error(f"Erreur chargement flux: {e}")
    
    async def _feed_monitor(self):
        """Surveillance des flux d'intelligence"""
        while True:
            try:
                await self._update_feeds()
                await asyncio.sleep(300)  # 5 minutes
            except Exception as e:
                logger.error(f"Erreur surveillance flux: {e}")
                await asyncio.sleep(60)
    
    async def _update_feeds(self):
        """Mise à jour des flux d'intelligence"""
        current_time = datetime.now()
        
        for feed_id, feed in self.feeds.items():
            if not feed.enabled:
                continue
            
            # Vérification si une mise à jour est nécessaire
            time_since_update = (current_time - feed.last_update).total_seconds()
            
            if time_since_update >= feed.update_interval:
                logger.info(f"🔄 Mise à jour du flux: {feed.name}")
                
                try:
                    await self._update_feed(feed)
                    feed.last_update = current_time
                    
                    # Sauvegarde en base
                    await self._save_feed(feed)
                    
                except Exception as e:
                    logger.error(f"Erreur mise à jour flux {feed.name}: {e}")
    
    async def _update_feed(self, feed: IntelligenceFeed):
        """Mise à jour d'un flux spécifique"""
        if feed.source == IntelligenceSource.MISP:
            await self._update_misp_feed(feed)
        elif feed.source == IntelligenceSource.ABUSEIPDB:
            await self._update_abuseipdb_feed(feed)
        elif feed.source == IntelligenceSource.THREATFOX:
            await self._update_threatfox_feed(feed)
        elif feed.source == IntelligenceSource.TAXII:
            await self._update_taxii_feed(feed)
        else:
            await self._update_generic_feed(feed)
    
    async def _update_misp_feed(self, feed: IntelligenceFeed):
        """Mise à jour d'un flux MISP"""
        try:
            # Construction de l'URL
            url = urljoin(feed.url, "events/index")
            
            # Paramètres de requête
            params = {
                "limit": 100,
                "page": 1,
                "published": 1
            }
            
            # Ajout des filtres
            if "tags" in feed.filters:
                params["tags"] = ",".join(feed.filters["tags"])
            
            # Requête HTTP
            async with aiohttp.ClientSession() as session:
                headers = feed.headers.copy()
                if feed.api_key:
                    headers["Authorization"] = f"Bearer {feed.api_key}"
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Traitement des événements MISP
                        for event in data.get("response", []):
                            await self._process_misp_event(event, feed)
                        
                        feed.total_indicators = len(data.get("response", []))
                        logger.info(f"📊 Flux MISP mis à jour: {feed.total_indicators} événements")
                    else:
                        logger.error(f"Erreur API MISP: {response.status}")
        
        except Exception as e:
            logger.error(f"Erreur mise à jour flux MISP: {e}")
    
    async def _process_misp_event(self, event: Dict[str, Any], feed: IntelligenceFeed):
        """Traitement d'un événement MISP"""
        try:
            event_id = event.get("Event", {}).get("id")
            event_info = event.get("Event", {}).get("info", "")
            event_tags = [tag.get("name") for tag in event.get("Event", {}).get("Tag", [])]
            
            # Traitement des attributs
            for attribute in event.get("Event", {}).get("Attribute", []):
                attribute_type = attribute.get("type")
                attribute_value = attribute.get("value")
                attribute_category = attribute.get("category", "")
                
                if attribute_type and attribute_value:
                    # Création de l'intelligence
                    intelligence = ThreatIntelligence(
                        id=f"misp_{event_id}_{hash(attribute_value)}",
                        type=self._map_misp_type(attribute_type),
                        value=attribute_value,
                        source=IntelligenceSource.MISP,
                        confidence=self._calculate_confidence(attribute),
                        first_seen=datetime.fromisoformat(attribute.get("first_seen", datetime.now().isoformat())),
                        last_seen=datetime.fromisoformat(attribute.get("last_seen", datetime.now().isoformat())),
                        tags=event_tags + [attribute_category],
                        description=event_info,
                        threat_level=attribute.get("threat_level", "medium"),
                        country=attribute.get("to_ids", {}).get("country", ""),
                        asn=attribute.get("to_ids", {}).get("asn", ""),
                        category=attribute_category,
                        metadata={
                            "misp_event_id": event_id,
                            "misp_attribute_id": attribute.get("id"),
                            "distribution": attribute.get("distribution", 0),
                            "to_ids": attribute.get("to_ids", False)
                        },
                        raw_data=attribute
                    )
                    
                    # Stockage de l'intelligence
                    await self._store_intelligence(intelligence)
        
        except Exception as e:
            logger.error(f"Erreur traitement événement MISP: {e}")
    
    def _map_misp_type(self, misp_type: str) -> IntelligenceType:
        """Mapping des types MISP vers IntelligenceType"""
        mapping = {
            "ip-src": IntelligenceType.IP,
            "ip-dst": IntelligenceType.IP,
            "domain": IntelligenceType.DOMAIN,
            "url": IntelligenceType.URL,
            "md5": IntelligenceType.HASH,
            "sha1": IntelligenceType.HASH,
            "sha256": IntelligenceType.HASH,
            "email-src": IntelligenceType.EMAIL,
            "email-dst": IntelligenceType.EMAIL,
            "malware-sample": IntelligenceType.MALWARE,
            "vulnerability": IntelligenceType.VULNERABILITY
        }
        
        return mapping.get(misp_type, IntelligenceType.IP)
    
    def _calculate_confidence(self, attribute: Dict[str, Any]) -> ConfidenceLevel:
        """Calcul du niveau de confiance"""
        # Logique de calcul basée sur les métadonnées MISP
        score = 0
        
        # Score basé sur la distribution
        distribution = attribute.get("distribution", 0)
        if distribution == 0:  # This Organisation
            score += 2
        elif distribution == 1:  # This Community
            score += 1
        
        # Score basé sur to_ids
        if attribute.get("to_ids", False):
            score += 1
        
        # Score basé sur les tags
        tags = attribute.get("Tag", [])
        if any("high" in tag.get("name", "").lower() for tag in tags):
            score += 1
        
        # Mapping vers ConfidenceLevel
        if score >= 3:
            return ConfidenceLevel.CRITICAL
        elif score >= 2:
            return ConfidenceLevel.HIGH
        elif score >= 1:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    async def _update_abuseipdb_feed(self, feed: IntelligenceFeed):
        """Mise à jour d'un flux AbuseIPDB"""
        try:
            url = feed.url
            
            # Paramètres de requête
            params = {
                "confidenceMinimum": feed.filters.get("confidenceMinimum", 90),
                "limit": 1000
            }
            
            # Requête HTTP
            async with aiohttp.ClientSession() as session:
                headers = feed.headers.copy()
                if feed.api_key:
                    headers["Key"] = feed.api_key
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Traitement des IPs
                        for ip_data in data.get("data", []):
                            await self._process_abuseipdb_entry(ip_data, feed)
                        
                        feed.total_indicators = len(data.get("data", []))
                        logger.info(f"📊 Flux AbuseIPDB mis à jour: {feed.total_indicators} IPs")
                    else:
                        logger.error(f"Erreur API AbuseIPDB: {response.status}")
        
        except Exception as e:
            logger.error(f"Erreur mise à jour flux AbuseIPDB: {e}")
    
    async def _process_abuseipdb_entry(self, ip_data: Dict[str, Any], feed: IntelligenceFeed):
        """Traitement d'une entrée AbuseIPDB"""
        try:
            ip_address = ip_data.get("ipAddress")
            abuse_confidence = ip_data.get("abuseConfidenceScore", 0)
            country_code = ip_data.get("countryCode", "")
            usage_type = ip_data.get("usageType", "")
            
            # Création de l'intelligence
            intelligence = ThreatIntelligence(
                id=f"abuseipdb_{hash(ip_address)}",
                type=IntelligenceType.IP,
                value=ip_address,
                source=IntelligenceSource.ABUSEIPDB,
                confidence=self._map_abuseipdb_confidence(abuse_confidence),
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                tags=["abuseipdb", "blacklist"],
                description=f"IP malveillante détectée par AbuseIPDB (Score: {abuse_confidence}%)",
                threat_level="high" if abuse_confidence > 80 else "medium",
                country=country_code,
                asn="",
                category="malware",
                metadata={
                    "abuse_confidence": abuse_confidence,
                    "usage_type": usage_type,
                    "total_reports": ip_data.get("totalReports", 0),
                    "last_reported": ip_data.get("lastReportedAt", "")
                },
                raw_data=ip_data
            )
            
            # Stockage de l'intelligence
            await self._store_intelligence(intelligence)
        
        except Exception as e:
            logger.error(f"Erreur traitement entrée AbuseIPDB: {e}")
    
    def _map_abuseipdb_confidence(self, confidence_score: int) -> ConfidenceLevel:
        """Mapping du score de confiance AbuseIPDB"""
        if confidence_score >= 90:
            return ConfidenceLevel.CRITICAL
        elif confidence_score >= 70:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 50:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    async def _update_threatfox_feed(self, feed: IntelligenceFeed):
        """Mise à jour d'un flux ThreatFox"""
        try:
            url = feed.url
            
            # Requête HTTP
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        csv_data = await response.text()
                        
                        # Parsing CSV
                        csv_reader = csv.DictReader(io.StringIO(csv_data))
                        
                        count = 0
                        for row in csv_reader:
                            await self._process_threatfox_entry(row, feed)
                            count += 1
                        
                        feed.total_indicators = count
                        logger.info(f"📊 Flux ThreatFox mis à jour: {feed.total_indicators} entrées")
                    else:
                        logger.error(f"Erreur API ThreatFox: {response.status}")
        
        except Exception as e:
            logger.error(f"Erreur mise à jour flux ThreatFox: {e}")
    
    async def _process_threatfox_entry(self, entry: Dict[str, str], feed: IntelligenceFeed):
        """Traitement d'une entrée ThreatFox"""
        try:
            malware_type = entry.get("malware_type", "")
            malware_name = entry.get("malware_name", "")
            malware_hash = entry.get("md5_hash", "")
            
            if malware_hash:
                # Création de l'intelligence
                intelligence = ThreatIntelligence(
                    id=f"threatfox_{hash(malware_hash)}",
                    type=IntelligenceType.MALWARE,
                    value=malware_hash,
                    source=IntelligenceSource.THREATFOX,
                    confidence=ConfidenceLevel.HIGH,
                    first_seen=datetime.now(),
                    last_seen=datetime.now(),
                    tags=["threatfox", "malware", malware_type],
                    description=f"Malware détecté: {malware_name} ({malware_type})",
                    threat_level="high",
                    country="",
                    asn="",
                    category="malware",
                    metadata={
                        "malware_type": malware_type,
                        "malware_name": malware_name,
                        "platform": entry.get("platform", ""),
                        "status": entry.get("status", "")
                    },
                    raw_data=entry
                )
                
                # Stockage de l'intelligence
                await self._store_intelligence(intelligence)
        
        except Exception as e:
            logger.error(f"Erreur traitement entrée ThreatFox: {e}")
    
    async def _update_taxii_feed(self, feed: IntelligenceFeed):
        """Mise à jour d'un flux TAXII"""
        try:
            # Implémentation TAXII 2.1
            # Cette partie nécessiterait une implémentation complète du protocole TAXII
            logger.info("🔄 Mise à jour flux TAXII (non implémenté)")
        
        except Exception as e:
            logger.error(f"Erreur mise à jour flux TAXII: {e}")
    
    async def _update_generic_feed(self, feed: IntelligenceFeed):
        """Mise à jour d'un flux générique"""
        try:
            # Requête HTTP générique
            async with aiohttp.ClientSession() as session:
                headers = feed.headers.copy()
                if feed.api_key:
                    headers["Authorization"] = f"Bearer {feed.api_key}"
                
                async with session.get(feed.url, headers=headers) as response:
                    if response.status == 200:
                        if feed.format == "json":
                            data = await response.json()
                        elif feed.format == "csv":
                            csv_data = await response.text()
                            data = list(csv.DictReader(io.StringIO(csv_data)))
                        else:
                            data = await response.text()
                        
                        # Traitement générique
                        await self._process_generic_feed(data, feed)
                        
                        logger.info(f"📊 Flux générique mis à jour: {feed.name}")
                    else:
                        logger.error(f"Erreur flux générique: {response.status}")
        
        except Exception as e:
            logger.error(f"Erreur mise à jour flux générique: {e}")
    
    async def _process_generic_feed(self, data: Any, feed: IntelligenceFeed):
        """Traitement d'un flux générique"""
        # Implémentation générique selon le format
        pass
    
    async def _store_intelligence(self, intelligence: ThreatIntelligence):
        """Stockage d'une intelligence"""
        try:
            # Stockage en cache
            self.intelligence_cache[intelligence.id] = intelligence
            
            # Stockage en base Redis
            await self.redis.hset(
                f"intelligence:{intelligence.id}",
                mapping=asdict(intelligence)
            )
            
            # Expiration (30 jours)
            await self.redis.expire(f"intelligence:{intelligence.id}", 2592000)
            
            # Notification via WebSocket
            await self._notify_intelligence(intelligence)
            
        except Exception as e:
            logger.error(f"Erreur stockage intelligence: {e}")
    
    async def _intelligence_correlator(self):
        """Corrélateur d'intelligence"""
        while True:
            try:
                await self._correlate_intelligence()
                await asyncio.sleep(600)  # 10 minutes
            except Exception as e:
                logger.error(f"Erreur corrélation intelligence: {e}")
                await asyncio.sleep(300)
    
    async def _correlate_intelligence(self):
        """Corrélation des intelligences"""
        # Recherche de corrélations entre différentes sources
        intelligence_list = list(self.intelligence_cache.values())
        
        for i, intel1 in enumerate(intelligence_list):
            for intel2 in intelligence_list[i+1:]:
                if self._are_correlated(intel1, intel2):
                    await self._create_correlation(intel1, intel2)
    
    def _are_correlated(self, intel1: ThreatIntelligence, intel2: ThreatIntelligence) -> bool:
        """Vérification si deux intelligences sont corrélées"""
        # Corrélation par valeur
        if intel1.value == intel2.value and intel1.type == intel2.type:
            return True
        
        # Corrélation par tags communs
        common_tags = set(intel1.tags) & set(intel2.tags)
        if len(common_tags) >= 2:
            return True
        
        # Corrélation par pays
        if intel1.country and intel2.country and intel1.country == intel2.country:
            return True
        
        return False
    
    async def _create_correlation(self, intel1: ThreatIntelligence, intel2: ThreatIntelligence):
        """Création d'une corrélation"""
        correlation_id = f"corr_{hash(intel1.id + intel2.id)}"
        
        correlation_data = {
            "id": correlation_id,
            "intelligence_ids": [intel1.id, intel2.id],
            "confidence": min(intel1.confidence.value, intel2.confidence.value),
            "timestamp": datetime.now().isoformat(),
            "description": f"Corrélation entre {intel1.source.value} et {intel2.source.value}"
        }
        
        # Stockage de la corrélation
        await self.redis.hset(f"correlation:{correlation_id}", mapping=correlation_data)
        
        logger.info(f"🔗 Corrélation créée: {correlation_id}")
    
    async def _stix_processor(self):
        """Processeur STIX"""
        while True:
            try:
                await self._process_stix_objects()
                await asyncio.sleep(1800)  # 30 minutes
            except Exception as e:
                logger.error(f"Erreur traitement STIX: {e}")
                await asyncio.sleep(900)
    
    async def _process_stix_objects(self):
        """Traitement des objets STIX"""
        # Conversion des intelligences en objets STIX
        for intelligence in self.intelligence_cache.values():
            stix_object = self._convert_to_stix(intelligence)
            if stix_object:
                self.stix_objects[stix_object.id] = stix_object
    
    def _convert_to_stix(self, intelligence: ThreatIntelligence) -> Optional[STIXObject]:
        """Conversion d'une intelligence en objet STIX"""
        try:
            # Création d'un pattern STIX
            pattern = self._create_stix_pattern(intelligence)
            
            if pattern:
                return STIXObject(
                    id=f"indicator--{intelligence.id}",
                    type="indicator",
                    created=intelligence.first_seen,
                    modified=intelligence.last_seen,
                    name=f"Indicator for {intelligence.value}",
                    description=intelligence.description,
                    labels=intelligence.tags,
                    pattern=pattern,
                    valid_from=intelligence.first_seen,
                    valid_until=intelligence.last_seen + timedelta(days=365),
                    confidence=intelligence.confidence.value,
                    threat_level=intelligence.threat_level,
                    raw_data=intelligence.raw_data
                )
        
        except Exception as e:
            logger.error(f"Erreur conversion STIX: {e}")
        
        return None
    
    def _create_stix_pattern(self, intelligence: ThreatIntelligence) -> str:
        """Création d'un pattern STIX"""
        if intelligence.type == IntelligenceType.IP:
            return f"[ipv4-addr:value = '{intelligence.value}']"
        elif intelligence.type == IntelligenceType.DOMAIN:
            return f"[domain-name:value = '{intelligence.value}']"
        elif intelligence.type == IntelligenceType.URL:
            return f"[url:value = '{intelligence.value}']"
        elif intelligence.type == IntelligenceType.HASH:
            return f"[file:hashes.MD5 = '{intelligence.value}']"
        else:
            return ""
    
    async def _cache_cleaner(self):
        """Nettoyeur de cache"""
        while True:
            try:
                await self._clean_cache()
                await asyncio.sleep(3600)  # 1 heure
            except Exception as e:
                logger.error(f"Erreur nettoyage cache: {e}")
                await asyncio.sleep(1800)
    
    async def _clean_cache(self):
        """Nettoyage du cache"""
        current_time = datetime.now()
        expired_keys = []
        
        for intel_id, intelligence in self.intelligence_cache.items():
            # Suppression des intelligences expirées (plus de 30 jours)
            if (current_time - intelligence.last_seen).days > 30:
                expired_keys.append(intel_id)
        
        for key in expired_keys:
            del self.intelligence_cache[key]
            await self.redis.delete(f"intelligence:{key}")
        
        if expired_keys:
            logger.info(f"🧹 Cache nettoyé: {len(expired_keys)} entrées supprimées")
    
    async def _save_feed(self, feed: IntelligenceFeed):
        """Sauvegarde d'un flux en base"""
        try:
            await self.redis.hset(
                f"feed:{feed.id}",
                mapping=asdict(feed)
            )
        except Exception as e:
            logger.error(f"Erreur sauvegarde flux: {e}")
    
    async def _notify_intelligence(self, intelligence: ThreatIntelligence):
        """Notification d'une intelligence via WebSocket"""
        message = {
            "type": "threat_intelligence",
            "intelligence": asdict(intelligence),
            "timestamp": datetime.now().isoformat()
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket: {e}")
                self.websocket_connections.discard(websocket)
    
    async def add_websocket_connection(self, websocket: WebSocket):
        """Ajout d'une connexion WebSocket"""
        self.websocket_connections.add(websocket)
    
    async def remove_websocket_connection(self, websocket: WebSocket):
        """Suppression d'une connexion WebSocket"""
        self.websocket_connections.discard(websocket)
    
    async def search_intelligence(self, query: str, intelligence_type: IntelligenceType = None) -> List[ThreatIntelligence]:
        """Recherche d'intelligence"""
        results = []
        
        for intelligence in self.intelligence_cache.values():
            if intelligence_type and intelligence.type != intelligence_type:
                continue
            
            # Recherche dans la valeur
            if query.lower() in intelligence.value.lower():
                results.append(intelligence)
                continue
            
            # Recherche dans la description
            if query.lower() in intelligence.description.lower():
                results.append(intelligence)
                continue
            
            # Recherche dans les tags
            if any(query.lower() in tag.lower() for tag in intelligence.tags):
                results.append(intelligence)
                continue
        
        return results
    
    async def get_intelligence_statistics(self) -> Dict[str, Any]:
        """Statistiques d'intelligence"""
        total_intelligence = len(self.intelligence_cache)
        
        # Statistiques par type
        type_stats = {}
        for intel_type in IntelligenceType:
            count = sum(1 for intel in self.intelligence_cache.values() if intel.type == intel_type)
            type_stats[intel_type.value] = count
        
        # Statistiques par source
        source_stats = {}
        for source in IntelligenceSource:
            count = sum(1 for intel in self.intelligence_cache.values() if intel.source == source)
            source_stats[source.value] = count
        
        # Statistiques par niveau de confiance
        confidence_stats = {}
        for confidence in ConfidenceLevel:
            count = sum(1 for intel in self.intelligence_cache.values() if intel.confidence == confidence)
            confidence_stats[confidence.name] = count
        
        return {
            "total_intelligence": total_intelligence,
            "by_type": type_stats,
            "by_source": source_stats,
            "by_confidence": confidence_stats,
            "total_feeds": len(self.feeds),
            "active_feeds": sum(1 for feed in self.feeds.values() if feed.enabled)
        }
    
    async def get_intelligence_history(self) -> List[ThreatIntelligence]:
        """Historique d'intelligence"""
        return list(self.intelligence_cache.values())
    
    async def add_custom_intelligence(self, intelligence: ThreatIntelligence):
        """Ajout d'intelligence personnalisée"""
        intelligence.id = f"custom_{int(time.time())}_{hash(intelligence.value)}"
        intelligence.source = IntelligenceSource.CUSTOM
        intelligence.first_seen = datetime.now()
        intelligence.last_seen = datetime.now()
        
        await self._store_intelligence(intelligence)
        
        return intelligence
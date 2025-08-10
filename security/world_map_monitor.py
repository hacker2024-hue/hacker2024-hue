"""
Surveillance Mondiale avec Carte Interactive
============================================

Ce module implémente une surveillance mondiale des cyberattaques
avec une carte interactive et les informations de contact du développeur.
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
from fastapi import WebSocket, HTTPException
from fastapi.responses import HTMLResponse
import folium
from folium import plugins
import geopy
from geopy.geocoders import Nominatim
import ipaddress
import requests
import random

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatLocation(Enum):
    """Types de localisation de menaces"""
    SOURCE = "source"
    DESTINATION = "destination"
    VICTIM = "victim"
    ATTACKER = "attacker"

@dataclass
class WorldThreat:
    """Menace mondiale"""
    id: str
    timestamp: datetime
    threat_type: str
    source_ip: str
    destination_ip: str
    source_country: str
    source_city: str
    source_lat: float
    source_lng: float
    dest_country: str
    dest_city: str
    dest_lat: float
    dest_lng: float
    threat_level: str
    description: str
    indicators: List[str]
    metadata: Dict[str, Any]

@dataclass
class WorldStatistics:
    """Statistiques mondiales"""
    total_threats: int
    threats_by_country: Dict[str, int]
    threats_by_type: Dict[str, int]
    active_attacks: int
    blocked_attacks: int
    global_risk_level: str
    top_attackers: List[str]
    top_victims: List[str]
    last_update: datetime

class WorldMapMonitor:
    """
    Moniteur de carte mondiale des cyberattaques
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.world_threats: Dict[str, WorldThreat] = {}
        self.websocket_connections: Set[WebSocket] = set()
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "title": "Développeur du Système Mondial de Défense Cybernétique",
            "contacts": {
                "primary": "hackerduckman89@gmail.com",
                "secondary": "yao.kouakou.dev@gmail.com"
            },
            "version": "2.0.0 - Edition Mondiale",
            "description": "Expert en cybersécurité et développement de systèmes de défense avancés"
        }
        
        # Configuration de la géolocalisation
        self.geolocator = Nominatim(user_agent="cyber_defense_world_map")
        
        # Cache de géolocalisation
        self.geo_cache = {}
        
        # Statistiques mondiales
        self.world_stats = WorldStatistics(
            total_threats=0,
            threats_by_country={},
            threats_by_type={},
            active_attacks=0,
            blocked_attacks=0,
            global_risk_level="LOW",
            top_attackers=[],
            top_victims=[],
            last_update=datetime.now()
        )
        
    async def initialize(self):
        """Initialisation du moniteur mondial"""
        logger.info("🌍 Initialisation du moniteur de carte mondiale")
        
        # Chargement des menaces existantes
        await self._load_existing_threats()
        
        # Démarrage des tâches en arrière-plan
        asyncio.create_task(self._world_statistics_updater())
        asyncio.create_task(self._threat_geolocator())
        asyncio.create_task(self._global_risk_analyzer())
        
        logger.info("✅ Moniteur de carte mondiale initialisé")
    
    async def _load_existing_threats(self):
        """Chargement des menaces existantes"""
        try:
            keys = await self.redis.keys("world_threat:*")
            for key in keys:
                data = await self.redis.hgetall(key)
                if data:
                    # Reconstruction de l'objet WorldThreat
                    threat = WorldThreat(
                        id=data.get("id", ""),
                        timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
                        threat_type=data.get("threat_type", ""),
                        source_ip=data.get("source_ip", ""),
                        destination_ip=data.get("destination_ip", ""),
                        source_country=data.get("source_country", ""),
                        source_city=data.get("source_city", ""),
                        source_lat=float(data.get("source_lat", 0)),
                        source_lng=float(data.get("source_lng", 0)),
                        dest_country=data.get("dest_country", ""),
                        dest_city=data.get("dest_city", ""),
                        dest_lat=float(data.get("dest_lat", 0)),
                        dest_lng=float(data.get("dest_lng", 0)),
                        threat_level=data.get("threat_level", ""),
                        description=data.get("description", ""),
                        indicators=json.loads(data.get("indicators", "[]")),
                        metadata=json.loads(data.get("metadata", "{}"))
                    )
                    self.world_threats[threat.id] = threat
        except Exception as e:
            logger.error(f"Erreur chargement menaces mondiales: {e}")
    
    async def add_world_threat(self, threat_data: Dict[str, Any]) -> WorldThreat:
        """Ajout d'une menace mondiale"""
        try:
            # Génération de l'ID
            threat_id = f"world_threat_{int(time.time())}_{hash(threat_data.get('source_ip', ''))}"
            
            # Géolocalisation des IPs
            source_geo = await self._geolocate_ip(threat_data.get('source_ip', ''))
            dest_geo = await self._geolocate_ip(threat_data.get('destination_ip', ''))
            
            # Création de l'objet WorldThreat
            threat = WorldThreat(
                id=threat_id,
                timestamp=datetime.now(),
                threat_type=threat_data.get('threat_type', 'unknown'),
                source_ip=threat_data.get('source_ip', ''),
                destination_ip=threat_data.get('destination_ip', ''),
                source_country=source_geo.get('country', 'Unknown'),
                source_city=source_geo.get('city', 'Unknown'),
                source_lat=source_geo.get('lat', 0),
                source_lng=source_geo.get('lng', 0),
                dest_country=dest_geo.get('country', 'Unknown'),
                dest_city=dest_geo.get('city', 'Unknown'),
                dest_lat=dest_geo.get('lat', 0),
                dest_lng=dest_geo.get('lng', 0),
                threat_level=threat_data.get('threat_level', 'medium'),
                description=threat_data.get('description', ''),
                indicators=threat_data.get('indicators', []),
                metadata=threat_data.get('metadata', {})
            )
            
            # Stockage de la menace
            self.world_threats[threat_id] = threat
            
            # Sauvegarde en Redis
            await self._save_threat_to_redis(threat)
            
            # Notification via WebSocket
            await self._notify_world_threat(threat)
            
            logger.info(f"🌍 Menace mondiale ajoutée: {threat_id} ({threat.source_country} → {threat.dest_country})")
            
            return threat
            
        except Exception as e:
            logger.error(f"Erreur ajout menace mondiale: {e}")
            raise
    
    async def _geolocate_ip(self, ip_address: str) -> Dict[str, Any]:
        """Géolocalisation d'une adresse IP"""
        if not ip_address or ip_address in self.geo_cache:
            return self.geo_cache.get(ip_address, {
                'country': 'Unknown',
                'city': 'Unknown',
                'lat': 0,
                'lng': 0
            })
        
        try:
            # Vérification si c'est une IP privée
            if ipaddress.ip_address(ip_address).is_private:
                return {
                    'country': 'Private Network',
                    'city': 'Local',
                    'lat': 0,
                    'lng': 0
                }
            
            # Utilisation d'un service de géolocalisation
            async with aiohttp.ClientSession() as session:
                url = f"http://ip-api.com/json/{ip_address}"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        geo_data = {
                            'country': data.get('country', 'Unknown'),
                            'city': data.get('city', 'Unknown'),
                            'lat': data.get('lat', 0),
                            'lng': data.get('lon', 0)
                        }
                        
                        # Mise en cache
                        self.geo_cache[ip_address] = geo_data
                        
                        return geo_data
                    else:
                        return {
                            'country': 'Unknown',
                            'city': 'Unknown',
                            'lat': 0,
                            'lng': 0
                        }
        
        except Exception as e:
            logger.error(f"Erreur géolocalisation IP {ip_address}: {e}")
            return {
                'country': 'Unknown',
                'city': 'Unknown',
                'lat': 0,
                'lng': 0
            }
    
    async def _save_threat_to_redis(self, threat: WorldThreat):
        """Sauvegarde d'une menace en Redis"""
        try:
            await self.redis.hset(
                f"world_threat:{threat.id}",
                mapping={
                    "id": threat.id,
                    "timestamp": threat.timestamp.isoformat(),
                    "threat_type": threat.threat_type,
                    "source_ip": threat.source_ip,
                    "destination_ip": threat.destination_ip,
                    "source_country": threat.source_country,
                    "source_city": threat.source_city,
                    "source_lat": str(threat.source_lat),
                    "source_lng": str(threat.source_lng),
                    "dest_country": threat.dest_country,
                    "dest_city": threat.dest_city,
                    "dest_lat": str(threat.dest_lat),
                    "dest_lng": str(threat.dest_lng),
                    "threat_level": threat.threat_level,
                    "description": threat.description,
                    "indicators": json.dumps(threat.indicators),
                    "metadata": json.dumps(threat.metadata)
                }
            )
            
            # Expiration (30 jours)
            await self.redis.expire(f"world_threat:{threat.id}", 2592000)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde menace Redis: {e}")
    
    async def _world_statistics_updater(self):
        """Mise à jour des statistiques mondiales"""
        while True:
            try:
                await self._update_world_statistics()
                await asyncio.sleep(300)  # 5 minutes
            except Exception as e:
                logger.error(f"Erreur mise à jour statistiques mondiales: {e}")
                await asyncio.sleep(60)
    
    async def _update_world_statistics(self):
        """Mise à jour des statistiques mondiales"""
        try:
            threats = list(self.world_threats.values())
            
            # Statistiques par pays
            threats_by_country = {}
            threats_by_type = {}
            
            for threat in threats:
                # Par pays source
                source_country = threat.source_country
                threats_by_country[source_country] = threats_by_country.get(source_country, 0) + 1
                
                # Par type de menace
                threat_type = threat.threat_type
                threats_by_type[threat_type] = threats_by_type.get(threat_type, 0) + 1
            
            # Top attaquants et victimes
            attacker_counts = {}
            victim_counts = {}
            
            for threat in threats:
                attacker_counts[threat.source_country] = attacker_counts.get(threat.source_country, 0) + 1
                victim_counts[threat.dest_country] = victim_counts.get(threat.dest_country, 0) + 1
            
            top_attackers = sorted(attacker_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            top_victims = sorted(victim_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Calcul du niveau de risque global
            total_threats = len(threats)
            critical_threats = sum(1 for t in threats if t.threat_level == 'critical')
            high_threats = sum(1 for t in threats if t.threat_level == 'high')
            
            if critical_threats > 10 or high_threats > 50:
                global_risk = "CRITICAL"
            elif critical_threats > 5 or high_threats > 25:
                global_risk = "HIGH"
            elif critical_threats > 2 or high_threats > 10:
                global_risk = "MEDIUM"
            else:
                global_risk = "LOW"
            
            # Mise à jour des statistiques
            self.world_stats = WorldStatistics(
                total_threats=total_threats,
                threats_by_country=threats_by_country,
                threats_by_type=threats_by_type,
                active_attacks=sum(1 for t in threats if (datetime.now() - t.timestamp).seconds < 3600),
                blocked_attacks=sum(1 for t in threats if t.metadata.get('blocked', False)),
                global_risk_level=global_risk,
                top_attackers=[country for country, _ in top_attackers],
                top_victims=[country for country, _ in top_victims],
                last_update=datetime.now()
            )
            
            logger.info(f"📊 Statistiques mondiales mises à jour: {total_threats} menaces, risque {global_risk}")
            
        except Exception as e:
            logger.error(f"Erreur calcul statistiques mondiales: {e}")
    
    async def _threat_geolocator(self):
        """Géolocalisation des menaces en arrière-plan"""
        while True:
            try:
                # Géolocalisation des menaces sans coordonnées
                threats_to_geolocate = [
                    threat for threat in self.world_threats.values()
                    if threat.source_lat == 0 and threat.source_lng == 0
                ]
                
                for threat in threats_to_geolocate[:10]:  # Limite à 10 par cycle
                    geo_data = await self._geolocate_ip(threat.source_ip)
                    threat.source_lat = geo_data['lat']
                    threat.source_lng = geo_data['lng']
                    threat.source_country = geo_data['country']
                    threat.source_city = geo_data['city']
                    
                    # Mise à jour en Redis
                    await self._save_threat_to_redis(threat)
                
                await asyncio.sleep(60)  # 1 minute
            except Exception as e:
                logger.error(f"Erreur géolocalisation arrière-plan: {e}")
                await asyncio.sleep(300)
    
    async def _global_risk_analyzer(self):
        """Analyseur de risque global"""
        while True:
            try:
                await self._analyze_global_risk()
                await asyncio.sleep(1800)  # 30 minutes
            except Exception as e:
                logger.error(f"Erreur analyse risque global: {e}")
                await asyncio.sleep(900)
    
    async def _analyze_global_risk(self):
        """Analyse du risque global"""
        try:
            # Analyse des tendances
            recent_threats = [
                threat for threat in self.world_threats.values()
                if (datetime.now() - threat.timestamp).seconds < 3600
            ]
            
            if len(recent_threats) > 100:
                logger.warning("⚠️ Activité cybernétique élevée détectée globalement")
                
                # Notification aux administrateurs
                alert_data = {
                    "type": "global_risk_alert",
                    "level": "HIGH",
                    "message": f"Activité cybernétique élevée: {len(recent_threats)} menaces en 1h",
                    "timestamp": datetime.now().isoformat(),
                    "developer_contact": self.developer_info["contacts"]["primary"]
                }
                
                await self._notify_global_alert(alert_data)
        
        except Exception as e:
            logger.error(f"Erreur analyse risque global: {e}")
    
    async def _notify_world_threat(self, threat: WorldThreat):
        """Notification d'une menace mondiale via WebSocket"""
        message = {
            "type": "world_threat",
            "threat": asdict(threat),
            "timestamp": datetime.now().isoformat(),
            "developer_info": self.developer_info
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket menace mondiale: {e}")
                self.websocket_connections.discard(websocket)
    
    async def _notify_global_alert(self, alert_data: Dict[str, Any]):
        """Notification d'alerte globale"""
        message = {
            "type": "global_alert",
            "alert": alert_data,
            "timestamp": datetime.now().isoformat(),
            "developer_info": self.developer_info
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket alerte globale: {e}")
                self.websocket_connections.discard(websocket)
    
    async def add_websocket_connection(self, websocket: WebSocket):
        """Ajout d'une connexion WebSocket"""
        self.websocket_connections.add(websocket)
    
    async def remove_websocket_connection(self, websocket: WebSocket):
        """Suppression d'une connexion WebSocket"""
        self.websocket_connections.discard(websocket)
    
    async def get_world_statistics(self) -> WorldStatistics:
        """Récupération des statistiques mondiales"""
        return self.world_stats
    
    async def get_world_threats(self) -> List[WorldThreat]:
        """Récupération des menaces mondiales"""
        return list(self.world_threats.values())
    
    async def get_developer_info(self) -> Dict[str, Any]:
        """Récupération des informations du développeur"""
        return self.developer_info
    
    def generate_world_map_html(self) -> str:
        """Génération de la carte mondiale HTML"""
        try:
            # Création de la carte
            world_map = folium.Map(
                location=[20, 0],
                zoom_start=2,
                tiles='OpenStreetMap'
            )
            
            # Ajout des menaces sur la carte
            for threat in self.world_threats.values():
                if threat.source_lat != 0 and threat.source_lng != 0:
                    # Marqueur source (rouge pour attaquant)
                    folium.Marker(
                        location=[threat.source_lat, threat.source_lng],
                        popup=f"""
                        <b>Attaquant</b><br>
                        IP: {threat.source_ip}<br>
                        Pays: {threat.source_country}<br>
                        Ville: {threat.source_city}<br>
                        Type: {threat.threat_type}<br>
                        Niveau: {threat.threat_level}
                        """,
                        icon=folium.Icon(color='red', icon='warning-sign')
                    ).add_to(world_map)
                
                if threat.dest_lat != 0 and threat.dest_lng != 0:
                    # Marqueur destination (bleu pour victime)
                    folium.Marker(
                        location=[threat.dest_lat, threat.dest_lng],
                        popup=f"""
                        <b>Victime</b><br>
                        IP: {threat.destination_ip}<br>
                        Pays: {threat.dest_country}<br>
                        Ville: {threat.dest_city}<br>
                        Type: {threat.threat_type}<br>
                        Niveau: {threat.threat_level}
                        """,
                        icon=folium.Icon(color='blue', icon='info-sign')
                    ).add_to(world_map)
                
                # Ligne entre source et destination
                if (threat.source_lat != 0 and threat.source_lng != 0 and 
                    threat.dest_lat != 0 and threat.dest_lng != 0):
                    folium.PolyLine(
                        locations=[[threat.source_lat, threat.source_lng], 
                                 [threat.dest_lat, threat.dest_lng]],
                        color='orange',
                        weight=2,
                        opacity=0.7,
                        popup=f"Attaque: {threat.threat_type}"
                    ).add_to(world_map)
            
            # Ajout des informations du développeur
            developer_html = f"""
            <div style="position: fixed; top: 10px; right: 10px; background: white; 
                        padding: 10px; border: 2px solid #007bff; border-radius: 5px; 
                        z-index: 1000; max-width: 300px;">
                <h3>🌐 Système Mondial de Défense Cybernétique</h3>
                <p><strong>Développé par:</strong> {self.developer_info['name']}</p>
                <p><strong>Version:</strong> {self.developer_info['version']}</p>
                <p><strong>Contact Principal:</strong><br>
                   <a href="mailto:{self.developer_info['contacts']['primary']}">
                   {self.developer_info['contacts']['primary']}</a></p>
                <p><strong>Contact Secondaire:</strong><br>
                   <a href="mailto:{self.developer_info['contacts']['secondary']}">
                   {self.developer_info['contacts']['secondary']}</a></p>
                <p><strong>Statistiques:</strong><br>
                   Menaces: {self.world_stats.total_threats}<br>
                   Risque Global: {self.world_stats.global_risk_level}</p>
            </div>
            """
            
            # Ajout du contrôle de couches
            folium.LayerControl().add_to(world_map)
            
            # Génération du HTML
            map_html = world_map._repr_html_()
            
            # Insertion des informations du développeur
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Système Mondial de Défense Cybernétique - Yao Kouakou</title>
                <meta charset="utf-8">
                <style>
                    body {{ margin: 0; padding: 0; }}
                    .info-panel {{ 
                        position: fixed; 
                        top: 10px; 
                        left: 10px; 
                        background: rgba(255,255,255,0.9); 
                        padding: 15px; 
                        border-radius: 5px; 
                        z-index: 1000; 
                        max-width: 400px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .developer-info {{
                        background: linear-gradient(135deg, #007bff, #0056b3);
                        color: white;
                        padding: 15px;
                        border-radius: 5px;
                        margin-bottom: 15px;
                    }}
                    .stats-panel {{
                        background: #f8f9fa;
                        padding: 10px;
                        border-radius: 5px;
                        border-left: 4px solid #007bff;
                    }}
                    .contact-links a {{
                        color: #007bff;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                    .contact-links a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="info-panel">
                    <div class="developer-info">
                        <h2>🌐 Système Mondial de Défense Cybernétique</h2>
                        <p><strong>Développé par:</strong> {self.developer_info['name']}</p>
                        <p><strong>Version:</strong> {self.developer_info['version']}</p>
                        <p><strong>Expert en Cybersécurité</strong></p>
                    </div>
                    
                    <div class="stats-panel">
                        <h3>📊 Statistiques Mondiales</h3>
                        <p><strong>Menaces Totales:</strong> {self.world_stats.total_threats}</p>
                        <p><strong>Attaques Actives:</strong> {self.world_stats.active_attacks}</p>
                        <p><strong>Attaques Bloquées:</strong> {self.world_stats.blocked_attacks}</p>
                        <p><strong>Risque Global:</strong> <span style="color: {'red' if self.world_stats.global_risk_level == 'CRITICAL' else 'orange' if self.world_stats.global_risk_level == 'HIGH' else 'green'}">{self.world_stats.global_risk_level}</span></p>
                        <p><strong>Dernière Mise à Jour:</strong> {self.world_stats.last_update.strftime('%H:%M:%S')}</p>
                    </div>
                    
                    <div class="contact-links">
                        <h3>📧 Contact</h3>
                        <p><strong>Email Principal:</strong><br>
                           <a href="mailto:{self.developer_info['contacts']['primary']}">
                           {self.developer_info['contacts']['primary']}</a></p>
                        <p><strong>Email Secondaire:</strong><br>
                           <a href="mailto:{self.developer_info['contacts']['secondary']}">
                           {self.developer_info['contacts']['secondary']}</a></p>
                    </div>
                </div>
                
                {map_html}
                
                <script>
                    // Auto-refresh toutes les 30 secondes
                    setInterval(function() {{
                        location.reload();
                    }}, 30000);
                </script>
            </body>
            </html>
            """
            
            return full_html
            
        except Exception as e:
            logger.error(f"Erreur génération carte mondiale: {e}")
            return f"""
            <html>
            <body>
                <h1>Erreur de génération de la carte</h1>
                <p>Erreur: {str(e)}</p>
                <p>Contact: {self.developer_info['contacts']['primary']}</p>
            </body>
            </html>
            """
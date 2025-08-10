"""
Surveillance Réseau en Temps Réel
=================================

Ce module implémente un système de surveillance réseau avancé avec capture
de paquets, analyse du trafic et détection d'anomalies en temps réel.
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
import struct
import socket
import threading
import queue
import ipaddress
import re
import hashlib
from collections import defaultdict, deque
import numpy as np
from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, Raw
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import ARP, Ether

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProtocolType(Enum):
    """Types de protocoles"""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    ARP = "arp"
    HTTP = "http"
    HTTPS = "https"
    DNS = "dns"
    SMTP = "smtp"
    FTP = "ftp"
    SSH = "ssh"
    TELNET = "telnet"
    UNKNOWN = "unknown"

class TrafficDirection(Enum):
    """Direction du trafic"""
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    INTERNAL = "internal"

@dataclass
class NetworkPacket:
    """Paquet réseau capturé"""
    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: ProtocolType
    payload_size: int
    flags: str
    ttl: int
    window_size: int
    checksum: str
    payload_hash: str
    direction: TrafficDirection
    interface: str

@dataclass
class NetworkFlow:
    """Flux réseau"""
    id: str
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: ProtocolType
    start_time: datetime
    last_seen: datetime
    packet_count: int
    byte_count: int
    duration: float
    status: str
    flags: Set[str]
    avg_packet_size: float
    packet_rate: float
    byte_rate: float

@dataclass
class NetworkAnomaly:
    """Anomalie réseau détectée"""
    id: str
    type: str
    severity: str
    description: str
    source_ip: str
    destination_ip: str
    protocol: ProtocolType
    timestamp: datetime
    evidence: Dict[str, Any]
    confidence: float
    status: str

@dataclass
class NetworkStatistics:
    """Statistiques réseau"""
    total_packets: int
    total_bytes: int
    active_flows: int
    protocols_distribution: Dict[str, int]
    top_source_ips: List[Tuple[str, int]]
    top_destination_ips: List[Tuple[str, int]]
    top_ports: List[Tuple[int, int]]
    packet_rate: float
    byte_rate: float
    anomaly_count: int

class NetworkMonitor:
    """
    Moniteur réseau en temps réel
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379", interface: str = "eth0"):
        self.redis = redis.from_url(redis_url)
        self.interface = interface
        self.capture_thread = None
        self.is_capturing = False
        self.packet_queue = queue.Queue(maxsize=10000)
        self.active_flows: Dict[str, NetworkFlow] = {}
        self.network_anomalies: Dict[str, NetworkAnomaly] = {}
        self.packet_statistics = defaultdict(int)
        self.flow_timeout = 300  # 5 minutes
        self.websocket_connections: Set[WebSocket] = set()
        
        # Configuration des seuils d'anomalie
        self.anomaly_thresholds = {
            "packet_rate": 1000,  # paquets/seconde
            "byte_rate": 1000000,  # bytes/seconde
            "connection_rate": 100,  # connexions/seconde
            "port_scan_threshold": 10,  # tentatives sur un port
            "syn_flood_threshold": 50,  # SYN par seconde
            "large_packet_threshold": 1500,  # bytes
            "unusual_protocol_threshold": 0.1  # % du trafic total
        }
        
        # Cache pour les analyses
        self.ip_reputation_cache = {}
        self.port_analysis_cache = {}
        self.protocol_analysis_cache = {}
        
        # Historique pour détection d'anomalies
        self.packet_history = deque(maxlen=10000)
        self.flow_history = deque(maxlen=1000)
        
    async def initialize(self):
        """Initialisation du moniteur réseau"""
        logger.info(f"🌐 Initialisation du moniteur réseau sur l'interface {self.interface}")
        
        # Démarrage de la capture de paquets
        await self._start_packet_capture()
        
        # Démarrage des tâches d'analyse
        asyncio.create_task(self._packet_processor())
        asyncio.create_task(self._flow_analyzer())
        asyncio.create_task(self._anomaly_detector())
        asyncio.create_task(self._statistics_generator())
        asyncio.create_task(self._network_health_monitor())
        
        logger.info("✅ Moniteur réseau initialisé")
    
    async def _start_packet_capture(self):
        """Démarrage de la capture de paquets"""
        try:
            self.is_capturing = True
            self.capture_thread = threading.Thread(
                target=self._packet_capture_worker,
                daemon=True
            )
            self.capture_thread.start()
            logger.info("📡 Capture de paquets démarrée")
        except Exception as e:
            logger.error(f"Erreur démarrage capture: {e}")
            raise
    
    def _packet_capture_worker(self):
        """Worker de capture de paquets"""
        try:
            def packet_handler(packet):
                if self.is_capturing:
                    self.packet_queue.put(packet)
            
            # Démarrage de la capture avec Scapy
            sniff(
                iface=self.interface,
                prn=packet_handler,
                store=False,
                stop_filter=lambda p: not self.is_capturing
            )
        except Exception as e:
            logger.error(f"Erreur capture paquets: {e}")
    
    async def _packet_processor(self):
        """Traitement des paquets capturés"""
        while self.is_capturing:
            try:
                # Récupération d'un paquet de la queue
                packet = self.packet_queue.get(timeout=1)
                
                # Analyse du paquet
                network_packet = await self._analyze_packet(packet)
                
                if network_packet:
                    # Ajout à l'historique
                    self.packet_history.append(network_packet)
                    
                    # Mise à jour des statistiques
                    await self._update_packet_statistics(network_packet)
                    
                    # Mise à jour des flux
                    await self._update_network_flows(network_packet)
                    
                    # Vérification d'anomalies
                    await self._check_packet_anomalies(network_packet)
                    
                    # Notification via WebSocket
                    await self._broadcast_packet_info(network_packet)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erreur traitement paquet: {e}")
    
    async def _analyze_packet(self, packet) -> Optional[NetworkPacket]:
        """Analyse d'un paquet réseau"""
        try:
            # Extraction des informations de base
            if IP in packet:
                source_ip = packet[IP].src
                destination_ip = packet[IP].dst
                ttl = packet[IP].ttl
            else:
                return None
            
            # Détermination du protocole
            protocol = ProtocolType.UNKNOWN
            source_port = 0
            destination_port = 0
            flags = ""
            window_size = 0
            
            if TCP in packet:
                protocol = ProtocolType.TCP
                source_port = packet[TCP].sport
                destination_port = packet[TCP].dport
                flags = str(packet[TCP].flags)
                window_size = packet[TCP].window
            elif UDP in packet:
                protocol = ProtocolType.UDP
                source_port = packet[UDP].sport
                destination_port = packet[UDP].dport
            elif ICMP in packet:
                protocol = ProtocolType.ICMP
            elif ARP in packet:
                protocol = ProtocolType.ARP
            
            # Détermination de la direction
            direction = self._determine_traffic_direction(source_ip, destination_ip)
            
            # Calcul de la taille du payload
            payload_size = len(packet[Raw].load) if Raw in packet else 0
            
            # Calcul du hash du payload
            payload_hash = hashlib.md5(packet[Raw].load).hexdigest() if Raw in packet else ""
            
            # Calcul du checksum
            checksum = hashlib.md5(str(packet).encode()).hexdigest()
            
            return NetworkPacket(
                timestamp=datetime.now(),
                source_ip=source_ip,
                destination_ip=destination_ip,
                source_port=source_port,
                destination_port=destination_port,
                protocol=protocol,
                payload_size=payload_size,
                flags=flags,
                ttl=ttl,
                window_size=window_size,
                checksum=checksum,
                payload_hash=payload_hash,
                direction=direction,
                interface=self.interface
            )
            
        except Exception as e:
            logger.error(f"Erreur analyse paquet: {e}")
            return None
    
    def _determine_traffic_direction(self, source_ip: str, destination_ip: str) -> TrafficDirection:
        """Détermination de la direction du trafic"""
        try:
            # Vérification si les IPs sont internes
            source_internal = ipaddress.ip_address(source_ip).is_private
            dest_internal = ipaddress.ip_address(destination_ip).is_private
            
            if source_internal and dest_internal:
                return TrafficDirection.INTERNAL
            elif source_internal:
                return TrafficDirection.OUTBOUND
            else:
                return TrafficDirection.INBOUND
        except:
            return TrafficDirection.UNKNOWN
    
    async def _update_packet_statistics(self, packet: NetworkPacket):
        """Mise à jour des statistiques de paquets"""
        # Statistiques par protocole
        self.packet_statistics[f"protocol_{packet.protocol.value}"] += 1
        
        # Statistiques par direction
        self.packet_statistics[f"direction_{packet.direction.value}"] += 1
        
        # Statistiques par IP source
        self.packet_statistics[f"source_ip_{packet.source_ip}"] += 1
        
        # Statistiques par IP destination
        self.packet_statistics[f"dest_ip_{packet.destination_ip}"] += 1
        
        # Statistiques par port
        if packet.destination_port > 0:
            self.packet_statistics[f"port_{packet.destination_port}"] += 1
    
    async def _update_network_flows(self, packet: NetworkPacket):
        """Mise à jour des flux réseau"""
        # Création de l'ID du flux
        if packet.source_ip < packet.destination_ip:
            flow_id = f"{packet.source_ip}:{packet.source_port}-{packet.destination_ip}:{packet.destination_port}-{packet.protocol.value}"
        else:
            flow_id = f"{packet.destination_ip}:{packet.destination_port}-{packet.source_ip}:{packet.source_port}-{packet.protocol.value}"
        
        current_time = datetime.now()
        
        if flow_id in self.active_flows:
            # Mise à jour du flux existant
            flow = self.active_flows[flow_id]
            flow.last_seen = current_time
            flow.packet_count += 1
            flow.byte_count += packet.payload_size
            flow.duration = (current_time - flow.start_time).total_seconds()
            
            # Ajout des flags TCP
            if packet.flags:
                flow.flags.add(packet.flags)
            
            # Calcul des taux
            if flow.duration > 0:
                flow.packet_rate = flow.packet_count / flow.duration
                flow.byte_rate = flow.byte_count / flow.duration
                flow.avg_packet_size = flow.byte_count / flow.packet_count
            
        else:
            # Création d'un nouveau flux
            flow = NetworkFlow(
                id=flow_id,
                source_ip=packet.source_ip,
                destination_ip=packet.destination_ip,
                source_port=packet.source_port,
                destination_port=packet.destination_port,
                protocol=packet.protocol,
                start_time=current_time,
                last_seen=current_time,
                packet_count=1,
                byte_count=packet.payload_size,
                duration=0.0,
                status="active",
                flags={packet.flags} if packet.flags else set(),
                avg_packet_size=packet.payload_size,
                packet_rate=0.0,
                byte_rate=0.0
            )
            self.active_flows[flow_id] = flow
        
        # Ajout à l'historique des flux
        self.flow_history.append(flow)
    
    async def _check_packet_anomalies(self, packet: NetworkPacket):
        """Vérification d'anomalies dans un paquet"""
        anomalies = []
        
        # Vérification de la taille du paquet
        if packet.payload_size > self.anomaly_thresholds["large_packet_threshold"]:
            anomalies.append({
                "type": "large_packet",
                "severity": "medium",
                "description": f"Paquet de grande taille détecté: {packet.payload_size} bytes",
                "evidence": {"payload_size": packet.payload_size}
            })
        
        # Vérification des ports suspects
        suspicious_ports = {22, 23, 3389, 445, 1433, 3306, 5432}
        if packet.destination_port in suspicious_ports:
            anomalies.append({
                "type": "suspicious_port",
                "severity": "high",
                "description": f"Connexion vers port suspect: {packet.destination_port}",
                "evidence": {"port": packet.destination_port}
            })
        
        # Vérification des flags TCP suspects
        if packet.flags and "S" in packet.flags and "A" not in packet.flags:
            # SYN sans ACK (possible scan)
            anomalies.append({
                "type": "syn_scan",
                "severity": "medium",
                "description": "Paquet SYN détecté (possible scan)",
                "evidence": {"flags": packet.flags}
            })
        
        # Création des anomalies
        for anomaly_data in anomalies:
            anomaly = NetworkAnomaly(
                id=f"anomaly_{int(time.time())}_{hash(packet.checksum)}",
                type=anomaly_data["type"],
                severity=anomaly_data["severity"],
                description=anomaly_data["description"],
                source_ip=packet.source_ip,
                destination_ip=packet.destination_ip,
                protocol=packet.protocol,
                timestamp=packet.timestamp,
                evidence=anomaly_data["evidence"],
                confidence=0.8,
                status="active"
            )
            
            self.network_anomalies[anomaly.id] = anomaly
            await self._notify_anomaly(anomaly)
    
    async def _flow_analyzer(self):
        """Analyseur de flux réseau"""
        while self.is_capturing:
            try:
                await self._analyze_network_flows()
                await asyncio.sleep(30)  # 30 secondes
            except Exception as e:
                logger.error(f"Erreur analyse flux: {e}")
                await asyncio.sleep(15)
    
    async def _analyze_network_flows(self):
        """Analyse des flux réseau actifs"""
        current_time = datetime.now()
        
        # Nettoyage des flux expirés
        expired_flows = []
        for flow_id, flow in self.active_flows.items():
            if (current_time - flow.last_seen).total_seconds() > self.flow_timeout:
                expired_flows.append(flow_id)
        
        for flow_id in expired_flows:
            del self.active_flows[flow_id]
        
        # Analyse des flux actifs
        for flow in self.active_flows.values():
            await self._check_flow_anomalies(flow)
    
    async def _check_flow_anomalies(self, flow: NetworkFlow):
        """Vérification d'anomalies dans un flux"""
        anomalies = []
        
        # Vérification du taux de paquets
        if flow.packet_rate > self.anomaly_thresholds["packet_rate"]:
            anomalies.append({
                "type": "high_packet_rate",
                "severity": "high",
                "description": f"Taux de paquets élevé: {flow.packet_rate:.2f} pkt/s",
                "evidence": {"packet_rate": flow.packet_rate}
            })
        
        # Vérification du taux de bytes
        if flow.byte_rate > self.anomaly_thresholds["byte_rate"]:
            anomalies.append({
                "type": "high_byte_rate",
                "severity": "medium",
                "description": f"Taux de bytes élevé: {flow.byte_rate:.2f} B/s",
                "evidence": {"byte_rate": flow.byte_rate}
            })
        
        # Vérification des connexions multiples (port scan)
        if flow.protocol == ProtocolType.TCP:
            port_connections = sum(1 for f in self.active_flows.values() 
                                 if f.source_ip == flow.source_ip and f.protocol == ProtocolType.TCP)
            
            if port_connections > self.anomaly_thresholds["port_scan_threshold"]:
                anomalies.append({
                    "type": "port_scan",
                    "severity": "high",
                    "description": f"Port scan détecté: {port_connections} connexions",
                    "evidence": {"connection_count": port_connections}
                })
        
        # Création des anomalies
        for anomaly_data in anomalies:
            anomaly = NetworkAnomaly(
                id=f"flow_anomaly_{int(time.time())}_{hash(flow.id)}",
                type=anomaly_data["type"],
                severity=anomaly_data["severity"],
                description=anomaly_data["description"],
                source_ip=flow.source_ip,
                destination_ip=flow.destination_ip,
                protocol=flow.protocol,
                timestamp=datetime.now(),
                evidence=anomaly_data["evidence"],
                confidence=0.9,
                status="active"
            )
            
            self.network_anomalies[anomaly.id] = anomaly
            await self._notify_anomaly(anomaly)
    
    async def _anomaly_detector(self):
        """Détecteur d'anomalies réseau"""
        while self.is_capturing:
            try:
                await self._detect_network_anomalies()
                await asyncio.sleep(60)  # 1 minute
            except Exception as e:
                logger.error(f"Erreur détection anomalies: {e}")
                await asyncio.sleep(30)
    
    async def _detect_network_anomalies(self):
        """Détection d'anomalies réseau avancées"""
        # Analyse des patterns de trafic
        await self._analyze_traffic_patterns()
        
        # Détection de comportements suspects
        await self._detect_suspicious_behavior()
        
        # Analyse de la réputation des IPs
        await self._analyze_ip_reputation()
    
    async def _analyze_traffic_patterns(self):
        """Analyse des patterns de trafic"""
        if len(self.packet_history) < 100:
            return
        
        # Calcul des statistiques de trafic
        packet_sizes = [p.payload_size for p in list(self.packet_history)[-1000:]]
        packet_intervals = []
        
        for i in range(1, len(self.packet_history)):
            interval = (self.packet_history[i].timestamp - self.packet_history[i-1].timestamp).total_seconds()
            packet_intervals.append(interval)
        
        # Détection d'anomalies statistiques
        if packet_sizes:
            mean_size = np.mean(packet_sizes)
            std_size = np.std(packet_sizes)
            
            # Paquets de taille anormale
            for packet in list(self.packet_history)[-100:]:
                if abs(packet.payload_size - mean_size) > 3 * std_size:
                    anomaly = NetworkAnomaly(
                        id=f"size_anomaly_{int(time.time())}_{hash(packet.checksum)}",
                        type="size_anomaly",
                        severity="medium",
                        description=f"Paquet de taille anormale: {packet.payload_size} bytes",
                        source_ip=packet.source_ip,
                        destination_ip=packet.destination_ip,
                        protocol=packet.protocol,
                        timestamp=packet.timestamp,
                        evidence={"size": packet.payload_size, "mean": mean_size, "std": std_size},
                        confidence=0.7,
                        status="active"
                    )
                    
                    self.network_anomalies[anomaly.id] = anomaly
                    await self._notify_anomaly(anomaly)
    
    async def _detect_suspicious_behavior(self):
        """Détection de comportements suspects"""
        # Analyse des tentatives de connexion répétées
        connection_attempts = defaultdict(int)
        
        for packet in list(self.packet_history)[-1000:]:
            if packet.protocol == ProtocolType.TCP and "S" in packet.flags:
                key = f"{packet.source_ip}:{packet.destination_ip}:{packet.destination_port}"
                connection_attempts[key] += 1
        
        # Détection des tentatives excessives
        for key, count in connection_attempts.items():
            if count > 5:  # Plus de 5 tentatives
                source_ip, dest_ip, port = key.split(":")
                anomaly = NetworkAnomaly(
                    id=f"connection_anomaly_{int(time.time())}_{hash(key)}",
                    type="excessive_connections",
                    severity="high",
                    description=f"Tentatives de connexion excessives: {count} vers {dest_ip}:{port}",
                    source_ip=source_ip,
                    destination_ip=dest_ip,
                    protocol=ProtocolType.TCP,
                    timestamp=datetime.now(),
                    evidence={"attempts": count, "port": port},
                    confidence=0.8,
                    status="active"
                )
                
                self.network_anomalies[anomaly.id] = anomaly
                await self._notify_anomaly(anomaly)
    
    async def _analyze_ip_reputation(self):
        """Analyse de la réputation des IPs"""
        # Ici, on pourrait intégrer avec des services de réputation IP
        # comme AbuseIPDB, VirusTotal, etc.
        pass
    
    async def _statistics_generator(self):
        """Générateur de statistiques réseau"""
        while self.is_capturing:
            try:
                stats = await self._generate_network_statistics()
                await self._broadcast_statistics(stats)
                await asyncio.sleep(10)  # 10 secondes
            except Exception as e:
                logger.error(f"Erreur génération statistiques: {e}")
                await asyncio.sleep(5)
    
    async def _generate_network_statistics(self) -> NetworkStatistics:
        """Génération des statistiques réseau"""
        current_time = datetime.now()
        
        # Calcul des statistiques de base
        total_packets = len(self.packet_history)
        total_bytes = sum(p.payload_size for p in self.packet_history)
        active_flows = len(self.active_flows)
        
        # Distribution des protocoles
        protocols_distribution = defaultdict(int)
        for packet in list(self.packet_history)[-1000:]:
            protocols_distribution[packet.protocol.value] += 1
        
        # Top IPs sources
        source_ip_counts = defaultdict(int)
        for packet in list(self.packet_history)[-1000:]:
            source_ip_counts[packet.source_ip] += 1
        
        top_source_ips = sorted(source_ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top IPs destinations
        dest_ip_counts = defaultdict(int)
        for packet in list(self.packet_history)[-1000:]:
            dest_ip_counts[packet.destination_ip] += 1
        
        top_destination_ips = sorted(dest_ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top ports
        port_counts = defaultdict(int)
        for packet in list(self.packet_history)[-1000:]:
            if packet.destination_port > 0:
                port_counts[packet.destination_port] += 1
        
        top_ports = sorted(port_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Calcul des taux
        if len(self.packet_history) > 1:
            time_span = (current_time - self.packet_history[0].timestamp).total_seconds()
            if time_span > 0:
                packet_rate = total_packets / time_span
                byte_rate = total_bytes / time_span
            else:
                packet_rate = byte_rate = 0.0
        else:
            packet_rate = byte_rate = 0.0
        
        return NetworkStatistics(
            total_packets=total_packets,
            total_bytes=total_bytes,
            active_flows=active_flows,
            protocols_distribution=dict(protocols_distribution),
            top_source_ips=top_source_ips,
            top_destination_ips=top_destination_ips,
            top_ports=top_ports,
            packet_rate=packet_rate,
            byte_rate=byte_rate,
            anomaly_count=len(self.network_anomalies)
        )
    
    async def _network_health_monitor(self):
        """Moniteur de santé réseau"""
        while self.is_capturing:
            try:
                await self._check_network_health()
                await asyncio.sleep(60)  # 1 minute
            except Exception as e:
                logger.error(f"Erreur surveillance santé réseau: {e}")
                await asyncio.sleep(30)
    
    async def _check_network_health(self):
        """Vérification de la santé du réseau"""
        # Vérification de la connectivité
        # Vérification de la latence
        # Vérification de la bande passante
        # Vérification des erreurs réseau
        pass
    
    async def _broadcast_packet_info(self, packet: NetworkPacket):
        """Diffusion d'informations sur un paquet via WebSocket"""
        message = {
            "type": "packet_info",
            "packet": asdict(packet),
            "timestamp": datetime.now().isoformat()
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket: {e}")
                self.websocket_connections.discard(websocket)
    
    async def _notify_anomaly(self, anomaly: NetworkAnomaly):
        """Notification d'une anomalie détectée"""
        message = {
            "type": "network_anomaly",
            "anomaly": asdict(anomaly),
            "timestamp": datetime.now().isoformat()
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket: {e}")
                self.websocket_connections.discard(websocket)
    
    async def _broadcast_statistics(self, stats: NetworkStatistics):
        """Diffusion des statistiques via WebSocket"""
        message = {
            "type": "network_statistics",
            "statistics": asdict(stats),
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
    
    async def get_network_statistics(self) -> NetworkStatistics:
        """Récupération des statistiques réseau"""
        return await self._generate_network_statistics()
    
    async def get_active_flows(self) -> List[NetworkFlow]:
        """Récupération des flux actifs"""
        return list(self.active_flows.values())
    
    async def get_network_anomalies(self) -> List[NetworkAnomaly]:
        """Récupération des anomalies réseau"""
        return list(self.network_anomalies.values())
    
    async def stop_capture(self):
        """Arrêt de la capture de paquets"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=5)
        logger.info("📡 Capture de paquets arrêtée")
    
    def set_anomaly_thresholds(self, thresholds: Dict[str, Any]):
        """Définition des seuils d'anomalie"""
        self.anomaly_thresholds.update(thresholds)
        logger.info("🔧 Seuils d'anomalie mis à jour")
    
    async def get_network_health(self) -> Dict[str, Any]:
        """Récupération de la santé du réseau"""
        return {
            "capture_active": self.is_capturing,
            "interface": self.interface,
            "active_flows_count": len(self.active_flows),
            "anomalies_count": len(self.network_anomalies),
            "packet_queue_size": self.packet_queue.qsize(),
            "websocket_connections": len(self.websocket_connections)
        }
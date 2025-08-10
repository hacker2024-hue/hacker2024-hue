"""
Analyseur de Menaces Intelligent
================================

Module d'analyse avancée des menaces cybernétiques utilisant l'IA.
"""

import asyncio
import hashlib
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
from loguru import logger
import httpx

from core.config import config


@dataclass
class ThreatIndicator:
    """Indicateur de menace"""
    type: str  # ip, domain, hash, url, etc.
    value: str
    confidence: float
    source: str
    first_seen: datetime
    last_seen: datetime
    tags: List[str]
    severity: str


@dataclass
class ThreatIntelligence:
    """Intelligence de menace"""
    threat_id: str
    name: str
    description: str
    tactics: List[str]  # MITRE ATT&CK tactics
    techniques: List[str]  # MITRE ATT&CK techniques
    indicators: List[ThreatIndicator]
    attribution: Optional[str]
    confidence: float
    created: datetime


class ThreatAnalyzer:
    """
    Analyseur de menaces utilisant l'intelligence artificielle
    
    Fonctionnalités:
    - Corrélation d'indicateurs de compromission
    - Analyse comportementale
    - Scoring de menaces
    - Attribution d'attaquants
    - Prédiction de nouvelles menaces
    """
    
    def __init__(self):
        self.threat_feeds: List[str] = config.threat_feeds
        self.indicators_db: Dict[str, ThreatIndicator] = {}
        self.threat_intelligence: Dict[str, ThreatIntelligence] = {}
        self.anomaly_detector = None
        self.text_vectorizer = None
        self.mitre_mapping = self._load_mitre_mapping()
        
    async def initialize(self):
        """Initialisation de l'analyseur de menaces"""
        logger.info("Initialisation de l'analyseur de menaces...")
        
        try:
            # Chargement des modèles d'IA
            await self._initialize_ml_models()
            
            # Mise à jour des feeds de threat intelligence
            await self._update_threat_feeds()
            
            # Chargement de la base MITRE ATT&CK
            await self._load_mitre_attack()
            
            logger.success("Analyseur de menaces initialisé")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}")
            raise
    
    async def _initialize_ml_models(self):
        """Initialisation des modèles de machine learning"""
        try:
            # Modèle de détection d'anomalies
            self.anomaly_detector = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
            
            # Vectoriseur pour l'analyse de texte
            self.text_vectorizer = TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                ngram_range=(1, 3)
            )
            
            logger.success("Modèles ML initialisés")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation des modèles: {e}")
            raise
    
    async def _update_threat_feeds(self):
        """Mise à jour des feeds de threat intelligence"""
        logger.info("Mise à jour des feeds de threat intelligence...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for feed_url in self.threat_feeds:
                try:
                    logger.info(f"Téléchargement du feed: {feed_url}")
                    response = await client.get(feed_url)
                    
                    if response.status_code == 200:
                        await self._parse_threat_feed(feed_url, response.text)
                        logger.success(f"Feed traité: {feed_url}")
                    else:
                        logger.warning(f"Erreur HTTP {response.status_code} pour {feed_url}")
                        
                except Exception as e:
                    logger.error(f"Erreur lors du téléchargement de {feed_url}: {e}")
                    
        logger.info(f"Mise à jour terminée. {len(self.indicators_db)} indicateurs chargés")
    
    async def _parse_threat_feed(self, source: str, content: str):
        """Parse d'un feed de threat intelligence"""
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Détection du type d'indicateur
            indicator_type = self._detect_indicator_type(line)
            if indicator_type:
                indicator = ThreatIndicator(
                    type=indicator_type,
                    value=line,
                    confidence=0.8,  # Confiance par défaut pour les feeds publics
                    source=source,
                    first_seen=datetime.utcnow(),
                    last_seen=datetime.utcnow(),
                    tags=["threat_feed"],
                    severity="medium"
                )
                
                self.indicators_db[line] = indicator
    
    def _detect_indicator_type(self, value: str) -> Optional[str]:
        """Détection automatique du type d'indicateur"""
        
        # IP Address
        ip_pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        if re.match(ip_pattern, value):
            return "ip"
        
        # Domain
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.([a-zA-Z]{2,})$'
        if re.match(domain_pattern, value):
            return "domain"
        
        # Hash (MD5, SHA1, SHA256)
        if re.match(r'^[a-fA-F0-9]{32}$', value):
            return "md5"
        elif re.match(r'^[a-fA-F0-9]{40}$', value):
            return "sha1"
        elif re.match(r'^[a-fA-F0-9]{64}$', value):
            return "sha256"
        
        # URL
        if value.startswith(('http://', 'https://')):
            return "url"
        
        return None
    
    async def _load_mitre_attack(self):
        """Chargement de la base MITRE ATT&CK"""
        # Simulation de chargement MITRE ATT&CK
        # En production, cela viendrait de l'API MITRE ou d'une base locale
        logger.info("Chargement de la base MITRE ATT&CK...")
        
        # Données simplifiées pour la démonstration
        sample_techniques = {
            "T1059": {
                "name": "Command and Scripting Interpreter",
                "tactic": "Execution",
                "description": "Adversaries may abuse command and script interpreters"
            },
            "T1055": {
                "name": "Process Injection",
                "tactic": "Defense Evasion",
                "description": "Adversaries may inject code into processes"
            },
            "T1083": {
                "name": "File and Directory Discovery",
                "tactic": "Discovery",
                "description": "Adversaries may enumerate files and directories"
            }
        }
        
        self.mitre_techniques = sample_techniques
        logger.success("Base MITRE ATT&CK chargée")
    
    def _load_mitre_mapping(self) -> Dict[str, List[str]]:
        """Mapping de mots-clés vers les techniques MITRE"""
        return {
            "powershell": ["T1059.001"],
            "cmd": ["T1059.003"],
            "injection": ["T1055"],
            "discovery": ["T1083"],
            "lateral_movement": ["T1021"],
            "persistence": ["T1053", "T1547"],
            "privilege_escalation": ["T1068", "T1055"],
            "credential_access": ["T1003", "T1110"],
            "exfiltration": ["T1041", "T1567"]
        }
    
    async def analyze_indicators(self, indicators: List[str]) -> Dict[str, Any]:
        """
        Analyse d'une liste d'indicateurs de compromission
        
        Args:
            indicators: Liste d'IoCs à analyser
            
        Returns:
            Résultat d'analyse avec scoring et recommandations
        """
        analysis_results = {
            "timestamp": datetime.utcnow(),
            "indicators_analyzed": len(indicators),
            "threats_detected": [],
            "risk_score": 0,
            "recommendations": [],
            "mitre_techniques": []
        }
        
        threat_score = 0
        detected_threats = []
        mitre_techniques = set()
        
        for indicator in indicators:
            # Vérification dans la base d'indicateurs connus
            if indicator in self.indicators_db:
                threat_info = self.indicators_db[indicator]
                detected_threats.append({
                    "indicator": indicator,
                    "type": threat_info.type,
                    "confidence": threat_info.confidence,
                    "severity": threat_info.severity,
                    "source": threat_info.source,
                    "tags": threat_info.tags
                })
                
                # Calcul du score de menace
                severity_weights = {"low": 1, "medium": 3, "high": 5, "critical": 10}
                threat_score += severity_weights.get(threat_info.severity, 1) * threat_info.confidence
            
            # Analyse comportementale
            behavioral_analysis = await self._analyze_behavior(indicator)
            if behavioral_analysis["suspicious"]:
                threat_score += behavioral_analysis["score"]
                detected_threats.append(behavioral_analysis)
            
            # Mapping MITRE ATT&CK
            techniques = await self._map_to_mitre(indicator)
            mitre_techniques.update(techniques)
        
        # Calcul du score de risque global
        analysis_results["risk_score"] = min(threat_score / len(indicators), 100) if indicators else 0
        analysis_results["threats_detected"] = detected_threats
        analysis_results["mitre_techniques"] = list(mitre_techniques)
        
        # Génération de recommandations
        analysis_results["recommendations"] = await self._generate_recommendations(
            analysis_results["risk_score"],
            detected_threats,
            mitre_techniques
        )
        
        return analysis_results
    
    async def _analyze_behavior(self, indicator: str) -> Dict[str, Any]:
        """Analyse comportementale d'un indicateur"""
        
        # Analyse basique (à améliorer avec des modèles ML plus sophistiqués)
        suspicious_patterns = [
            r'\.tmp$',  # Fichiers temporaires
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IPs
            r'(cmd|powershell|bash)',  # Commandes système
            r'(download|upload|connect)',  # Actions réseau
            r'[a-fA-F0-9]{32,64}',  # Hashes
        ]
        
        suspicion_score = 0
        matched_patterns = []
        
        for pattern in suspicious_patterns:
            if re.search(pattern, indicator, re.IGNORECASE):
                suspicion_score += 10
                matched_patterns.append(pattern)
        
        return {
            "indicator": indicator,
            "suspicious": suspicion_score > 0,
            "score": suspicion_score,
            "patterns": matched_patterns,
            "type": "behavioral_analysis",
            "confidence": min(suspicion_score / 50, 1.0)
        }
    
    async def _map_to_mitre(self, indicator: str) -> List[str]:
        """Mapping d'un indicateur vers les techniques MITRE ATT&CK"""
        techniques = []
        
        indicator_lower = indicator.lower()
        
        for keyword, technique_ids in self.mitre_mapping.items():
            if keyword in indicator_lower:
                techniques.extend(technique_ids)
        
        return list(set(techniques))
    
    async def _generate_recommendations(
        self,
        risk_score: float,
        threats: List[Dict[str, Any]],
        mitre_techniques: set
    ) -> List[str]:
        """Génération de recommandations basées sur l'analyse"""
        
        recommendations = []
        
        # Recommandations basées sur le score de risque
        if risk_score >= 70:
            recommendations.extend([
                "🚨 ALERTE CRITIQUE: Isoler immédiatement les systèmes affectés",
                "Activer la procédure d'incident de sécurité",
                "Notifier l'équipe de réponse aux incidents",
                "Effectuer une analyse forensique complète"
            ])
        elif risk_score >= 40:
            recommendations.extend([
                "⚠️ ALERTE ÉLEVÉE: Surveillance renforcée recommandée",
                "Vérifier les logs de sécurité",
                "Examiner les connexions réseau suspectes",
                "Mettre à jour les signatures de détection"
            ])
        elif risk_score >= 20:
            recommendations.extend([
                "ℹ️ Risque modéré détecté",
                "Surveiller l'évolution des indicateurs",
                "Vérifier les configurations de sécurité",
                "Sensibiliser les utilisateurs"
            ])
        
        # Recommandations spécifiques aux techniques MITRE
        if "T1059" in mitre_techniques:
            recommendations.append("Surveiller l'exécution de scripts suspects")
        if "T1055" in mitre_techniques:
            recommendations.append("Activer la surveillance des injections de processus")
        if "T1083" in mitre_techniques:
            recommendations.append("Monitorer les accès aux fichiers système")
        
        return recommendations
    
    async def correlate_threats(self, time_window: int = 3600) -> List[Dict[str, Any]]:
        """
        Corrélation de menaces dans une fenêtre temporelle
        
        Args:
            time_window: Fenêtre temporelle en secondes (défaut: 1 heure)
            
        Returns:
            Liste des menaces corrélées
        """
        current_time = datetime.utcnow()
        cutoff_time = current_time - timedelta(seconds=time_window)
        
        # Simulation de corrélation (en production, cela utiliserait une vraie base de données)
        correlated_threats = []
        
        # Groupe d'indicateurs par source et timeline
        threat_groups = {}
        
        for indicator_value, indicator in self.indicators_db.items():
            if indicator.last_seen >= cutoff_time:
                group_key = f"{indicator.source}_{indicator.severity}"
                if group_key not in threat_groups:
                    threat_groups[group_key] = []
                threat_groups[group_key].append(indicator)
        
        # Analyse des groupes pour détecter des campagnes
        for group_key, indicators in threat_groups.items():
            if len(indicators) >= 3:  # Seuil minimum pour une campagne
                correlation = {
                    "campaign_id": hashlib.md5(group_key.encode()).hexdigest()[:8],
                    "indicators_count": len(indicators),
                    "confidence": min(len(indicators) / 10, 1.0),
                    "severity": indicators[0].severity,
                    "first_seen": min(ind.first_seen for ind in indicators),
                    "last_seen": max(ind.last_seen for ind in indicators),
                    "indicators": [ind.value for ind in indicators[:5]]  # Top 5
                }
                correlated_threats.append(correlation)
        
        return sorted(correlated_threats, key=lambda x: x["confidence"], reverse=True)
    
    async def predict_next_threats(self, historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prédiction de menaces futures basée sur l'analyse historique
        
        Args:
            historical_data: Données historiques d'incidents
            
        Returns:
            Prédictions de menaces futures
        """
        
        if not historical_data:
            return []
        
        # Analyse des tendances (version simplifiée)
        threat_patterns = {}
        
        for incident in historical_data:
            threat_type = incident.get("type", "unknown")
            timestamp = incident.get("timestamp", datetime.utcnow())
            
            # Groupement par mois
            month_key = timestamp.strftime("%Y-%m")
            if month_key not in threat_patterns:
                threat_patterns[month_key] = {}
            
            threat_patterns[month_key][threat_type] = threat_patterns[month_key].get(threat_type, 0) + 1
        
        # Prédictions basiques (à améliorer avec des modèles de time series)
        predictions = []
        
        current_month = datetime.utcnow().strftime("%Y-%m")
        
        for threat_type in ["malware", "phishing", "ddos", "vulnerability"]:
            # Calcul de la tendance
            recent_months = sorted(threat_patterns.keys())[-3:]  # 3 derniers mois
            trend = 0
            
            if len(recent_months) >= 2:
                for month in recent_months:
                    trend += threat_patterns.get(month, {}).get(threat_type, 0)
                
                trend = trend / len(recent_months)
                
                prediction = {
                    "threat_type": threat_type,
                    "predicted_incidents": int(trend * 1.1),  # Augmentation de 10%
                    "confidence": 0.6,  # Confiance modérée pour un modèle simple
                    "time_frame": "next_30_days",
                    "recommendation": f"Renforcer les défenses contre {threat_type}"
                }
                
                predictions.append(prediction)
        
        return sorted(predictions, key=lambda x: x["predicted_incidents"], reverse=True)
    
    async def generate_threat_report(self, indicators: List[str]) -> Dict[str, Any]:
        """Génération d'un rapport de menace complet"""
        
        # Analyse des indicateurs
        analysis = await self.analyze_indicators(indicators)
        
        # Corrélation des menaces
        correlations = await self.correlate_threats()
        
        # Prédictions (basées sur des données simulées)
        sample_historical = [
            {"type": "malware", "timestamp": datetime.utcnow() - timedelta(days=30)},
            {"type": "phishing", "timestamp": datetime.utcnow() - timedelta(days=15)},
        ]
        predictions = await self.predict_next_threats(sample_historical)
        
        # Compilation du rapport
        report = {
            "report_id": hashlib.md5(str(datetime.utcnow()).encode()).hexdigest()[:8],
            "generated_at": datetime.utcnow(),
            "summary": {
                "total_indicators": len(indicators),
                "threats_detected": len(analysis["threats_detected"]),
                "risk_score": analysis["risk_score"],
                "severity": self._calculate_severity(analysis["risk_score"])
            },
            "detailed_analysis": analysis,
            "threat_correlations": correlations,
            "future_predictions": predictions,
            "mitre_mapping": {
                technique_id: self.mitre_techniques.get(technique_id, {})
                for technique_id in analysis["mitre_techniques"]
            },
            "executive_summary": self._generate_executive_summary(analysis, correlations)
        }
        
        return report
    
    def _calculate_severity(self, risk_score: float) -> str:
        """Calcul de la sévérité basée sur le score de risque"""
        if risk_score >= 70:
            return "critical"
        elif risk_score >= 40:
            return "high"
        elif risk_score >= 20:
            return "medium"
        else:
            return "low"
    
    def _generate_executive_summary(
        self,
        analysis: Dict[str, Any],
        correlations: List[Dict[str, Any]]
    ) -> str:
        """Génération d'un résumé exécutif"""
        
        threats_count = len(analysis["threats_detected"])
        risk_score = analysis["risk_score"]
        correlations_count = len(correlations)
        
        if risk_score >= 70:
            summary = f"🚨 SITUATION CRITIQUE: {threats_count} menaces détectées avec un score de risque élevé ({risk_score:.1f}/100). "
        elif risk_score >= 40:
            summary = f"⚠️ VIGILANCE REQUISE: {threats_count} menaces identifiées nécessitant une attention immédiate. "
        else:
            summary = f"ℹ️ SURVEILLANCE NORMALE: {threats_count} indicateurs analysés, risque maîtrisé. "
        
        if correlations_count > 0:
            summary += f"{correlations_count} campagnes potentielles détectées. "
        
        summary += "Actions recommandées incluses dans le rapport détaillé."
        
        return summary
#!/usr/bin/env python3
"""
Module Avancé d'IA de Sécurité - Intelligence Prédictive
========================================================

Fonctionnalités avancées :
- Analyse prédictive des menaces
- Machine Learning pour la détection comportementale
- Corrélation d'événements multicouches
- Intelligence artificielle conversationnelle
- Apprentissage automatique adaptatif
"""

import asyncio
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import pickle
import hashlib
import re

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.cluster import DBSCAN, KMeans
    import warnings
    warnings.filterwarnings('ignore')
except ImportError:
    print("Modules ML non disponibles - fonctionnement en mode dégradé")

from loguru import logger


class ThreatPredictionLevel(Enum):
    """Niveaux de prédiction des menaces"""
    IMMINENT = "imminent"           # 0-2h
    PROBABLE = "probable"           # 2-24h  
    POSSIBLE = "possible"           # 1-7j
    UNLIKELY = "unlikely"           # >7j
    UNKNOWN = "unknown"             # Impossible à prédire


class AttackVector(Enum):
    """Vecteurs d'attaque identifiés"""
    MALWARE = "malware"
    PHISHING = "phishing" 
    RANSOMWARE = "ransomware"
    APT = "apt"
    DDOS = "ddos"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    BRUTE_FORCE = "brute_force"
    INSIDER_THREAT = "insider_threat"
    ZERO_DAY = "zero_day"
    SOCIAL_ENGINEERING = "social_engineering"


class BehaviorPattern(Enum):
    """Patterns comportementaux"""
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    ANOMALOUS = "anomalous"
    MALICIOUS = "malicious"
    UNKNOWN = "unknown"


@dataclass
class ThreatPrediction:
    """Prédiction de menace"""
    vector: AttackVector
    level: ThreatPredictionLevel
    confidence: float  # 0.0 - 1.0
    timeframe: timedelta
    indicators: List[str]
    mitigation_steps: List[str]
    risk_score: float
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class BehaviorAnalysis:
    """Analyse comportementale"""
    entity_id: str  # IP, user, process, etc.
    pattern: BehaviorPattern
    anomaly_score: float
    baseline_deviation: float
    features: Dict[str, float]
    timeline: List[datetime]
    confidence: float


@dataclass
class SecurityEvent:
    """Événement de sécurité enrichi"""
    event_id: str
    timestamp: datetime
    source_ip: str
    destination_ip: Optional[str]
    event_type: str
    severity: str
    raw_data: Dict[str, Any]
    processed_features: Dict[str, float]
    ml_prediction: Optional[str] = None
    threat_vector: Optional[AttackVector] = None
    behavior_score: Optional[float] = None


class AdvancedThreatDetector:
    """Détecteur de menaces avancé avec ML"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.baseline_profiles = {}
        self.event_history = []
        self.behavior_models = {}
        
        # Initialisation des modèles ML
        self._initialize_ml_models()
        
        # Base de connaissances des menaces
        self.threat_intelligence = self._load_threat_intelligence()
        
        logger.info("AdvancedThreatDetector initialisé avec succès")
    
    def _initialize_ml_models(self):
        """Initialise les modèles de machine learning"""
        try:
            # Modèle de classification des menaces
            self.models['threat_classifier'] = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Modèle de détection d'anomalies comportementales
            self.models['behavior_detector'] = MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42
            )
            
            # Modèle de prédiction temporelle
            self.models['temporal_predictor'] = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                random_state=42
            )
            
            # Scalers pour normalisation
            self.scalers['standard'] = StandardScaler()
            self.encoders['label'] = LabelEncoder()
            
            logger.info("Modèles ML initialisés")
            
        except Exception as e:
            logger.error(f"Erreur initialisation ML: {e}")
            # Mode dégradé sans ML
            self.models = {}
    
    def _load_threat_intelligence(self) -> Dict[str, Any]:
        """Charge la base de connaissances des menaces"""
        return {
            "malicious_domains": [
                "malware-c2.example.com",
                "phishing-site.evil.org", 
                "ransomware-payment.onion",
                "apt-command.control.net"
            ],
            "attack_signatures": {
                AttackVector.SQL_INJECTION: [
                    r"(\%27)|(\')|(\-\-)|(%23)|(#)",
                    r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(%23)|(#))",
                    r"w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))"
                ],
                AttackVector.XSS: [
                    r"<script[\s\S]*?>[\s\S]*?</script>",
                    r"javascript:",
                    r"on\w+\s*="
                ],
                AttackVector.RANSOMWARE: [
                    r"\.encrypt\(",
                    r"ransom",
                    r"bitcoin",
                    r"\.locked$",
                    r"decrypt_instruction"
                ]
            },
            "ioc_patterns": {
                "ip_ranges": [
                    "192.168.1.0/24",
                    "10.0.0.0/8", 
                    "172.16.0.0/12"
                ],
                "file_extensions": [
                    ".exe", ".bat", ".cmd", ".scr", ".pif",
                    ".com", ".dll", ".sys", ".vbs", ".js"
                ]
            }
        }
    
    async def analyze_event(self, event: SecurityEvent) -> Tuple[BehaviorAnalysis, Optional[ThreatPrediction]]:
        """Analyse complète d'un événement de sécurité"""
        
        # 1. Extraction des caractéristiques
        features = self._extract_features(event)
        
        # 2. Analyse comportementale
        behavior_analysis = await self._analyze_behavior(event, features)
        
        # 3. Prédiction de menace
        threat_prediction = None
        if behavior_analysis.pattern in [BehaviorPattern.SUSPICIOUS, BehaviorPattern.ANOMALOUS, BehaviorPattern.MALICIOUS]:
            threat_prediction = await self._predict_threat(event, features, behavior_analysis)
        
        # 4. Mise à jour des profils
        await self._update_baseline_profiles(event, features)
        
        return behavior_analysis, threat_prediction
    
    def _extract_features(self, event: SecurityEvent) -> Dict[str, float]:
        """Extrait les caractéristiques numériques d'un événement"""
        features = {}
        
        # Caractéristiques temporelles
        features['hour_of_day'] = event.timestamp.hour
        features['day_of_week'] = event.timestamp.weekday()
        features['is_weekend'] = 1.0 if event.timestamp.weekday() >= 5 else 0.0
        
        # Caractéristiques réseau
        if event.source_ip:
            ip_parts = event.source_ip.split('.')
            if len(ip_parts) == 4:
                try:
                    features['src_ip_class'] = float(ip_parts[0])
                    features['src_ip_entropy'] = self._calculate_ip_entropy(event.source_ip)
                except:
                    features['src_ip_class'] = 0.0
                    features['src_ip_entropy'] = 0.0
        
        # Caractéristiques de contenu
        raw_data_str = json.dumps(event.raw_data, default=str)
        features['content_length'] = float(len(raw_data_str))
        features['special_chars_ratio'] = self._calculate_special_chars_ratio(raw_data_str)
        features['entropy'] = self._calculate_entropy(raw_data_str)
        
        # Indicateurs de menace
        features['threat_indicators'] = self._count_threat_indicators(raw_data_str)
        
        # Fréquence historique
        features['frequency_score'] = self._calculate_frequency_score(event)
        
        return features
    
    def _calculate_ip_entropy(self, ip: str) -> float:
        """Calcule l'entropie d'une adresse IP"""
        try:
            chars = list(ip.replace('.', ''))
            return self._calculate_entropy(''.join(chars))
        except:
            return 0.0
    
    def _calculate_special_chars_ratio(self, text: str) -> float:
        """Calcule le ratio de caractères spéciaux"""
        if not text:
            return 0.0
        special_count = len(re.findall(r'[^a-zA-Z0-9\s]', text))
        return special_count / len(text)
    
    def _calculate_entropy(self, text: str) -> float:
        """Calcule l'entropie de Shannon"""
        if not text:
            return 0.0
        
        # Comptage des caractères
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calcul de l'entropie
        length = len(text)
        entropy = 0.0
        for count in char_counts.values():
            p = count / length
            entropy -= p * np.log2(p)
        
        return entropy
    
    def _count_threat_indicators(self, text: str) -> float:
        """Compte les indicateurs de menace dans le texte"""
        indicators = 0
        text_lower = text.lower()
        
        # Mots-clés suspects
        suspicious_keywords = [
            'exploit', 'payload', 'shell', 'backdoor', 'trojan',
            'virus', 'malware', 'ransomware', 'phishing', 'scam',
            'bitcoin', 'cryptocurrency', 'decrypt', 'encrypt'
        ]
        
        for keyword in suspicious_keywords:
            indicators += text_lower.count(keyword)
        
        # Patterns d'attaque
        for vector, patterns in self.threat_intelligence['attack_signatures'].items():
            for pattern in patterns:
                try:
                    matches = len(re.findall(pattern, text, re.IGNORECASE))
                    indicators += matches * 2  # Pondération plus forte
                except:
                    continue
        
        return float(indicators)
    
    def _calculate_frequency_score(self, event: SecurityEvent) -> float:
        """Calcule un score de fréquence basé sur l'historique"""
        # Recherche d'événements similaires dans les dernières 24h
        recent_events = [
            e for e in self.event_history
            if e.timestamp > (datetime.now() - timedelta(hours=24))
            and e.source_ip == event.source_ip
        ]
        
        return min(len(recent_events) / 10.0, 10.0)  # Normalisé sur 10
    
    async def _analyze_behavior(self, event: SecurityEvent, features: Dict[str, float]) -> BehaviorAnalysis:
        """Analyse le comportement de l'entité source"""
        
        entity_id = event.source_ip
        
        # Récupération du profil de base
        baseline = self.baseline_profiles.get(entity_id, {})
        
        if not baseline:
            # Première observation - comportement normal par défaut
            return BehaviorAnalysis(
                entity_id=entity_id,
                pattern=BehaviorPattern.NORMAL,
                anomaly_score=0.0,
                baseline_deviation=0.0,
                features=features,
                timeline=[event.timestamp],
                confidence=0.5
            )
        
        # Calcul de la déviation par rapport à la baseline
        deviation = self._calculate_baseline_deviation(features, baseline)
        
        # Détermination du pattern comportemental
        pattern = self._classify_behavior_pattern(deviation, features)
        
        # Score d'anomalie
        anomaly_score = min(deviation * features.get('threat_indicators', 0) / 10.0, 1.0)
        
        # Confiance basée sur l'historique
        confidence = min(len(baseline.get('history', [])) / 100.0, 1.0)
        
        return BehaviorAnalysis(
            entity_id=entity_id,
            pattern=pattern,
            anomaly_score=anomaly_score,
            baseline_deviation=deviation,
            features=features,
            timeline=[event.timestamp],
            confidence=confidence
        )
    
    def _calculate_baseline_deviation(self, features: Dict[str, float], baseline: Dict[str, Any]) -> float:
        """Calcule la déviation par rapport à la baseline"""
        if not baseline.get('avg_features'):
            return 0.0
        
        total_deviation = 0.0
        feature_count = 0
        
        for key, value in features.items():
            if key in baseline['avg_features']:
                baseline_value = baseline['avg_features'][key]
                if baseline_value > 0:
                    deviation = abs(value - baseline_value) / baseline_value
                    total_deviation += deviation
                    feature_count += 1
        
        return total_deviation / max(feature_count, 1)
    
    def _classify_behavior_pattern(self, deviation: float, features: Dict[str, float]) -> BehaviorPattern:
        """Classifie le pattern comportemental"""
        threat_score = features.get('threat_indicators', 0)
        
        if threat_score > 5 or deviation > 2.0:
            return BehaviorPattern.MALICIOUS
        elif threat_score > 2 or deviation > 1.0:
            return BehaviorPattern.ANOMALOUS
        elif threat_score > 0 or deviation > 0.5:
            return BehaviorPattern.SUSPICIOUS
        else:
            return BehaviorPattern.NORMAL
    
    async def _predict_threat(self, event: SecurityEvent, features: Dict[str, float], 
                            behavior: BehaviorAnalysis) -> ThreatPrediction:
        """Prédit les menaces futures"""
        
        # Détermination du vecteur d'attaque le plus probable
        vector = self._identify_attack_vector(features, event.raw_data)
        
        # Niveau de prédiction basé sur l'analyse comportementale
        level = self._determine_prediction_level(behavior, features)
        
        # Calcul de la confiance
        confidence = (behavior.confidence + (behavior.anomaly_score * 0.5)) / 1.5
        
        # Timeframe basé sur le niveau
        timeframe = self._get_prediction_timeframe(level)
        
        # Indicateurs de compromission
        indicators = self._extract_iocs(event, features)
        
        # Étapes de mitigation
        mitigation_steps = self._generate_mitigation_steps(vector, level)
        
        # Score de risque global
        risk_score = min(
            (behavior.anomaly_score * 0.4 + 
             features.get('threat_indicators', 0) / 10 * 0.3 +
             behavior.baseline_deviation * 0.3), 
            1.0
        )
        
        return ThreatPrediction(
            vector=vector,
            level=level,
            confidence=confidence,
            timeframe=timeframe,
            indicators=indicators,
            mitigation_steps=mitigation_steps,
            risk_score=risk_score
        )
    
    def _identify_attack_vector(self, features: Dict[str, float], raw_data: Dict[str, Any]) -> AttackVector:
        """Identifie le vecteur d'attaque le plus probable"""
        
        # Analyse du contenu pour des signatures spécifiques
        content = json.dumps(raw_data, default=str).lower()
        
        # Scores pour chaque vecteur
        vector_scores = {}
        
        for vector, patterns in self.threat_intelligence['attack_signatures'].items():
            score = 0
            for pattern in patterns:
                try:
                    matches = len(re.findall(pattern, content, re.IGNORECASE))
                    score += matches
                except:
                    continue
            vector_scores[vector] = score
        
        # Retourne le vecteur avec le score le plus élevé
        if vector_scores:
            best_vector = max(vector_scores, key=vector_scores.get)
            if vector_scores[best_vector] > 0:
                return best_vector
        
        # Fallback basé sur les caractéristiques
        if features.get('threat_indicators', 0) > 3:
            return AttackVector.MALWARE
        elif features.get('frequency_score', 0) > 5:
            return AttackVector.BRUTE_FORCE
        else:
            return AttackVector.MALWARE  # Défaut
    
    def _determine_prediction_level(self, behavior: BehaviorAnalysis, features: Dict[str, float]) -> ThreatPredictionLevel:
        """Détermine le niveau de prédiction temporelle"""
        
        urgency_score = (
            behavior.anomaly_score * 0.4 +
            features.get('threat_indicators', 0) / 10 * 0.3 +
            behavior.baseline_deviation * 0.3
        )
        
        if urgency_score > 0.8:
            return ThreatPredictionLevel.IMMINENT
        elif urgency_score > 0.6:
            return ThreatPredictionLevel.PROBABLE
        elif urgency_score > 0.3:
            return ThreatPredictionLevel.POSSIBLE
        else:
            return ThreatPredictionLevel.UNLIKELY
    
    def _get_prediction_timeframe(self, level: ThreatPredictionLevel) -> timedelta:
        """Retourne le timeframe correspondant au niveau"""
        timeframes = {
            ThreatPredictionLevel.IMMINENT: timedelta(hours=2),
            ThreatPredictionLevel.PROBABLE: timedelta(hours=24),
            ThreatPredictionLevel.POSSIBLE: timedelta(days=7),
            ThreatPredictionLevel.UNLIKELY: timedelta(days=30),
            ThreatPredictionLevel.UNKNOWN: timedelta(days=365)
        }
        return timeframes.get(level, timedelta(days=30))
    
    def _extract_iocs(self, event: SecurityEvent, features: Dict[str, float]) -> List[str]:
        """Extrait les indicateurs de compromission"""
        iocs = []
        
        # IP source si suspecte
        if features.get('threat_indicators', 0) > 0:
            iocs.append(f"IP suspecte: {event.source_ip}")
        
        # Patterns détectés
        content = json.dumps(event.raw_data, default=str)
        for vector, patterns in self.threat_intelligence['attack_signatures'].items():
            for pattern in patterns:
                try:
                    if re.search(pattern, content, re.IGNORECASE):
                        iocs.append(f"Pattern {vector.value}: {pattern[:50]}...")
                except:
                    continue
        
        # Anomalies comportementales
        if features.get('frequency_score', 0) > 3:
            iocs.append(f"Fréquence anormale: {features['frequency_score']:.1f}/10")
        
        if features.get('entropy', 0) > 6:
            iocs.append(f"Entropie élevée: {features['entropy']:.1f}")
        
        return iocs[:10]  # Limite à 10 IOCs
    
    def _generate_mitigation_steps(self, vector: AttackVector, level: ThreatPredictionLevel) -> List[str]:
        """Génère les étapes de mitigation"""
        
        base_steps = [
            "🔍 Surveillance renforcée de l'entité source",
            "📊 Collecte d'informations supplémentaires",
            "🛡️ Application des règles de sécurité préventives"
        ]
        
        vector_specific = {
            AttackVector.MALWARE: [
                "🦠 Scan antivirus complet",
                "🔒 Isolation des systèmes potentiellement infectés",
                "📋 Analyse forensique des fichiers suspects"
            ],
            AttackVector.RANSOMWARE: [
                "💾 Vérification des sauvegardes",
                "🚫 Isolation immédiate des réseaux partagés",
                "🔐 Activation du plan de continuité"
            ],
            AttackVector.DDOS: [
                "🌐 Activation des protections DDoS",
                "📈 Monitoring de la bande passante",
                "🔄 Répartition de charge d'urgence"
            ],
            AttackVector.SQL_INJECTION: [
                "🗄️ Audit des bases de données",
                "🛡️ Mise à jour des WAF",
                "🔍 Validation des requêtes SQL"
            ]
        }
        
        urgency_steps = {
            ThreatPredictionLevel.IMMINENT: [
                "🚨 URGENCE: Activation du plan d'urgence",
                "📞 Notification immédiate de l'équipe de crise",
                "🔒 Isolation préventive des systèmes critiques"
            ],
            ThreatPredictionLevel.PROBABLE: [
                "⚠️ Préparation des équipes de réponse",
                "📋 Révision des procédures d'urgence",
                "🎯 Surveillance ciblée renforcée"
            ]
        }
        
        steps = base_steps.copy()
        steps.extend(vector_specific.get(vector, []))
        steps.extend(urgency_steps.get(level, []))
        
        return steps
    
    async def _update_baseline_profiles(self, event: SecurityEvent, features: Dict[str, float]):
        """Met à jour les profils de base comportementaux"""
        entity_id = event.source_ip
        
        if entity_id not in self.baseline_profiles:
            self.baseline_profiles[entity_id] = {
                'first_seen': event.timestamp,
                'last_updated': event.timestamp,
                'event_count': 0,
                'avg_features': {},
                'history': []
            }
        
        profile = self.baseline_profiles[entity_id]
        profile['last_updated'] = event.timestamp
        profile['event_count'] += 1
        profile['history'].append({
            'timestamp': event.timestamp,
            'features': features.copy()
        })
        
        # Maintien d'un historique limité (derniers 1000 événements)
        if len(profile['history']) > 1000:
            profile['history'] = profile['history'][-1000:]
        
        # Mise à jour des moyennes des caractéristiques
        if not profile['avg_features']:
            profile['avg_features'] = features.copy()
        else:
            # Moyenne mobile
            alpha = 0.1  # Facteur de lissage
            for key, value in features.items():
                if key in profile['avg_features']:
                    profile['avg_features'][key] = (
                        alpha * value + (1 - alpha) * profile['avg_features'][key]
                    )
                else:
                    profile['avg_features'][key] = value
        
        # Ajout à l'historique global
        self.event_history.append(event)
        
        # Nettoyage de l'historique (garde les 10000 derniers événements)
        if len(self.event_history) > 10000:
            self.event_history = self.event_history[-10000:]
    
    async def train_models(self, training_data: List[SecurityEvent]):
        """Entraîne les modèles ML avec les données historiques"""
        if not self.models or not training_data:
            logger.warning("Modèles ML non disponibles ou données insuffisantes")
            return
        
        logger.info(f"Entraînement des modèles avec {len(training_data)} événements")
        
        # Préparation des données
        features_list = []
        labels_threat = []
        labels_behavior = []
        
        for event in training_data:
            features = self._extract_features(event)
            features_array = [features.get(key, 0.0) for key in sorted(features.keys())]
            features_list.append(features_array)
            
            # Labels pour classification des menaces (simulés)
            threat_score = features.get('threat_indicators', 0)
            labels_threat.append(1 if threat_score > 2 else 0)
            
            # Labels pour détection comportementale (simulés)
            anomaly_score = features.get('frequency_score', 0) + threat_score
            labels_behavior.append(1 if anomaly_score > 3 else 0)
        
        if len(features_list) < 10:
            logger.warning("Données insuffisantes pour l'entraînement")
            return
        
        try:
            X = np.array(features_list)
            y_threat = np.array(labels_threat)
            y_behavior = np.array(labels_behavior)
            
            # Normalisation
            X_scaled = self.scalers['standard'].fit_transform(X)
            
            # Division train/test
            X_train, X_test, y_threat_train, y_threat_test = train_test_split(
                X_scaled, y_threat, test_size=0.2, random_state=42
            )
            
            # Entraînement du classificateur de menaces
            self.models['threat_classifier'].fit(X_train, y_threat_train)
            threat_accuracy = self.models['threat_classifier'].score(X_test, y_threat_test)
            
            # Entraînement du détecteur comportemental
            _, _, y_behavior_train, y_behavior_test = train_test_split(
                X_scaled, y_behavior, test_size=0.2, random_state=42
            )
            
            self.models['behavior_detector'].fit(X_train, y_behavior_train)
            behavior_accuracy = self.models['behavior_detector'].score(X_test, y_behavior_test)
            
            logger.info(f"Entraînement terminé - Précision menaces: {threat_accuracy:.2f}, "
                       f"Précision comportement: {behavior_accuracy:.2f}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement: {e}")
    
    async def predict_with_ml(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Utilise les modèles ML pour la prédiction"""
        if not self.models:
            return {}
        
        try:
            # Préparation des features
            features_array = np.array([[features.get(key, 0.0) for key in sorted(features.keys())]])
            features_scaled = self.scalers['standard'].transform(features_array)
            
            predictions = {}
            
            # Prédiction de menace
            if 'threat_classifier' in self.models:
                threat_pred = self.models['threat_classifier'].predict(features_scaled)[0]
                threat_proba = self.models['threat_classifier'].predict_proba(features_scaled)[0]
                predictions['threat_detected'] = bool(threat_pred)
                predictions['threat_probability'] = float(max(threat_proba))
            
            # Prédiction comportementale
            if 'behavior_detector' in self.models:
                behavior_pred = self.models['behavior_detector'].predict(features_scaled)[0]
                behavior_proba = self.models['behavior_detector'].predict_proba(features_scaled)[0]
                predictions['anomalous_behavior'] = bool(behavior_pred)
                predictions['behavior_probability'] = float(max(behavior_proba))
            
            return predictions
            
        except Exception as e:
            logger.error(f"Erreur prédiction ML: {e}")
            return {}


class ConversationalAI:
    """IA conversationnelle pour l'interaction naturelle"""
    
    def __init__(self):
        self.conversation_history = []
        self.context = {}
        self.personality = {
            'professional': True,
            'helpful': True,
            'security_focused': True,
            'multilingual': True
        }
        
        # Templates de réponses contextuelles
        self.response_templates = self._load_response_templates()
        
        logger.info("IA conversationnelle initialisée")
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Charge les templates de réponses"""
        return {
            'threat_detected': [
                "🚨 J'ai détecté une menace de niveau {level}. Vector d'attaque probable: {vector}.",
                "⚠️ Alerte sécurité: {threat_type} identifiée avec {confidence:.0%} de confiance.",
                "🛡️ Incident de sécurité détecté. Recommandations d'action immédiate disponibles."
            ],
            'normal_activity': [
                "✅ L'activité analysée semble normale. Surveillance continue maintenue.",
                "🟢 Comportement standard détecté. Aucune action requise pour le moment.",
                "📊 Analyse complète: activité conforme aux patterns habituels."
            ],
            'prediction_warning': [
                "🔮 Prédiction: risque d'attaque {vector} dans les {timeframe}.",
                "⏰ Alerte prédictive: menace {level} anticipée. Préparation recommandée.",
                "🎯 Intelligence prédictive: {confidence:.0%} de probabilité d'incident imminent."
            ],
            'mitigation_advice': [
                "🛠️ Actions recommandées pour cette menace:",
                "🔧 Voici les étapes de mitigation suggérées:",
                "⚡ Plan d'action immédiat:"
            ],
            'status_update': [
                "📈 État du système: {status}. {details}",
                "🔄 Mise à jour de sécurité: {update_info}",
                "📊 Rapport de surveillance: {metrics}"
            ]
        }
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> str:
        """Traite une requête utilisateur de manière conversationnelle"""
        
        # Sauvegarde du contexte
        self.context.update(context)
        
        # Analyse de l'intention
        intent = self._analyze_intent(query)
        
        # Génération de la réponse
        response = await self._generate_response(query, intent, context)
        
        # Sauvegarde de l'historique
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'query': query,
            'intent': intent,
            'response': response,
            'context': context.copy()
        })
        
        return response
    
    def _analyze_intent(self, query: str) -> str:
        """Analyse l'intention de la requête utilisateur"""
        query_lower = query.lower()
        
        # Intentions liées à la sécurité
        if any(word in query_lower for word in ['threat', 'menace', 'attaque', 'attack', 'danger']):
            return 'threat_inquiry'
        elif any(word in query_lower for word in ['status', 'état', 'statut', 'report', 'rapport']):
            return 'status_request'
        elif any(word in query_lower for word in ['predict', 'prédire', 'anticiper', 'forecast']):
            return 'prediction_request'
        elif any(word in query_lower for word in ['help', 'aide', 'comment', 'how', 'que faire']):
            return 'help_request'
        elif any(word in query_lower for word in ['recommand', 'suggest', 'conseil', 'advice']):
            return 'advice_request'
        else:
            return 'general_inquiry'
    
    async def _generate_response(self, query: str, intent: str, context: Dict[str, Any]) -> str:
        """Génère une réponse contextuelle"""
        
        if intent == 'threat_inquiry':
            return self._handle_threat_inquiry(context)
        elif intent == 'status_request':
            return self._handle_status_request(context)
        elif intent == 'prediction_request':
            return self._handle_prediction_request(context)
        elif intent == 'help_request':
            return self._handle_help_request(query)
        elif intent == 'advice_request':
            return self._handle_advice_request(context)
        else:
            return self._handle_general_inquiry(query, context)
    
    def _handle_threat_inquiry(self, context: Dict[str, Any]) -> str:
        """Gère les questions sur les menaces"""
        
        if 'threat_prediction' in context:
            prediction = context['threat_prediction']
            return (f"🚨 Menace détectée: {prediction.vector.value.upper()}\n"
                   f"📊 Niveau: {prediction.level.value}\n"
                   f"🎯 Confiance: {prediction.confidence:.0%}\n"
                   f"⏰ Timeframe: {prediction.timeframe}\n"
                   f"⚠️ Score de risque: {prediction.risk_score:.2f}/1.0")
        
        elif 'behavior_analysis' in context:
            behavior = context['behavior_analysis']
            return (f"🔍 Analyse comportementale:\n"
                   f"📈 Pattern: {behavior.pattern.value}\n"
                   f"🚨 Score d'anomalie: {behavior.anomaly_score:.2f}\n"
                   f"📊 Déviation baseline: {behavior.baseline_deviation:.2f}")
        
        else:
            return "🛡️ Aucune menace active détectée. Surveillance continue en cours."
    
    def _handle_status_request(self, context: Dict[str, Any]) -> str:
        """Gère les demandes de statut"""
        
        status_info = []
        
        if 'events_processed' in context:
            status_info.append(f"📊 Événements traités: {context['events_processed']}")
        
        if 'active_threats' in context:
            status_info.append(f"🚨 Menaces actives: {context['active_threats']}")
        
        if 'ml_models_status' in context:
            status_info.append(f"🤖 Modèles ML: {context['ml_models_status']}")
        
        if status_info:
            return "📈 État du système:\n" + "\n".join(status_info)
        else:
            return "✅ Système opérationnel. Tous les composants fonctionnent normalement."
    
    def _handle_prediction_request(self, context: Dict[str, Any]) -> str:
        """Gère les demandes de prédiction"""
        
        if 'threat_prediction' in context:
            prediction = context['threat_prediction']
            
            timeframe_str = str(prediction.timeframe)
            if prediction.timeframe.days > 0:
                timeframe_str = f"{prediction.timeframe.days} jour(s)"
            elif prediction.timeframe.seconds > 3600:
                timeframe_str = f"{prediction.timeframe.seconds // 3600} heure(s)"
            
            return (f"🔮 Prédiction de menace:\n"
                   f"🎯 Vector: {prediction.vector.value}\n"
                   f"⏰ Probabilité dans: {timeframe_str}\n"
                   f"📊 Confiance: {prediction.confidence:.0%}\n"
                   f"🚨 Actions préventives recommandées")
        
        return "🔮 Analyse prédictive en cours. Données insuffisantes pour une prédiction fiable."
    
    def _handle_help_request(self, query: str) -> str:
        """Gère les demandes d'aide"""
        
        help_topics = {
            'commandes': "🔧 Commandes disponibles: status, threats, predict, analyze, help",
            'fonctionnalités': "⚙️ Fonctionnalités: détection temps-réel, prédiction, analyse comportementale",
            'alertes': "🚨 Types d'alertes: normale, suspecte, anomale, malicieuse, critique",
            'analyse': "🔍 Types d'analyse: comportementale, prédictive, corrélative, forensique"
        }
        
        query_lower = query.lower()
        for topic, description in help_topics.items():
            if topic in query_lower:
                return description
        
        return ("🆘 Aide - IA de Sécurité Vocale:\n"
               "• Posez des questions sur les menaces détectées\n"
               "• Demandez le statut du système\n" 
               "• Consultez les prédictions de sécurité\n"
               "• Obtenez des recommandations d'action\n"
               "• Commandes: 'status', 'threats', 'predict', 'help'")
    
    def _handle_advice_request(self, context: Dict[str, Any]) -> str:
        """Gère les demandes de conseil"""
        
        if 'threat_prediction' in context:
            prediction = context['threat_prediction']
            advice = "🛠️ Recommandations:\n"
            for i, step in enumerate(prediction.mitigation_steps[:5], 1):
                advice += f"{i}. {step}\n"
            return advice
        
        return ("💡 Conseils généraux de sécurité:\n"
               "• Maintenir les systèmes à jour\n"
               "• Surveiller les logs régulièrement\n"
               "• Former les utilisateurs aux bonnes pratiques\n"
               "• Implémenter une défense en profondeur\n"
               "• Effectuer des audits de sécurité périodiques")
    
    def _handle_general_inquiry(self, query: str, context: Dict[str, Any]) -> str:
        """Gère les questions générales"""
        
        return ("🤖 Je suis votre assistant IA de sécurité informatique.\n"
               "Je peux vous aider avec:\n"
               "• L'analyse des menaces en temps réel\n"
               "• La prédiction d'incidents de sécurité\n"
               "• Les recommandations d'actions préventives\n"
               "• Le monitoring comportemental\n"
               "\nComment puis-je vous assister aujourd'hui?")


async def main():
    """Fonction de test du module avancé"""
    
    # Initialisation
    detector = AdvancedThreatDetector()
    ai = ConversationalAI()
    
    # Événement de test
    test_event = SecurityEvent(
        event_id="test-001",
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        destination_ip="10.0.0.1",
        event_type="suspicious_activity",
        severity="high",
        raw_data={
            "request": "SELECT * FROM users WHERE id = '1' OR '1'='1'",
            "user_agent": "Mozilla/5.0 (Malicious Scanner)",
            "payload_size": 1024
        },
        processed_features={}
    )
    
    # Analyse
    print("🔍 Analyse de l'événement de test...")
    behavior, prediction = await detector.analyze_event(test_event)
    
    # Interaction conversationnelle
    context = {
        'behavior_analysis': behavior,
        'threat_prediction': prediction,
        'events_processed': 1,
        'active_threats': 1 if prediction else 0
    }
    
    print("\n🤖 Interaction conversationnelle:")
    
    queries = [
        "Quel est le statut du système?",
        "Y a-t-il des menaces détectées?",
        "Peux-tu prédire les prochaines attaques?",
        "Quelles sont tes recommandations?"
    ]
    
    for query in queries:
        print(f"\n👤 Utilisateur: {query}")
        response = await ai.process_query(query, context)
        print(f"🤖 Assistant: {response}")


if __name__ == "__main__":
    asyncio.run(main())
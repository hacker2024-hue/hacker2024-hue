"""
Analyseur de Menaces par Intelligence Artificielle
==================================================

Ce module implémente un système d'analyse des menaces basé sur l'IA
avec des modèles de machine learning pour la détection et classification
des cyberattaques.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import pickle
import hashlib
import redis.asyncio as redis
from fastapi import WebSocket
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoTokenizer, AutoModel
import warnings
warnings.filterwarnings('ignore')
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatCategory(Enum):
    """Catégories de menaces"""
    BENIGN = "benign"
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
    UNKNOWN = "unknown"

class ModelType(Enum):
    """Types de modèles IA"""
    RANDOM_FOREST = "random_forest"
    ISOLATION_FOREST = "isolation_forest"
    NEURAL_NETWORK = "neural_network"
    TRANSFORMER = "transformer"
    ENSEMBLE = "ensemble"

@dataclass
class ThreatFeatures:
    """Features d'une menace pour l'IA"""
    id: str
    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    payload_size: int
    packet_count: int
    byte_count: int
    duration: float
    flags: str
    ttl: int
    window_size: int
    country_source: str
    country_dest: str
    asn_source: str
    asn_dest: str
    is_private_source: bool
    is_private_dest: bool
    port_scan_score: float
    syn_flood_score: float
    payload_entropy: float
    connection_rate: float
    byte_rate: float
    packet_rate: float
    avg_packet_size: float
    std_packet_size: float
    flow_duration: float
    flow_bytes_per_sec: float
    flow_packets_per_sec: float
    fwd_packets_per_sec: float
    bwd_packets_per_sec: float
    fwd_bytes_per_sec: float
    bwd_bytes_per_sec: float
    fwd_packet_length_max: float
    fwd_packet_length_min: float
    fwd_packet_length_mean: float
    fwd_packet_length_std: float
    bwd_packet_length_max: float
    bwd_packet_length_min: float
    bwd_packet_length_mean: float
    bwd_packet_length_std: float
    flow_bytes_per_sec: float
    flow_packets_per_sec: float
    flow_iat_mean: float
    flow_iat_std: float
    flow_iat_max: float
    flow_iat_min: float
    fwd_iat_mean: float
    fwd_iat_std: float
    fwd_iat_max: float
    fwd_iat_min: float
    bwd_iat_mean: float
    bwd_iat_std: float
    bwd_iat_max: float
    bwd_iat_min: float
    fwd_psh_flags: int
    bwd_psh_flags: int
    fwd_urg_flags: int
    bwd_urg_flags: int
    fwd_header_length: int
    bwd_header_length: int
    fwd_packets_per_sec: float
    bwd_packets_per_sec: float
    min_packet_length: int
    max_packet_length: int
    packet_length_variance: float
    fin_flag_count: int
    syn_flag_count: int
    rst_flag_count: int
    psh_flag_count: int
    ack_flag_count: int
    urg_flag_count: int
    cwe_flag_count: int
    ece_flag_count: int
    down_up_ratio: float
    avg_packet_size: float
    avg_fwd_segment_size: float
    avg_bwd_segment_size: float
    fwd_header_length: int
    fwd_avg_bytes_per_bulk: float
    fwd_avg_packets_per_bulk: float
    fwd_avg_bulk_rate: float
    bwd_avg_bytes_per_bulk: float
    bwd_avg_packets_per_bulk: float
    bwd_avg_bulk_rate: float
    subflow_fwd_packets: int
    subflow_fwd_bytes: int
    subflow_bwd_packets: int
    subflow_bwd_bytes: int
    init_win_bytes_forward: int
    init_win_bytes_backward: int
    act_data_pkt_fwd: int
    min_seg_size_forward: int
    active_mean: float
    active_std: float
    active_max: float
    active_min: float
    idle_mean: float
    idle_std: float
    idle_max: float
    idle_min: float

@dataclass
class ThreatPrediction:
    """Prédiction d'une menace par l'IA"""
    id: str
    threat_features_id: str
    model_type: ModelType
    predicted_category: ThreatCategory
    confidence_score: float
    probability_scores: Dict[str, float]
    anomaly_score: float
    timestamp: datetime
    model_version: str
    features_used: List[str]
    prediction_time: float

@dataclass
class AIModel:
    """Modèle d'IA"""
    id: str
    name: str
    model_type: ModelType
    version: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_date: datetime
    last_updated: datetime
    is_active: bool
    model_path: str
    feature_columns: List[str]
    hyperparameters: Dict[str, Any]

class AIThreatAnalyzer:
    """
    Analyseur de menaces basé sur l'intelligence artificielle
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379", models_dir: str = "models"):
        self.redis = redis.from_url(redis_url)
        self.models_dir = models_dir
        self.models: Dict[str, AIModel] = {}
        self.active_models: Dict[ModelType, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.feature_columns = self._get_feature_columns()
        self.websocket_connections: Set[WebSocket] = set()
        
        # Configuration des modèles
        self.model_configs = {
            ModelType.RANDOM_FOREST: {
                "n_estimators": 100,
                "max_depth": 10,
                "random_state": 42
            },
            ModelType.ISOLATION_FOREST: {
                "contamination": 0.1,
                "random_state": 42
            },
            ModelType.NEURAL_NETWORK: {
                "layers": [64, 32, 16],
                "dropout": 0.2,
                "learning_rate": 0.001
            }
        }
        
        # Historique des prédictions
        self.prediction_history = []
        
    async def initialize(self):
        """Initialisation de l'analyseur IA"""
        logger.info("🧠 Initialisation de l'analyseur de menaces IA")
        
        # Création du répertoire des modèles
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Chargement des modèles existants
        await self._load_existing_models()
        
        # Entraînement des modèles si nécessaire
        if not self.active_models:
            await self._train_initial_models()
        
        # Démarrage des tâches en arrière-plan
        asyncio.create_task(self._model_monitor())
        asyncio.create_task(self._performance_analyzer())
        asyncio.create_task(self._feature_importance_analyzer())
        
        logger.info("✅ Analyseur de menaces IA initialisé")
    
    def _get_feature_columns(self) -> List[str]:
        """Récupération des colonnes de features"""
        return [
            'source_port', 'destination_port', 'payload_size', 'packet_count',
            'byte_count', 'duration', 'ttl', 'window_size', 'port_scan_score',
            'syn_flood_score', 'payload_entropy', 'connection_rate', 'byte_rate',
            'packet_rate', 'avg_packet_size', 'std_packet_size', 'flow_duration',
            'flow_bytes_per_sec', 'flow_packets_per_sec', 'fwd_packets_per_sec',
            'bwd_packets_per_sec', 'fwd_bytes_per_sec', 'bwd_bytes_per_sec',
            'fwd_packet_length_max', 'fwd_packet_length_min', 'fwd_packet_length_mean',
            'fwd_packet_length_std', 'bwd_packet_length_max', 'bwd_packet_length_min',
            'bwd_packet_length_mean', 'bwd_packet_length_std', 'flow_iat_mean',
            'flow_iat_std', 'flow_iat_max', 'flow_iat_min', 'fwd_iat_mean',
            'fwd_iat_std', 'fwd_iat_max', 'fwd_iat_min', 'bwd_iat_mean',
            'bwd_iat_std', 'bwd_iat_max', 'bwd_iat_min', 'fwd_psh_flags',
            'bwd_psh_flags', 'fwd_urg_flags', 'bwd_urg_flags', 'fwd_header_length',
            'bwd_header_length', 'min_packet_length', 'max_packet_length',
            'packet_length_variance', 'fin_flag_count', 'syn_flag_count',
            'rst_flag_count', 'psh_flag_count', 'ack_flag_count', 'urg_flag_count',
            'down_up_ratio', 'avg_fwd_segment_size', 'avg_bwd_segment_size',
            'fwd_avg_bytes_per_bulk', 'fwd_avg_packets_per_bulk', 'fwd_avg_bulk_rate',
            'bwd_avg_bytes_per_bulk', 'bwd_avg_packets_per_bulk', 'bwd_avg_bulk_rate',
            'subflow_fwd_packets', 'subflow_fwd_bytes', 'subflow_bwd_packets',
            'subflow_bwd_bytes', 'init_win_bytes_forward', 'init_win_bytes_backward',
            'act_data_pkt_fwd', 'min_seg_size_forward', 'active_mean', 'active_std',
            'active_max', 'active_min', 'idle_mean', 'idle_std', 'idle_max', 'idle_min'
        ]
    
    async def _load_existing_models(self):
        """Chargement des modèles existants"""
        try:
            model_files = os.listdir(self.models_dir)
            
            for model_file in model_files:
                if model_file.endswith('.joblib') or model_file.endswith('.pkl'):
                    model_path = os.path.join(self.models_dir, model_file)
                    
                    # Chargement du modèle
                    model = joblib.load(model_path)
                    
                    # Extraction des métadonnées
                    model_name = model_file.replace('.joblib', '').replace('.pkl', '')
                    model_type = self._get_model_type_from_name(model_name)
                    
                    # Création de l'objet AIModel
                    ai_model = AIModel(
                        id=model_name,
                        name=model_name,
                        model_type=model_type,
                        version="1.0",
                        accuracy=0.0,  # À calculer
                        precision=0.0,  # À calculer
                        recall=0.0,     # À calculer
                        f1_score=0.0,   # À calculer
                        training_date=datetime.now(),
                        last_updated=datetime.now(),
                        is_active=True,
                        model_path=model_path,
                        feature_columns=self.feature_columns,
                        hyperparameters=self.model_configs.get(model_type, {})
                    )
                    
                    self.models[model_name] = ai_model
                    self.active_models[model_type] = model
                    
                    logger.info(f"📦 Modèle chargé: {model_name}")
        
        except Exception as e:
            logger.error(f"Erreur chargement modèles: {e}")
    
    def _get_model_type_from_name(self, model_name: str) -> ModelType:
        """Détermination du type de modèle à partir du nom"""
        if "random_forest" in model_name.lower():
            return ModelType.RANDOM_FOREST
        elif "isolation_forest" in model_name.lower():
            return ModelType.ISOLATION_FOREST
        elif "neural_network" in model_name.lower():
            return ModelType.NEURAL_NETWORK
        elif "transformer" in model_name.lower():
            return ModelType.TRANSFORMER
        else:
            return ModelType.RANDOM_FOREST
    
    async def _train_initial_models(self):
        """Entraînement des modèles initiaux"""
        logger.info("🎯 Entraînement des modèles initiaux")
        
        # Génération de données d'entraînement simulées
        training_data = await self._generate_training_data()
        
        # Entraînement du Random Forest
        await self._train_random_forest(training_data)
        
        # Entraînement de l'Isolation Forest
        await self._train_isolation_forest(training_data)
        
        # Entraînement du Neural Network
        await self._train_neural_network(training_data)
        
        logger.info("✅ Modèles initiaux entraînés")
    
    async def _generate_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Génération de données d'entraînement simulées"""
        logger.info("📊 Génération de données d'entraînement")
        
        # Paramètres pour la génération
        n_samples = 10000
        n_features = len(self.feature_columns)
        
        # Génération de features
        X = np.random.randn(n_samples, n_features)
        
        # Génération de labels (simulation de menaces)
        # 80% de trafic normal, 20% de menaces
        y = np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])
        
        # Ajout de patterns spécifiques pour les menaces
        threat_indices = np.where(y == 1)[0]
        
        for idx in threat_indices:
            # Pattern DDoS
            if np.random.random() < 0.3:
                X[idx, 2] = np.random.uniform(1000, 5000)  # payload_size élevé
                X[idx, 12] = np.random.uniform(100, 1000)  # packet_rate élevé
            
            # Pattern APT
            elif np.random.random() < 0.3:
                X[idx, 1] = np.random.choice([22, 23, 3389])  # ports suspects
                X[idx, 8] = np.random.uniform(0.7, 1.0)  # port_scan_score élevé
            
            # Pattern Malware
            else:
                X[idx, 11] = np.random.uniform(0.8, 1.0)  # payload_entropy élevé
                X[idx, 15] = np.random.uniform(100, 500)  # avg_packet_size anormal
        
        return X, y
    
    async def _train_random_forest(self, training_data: Tuple[np.ndarray, np.ndarray]):
        """Entraînement du modèle Random Forest"""
        X, y = training_data
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normalisation
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Entraînement du modèle
        model = RandomForestClassifier(**self.model_configs[ModelType.RANDOM_FOREST])
        model.fit(X_train_scaled, y_train)
        
        # Évaluation
        y_pred = model.predict(X_test_scaled)
        accuracy = model.score(X_test_scaled, y_test)
        
        # Sauvegarde du modèle
        model_name = "random_forest_threat_detector"
        model_path = os.path.join(self.models_dir, f"{model_name}.joblib")
        
        joblib.dump(model, model_path)
        
        # Sauvegarde du scaler
        scaler_path = os.path.join(self.models_dir, f"{model_name}_scaler.joblib")
        joblib.dump(scaler, scaler_path)
        
        # Création de l'objet AIModel
        ai_model = AIModel(
            id=model_name,
            name="Random Forest Threat Detector",
            model_type=ModelType.RANDOM_FOREST,
            version="1.0",
            accuracy=accuracy,
            precision=0.0,  # À calculer
            recall=0.0,     # À calculer
            f1_score=0.0,   # À calculer
            training_date=datetime.now(),
            last_updated=datetime.now(),
            is_active=True,
            model_path=model_path,
            feature_columns=self.feature_columns,
            hyperparameters=self.model_configs[ModelType.RANDOM_FOREST]
        )
        
        self.models[model_name] = ai_model
        self.active_models[ModelType.RANDOM_FOREST] = model
        self.scalers[model_name] = scaler
        
        logger.info(f"🌲 Random Forest entraîné - Accuracy: {accuracy:.3f}")
    
    async def _train_isolation_forest(self, training_data: Tuple[np.ndarray, np.ndarray]):
        """Entraînement du modèle Isolation Forest"""
        X, _ = training_data
        
        # Normalisation
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Entraînement du modèle
        model = IsolationForest(**self.model_configs[ModelType.ISOLATION_FOREST])
        model.fit(X_scaled)
        
        # Sauvegarde du modèle
        model_name = "isolation_forest_anomaly_detector"
        model_path = os.path.join(self.models_dir, f"{model_name}.joblib")
        
        joblib.dump(model, model_path)
        
        # Sauvegarde du scaler
        scaler_path = os.path.join(self.models_dir, f"{model_name}_scaler.joblib")
        joblib.dump(scaler, scaler_path)
        
        # Création de l'objet AIModel
        ai_model = AIModel(
            id=model_name,
            name="Isolation Forest Anomaly Detector",
            model_type=ModelType.ISOLATION_FOREST,
            version="1.0",
            accuracy=0.0,  # Pas applicable pour Isolation Forest
            precision=0.0,
            recall=0.0,
            f1_score=0.0,
            training_date=datetime.now(),
            last_updated=datetime.now(),
            is_active=True,
            model_path=model_path,
            feature_columns=self.feature_columns,
            hyperparameters=self.model_configs[ModelType.ISOLATION_FOREST]
        )
        
        self.models[model_name] = ai_model
        self.active_models[ModelType.ISOLATION_FOREST] = model
        self.scalers[model_name] = scaler
        
        logger.info("🌲 Isolation Forest entraîné")
    
    async def _train_neural_network(self, training_data: Tuple[np.ndarray, np.ndarray]):
        """Entraînement du modèle Neural Network"""
        X, y = training_data
        
        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normalisation
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Conversion en tenseurs TensorFlow
        X_train_tensor = tf.convert_to_tensor(X_train_scaled, dtype=tf.float32)
        y_train_tensor = tf.convert_to_tensor(y_train, dtype=tf.float32)
        X_test_tensor = tf.convert_to_tensor(X_test_scaled, dtype=tf.float32)
        y_test_tensor = tf.convert_to_tensor(y_test, dtype=tf.float32)
        
        # Création du modèle
        model = self._create_neural_network(len(self.feature_columns))
        
        # Compilation
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Entraînement
        history = model.fit(
            X_train_tensor, y_train_tensor,
            epochs=50,
            batch_size=32,
            validation_data=(X_test_tensor, y_test_tensor),
            verbose=0
        )
        
        # Évaluation
        test_loss, test_accuracy = model.evaluate(X_test_tensor, y_test_tensor, verbose=0)
        
        # Sauvegarde du modèle
        model_name = "neural_network_threat_detector"
        model_path = os.path.join(self.models_dir, f"{model_name}")
        
        model.save(model_path)
        
        # Sauvegarde du scaler
        scaler_path = os.path.join(self.models_dir, f"{model_name}_scaler.joblib")
        joblib.dump(scaler, scaler_path)
        
        # Création de l'objet AIModel
        ai_model = AIModel(
            id=model_name,
            name="Neural Network Threat Detector",
            model_type=ModelType.NEURAL_NETWORK,
            version="1.0",
            accuracy=test_accuracy,
            precision=0.0,  # À calculer
            recall=0.0,     # À calculer
            f1_score=0.0,   # À calculer
            training_date=datetime.now(),
            last_updated=datetime.now(),
            is_active=True,
            model_path=model_path,
            feature_columns=self.feature_columns,
            hyperparameters=self.model_configs[ModelType.NEURAL_NETWORK]
        )
        
        self.models[model_name] = ai_model
        self.active_models[ModelType.NEURAL_NETWORK] = model
        self.scalers[model_name] = scaler
        
        logger.info(f"🧠 Neural Network entraîné - Accuracy: {test_accuracy:.3f}")
    
    def _create_neural_network(self, input_dim: int) -> keras.Model:
        """Création d'un réseau de neurones"""
        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(input_dim,)),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        return model
    
    async def analyze_threat(self, threat_features: ThreatFeatures) -> ThreatPrediction:
        """
        Analyse d'une menace avec l'IA
        """
        start_time = time.time()
        
        try:
            # Extraction des features
            features = self._extract_features(threat_features)
            
            # Prédictions par différents modèles
            predictions = {}
            anomaly_scores = {}
            
            # Random Forest
            if ModelType.RANDOM_FOREST in self.active_models:
                rf_prediction = await self._predict_random_forest(features)
                predictions[ModelType.RANDOM_FOREST] = rf_prediction
            
            # Isolation Forest
            if ModelType.ISOLATION_FOREST in self.active_models:
                if_prediction = await self._predict_isolation_forest(features)
                anomaly_scores[ModelType.ISOLATION_FOREST] = if_prediction
            
            # Neural Network
            if ModelType.NEURAL_NETWORK in self.active_models:
                nn_prediction = await self._predict_neural_network(features)
                predictions[ModelType.NEURAL_NETWORK] = nn_prediction
            
            # Ensemble des prédictions
            ensemble_prediction = self._ensemble_predictions(predictions, anomaly_scores)
            
            # Création de l'objet ThreatPrediction
            prediction = ThreatPrediction(
                id=f"pred_{int(time.time())}_{hash(threat_features.id)}",
                threat_features_id=threat_features.id,
                model_type=ModelType.ENSEMBLE,
                predicted_category=ensemble_prediction["category"],
                confidence_score=ensemble_prediction["confidence"],
                probability_scores=ensemble_prediction["probabilities"],
                anomaly_score=ensemble_prediction["anomaly_score"],
                timestamp=datetime.now(),
                model_version="1.0",
                features_used=self.feature_columns,
                prediction_time=time.time() - start_time
            )
            
            # Stockage de la prédiction
            self.prediction_history.append(prediction)
            
            # Notification via WebSocket
            await self._notify_prediction(prediction)
            
            return prediction
            
        except Exception as e:
            logger.error(f"Erreur analyse menace IA: {e}")
            raise
    
    def _extract_features(self, threat_features: ThreatFeatures) -> np.ndarray:
        """Extraction des features pour l'IA"""
        features = []
        
        for column in self.feature_columns:
            if hasattr(threat_features, column):
                value = getattr(threat_features, column)
                features.append(float(value) if value is not None else 0.0)
            else:
                features.append(0.0)
        
        return np.array(features).reshape(1, -1)
    
    async def _predict_random_forest(self, features: np.ndarray) -> Dict[str, Any]:
        """Prédiction avec Random Forest"""
        model_name = "random_forest_threat_detector"
        
        if model_name not in self.scalers:
            return {"prediction": 0, "probability": 0.5}
        
        # Normalisation
        scaler = self.scalers[model_name]
        features_scaled = scaler.transform(features)
        
        # Prédiction
        model = self.active_models[ModelType.RANDOM_FOREST]
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]  # Probabilité de menace
        
        return {
            "prediction": prediction,
            "probability": probability
        }
    
    async def _predict_isolation_forest(self, features: np.ndarray) -> float:
        """Prédiction avec Isolation Forest"""
        model_name = "isolation_forest_anomaly_detector"
        
        if model_name not in self.scalers:
            return 0.0
        
        # Normalisation
        scaler = self.scalers[model_name]
        features_scaled = scaler.transform(features)
        
        # Prédiction
        model = self.active_models[ModelType.ISOLATION_FOREST]
        anomaly_score = model.decision_function(features_scaled)[0]
        
        return anomaly_score
    
    async def _predict_neural_network(self, features: np.ndarray) -> Dict[str, Any]:
        """Prédiction avec Neural Network"""
        model_name = "neural_network_threat_detector"
        
        if model_name not in self.scalers:
            return {"prediction": 0, "probability": 0.5}
        
        # Normalisation
        scaler = self.scalers[model_name]
        features_scaled = scaler.transform(features)
        
        # Conversion en tenseur
        features_tensor = tf.convert_to_tensor(features_scaled, dtype=tf.float32)
        
        # Prédiction
        model = self.active_models[ModelType.NEURAL_NETWORK]
        probability = model.predict(features_tensor)[0][0]
        prediction = 1 if probability > 0.5 else 0
        
        return {
            "prediction": prediction,
            "probability": float(probability)
        }
    
    def _ensemble_predictions(self, predictions: Dict, anomaly_scores: Dict) -> Dict[str, Any]:
        """Ensemble des prédictions de différents modèles"""
        # Calcul de la prédiction moyenne
        probabilities = []
        for model_type, pred in predictions.items():
            probabilities.append(pred["probability"])
        
        avg_probability = np.mean(probabilities) if probabilities else 0.5
        
        # Calcul du score d'anomalie moyen
        anomaly_score = np.mean(list(anomaly_scores.values())) if anomaly_scores else 0.0
        
        # Détermination de la catégorie
        if avg_probability > 0.7:
            category = ThreatCategory.MALWARE
        elif avg_probability > 0.5:
            category = ThreatCategory.DDoS
        elif anomaly_score < -0.5:
            category = ThreatCategory.APT
        else:
            category = ThreatCategory.BENIGN
        
        # Calcul de la confiance
        confidence = min(avg_probability + abs(anomaly_score), 1.0)
        
        # Probabilités par catégorie
        probabilities_dict = {
            ThreatCategory.BENIGN.value: 1 - avg_probability,
            ThreatCategory.MALWARE.value: avg_probability * 0.4,
            ThreatCategory.DDoS.value: avg_probability * 0.3,
            ThreatCategory.APT.value: avg_probability * 0.2,
            ThreatCategory.PHISHING.value: avg_probability * 0.1
        }
        
        return {
            "category": category,
            "confidence": confidence,
            "probabilities": probabilities_dict,
            "anomaly_score": anomaly_score
        }
    
    async def _model_monitor(self):
        """Surveillance des modèles"""
        while True:
            try:
                await self._check_model_performance()
                await asyncio.sleep(3600)  # 1 heure
            except Exception as e:
                logger.error(f"Erreur surveillance modèles: {e}")
                await asyncio.sleep(1800)
    
    async def _check_model_performance(self):
        """Vérification de la performance des modèles"""
        if len(self.prediction_history) < 100:
            return
        
        # Calcul des métriques de performance
        recent_predictions = self.prediction_history[-100:]
        
        for model_name, model in self.models.items():
            if model.model_type == ModelType.RANDOM_FOREST:
                # Calcul de l'accuracy récente
                correct_predictions = sum(1 for p in recent_predictions 
                                        if p.confidence_score > 0.7)
                accuracy = correct_predictions / len(recent_predictions)
                
                # Mise à jour du modèle
                model.accuracy = accuracy
                model.last_updated = datetime.now()
                
                logger.info(f"📊 Performance {model_name}: {accuracy:.3f}")
    
    async def _performance_analyzer(self):
        """Analyseur de performance"""
        while True:
            try:
                await self._analyze_performance_trends()
                await asyncio.sleep(7200)  # 2 heures
            except Exception as e:
                logger.error(f"Erreur analyse performance: {e}")
                await asyncio.sleep(3600)
    
    async def _analyze_performance_trends(self):
        """Analyse des tendances de performance"""
        if len(self.prediction_history) < 50:
            return
        
        # Analyse des tendances
        recent_predictions = self.prediction_history[-50:]
        
        # Calcul des statistiques
        confidence_scores = [p.confidence_score for p in recent_predictions]
        avg_confidence = np.mean(confidence_scores)
        
        # Détection de dégradation
        if avg_confidence < 0.6:
            logger.warning("⚠️ Dégradation de la performance des modèles détectée")
            # Déclenchement du réentraînement
            await self._retrain_models()
    
    async def _feature_importance_analyzer(self):
        """Analyseur d'importance des features"""
        while True:
            try:
                await self._analyze_feature_importance()
                await asyncio.sleep(86400)  # 24 heures
            except Exception as e:
                logger.error(f"Erreur analyse features: {e}")
                await asyncio.sleep(43200)
    
    async def _analyze_feature_importance(self):
        """Analyse de l'importance des features"""
        if ModelType.RANDOM_FOREST not in self.active_models:
            return
        
        model = self.active_models[ModelType.RANDOM_FOREST]
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            # Tri par importance
            feature_importance = list(zip(self.feature_columns, importances))
            feature_importance.sort(key=lambda x: x[1], reverse=True)
            
            # Top 10 features
            top_features = feature_importance[:10]
            
            logger.info("🔍 Top 10 features importantes:")
            for feature, importance in top_features:
                logger.info(f"   {feature}: {importance:.4f}")
    
    async def _retrain_models(self):
        """Réentraînement des modèles"""
        logger.info("🔄 Réentraînement des modèles")
        
        # Génération de nouvelles données
        training_data = await self._generate_training_data()
        
        # Réentraînement
        await self._train_random_forest(training_data)
        await self._train_isolation_forest(training_data)
        await self._train_neural_network(training_data)
        
        logger.info("✅ Modèles réentraînés")
    
    async def _notify_prediction(self, prediction: ThreatPrediction):
        """Notification d'une prédiction via WebSocket"""
        message = {
            "type": "ai_prediction",
            "prediction": asdict(prediction),
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
    
    async def get_model_statistics(self) -> Dict[str, Any]:
        """Statistiques des modèles"""
        return {
            "total_models": len(self.models),
            "active_models": len(self.active_models),
            "total_predictions": len(self.prediction_history),
            "model_types": [model_type.value for model_type in self.active_models.keys()],
            "average_confidence": np.mean([p.confidence_score for p in self.prediction_history[-100:]]) if self.prediction_history else 0.0
        }
    
    async def get_prediction_history(self) -> List[ThreatPrediction]:
        """Historique des prédictions"""
        return self.prediction_history[-100:]  # Dernières 100 prédictions
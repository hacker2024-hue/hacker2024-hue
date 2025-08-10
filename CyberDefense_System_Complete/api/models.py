"""
Modèles Pydantic pour l'API REST
================================

Schémas de données pour les requêtes et réponses de l'API.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum


class CommunicationModeEnum(str, Enum):
    """Modes de communication"""
    TEXT = "text"
    VOICE = "voice"
    VISUAL = "visual"
    MIXED = "mixed"


class UrgencyLevelEnum(str, Enum):
    """Niveaux d'urgence"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SeverityEnum(str, Enum):
    """Niveaux de sévérité"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Modèles de requête
class ChatRequest(BaseModel):
    """Requête de chat"""
    content: str = Field(..., description="Contenu du message")
    user_id: str = Field(..., description="Identifiant utilisateur")
    session_id: Optional[str] = Field(None, description="Identifiant de session")
    mode: CommunicationModeEnum = Field(CommunicationModeEnum.TEXT, description="Mode de communication")
    urgency: UrgencyLevelEnum = Field(UrgencyLevelEnum.MEDIUM, description="Niveau d'urgence")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Métadonnées additionnelles")
    attachments: Optional[List[str]] = Field(None, description="Fichiers attachés")
    
    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Le contenu ne peut pas être vide')
        if len(v) > 10000:
            raise ValueError('Le contenu ne peut pas dépasser 10000 caractères')
        return v.strip()


class ThreatAnalysisRequest(BaseModel):
    """Requête d'analyse de menace"""
    indicators: List[str] = Field(..., description="Liste d'indicateurs à analyser")
    context: Optional[str] = Field(None, description="Contexte de l'analyse")
    user_id: str = Field(..., description="Identifiant utilisateur")
    
    @validator('indicators')
    def validate_indicators(cls, v):
        if not v:
            raise ValueError('Au moins un indicateur est requis')
        if len(v) > 100:
            raise ValueError('Maximum 100 indicateurs par requête')
        return v


class ReportRequest(BaseModel):
    """Requête de génération de rapport"""
    indicators: List[str] = Field(..., description="Indicateurs pour le rapport")
    report_type: str = Field("comprehensive", description="Type de rapport")
    user_id: str = Field(..., description="Identifiant utilisateur")
    include_predictions: bool = Field(True, description="Inclure les prédictions")


# Modèles de réponse
class SecurityAlertResponse(BaseModel):
    """Réponse d'alerte de sécurité"""
    alert_id: str
    severity: SeverityEnum
    category: str
    description: str
    indicators: List[str]
    recommendations: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime


class ChatResponse(BaseModel):
    """Réponse de chat"""
    response_id: str
    message_id: str
    content: str
    mode: CommunicationModeEnum
    confidence: float = Field(..., ge=0.0, le=1.0)
    urgency: UrgencyLevelEnum
    timestamp: datetime
    security_alert: Optional[SecurityAlertResponse]
    recommendations: List[str]
    follow_up_questions: List[str]


class ThreatIndicatorResponse(BaseModel):
    """Réponse d'indicateur de menace"""
    type: str
    value: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    source: str
    first_seen: datetime
    last_seen: datetime
    tags: List[str]
    severity: SeverityEnum


class ThreatAnalysisResponse(BaseModel):
    """Réponse d'analyse de menace"""
    timestamp: datetime
    indicators_analyzed: int
    threats_detected: List[Dict[str, Any]]
    risk_score: float = Field(..., ge=0.0, le=100.0)
    recommendations: List[str]
    mitre_techniques: List[str]


class ThreatCorrelationResponse(BaseModel):
    """Réponse de corrélation de menaces"""
    campaign_id: str
    indicators_count: int
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: SeverityEnum
    first_seen: datetime
    last_seen: datetime
    indicators: List[str]


class ThreatPredictionResponse(BaseModel):
    """Réponse de prédiction de menace"""
    threat_type: str
    predicted_incidents: int
    confidence: float = Field(..., ge=0.0, le=1.0)
    time_frame: str
    recommendation: str


class ThreatReportResponse(BaseModel):
    """Réponse de rapport de menace"""
    report_id: str
    generated_at: datetime
    summary: Dict[str, Any]
    detailed_analysis: ThreatAnalysisResponse
    threat_correlations: List[ThreatCorrelationResponse]
    future_predictions: List[ThreatPredictionResponse]
    mitre_mapping: Dict[str, Dict[str, Any]]
    executive_summary: str


class SessionSummaryResponse(BaseModel):
    """Réponse de résumé de session"""
    session_id: str
    user_id: str
    created_at: datetime
    duration: float
    message_count: int
    response_count: int
    urgency_level: UrgencyLevelEnum
    active_alerts: int
    main_topics: List[tuple]
    last_activity: datetime
    status: str


class HealthResponse(BaseModel):
    """Réponse de statut système"""
    status: str
    timestamp: datetime
    version: str
    components: Dict[str, Union[bool, int]]


class UserSessionsResponse(BaseModel):
    """Réponse des sessions utilisateur"""
    user_id: str
    sessions: List[SessionSummaryResponse]
    total_sessions: int


# Modèles d'erreur
class ErrorResponse(BaseModel):
    """Réponse d'erreur"""
    error: str
    detail: str
    timestamp: datetime
    request_id: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    """Réponse d'erreur de validation"""
    error: str = "Validation Error"
    details: List[Dict[str, Any]]
    timestamp: datetime


# Modèles pour WebSocket
class WebSocketMessage(BaseModel):
    """Message WebSocket"""
    content: str
    user_id: str
    session_id: str
    timestamp: Optional[datetime] = None


class WebSocketResponse(BaseModel):
    """Réponse WebSocket"""
    content: str
    urgency: UrgencyLevelEnum
    recommendations: List[str]
    follow_up_questions: List[str]
    timestamp: datetime
    type: str = "response"


class WebSocketNotification(BaseModel):
    """Notification WebSocket"""
    type: str = "notification"
    content: str
    urgency: UrgencyLevelEnum
    timestamp: datetime


# Modèles pour la configuration
class ExpertiseLevelEnum(str, Enum):
    """Niveaux d'expertise"""
    NOVICE = "novice"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class UserPreferences(BaseModel):
    """Préférences utilisateur"""
    expertise_level: ExpertiseLevelEnum = ExpertiseLevelEnum.INTERMEDIATE
    preferred_language: str = "fr"
    notification_level: UrgencyLevelEnum = UrgencyLevelEnum.MEDIUM
    communication_mode: CommunicationModeEnum = CommunicationModeEnum.TEXT


class UpdatePreferencesRequest(BaseModel):
    """Requête de mise à jour des préférences"""
    user_id: str
    preferences: UserPreferences


# Modèles pour les statistiques
class SystemStatsResponse(BaseModel):
    """Statistiques système"""
    total_sessions: int
    active_sessions: int
    total_messages: int
    total_threats_detected: int
    average_response_time: float
    uptime: float
    last_updated: datetime


class UserStatsResponse(BaseModel):
    """Statistiques utilisateur"""
    user_id: str
    total_sessions: int
    total_messages: int
    threats_detected: int
    average_session_duration: float
    most_common_topics: List[tuple]
    last_activity: datetime


# Modèles pour les batch operations
class BatchAnalysisRequest(BaseModel):
    """Requête d'analyse en lot"""
    batch_id: str
    indicators: List[str] = Field(..., max_items=1000)
    user_id: str
    priority: UrgencyLevelEnum = UrgencyLevelEnum.MEDIUM
    
    @validator('indicators')
    def validate_indicators(cls, v):
        if len(v) == 0:
            raise ValueError('Au moins un indicateur est requis')
        return v


class BatchAnalysisResponse(BaseModel):
    """Réponse d'analyse en lot"""
    batch_id: str
    status: str  # pending, processing, completed, failed
    total_indicators: int
    processed_indicators: int
    results: Optional[List[ThreatAnalysisResponse]] = None
    estimated_completion: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
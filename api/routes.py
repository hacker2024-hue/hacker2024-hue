"""
Routes API REST
===============

Endpoints pour l'interaction avec CyberSec AI Assistant.
"""

import asyncio
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from loguru import logger

from core.ai_engine import CyberSecAI
from communication.interface import CommunicationInterface, CommunicationMode, UrgencyLevel
from security.threat_analyzer import ThreatAnalyzer
from .models import *
from .main import get_ai_engine, get_comm_interface, get_threat_analyzer

# Création du routeur
router = APIRouter(
    tags=["CyberSec AI Assistant"],
    responses={
        500: {"model": ErrorResponse, "description": "Erreur interne du serveur"},
        422: {"model": ValidationErrorResponse, "description": "Erreur de validation"},
    }
)


@router.get("/health", 
           response_model=HealthResponse,
           summary="Vérification de l'état du système",
           description="Endpoint pour vérifier l'état de santé du système et de ses composants")
async def health_check(
    ai_engine: CyberSecAI = Depends(get_ai_engine),
    comm_interface: CommunicationInterface = Depends(get_comm_interface),
    threat_analyzer: ThreatAnalyzer = Depends(get_threat_analyzer)
):
    """Vérification de l'état du système"""
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        components={
            "ai_engine": ai_engine.model is not None,
            "communication_interface": True,
            "threat_analyzer": True,
            "websocket_connections": 0
        }
    )


@router.post("/chat", 
            response_model=ChatResponse,
            summary="Communication avec l'IA",
            description="Envoyer un message à l'IA et recevoir une réponse contextuelle")
async def chat(
    request: ChatRequest,
    comm_interface: CommunicationInterface = Depends(get_comm_interface)
):
    """Endpoint de chat avec l'IA"""
    
    try:
        # Conversion des enums
        mode = CommunicationMode(request.mode.value)
        urgency = UrgencyLevel(request.urgency.value)
        
        # Traitement du message
        response = await comm_interface.process_message(
            content=request.content,
            user_id=request.user_id,
            session_id=request.session_id,
            mode=mode,
            urgency=urgency,
            metadata=request.metadata,
            attachments=request.attachments
        )
        
        # Conversion de la réponse
        security_alert = None
        if response.security_alert:
            security_alert = SecurityAlertResponse(
                alert_id=response.security_alert.alert_id,
                severity=SeverityEnum(response.security_alert.severity),
                category=response.security_alert.category,
                description=response.security_alert.description,
                indicators=response.security_alert.indicators,
                recommendations=response.security_alert.recommendations,
                confidence=response.security_alert.confidence,
                timestamp=response.security_alert.timestamp
            )
        
        return ChatResponse(
            response_id=response.response_id,
            message_id=response.message_id,
            content=response.content,
            mode=CommunicationModeEnum(response.mode.value),
            confidence=response.confidence,
            urgency=UrgencyLevelEnum(response.urgency.value),
            timestamp=response.timestamp,
            security_alert=security_alert,
            recommendations=response.recommendations,
            follow_up_questions=response.follow_up_questions
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze",
            response_model=ThreatAnalysisResponse,
            summary="Analyse de menaces",
            description="Analyser des indicateurs de compromission et évaluer les menaces")
async def analyze_threats(
    request: ThreatAnalysisRequest,
    threat_analyzer: ThreatAnalyzer = Depends(get_threat_analyzer)
):
    """Endpoint d'analyse de menaces"""
    
    try:
        # Analyse des indicateurs
        analysis = await threat_analyzer.analyze_indicators(request.indicators)
        
        return ThreatAnalysisResponse(
            timestamp=analysis["timestamp"],
            indicators_analyzed=analysis["indicators_analyzed"],
            threats_detected=analysis["threats_detected"],
            risk_score=analysis["risk_score"],
            recommendations=analysis["recommendations"],
            mitre_techniques=analysis["mitre_techniques"]
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/correlations",
           response_model=List[ThreatCorrelationResponse],
           summary="Corrélation de menaces",
           description="Obtenir les corrélations de menaces détectées")
async def get_threat_correlations(
    time_window: int = Query(3600, description="Fenêtre temporelle en secondes"),
    threat_analyzer: ThreatAnalyzer = Depends(get_threat_analyzer)
):
    """Endpoint de corrélation de menaces"""
    
    try:
        correlations = await threat_analyzer.correlate_threats(time_window)
        
        return [
            ThreatCorrelationResponse(
                campaign_id=corr["campaign_id"],
                indicators_count=corr["indicators_count"],
                confidence=corr["confidence"],
                severity=SeverityEnum(corr["severity"]),
                first_seen=corr["first_seen"],
                last_seen=corr["last_seen"],
                indicators=corr["indicators"]
            )
            for corr in correlations
        ]
        
    except Exception as e:
        logger.error(f"Erreur lors de la corrélation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/report",
            response_model=ThreatReportResponse,
            summary="Génération de rapport",
            description="Générer un rapport complet d'analyse de menaces")
async def generate_threat_report(
    request: ReportRequest,
    threat_analyzer: ThreatAnalyzer = Depends(get_threat_analyzer)
):
    """Endpoint de génération de rapport"""
    
    try:
        report = await threat_analyzer.generate_threat_report(request.indicators)
        
        # Conversion des corrélations
        correlations = [
            ThreatCorrelationResponse(
                campaign_id=corr["campaign_id"],
                indicators_count=corr["indicators_count"],
                confidence=corr["confidence"],
                severity=SeverityEnum(corr["severity"]),
                first_seen=corr["first_seen"],
                last_seen=corr["last_seen"],
                indicators=corr["indicators"]
            )
            for corr in report["threat_correlations"]
        ]
        
        # Conversion des prédictions
        predictions = [
            ThreatPredictionResponse(
                threat_type=pred["threat_type"],
                predicted_incidents=pred["predicted_incidents"],
                confidence=pred["confidence"],
                time_frame=pred["time_frame"],
                recommendation=pred["recommendation"]
            )
            for pred in report["future_predictions"]
        ]
        
        # Conversion de l'analyse détaillée
        detailed_analysis = ThreatAnalysisResponse(
            timestamp=report["detailed_analysis"]["timestamp"],
            indicators_analyzed=report["detailed_analysis"]["indicators_analyzed"],
            threats_detected=report["detailed_analysis"]["threats_detected"],
            risk_score=report["detailed_analysis"]["risk_score"],
            recommendations=report["detailed_analysis"]["recommendations"],
            mitre_techniques=report["detailed_analysis"]["mitre_techniques"]
        )
        
        return ThreatReportResponse(
            report_id=report["report_id"],
            generated_at=report["generated_at"],
            summary=report["summary"],
            detailed_analysis=detailed_analysis,
            threat_correlations=correlations,
            future_predictions=predictions,
            mitre_mapping=report["mitre_mapping"],
            executive_summary=report["executive_summary"]
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération du rapport: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}",
           response_model=SessionSummaryResponse,
           summary="Résumé de session",
           description="Obtenir le résumé d'une session de communication")
async def get_session_summary(
    session_id: str,
    comm_interface: CommunicationInterface = Depends(get_comm_interface)
):
    """Endpoint de résumé de session"""
    
    try:
        summary = await comm_interface.get_session_summary(session_id)
        
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        
        return SessionSummaryResponse(
            session_id=summary["session_id"],
            user_id=summary["user_id"],
            created_at=summary["created_at"],
            duration=summary["duration"],
            message_count=summary["message_count"],
            response_count=summary["response_count"],
            urgency_level=UrgencyLevelEnum(summary["urgency_level"]),
            active_alerts=summary["active_alerts"],
            main_topics=summary["main_topics"],
            last_activity=summary["last_activity"],
            status=summary["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du résumé: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/sessions",
           response_model=UserSessionsResponse,
           summary="Sessions utilisateur",
           description="Obtenir toutes les sessions d'un utilisateur")
async def get_user_sessions(
    user_id: str,
    comm_interface: CommunicationInterface = Depends(get_comm_interface)
):
    """Endpoint des sessions utilisateur"""
    
    try:
        sessions_data = await comm_interface.get_user_sessions(user_id)
        
        sessions = [
            SessionSummaryResponse(
                session_id=session["session_id"],
                user_id=session["user_id"],
                created_at=session["created_at"],
                duration=session["duration"],
                message_count=session["message_count"],
                response_count=session["response_count"],
                urgency_level=UrgencyLevelEnum(session["urgency_level"]),
                active_alerts=session["active_alerts"],
                main_topics=session["main_topics"],
                last_activity=session["last_activity"],
                status=session["status"]
            )
            for session in sessions_data
        ]
        
        return UserSessionsResponse(
            user_id=user_id,
            sessions=sessions,
            total_sessions=len(sessions)
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}",
              summary="Fermeture de session",
              description="Fermer une session de communication")
async def close_session(
    session_id: str,
    comm_interface: CommunicationInterface = Depends(get_comm_interface)
):
    """Endpoint de fermeture de session"""
    
    try:
        success = await comm_interface.close_session(session_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Session non trouvée")
        
        return {"message": f"Session {session_id} fermée avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la fermeture de session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{user_id}/{session_id}",
           summary="Résumé de conversation",
           description="Obtenir un résumé de conversation IA")
async def get_conversation_summary(
    user_id: str,
    session_id: str,
    ai_engine: CyberSecAI = Depends(get_ai_engine)
):
    """Endpoint de résumé de conversation"""
    
    try:
        summary = await ai_engine.get_conversation_summary(user_id, session_id)
        return summary
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du résumé de conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch/analyze",
            response_model=BatchAnalysisResponse,
            summary="Analyse en lot",
            description="Lancer une analyse en lot d'indicateurs")
async def batch_analyze(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks,
    threat_analyzer: ThreatAnalyzer = Depends(get_threat_analyzer)
):
    """Endpoint d'analyse en lot"""
    
    try:
        # Création de la tâche en arrière-plan
        batch_id = request.batch_id or f"batch_{uuid.uuid4().hex[:8]}"
        
        # En production, utiliser une queue (Redis, Celery, etc.)
        background_tasks.add_task(
            process_batch_analysis,
            batch_id,
            request.indicators,
            threat_analyzer
        )
        
        return BatchAnalysisResponse(
            batch_id=batch_id,
            status="pending",
            total_indicators=len(request.indicators),
            processed_indicators=0,
            estimated_completion=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du lancement de l'analyse en lot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/batch/{batch_id}",
           response_model=BatchAnalysisResponse,
           summary="Statut analyse en lot",
           description="Obtenir le statut d'une analyse en lot")
async def get_batch_status(batch_id: str):
    """Endpoint de statut d'analyse en lot"""
    
    # En production, récupérer depuis la base de données
    return BatchAnalysisResponse(
        batch_id=batch_id,
        status="completed",
        total_indicators=10,
        processed_indicators=10,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@router.get("/stats/system",
           response_model=SystemStatsResponse,
           summary="Statistiques système",
           description="Obtenir les statistiques globales du système")
async def get_system_stats():
    """Endpoint de statistiques système"""
    
    return SystemStatsResponse(
        total_sessions=100,
        active_sessions=5,
        total_messages=1500,
        total_threats_detected=50,
        average_response_time=0.5,
        uptime=3600.0,
        last_updated=datetime.utcnow()
    )


@router.get("/stats/user/{user_id}",
           response_model=UserStatsResponse,
           summary="Statistiques utilisateur",
           description="Obtenir les statistiques d'un utilisateur")
async def get_user_stats(user_id: str):
    """Endpoint de statistiques utilisateur"""
    
    return UserStatsResponse(
        user_id=user_id,
        total_sessions=10,
        total_messages=100,
        threats_detected=5,
        average_session_duration=300.0,
        most_common_topics=[("malware", 3), ("network", 2)],
        last_activity=datetime.utcnow()
    )


@router.post("/preferences",
            summary="Mise à jour des préférences",
            description="Mettre à jour les préférences utilisateur")
async def update_user_preferences(request: UpdatePreferencesRequest):
    """Endpoint de mise à jour des préférences"""
    
    # En production, sauvegarder en base de données
    return {"message": f"Préférences mises à jour pour l'utilisateur {request.user_id}"}


@router.get("/mitre/{technique_id}",
           summary="Information MITRE ATT&CK",
           description="Obtenir les informations d'une technique MITRE ATT&CK")
async def get_mitre_technique(
    technique_id: str,
    threat_analyzer: ThreatAnalyzer = Depends(get_threat_analyzer)
):
    """Endpoint d'information MITRE ATT&CK"""
    
    try:
        technique_info = threat_analyzer.mitre_techniques.get(technique_id)
        
        if not technique_info:
            raise HTTPException(status_code=404, detail="Technique MITRE non trouvée")
        
        return {
            "technique_id": technique_id,
            **technique_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la technique MITRE: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/indicators/{indicator_value}",
           summary="Information sur un indicateur",
           description="Obtenir les informations détaillées sur un indicateur")
async def get_indicator_info(
    indicator_value: str,
    threat_analyzer: ThreatAnalyzer = Depends(get_threat_analyzer)
):
    """Endpoint d'information sur un indicateur"""
    
    try:
        indicator_info = threat_analyzer.indicators_db.get(indicator_value)
        
        if not indicator_info:
            raise HTTPException(status_code=404, detail="Indicateur non trouvé")
        
        return ThreatIndicatorResponse(
            type=indicator_info.type,
            value=indicator_info.value,
            confidence=indicator_info.confidence,
            source=indicator_info.source,
            first_seen=indicator_info.first_seen,
            last_seen=indicator_info.last_seen,
            tags=indicator_info.tags,
            severity=SeverityEnum(indicator_info.severity)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'indicateur: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Fonctions utilitaires
async def process_batch_analysis(
    batch_id: str,
    indicators: List[str],
    threat_analyzer: ThreatAnalyzer
):
    """Traitement d'analyse en lot en arrière-plan"""
    
    try:
        logger.info(f"Démarrage de l'analyse en lot {batch_id}")
        
        # Simulation du traitement
        for i, indicator in enumerate(indicators):
            # En production, traiter chaque indicateur
            await asyncio.sleep(0.1)  # Simulation
            logger.debug(f"Traitement {i+1}/{len(indicators)} pour {batch_id}")
        
        logger.success(f"Analyse en lot {batch_id} terminée")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse en lot {batch_id}: {e}")


# Gestionnaires d'erreur
@router.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Gestionnaire d'erreur de validation"""
    return JSONResponse(
        status_code=422,
        content=ValidationErrorResponse(
            details=[{"error": str(exc)}],
            timestamp=datetime.utcnow()
        ).dict()
    )


@router.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Gestionnaire d'erreur général"""
    logger.error(f"Erreur non gérée: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Erreur interne du serveur",
            detail=str(exc),
            timestamp=datetime.utcnow()
        ).dict()
    )
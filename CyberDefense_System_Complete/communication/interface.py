"""
Interface de Communication Avancée
==================================

Interface multimodale pour la communication avec les experts en sécurité.
"""

import asyncio
import json
import uuid
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from loguru import logger

from core.ai_engine import CyberSecAI, ConversationContext, SecurityAlert
from core.config import config


class CommunicationMode(Enum):
    """Modes de communication disponibles"""
    TEXT = "text"
    VOICE = "voice"
    VISUAL = "visual"
    MIXED = "mixed"


class UrgencyLevel(Enum):
    """Niveaux d'urgence pour les communications"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Message:
    """Structure d'un message"""
    message_id: str
    user_id: str
    session_id: str
    content: str
    mode: CommunicationMode
    timestamp: datetime
    urgency: UrgencyLevel
    metadata: Dict[str, Any]
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []


@dataclass
class Response:
    """Structure d'une réponse"""
    response_id: str
    message_id: str
    content: str
    mode: CommunicationMode
    confidence: float
    urgency: UrgencyLevel
    timestamp: datetime
    security_alert: Optional[SecurityAlert]
    recommendations: List[str]
    follow_up_questions: List[str]


class CommunicationInterface:
    """
    Interface de communication avancée pour CyberSec AI
    
    Fonctionnalités:
    - Communication multimodale (texte, voix, visuel)
    - Adaptation au contexte et à l'urgence
    - Gestion de sessions multiples
    - Escalade automatique des alertes critiques
    - Interface intuitive pour experts et novices
    """
    
    def __init__(self, ai_engine: CyberSecAI):
        self.ai_engine = ai_engine
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.message_history: Dict[str, List[Message]] = {}
        self.response_history: Dict[str, List[Response]] = {}
        self.escalation_handlers: Dict[str, callable] = {}
        
    async def initialize(self):
        """Initialisation de l'interface de communication"""
        logger.info("Initialisation de l'interface de communication...")
        
        try:
            # Initialisation du moteur IA si nécessaire
            if not self.ai_engine.model:
                await self.ai_engine.initialize()
            
            # Configuration des handlers d'escalade
            await self._setup_escalation_handlers()
            
            # Initialisation des canaux de communication
            await self._setup_communication_channels()
            
            logger.success("Interface de communication initialisée")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}")
            raise
    
    async def _setup_escalation_handlers(self):
        """Configuration des handlers pour l'escalade d'alertes"""
        self.escalation_handlers = {
            UrgencyLevel.CRITICAL.value: self._handle_critical_escalation,
            UrgencyLevel.HIGH.value: self._handle_high_escalation,
            UrgencyLevel.MEDIUM.value: self._handle_medium_escalation,
            UrgencyLevel.LOW.value: self._handle_low_escalation
        }
    
    async def _setup_communication_channels(self):
        """Configuration des canaux de communication"""
        # Configuration des canaux (WebSocket, REST API, etc.)
        logger.info("Canaux de communication configurés")
    
    async def process_message(
        self,
        content: str,
        user_id: str,
        session_id: Optional[str] = None,
        mode: CommunicationMode = CommunicationMode.TEXT,
        urgency: UrgencyLevel = UrgencyLevel.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None,
        attachments: Optional[List[str]] = None
    ) -> Response:
        """
        Traitement d'un message utilisateur
        
        Args:
            content: Contenu du message
            user_id: Identifiant utilisateur
            session_id: Identifiant de session (généré si None)
            mode: Mode de communication
            urgency: Niveau d'urgence
            metadata: Métadonnées additionnelles
            attachments: Fichiers attachés
            
        Returns:
            Réponse structurée
        """
        
        # Génération d'IDs si nécessaires
        if session_id is None:
            session_id = f"session_{uuid.uuid4().hex[:8]}"
        
        message_id = f"msg_{uuid.uuid4().hex[:8]}"
        response_id = f"resp_{uuid.uuid4().hex[:8]}"
        
        # Création du message
        message = Message(
            message_id=message_id,
            user_id=user_id,
            session_id=session_id,
            content=content,
            mode=mode,
            timestamp=datetime.utcnow(),
            urgency=urgency,
            metadata=metadata or {},
            attachments=attachments or []
        )
        
        # Sauvegarde du message
        await self._save_message(message)
        
        try:
            # Traitement par le moteur IA
            ai_response, security_alert = await self.ai_engine.process_message(
                content, user_id, session_id, metadata
            )
            
            # Analyse de l'urgence et adaptation de la réponse
            adapted_response, detected_urgency = await self._adapt_response(
                ai_response, security_alert, urgency, mode
            )
            
            # Génération de questions de suivi
            follow_up_questions = await self._generate_follow_up_questions(
                content, adapted_response, security_alert
            )
            
            # Génération de recommandations
            recommendations = await self._generate_recommendations(
                security_alert, detected_urgency
            )
            
            # Création de la réponse
            response = Response(
                response_id=response_id,
                message_id=message_id,
                content=adapted_response,
                mode=mode,
                confidence=0.85,  # À calculer dynamiquement
                urgency=detected_urgency,
                timestamp=datetime.utcnow(),
                security_alert=security_alert,
                recommendations=recommendations,
                follow_up_questions=follow_up_questions
            )
            
            # Sauvegarde de la réponse
            await self._save_response(response)
            
            # Gestion de l'escalade si nécessaire
            if detected_urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]:
                await self._handle_escalation(response, message)
            
            # Mise à jour de la session
            await self._update_session(session_id, message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")
            
            # Réponse d'erreur
            error_response = Response(
                response_id=response_id,
                message_id=message_id,
                content="Je rencontre actuellement des difficultés techniques. Un expert va examiner votre demande.",
                mode=mode,
                confidence=0.0,
                urgency=UrgencyLevel.HIGH,  # Escalade en cas d'erreur
                timestamp=datetime.utcnow(),
                security_alert=None,
                recommendations=["Contacter le support technique"],
                follow_up_questions=[]
            )
            
            await self._save_response(error_response)
            return error_response
    
    async def _adapt_response(
        self,
        ai_response: str,
        security_alert: Optional[SecurityAlert],
        original_urgency: UrgencyLevel,
        mode: CommunicationMode
    ) -> tuple[str, UrgencyLevel]:
        """Adaptation de la réponse selon le contexte"""
        
        # Détection automatique de l'urgence basée sur l'alerte
        detected_urgency = original_urgency
        
        if security_alert:
            severity_mapping = {
                "critical": UrgencyLevel.CRITICAL,
                "high": UrgencyLevel.HIGH,
                "medium": UrgencyLevel.MEDIUM,
                "low": UrgencyLevel.LOW
            }
            detected_urgency = severity_mapping.get(
                security_alert.severity, original_urgency
            )
        
        # Adaptation du contenu selon l'urgence
        if detected_urgency == UrgencyLevel.CRITICAL:
            adapted_response = f"🚨 **ALERTE CRITIQUE** 🚨\n\n{ai_response}\n\n" \
                             f"**ACTION IMMÉDIATE REQUISE** - Cette situation nécessite une intervention urgente."
                             
        elif detected_urgency == UrgencyLevel.HIGH:
            adapted_response = f"⚠️ **ALERTE ÉLEVÉE** ⚠️\n\n{ai_response}\n\n" \
                             f"Surveillance renforcée recommandée."
                             
        elif mode == CommunicationMode.VOICE:
            # Adaptation pour la communication vocale
            adapted_response = self._adapt_for_voice(ai_response)
            
        else:
            adapted_response = ai_response
        
        return adapted_response, detected_urgency
    
    def _adapt_for_voice(self, text: str) -> str:
        """Adaptation du texte pour la communication vocale"""
        # Simplification pour la synthèse vocale
        adapted = text.replace("🚨", "ALERTE")
        adapted = adapted.replace("⚠️", "ATTENTION")
        adapted = adapted.replace("ℹ️", "INFORMATION")
        
        # Ajout de pauses naturelles
        adapted = adapted.replace(". ", ". [pause] ")
        adapted = adapted.replace("? ", "? [pause] ")
        adapted = adapted.replace("! ", "! [pause] ")
        
        return adapted
    
    async def _generate_follow_up_questions(
        self,
        original_message: str,
        response: str,
        security_alert: Optional[SecurityAlert]
    ) -> List[str]:
        """Génération de questions de suivi intelligentes"""
        
        questions = []
        
        # Questions basées sur le type d'alerte
        if security_alert:
            if security_alert.severity in ["high", "critical"]:
                questions.extend([
                    "Avez-vous observé d'autres comportements suspects récemment ?",
                    "Quels systèmes pourraient être affectés ?",
                    "Disposez-vous de logs additionnels pour l'analyse ?"
                ])
            
            if "malware" in security_alert.category:
                questions.extend([
                    "Sur quels systèmes ce fichier a-t-il été détecté ?",
                    "Y a-t-il eu des modifications récentes sur ces machines ?"
                ])
            
            if "network" in security_alert.category:
                questions.extend([
                    "Avez-vous noté des ralentissements réseau ?",
                    "D'autres adresses IP suspectes ont-elles été observées ?"
                ])
        
        # Questions contextuelles basées sur le message original
        message_lower = original_message.lower()
        
        if "analyse" in message_lower:
            questions.append("Souhaitez-vous une analyse plus détaillée ?")
        
        if "protection" in message_lower:
            questions.append("Voulez-vous que je vous guide dans la mise en place des protections ?")
        
        if "incident" in message_lower:
            questions.append("Faut-il documenter cet incident dans le système de gestion ?")
        
        # Limitation du nombre de questions
        return questions[:3]
    
    async def _generate_recommendations(
        self,
        security_alert: Optional[SecurityAlert],
        urgency: UrgencyLevel
    ) -> List[str]:
        """Génération de recommandations adaptées"""
        
        recommendations = []
        
        # Recommandations basées sur l'urgence
        if urgency == UrgencyLevel.CRITICAL:
            recommendations.extend([
                "Isoler immédiatement les systèmes affectés",
                "Activer la cellule de crise",
                "Documenter toutes les actions entreprises",
                "Préparer la communication de crise"
            ])
        
        elif urgency == UrgencyLevel.HIGH:
            recommendations.extend([
                "Renforcer la surveillance",
                "Vérifier l'intégrité des sauvegardes",
                "Informer l'équipe de sécurité",
                "Préparer un plan de réponse"
            ])
        
        # Recommandations spécifiques aux alertes
        if security_alert and security_alert.recommendations:
            recommendations.extend(security_alert.recommendations)
        
        # Recommandations générales
        recommendations.extend([
            "Maintenir une communication régulière",
            "Documenter les observations",
            "Suivre les procédures établies"
        ])
        
        # Suppression des doublons et limitation
        return list(dict.fromkeys(recommendations))[:5]
    
    async def _save_message(self, message: Message):
        """Sauvegarde d'un message"""
        session_id = message.session_id
        
        if session_id not in self.message_history:
            self.message_history[session_id] = []
        
        self.message_history[session_id].append(message)
        
        # Limitation de l'historique
        if len(self.message_history[session_id]) > config.max_conversation_history:
            self.message_history[session_id] = self.message_history[session_id][-config.max_conversation_history:]
    
    async def _save_response(self, response: Response):
        """Sauvegarde d'une réponse"""
        # Récupération de la session via le message
        session_id = None
        for sid, messages in self.message_history.items():
            if any(msg.message_id == response.message_id for msg in messages):
                session_id = sid
                break
        
        if session_id:
            if session_id not in self.response_history:
                self.response_history[session_id] = []
            
            self.response_history[session_id].append(response)
            
            # Limitation de l'historique
            if len(self.response_history[session_id]) > config.max_conversation_history:
                self.response_history[session_id] = self.response_history[session_id][-config.max_conversation_history:]
    
    async def _update_session(self, session_id: str, message: Message, response: Response):
        """Mise à jour des informations de session"""
        
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = {
                "created_at": datetime.utcnow(),
                "user_id": message.user_id,
                "message_count": 0,
                "last_activity": datetime.utcnow(),
                "current_topic": None,
                "urgency_level": UrgencyLevel.LOW,
                "active_alerts": []
            }
        
        session = self.active_sessions[session_id]
        session["message_count"] += 1
        session["last_activity"] = datetime.utcnow()
        session["urgency_level"] = max(session["urgency_level"], response.urgency, key=lambda x: x.value)
        
        # Gestion des alertes actives
        if response.security_alert:
            session["active_alerts"].append(response.security_alert)
            
            # Limitation des alertes actives
            if len(session["active_alerts"]) > 10:
                session["active_alerts"] = session["active_alerts"][-10:]
    
    async def _handle_escalation(self, response: Response, message: Message):
        """Gestion de l'escalade des alertes"""
        
        urgency = response.urgency.value
        handler = self.escalation_handlers.get(urgency)
        
        if handler:
            await handler(response, message)
    
    async def _handle_critical_escalation(self, response: Response, message: Message):
        """Escalade critique - notification immédiate"""
        logger.critical(f"ESCALADE CRITIQUE: Session {message.session_id}")
        
        # En production: notification SMS, email, appel automatique
        escalation_data = {
            "level": "CRITICAL",
            "session_id": message.session_id,
            "user_id": message.user_id,
            "alert": asdict(response.security_alert) if response.security_alert else None,
            "timestamp": datetime.utcnow(),
            "automatic_actions": [
                "Équipe de crise notifiée",
                "Procédures d'urgence activées",
                "Surveillance continue établie"
            ]
        }
        
        # Simulation de notification
        logger.warning(f"Notification d'escalade critique envoyée: {escalation_data}")
    
    async def _handle_high_escalation(self, response: Response, message: Message):
        """Escalade élevée - notification prioritaire"""
        logger.warning(f"ESCALADE ÉLEVÉE: Session {message.session_id}")
        
        escalation_data = {
            "level": "HIGH",
            "session_id": message.session_id,
            "user_id": message.user_id,
            "alert": asdict(response.security_alert) if response.security_alert else None,
            "timestamp": datetime.utcnow()
        }
        
        # Simulation de notification
        logger.info(f"Notification d'escalade élevée envoyée: {escalation_data}")
    
    async def _handle_medium_escalation(self, response: Response, message: Message):
        """Escalade modérée - notification standard"""
        logger.info(f"Escalade modérée: Session {message.session_id}")
    
    async def _handle_low_escalation(self, response: Response, message: Message):
        """Escalade faible - logging seulement"""
        logger.debug(f"Escalade faible: Session {message.session_id}")
    
    async def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Génération d'un résumé de session"""
        
        if session_id not in self.active_sessions:
            return {"error": "Session non trouvée"}
        
        session = self.active_sessions[session_id]
        messages = self.message_history.get(session_id, [])
        responses = self.response_history.get(session_id, [])
        
        # Calcul de statistiques
        total_messages = len(messages)
        total_responses = len(responses)
        active_alerts = len(session["active_alerts"])
        
        # Analyse des topics
        topics = {}
        for response in responses:
            if response.security_alert:
                category = response.security_alert.category
                topics[category] = topics.get(category, 0) + 1
        
        return {
            "session_id": session_id,
            "user_id": session["user_id"],
            "created_at": session["created_at"],
            "duration": (datetime.utcnow() - session["created_at"]).total_seconds(),
            "message_count": total_messages,
            "response_count": total_responses,
            "urgency_level": session["urgency_level"].value,
            "active_alerts": active_alerts,
            "main_topics": sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3],
            "last_activity": session["last_activity"],
            "status": "active" if session["last_activity"] > datetime.utcnow() - timedelta(minutes=30) else "inactive"
        }
    
    async def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Récupération des sessions d'un utilisateur"""
        
        user_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if session["user_id"] == user_id:
                summary = await self.get_session_summary(session_id)
                user_sessions.append(summary)
        
        return sorted(user_sessions, key=lambda x: x["last_activity"], reverse=True)
    
    async def close_session(self, session_id: str) -> bool:
        """Fermeture d'une session"""
        
        if session_id in self.active_sessions:
            # Archivage des données de session si nécessaire
            session = self.active_sessions[session_id]
            session["closed_at"] = datetime.utcnow()
            
            # Nettoyage
            del self.active_sessions[session_id]
            
            logger.info(f"Session {session_id} fermée")
            return True
        
        return False
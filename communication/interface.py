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
from core.security_intelligence import SecurityIntelligenceEngine, SecurityIncident, NetworkEvent
from communication.voice_engine import VoiceEngine, VoiceSettings, EmotionalTone, Language
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
    - Intégration complète avec l'intelligence de sécurité
    - Communication vocale haute qualité
    """
    
    def __init__(self, ai_engine: CyberSecAI):
        self.ai_engine = ai_engine
        self.security_intelligence = SecurityIntelligenceEngine()
        self.voice_engine = VoiceEngine()
        
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.message_history: Dict[str, List[Message]] = {}
        self.response_history: Dict[str, List[Response]] = {}
        self.escalation_handlers: Dict[str, callable] = {}
        
        # État de communication vocale
        self.voice_enabled = False
        self.current_voice_settings = VoiceSettings()
        self.is_listening = False
        
        # Callbacks et handlers
        self.security_alert_handler = None
        self.emergency_response_handler = None
        
    async def initialize(self):
        """Initialisation de l'interface de communication"""
        logger.info("Initialisation de l'interface de communication avancée...")
        
        try:
            # Initialisation du moteur IA si nécessaire
            if not self.ai_engine.model:
                await self.ai_engine.initialize()
            
            # Initialisation de l'intelligence de sécurité
            await self.security_intelligence.initialize()
            
            # Initialisation du moteur vocal
            voice_initialized = await self.voice_engine.initialize()
            if voice_initialized:
                self.voice_enabled = True
                logger.success("Moteur vocal activé")
            else:
                logger.warning("Moteur vocal non disponible - mode texte uniquement")
            
            # Configuration des callbacks
            await self._setup_callbacks()
            
            # Configuration des handlers d'escalade
            await self._setup_escalation_handlers()
            
            logger.success("Interface de communication initialisée")
            
        except Exception as e:
            logger.error(f"Erreur initialisation interface: {e}")
            raise
    
    async def _setup_callbacks(self):
        """Configuration des callbacks entre modules"""
        
        # Callback pour les alertes de sécurité
        self.security_intelligence.set_alert_callback(self._handle_security_alert)
        
        # Callback pour les communications vocales d'urgence
        self.security_intelligence.set_voice_callback(self._handle_voice_alert)
        
        # Callback pour la reconnaissance vocale
        if self.voice_enabled:
            await self.voice_engine.start_listening(self._handle_voice_input)
    
    async def _setup_escalation_handlers(self):
        """Configuration des handlers d'escalade"""
        try:
            # Handler pour alertes critiques
            self.escalation_handlers["critical"] = self._handle_critical_escalation
            
            # Handler pour urgences maximum
            self.escalation_handlers["emergency"] = self._handle_emergency_escalation
            
            # Handler pour incidents techniques
            self.escalation_handlers["technical"] = self._handle_technical_escalation
            
            logger.success("Handlers d'escalade configurés")
            
        except Exception as e:
            logger.error(f"Erreur configuration escalade: {e}")
    
    async def process_message(
        self, 
        user_id: str, 
        content: str, 
        mode: CommunicationMode = CommunicationMode.TEXT,
        session_id: Optional[str] = None
    ) -> Response:
        """
        Traitement d'un message utilisateur avec analyse de sécurité intégrée
        """
        
        try:
            # Génération de l'ID de session si nécessaire
            if not session_id:
                session_id = f"session_{uuid.uuid4().hex[:8]}"
            
            # Création du message
            message = Message(
                message_id=f"msg_{uuid.uuid4().hex[:8]}",
                user_id=user_id,
                session_id=session_id,
                content=content,
                mode=mode,
                timestamp=datetime.now(),
                urgency=UrgencyLevel.LOW,
                metadata={}
            )
            
            # Ajout à l'historique
            if session_id not in self.message_history:
                self.message_history[session_id] = []
            self.message_history[session_id].append(message)
            
            # Analyse de sécurité du message
            security_analysis = await self._analyze_message_security(message)
            
            # Adaptation de l'urgence selon l'analyse
            message.urgency = self._determine_urgency(security_analysis)
            
            # Obtention du contexte utilisateur
            user_context = await self._get_user_context(user_id, session_id)
            
            # Génération de la réponse
            response = await self._generate_response(message, user_context, security_analysis)
            
            # Ajout à l'historique des réponses
            if session_id not in self.response_history:
                self.response_history[session_id] = []
            self.response_history[session_id].append(response)
            
            # Communication vocale si nécessaire
            if self.voice_enabled and response.urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]:
                await self._voice_respond(response)
            
            # Escalade si nécessaire
            await self._check_escalation(response, security_analysis)
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur traitement message: {e}")
            return self._create_error_response(str(e))
    
    async def _analyze_message_security(self, message: Message) -> Dict[str, Any]:
        """Analyse de sécurité d'un message"""
        try:
            # Obtention du contexte utilisateur
            user_context = {
                "user_id": message.user_id,
                "session_id": message.session_id,
                "timestamp": message.timestamp.isoformat(),
                "mode": message.mode.value
            }
            
            # Analyse par l'intelligence de sécurité
            analysis = await self.security_intelligence.analyze_text_input(
                message.content, 
                user_context
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erreur analyse sécurité message: {e}")
            return {"error": str(e), "risk_score": 0.0}
    
    def _determine_urgency(self, security_analysis: Dict[str, Any]) -> UrgencyLevel:
        """Détermination du niveau d'urgence basé sur l'analyse de sécurité"""
        
        risk_score = security_analysis.get("risk_score", 0.0)
        malicious_patterns = security_analysis.get("malicious_patterns", [])
        intent = security_analysis.get("intent", "general_inquiry")
        
        # Urgence basée sur le score de risque
        if risk_score >= 0.8:
            return UrgencyLevel.CRITICAL
        elif risk_score >= 0.6:
            return UrgencyLevel.HIGH
        elif risk_score >= 0.3:
            return UrgencyLevel.MEDIUM
        
        # Urgence basée sur l'intention
        if intent == "incident_report":
            return UrgencyLevel.HIGH
        elif intent in ["vulnerability_inquiry", "threat_intelligence"]:
            return UrgencyLevel.MEDIUM
        
        # Urgence basée sur les patterns malicieux
        if malicious_patterns:
            return UrgencyLevel.HIGH
        
        return UrgencyLevel.LOW
    
    async def _get_user_context(self, user_id: str, session_id: str) -> ConversationContext:
        """Récupération du contexte utilisateur"""
        
        # Récupération de l'historique de conversation
        conversation_history = []
        if session_id in self.message_history:
            for msg in self.message_history[session_id][-10:]:  # 10 derniers messages
                conversation_history.append({
                    "role": "user",
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                })
        
        if session_id in self.response_history:
            for resp in self.response_history[session_id][-10:]:  # 10 dernières réponses
                conversation_history.append({
                    "role": "assistant",
                    "content": resp.content,
                    "timestamp": resp.timestamp.isoformat()
                })
        
        # Tri par timestamp
        conversation_history.sort(key=lambda x: x["timestamp"])
        
        # Création du contexte
        context = ConversationContext(
            user_id=user_id,
            session_id=session_id,
            conversation_history=conversation_history,
            user_expertise_level="intermediate",  # À déterminer dynamiquement
            preferred_language="fr",
            timestamp=datetime.now()
        )
        
        return context
    
    async def _generate_response(
        self, 
        message: Message, 
        user_context: ConversationContext,
        security_analysis: Dict[str, Any]
    ) -> Response:
        """Génération d'une réponse intelligente"""
        
        try:
            # Génération de la réponse par l'IA
            ai_response = await self.ai_engine.generate_response(
                message.content,
                user_context,
                include_security_context=True
            )
            
            # Enrichissement avec l'analyse de sécurité
            enriched_content = await self._enrich_response_with_security(
                ai_response.get("content", ""),
                security_analysis
            )
            
            # Génération des recommandations
            recommendations = await self._generate_security_recommendations(
                security_analysis,
                message.urgency
            )
            
            # Questions de suivi
            follow_up_questions = await self._generate_follow_up_questions(
                message.content,
                security_analysis["intent"]
            )
            
            # Création de la réponse
            response = Response(
                response_id=f"resp_{uuid.uuid4().hex[:8]}",
                message_id=message.message_id,
                content=enriched_content,
                mode=message.mode,
                confidence=ai_response.get("confidence", 0.8),
                urgency=message.urgency,
                timestamp=datetime.now(),
                security_alert=None,  # À déterminer si nécessaire
                recommendations=recommendations,
                follow_up_questions=follow_up_questions
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur génération réponse: {e}")
            return self._create_error_response(str(e))
    
    async def _enrich_response_with_security(
        self, 
        base_response: str, 
        security_analysis: Dict[str, Any]
    ) -> str:
        """Enrichissement de la réponse avec le contexte de sécurité"""
        
        risk_score = security_analysis.get("risk_score", 0.0)
        intent = security_analysis.get("intent", "general_inquiry")
        malicious_patterns = security_analysis.get("malicious_patterns", [])
        
        enriched_parts = [base_response]
        
        # Ajout d'informations de sécurité si pertinentes
        if risk_score > 0.3:
            enriched_parts.append(
                f"\n⚠️ **Analyse de sécurité**: Score de risque détecté: {risk_score:.2f}/1.0"
            )
        
        if malicious_patterns:
            pattern_names = [pattern[0] for pattern in malicious_patterns]
            enriched_parts.append(
                f"\n🚨 **Patterns suspects détectés**: {', '.join(pattern_names)}"
            )
        
        # Contextualisation selon l'intention
        if intent == "incident_report":
            enriched_parts.append(
                "\n📋 **Protocole d'incident activé**: Veuillez fournir tous les détails disponibles."
            )
        elif intent == "vulnerability_inquiry":
            enriched_parts.append(
                "\n🔍 **Mode analyse de vulnérabilité**: Vérification des bases de données CVE en cours..."
            )
        
        return "\n".join(enriched_parts)
    
    async def _generate_security_recommendations(
        self, 
        security_analysis: Dict[str, Any], 
        urgency: UrgencyLevel
    ) -> List[str]:
        """Génération de recommandations de sécurité personnalisées"""
        
        recommendations = security_analysis.get("recommendations", [])
        
        # Recommandations basées sur l'urgence
        if urgency == UrgencyLevel.CRITICAL:
            recommendations.extend([
                "Escalade immédiate vers l'équipe de sécurité",
                "Isolation des systèmes affectés si nécessaire",
                "Documentation complète de l'incident"
            ])
        elif urgency == UrgencyLevel.HIGH:
            recommendations.extend([
                "Surveillance renforcée recommandée",
                "Vérification des logs système",
                "Notification de l'équipe de sécurité"
            ])
        
        # Recommandations basées sur les patterns détectés
        malicious_patterns = security_analysis.get("malicious_patterns", [])
        for pattern_type, _ in malicious_patterns:
            if pattern_type == "sql_injection":
                recommendations.append("Vérifier la validation des entrées utilisateur")
                recommendations.append("Audit des requêtes SQL")
            elif pattern_type == "xss":
                recommendations.append("Vérifier l'encodage des sorties")
                recommendations.append("Mise à jour des politiques CSP")
        
        # Suppression des doublons
        return list(set(recommendations))
    
    async def _generate_follow_up_questions(self, content: str, intent: str) -> List[str]:
        """Génération de questions de suivi contextuelles"""
        
        questions = []
        
        if intent == "incident_report":
            questions.extend([
                "Quand l'incident a-t-il été détecté pour la première fois ?",
                "Quels systèmes sont actuellement affectés ?",
                "Y a-t-il des signes de compromission de données ?",
                "Des mesures de confinement ont-elles déjà été prises ?"
            ])
        elif intent == "vulnerability_inquiry":
            questions.extend([
                "Quel est le niveau de criticité de cette vulnérabilité ?",
                "Y a-t-il des systèmes actuellement exposés ?",
                "Un calendrier de correction est-il défini ?",
                "Des mesures de contournement sont-elles en place ?"
            ])
        elif intent == "threat_intelligence":
            questions.extend([
                "Cette menace est-elle liée à une campagne connue ?",
                "Y a-t-il des indicateurs de compromission associés ?",
                "Quelle est la source de cette information ?",
                "Des actions préventives sont-elles nécessaires ?"
            ])
        
        return questions[:3]  # Limitation à 3 questions
    
    async def _voice_respond(self, response: Response):
        """Communication vocale d'une réponse"""
        if not self.voice_enabled:
            return
        
        try:
            # Adaptation du ton selon l'urgence
            tone_map = {
                UrgencyLevel.LOW: EmotionalTone.NEUTRAL,
                UrgencyLevel.MEDIUM: EmotionalTone.CONCERNED,
                UrgencyLevel.HIGH: EmotionalTone.URGENT,
                UrgencyLevel.CRITICAL: EmotionalTone.URGENT
            }
            
            # Configuration vocale
            voice_settings = VoiceSettings(
                language=Language.FRENCH,
                tone=tone_map.get(response.urgency, EmotionalTone.NEUTRAL),
                speed=1.2 if response.urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL] else 1.0
            )
            
            # Adaptation du contenu pour la voix
            voice_content = self._adapt_content_for_voice(response.content)
            
            # Synthèse vocale
            await self.voice_engine.speak(voice_content, voice_settings)
            
            logger.info(f"Réponse vocale transmise (urgence: {response.urgency.value})")
            
        except Exception as e:
            logger.error(f"Erreur communication vocale: {e}")
    
    def _adapt_content_for_voice(self, content: str) -> str:
        """Adaptation du contenu pour la communication vocale"""
        
        # Suppression du markdown
        voice_content = content.replace("**", "").replace("*", "")
        voice_content = voice_content.replace("#", "")
        
        # Suppression des emojis pour une meilleure prononciation
        import re
        voice_content = re.sub(r'[^\w\s\.,\!\?\-\:]', '', voice_content)
        
        # Raccourcissement si nécessaire
        if len(voice_content) > 500:
            voice_content = voice_content[:500] + "... Pour plus de détails, consultez l'interface textuelle."
        
        return voice_content
    
    async def _check_escalation(self, response: Response, security_analysis: Dict[str, Any]):
        """Vérification et déclenchement d'escalades"""
        
        try:
            risk_score = security_analysis.get("risk_score", 0.0)
            
            # Escalade critique
            if response.urgency == UrgencyLevel.CRITICAL or risk_score >= 0.8:
                await self._trigger_escalation("critical", response, security_analysis)
            
            # Escalade technique
            elif "malicious_patterns" in security_analysis and security_analysis["malicious_patterns"]:
                await self._trigger_escalation("technical", response, security_analysis)
            
        except Exception as e:
            logger.error(f"Erreur vérification escalade: {e}")
    
    async def _trigger_escalation(
        self, 
        escalation_type: str, 
        response: Response, 
        security_analysis: Dict[str, Any]
    ):
        """Déclenchement d'une escalade"""
        
        try:
            handler = self.escalation_handlers.get(escalation_type)
            if handler:
                await handler(response, security_analysis)
                logger.warning(f"Escalade {escalation_type} déclenchée")
            
        except Exception as e:
            logger.error(f"Erreur déclenchement escalade {escalation_type}: {e}")
    
    async def _handle_critical_escalation(self, response: Response, security_analysis: Dict[str, Any]):
        """Gestion des escalades critiques"""
        
        # Notification vocale d'urgence
        if self.voice_enabled:
            urgent_message = f"ALERTE CRITIQUE: Escalade de sécurité déclenchée. Intervention immédiate requise."
            
            urgent_settings = VoiceSettings(
                language=Language.FRENCH,
                tone=EmotionalTone.URGENT,
                speed=1.3,
                volume=1.0
            )
            
            await self.voice_engine.speak(urgent_message, urgent_settings)
        
        # Notification des handlers externes
        if self.security_alert_handler:
            await self.security_alert_handler("critical", response, security_analysis)
    
    async def _handle_emergency_escalation(self, response: Response, security_analysis: Dict[str, Any]):
        """Gestion des escalades d'urgence maximum"""
        
        # Communication vocale d'urgence maximale
        if self.voice_enabled:
            emergency_message = "URGENCE MAXIMALE! Menace de sécurité critique détectée. Protocole d'urgence activé."
            
            emergency_settings = VoiceSettings(
                language=Language.FRENCH,
                tone=EmotionalTone.URGENT,
                speed=1.5,
                volume=1.0
            )
            
            await self.voice_engine.speak(emergency_message, emergency_settings)
        
        # Notification d'urgence
        if self.emergency_response_handler:
            await self.emergency_response_handler(response, security_analysis)
    
    async def _handle_technical_escalation(self, response: Response, security_analysis: Dict[str, Any]):
        """Gestion des escalades techniques"""
        
        # Analyse technique approfondie
        patterns = security_analysis.get("malicious_patterns", [])
        
        technical_message = f"Escalade technique: {len(patterns)} patterns suspects détectés. Analyse approfondie en cours."
        
        if self.voice_enabled:
            technical_settings = VoiceSettings(
                language=Language.FRENCH,
                tone=EmotionalTone.AUTHORITATIVE
            )
            
            await self.voice_engine.speak(technical_message, technical_settings)
    
    async def _handle_security_alert(self, incident: SecurityIncident):
        """Gestion des alertes de sécurité"""
        
        try:
            logger.warning(f"Alerte de sécurité reçue: {incident.title}")
            
            # Communication vocale pour les incidents critiques
            if incident.threat_level.value in ["critical", "catastrophic"]:
                alert_message = f"Alerte de sécurité {incident.threat_level.value}: {incident.title}"
                
                alert_settings = VoiceSettings(
                    language=Language.FRENCH,
                    tone=EmotionalTone.URGENT if incident.threat_level.value == "catastrophic" else EmotionalTone.CONCERNED
                )
                
                if self.voice_enabled:
                    await self.voice_engine.speak(alert_message, alert_settings)
            
            # Notification des handlers externes
            if self.security_alert_handler:
                await self.security_alert_handler("security_incident", incident, None)
                
        except Exception as e:
            logger.error(f"Erreur gestion alerte sécurité: {e}")
    
    async def _handle_voice_alert(self, message: str, tone: str, incident: SecurityIncident):
        """Gestion des alertes vocales spécialisées"""
        
        if not self.voice_enabled:
            return
        
        try:
            # Mapping des tons
            tone_map = {
                "urgent": EmotionalTone.URGENT,
                "concerned": EmotionalTone.CONCERNED,
                "authoritative": EmotionalTone.AUTHORITATIVE,
                "reassuring": EmotionalTone.REASSURING
            }
            
            alert_settings = VoiceSettings(
                language=Language.FRENCH,
                tone=tone_map.get(tone, EmotionalTone.NEUTRAL),
                speed=1.2 if tone == "urgent" else 1.0
            )
            
            await self.voice_engine.speak(message, alert_settings)
            
        except Exception as e:
            logger.error(f"Erreur alerte vocale: {e}")
    
    async def _handle_voice_input(self, text: str, timestamp: datetime):
        """Gestion des entrées vocales"""
        
        try:
            logger.info(f"Entrée vocale reçue: '{text[:50]}...'")
            
            # Traitement comme message texte
            response = await self.process_message(
                user_id="voice_user",
                content=text,
                mode=CommunicationMode.VOICE
            )
            
            # Réponse vocale automatique
            await self._voice_respond(response)
            
        except Exception as e:
            logger.error(f"Erreur traitement entrée vocale: {e}")
    
    def _create_error_response(self, error_message: str) -> Response:
        """Création d'une réponse d'erreur"""
        
        return Response(
            response_id=f"error_{uuid.uuid4().hex[:8]}",
            message_id="unknown",
            content=f"Erreur lors du traitement: {error_message}",
            mode=CommunicationMode.TEXT,
            confidence=0.0,
            urgency=UrgencyLevel.LOW,
            timestamp=datetime.now(),
            security_alert=None,
            recommendations=["Veuillez réessayer ou contacter le support technique"],
            follow_up_questions=[]
        )
    
    # Interface publique
    
    async def enable_voice_mode(self, settings: Optional[VoiceSettings] = None):
        """Activation du mode vocal"""
        if not self.voice_enabled:
            logger.warning("Moteur vocal non disponible")
            return False
        
        if settings:
            await self.voice_engine.set_voice_settings(settings)
            self.current_voice_settings = settings
        
        self.is_listening = True
        logger.info("Mode vocal activé")
        return True
    
    async def disable_voice_mode(self):
        """Désactivation du mode vocal"""
        self.is_listening = False
        if self.voice_enabled:
            self.voice_engine.stop_listening()
        logger.info("Mode vocal désactivé")
    
    async def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Résumé d'une session de communication"""
        
        try:
            messages = self.message_history.get(session_id, [])
            responses = self.response_history.get(session_id, [])
            
            # Calcul des statistiques
            total_interactions = len(messages)
            avg_response_confidence = sum(r.confidence for r in responses) / len(responses) if responses else 0
            
            urgency_distribution = {}
            for msg in messages:
                urgency = msg.urgency.value
                urgency_distribution[urgency] = urgency_distribution.get(urgency, 0) + 1
            
            summary = {
                "session_id": session_id,
                "total_interactions": total_interactions,
                "average_confidence": avg_response_confidence,
                "urgency_distribution": urgency_distribution,
                "start_time": messages[0].timestamp.isoformat() if messages else None,
                "end_time": messages[-1].timestamp.isoformat() if messages else None,
                "duration_minutes": (messages[-1].timestamp - messages[0].timestamp).total_seconds() / 60 if len(messages) > 1 else 0,
                "voice_interactions": sum(1 for m in messages if m.mode == CommunicationMode.VOICE)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Erreur génération résumé session: {e}")
            return {"error": str(e)}
    
    async def get_threat_status(self) -> Dict[str, Any]:
        """État actuel des menaces de sécurité"""
        
        try:
            return await self.security_intelligence.get_threat_summary()
        except Exception as e:
            logger.error(f"Erreur récupération état menaces: {e}")
            return {"error": str(e)}
    
    async def simulate_network_traffic(self, events_data: List[Dict[str, Any]]) -> List[SecurityIncident]:
        """Simulation d'analyse de trafic réseau"""
        
        try:
            # Conversion des données en objets NetworkEvent
            events = []
            for event_data in events_data:
                event = NetworkEvent(
                    timestamp=datetime.fromisoformat(event_data.get("timestamp", datetime.now().isoformat())),
                    source_ip=event_data["source_ip"],
                    destination_ip=event_data["destination_ip"],
                    source_port=event_data["source_port"],
                    destination_port=event_data["destination_port"],
                    protocol=event_data["protocol"],
                    bytes_transferred=event_data["bytes_transferred"],
                    packets_count=event_data.get("packets_count", 1),
                    duration=event_data.get("duration", 1.0),
                    status=event_data.get("status", "success"),
                    user_agent=event_data.get("user_agent"),
                    http_method=event_data.get("http_method"),
                    uri=event_data.get("uri")
                )
                events.append(event)
            
            # Analyse par l'intelligence de sécurité
            incidents = await self.security_intelligence.analyze_network_traffic(events)
            
            return incidents
            
        except Exception as e:
            logger.error(f"Erreur simulation trafic réseau: {e}")
            return []
    
    def set_security_alert_handler(self, handler):
        """Configuration du handler d'alertes de sécurité"""
        self.security_alert_handler = handler
    
    def set_emergency_response_handler(self, handler):
        """Configuration du handler de réponse d'urgence"""
        self.emergency_response_handler = handler
    
    async def shutdown(self):
        """Arrêt propre de l'interface"""
        try:
            # Arrêt du mode vocal
            await self.disable_voice_mode()
            
            # Nettoyage du moteur vocal
            if self.voice_enabled:
                self.voice_engine.cleanup()
            
            # Nettoyage de l'intelligence de sécurité
            self.security_intelligence.cleanup()
            
            logger.info("Interface de communication arrêtée proprement")
            
        except Exception as e:
            logger.error(f"Erreur arrêt interface: {e}")
"""
Moteur IA principal pour CyberSec AI Assistant
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import torch
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    pipeline,
    GPT2LMHeadModel,
    GPT2Tokenizer
)
from loguru import logger
import spacy
from textblob import TextBlob
from langdetect import detect

from .config import config


@dataclass
class ConversationContext:
    """Contexte de conversation avec l'utilisateur"""
    user_id: str
    session_id: str
    conversation_history: List[Dict[str, Any]]
    user_expertise_level: str  # novice, intermediate, expert
    preferred_language: str
    current_topic: Optional[str] = None
    threat_context: Optional[Dict[str, Any]] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class SecurityAlert:
    """Structure d'alerte de sécurité"""
    alert_id: str
    severity: str  # low, medium, high, critical
    category: str  # malware, intrusion, vulnerability, etc.
    description: str
    indicators: List[str]
    recommendations: List[str]
    confidence: float
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class CyberSecAI:
    """
    Moteur IA principal spécialisé en cybersécurité
    
    Fonctionnalités :
    - Communication naturelle avancée
    - Analyse contextuelle des menaces
    - Adaptation au niveau d'expertise de l'utilisateur
    - Génération de réponses personnalisées
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.nlp = None
        self.security_classifier = None
        self.conversation_contexts: Dict[str, ConversationContext] = {}
        self.threat_keywords = self._load_threat_keywords()
        self.response_templates = self._load_response_templates()
        
    async def initialize(self):
        """Initialisation asynchrone du moteur IA"""
        logger.info("Initialisation du moteur CyberSec AI...")
        
        try:
            # Chargement du modèle de langage
            await self._load_language_model()
            
            # Chargement du modèle NLP
            await self._load_nlp_model()
            
            # Initialisation du classificateur de sécurité
            await self._initialize_security_classifier()
            
            logger.success("Moteur IA initialisé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}")
            raise
    
    async def _load_language_model(self):
        """Chargement du modèle de langage pour la génération de réponses"""
        try:
            model_name = config.model_name
            device = config.model_device
            
            logger.info(f"Chargement du modèle {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None
            )
            
            # Configuration du padding token si nécessaire
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            logger.success(f"Modèle {model_name} chargé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            raise
    
    async def _load_nlp_model(self):
        """Chargement du modèle NLP pour l'analyse linguistique"""
        try:
            logger.info("Chargement du modèle spaCy...")
            self.nlp = spacy.load("en_core_web_sm")
            logger.success("Modèle spaCy chargé avec succès")
        except OSError:
            logger.warning("Modèle spaCy non trouvé, utilisation de la version de base")
            self.nlp = spacy.blank("en")
    
    async def _initialize_security_classifier(self):
        """Initialisation du classificateur de menaces de sécurité"""
        try:
            self.security_classifier = pipeline(
                "text-classification",
                model="unitary/toxic-bert",
                device=0 if config.model_device == "cuda" else -1
            )
            logger.success("Classificateur de sécurité initialisé")
        except Exception as e:
            logger.warning(f"Impossible de charger le classificateur: {e}")
    
    def _load_threat_keywords(self) -> Dict[str, List[str]]:
        """Chargement des mots-clés de menaces par catégorie"""
        return {
            "malware": [
                "virus", "trojan", "ransomware", "spyware", "adware", "rootkit",
                "botnet", "worm", "backdoor", "keylogger", "cryptominer"
            ],
            "network": [
                "ddos", "mitm", "phishing", "spoofing", "sniffing", "injection",
                "xss", "csrf", "sql injection", "port scan", "brute force"
            ],
            "vulnerability": [
                "cve", "exploit", "zero-day", "buffer overflow", "privilege escalation",
                "authentication bypass", "directory traversal", "rce", "lfi", "rfi"
            ],
            "incident": [
                "breach", "leak", "compromise", "intrusion", "unauthorized access",
                "data theft", "insider threat", "apt", "campaign", "attribution"
            ]
        }
    
    def _load_response_templates(self) -> Dict[str, Dict[str, str]]:
        """Modèles de réponse adaptés au niveau d'expertise"""
        return {
            "novice": {
                "greeting": "Bonjour ! Je suis votre assistant IA en cybersécurité. Je peux vous expliquer les concepts de sécurité de manière simple et vous aider à protéger vos systèmes.",
                "explanation_style": "simple et détaillé avec des exemples concrets",
                "technical_depth": "basique avec vulgarisation"
            },
            "intermediate": {
                "greeting": "Salut ! Prêt à plonger dans l'analyse de sécurité ? Je peux vous aider avec l'analyse de menaces, les investigations et les contre-mesures.",
                "explanation_style": "technique mais accessible",
                "technical_depth": "modéré avec contexte pratique"
            },
            "expert": {
                "greeting": "Bonjour collègue ! Analysons ensemble les dernières menaces. Je peux vous assister sur l'analyse forensique, la threat intelligence et les techniques avancées.",
                "explanation_style": "technique et précis",
                "technical_depth": "avancé avec détails techniques"
            }
        }
    
    async def process_message(
        self, 
        message: str, 
        user_id: str, 
        session_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[SecurityAlert]]:
        """
        Traitement principal d'un message utilisateur
        
        Args:
            message: Message de l'utilisateur
            user_id: Identifiant utilisateur
            session_id: Identifiant de session
            context: Contexte additionnel
            
        Returns:
            Tuple contenant la réponse et une éventuelle alerte de sécurité
        """
        try:
            # Récupération ou création du contexte de conversation
            conv_context = await self._get_or_create_context(user_id, session_id)
            
            # Analyse linguistique du message
            linguistic_analysis = await self._analyze_message_linguistics(message)
            
            # Détection d'entités de sécurité
            security_entities = await self._extract_security_entities(message)
            
            # Classification de l'intent
            intent = await self._classify_intent(message, security_entities)
            
            # Détection de menaces potentielles
            threat_analysis = await self._analyze_threats(message, security_entities)
            
            # Génération de la réponse adaptée
            response = await self._generate_adaptive_response(
                message, conv_context, intent, security_entities, linguistic_analysis
            )
            
            # Mise à jour du contexte de conversation
            await self._update_conversation_context(
                conv_context, message, response, security_entities
            )
            
            # Création d'alerte si nécessaire
            alert = None
            if threat_analysis.get("severity", "low") in ["high", "critical"]:
                alert = await self._create_security_alert(threat_analysis, security_entities)
            
            return response, alert
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement du message: {e}")
            return self._get_error_response(), None
    
    async def _get_or_create_context(self, user_id: str, session_id: str) -> ConversationContext:
        """Récupération ou création du contexte de conversation"""
        context_key = f"{user_id}:{session_id}"
        
        if context_key not in self.conversation_contexts:
            # Détection automatique du niveau d'expertise (à améliorer avec ML)
            expertise_level = "intermediate"  # Par défaut
            
            self.conversation_contexts[context_key] = ConversationContext(
                user_id=user_id,
                session_id=session_id,
                conversation_history=[],
                user_expertise_level=expertise_level,
                preferred_language="fr"
            )
        
        return self.conversation_contexts[context_key]
    
    async def _analyze_message_linguistics(self, message: str) -> Dict[str, Any]:
        """Analyse linguistique approfondie du message"""
        try:
            # Détection de la langue
            detected_language = detect(message)
            
            # Analyse avec spaCy
            doc = self.nlp(message)
            
            # Analyse de sentiment avec TextBlob
            blob = TextBlob(message)
            sentiment = blob.sentiment
            
            # Extraction d'entités nommées
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            
            # Analyse de la complexité
            complexity_score = len(doc) / len(message.split()) if message.split() else 0
            
            return {
                "language": detected_language,
                "sentiment": {
                    "polarity": sentiment.polarity,
                    "subjectivity": sentiment.subjectivity
                },
                "entities": entities,
                "complexity": complexity_score,
                "token_count": len(doc),
                "question_detected": "?" in message
            }
            
        except Exception as e:
            logger.warning(f"Erreur lors de l'analyse linguistique: {e}")
            return {"language": "unknown", "sentiment": {"polarity": 0, "subjectivity": 0}}
    
    async def _extract_security_entities(self, message: str) -> Dict[str, List[str]]:
        """Extraction d'entités liées à la cybersécurité"""
        entities = {category: [] for category in self.threat_keywords.keys()}
        
        message_lower = message.lower()
        
        for category, keywords in self.threat_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    entities[category].append(keyword)
        
        # Extraction d'IoCs (Indicators of Compromise)
        iocs = await self._extract_iocs(message)
        entities["iocs"] = iocs
        
        return entities
    
    async def _extract_iocs(self, text: str) -> List[str]:
        """Extraction d'indicateurs de compromission"""
        iocs = []
        
        # Regex pour IPs
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        iocs.extend(re.findall(ip_pattern, text))
        
        # Regex pour domaines
        domain_pattern = r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.([a-zA-Z]{2,})\b'
        iocs.extend(re.findall(domain_pattern, text))
        
        # Regex pour hashes MD5/SHA1/SHA256
        hash_pattern = r'\b[a-fA-F0-9]{32,64}\b'
        iocs.extend(re.findall(hash_pattern, text))
        
        # Regex pour URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        iocs.extend(re.findall(url_pattern, text))
        
        return list(set(iocs))  # Suppression des doublons
    
    async def _classify_intent(self, message: str, security_entities: Dict[str, List[str]]) -> str:
        """Classification de l'intention du message"""
        message_lower = message.lower()
        
        # Classification basée sur des mots-clés (à améliorer avec ML)
        if any(word in message_lower for word in ["analyser", "analyse", "examiner", "investigation"]):
            return "analysis_request"
        elif any(word in message_lower for word in ["comment", "expliquer", "qu'est-ce que"]):
            return "explanation_request"
        elif any(word in message_lower for word in ["protéger", "sécuriser", "défendre"]):
            return "protection_advice"
        elif any(word in message_lower for word in ["alerte", "incident", "compromis", "attaque"]):
            return "incident_report"
        elif sum(len(entities) for entities in security_entities.values()) > 0:
            return "security_consultation"
        else:
            return "general_conversation"
    
    async def _analyze_threats(self, message: str, security_entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyse des menaces potentielles dans le message"""
        threat_score = 0
        threat_categories = []
        
        # Calcul du score de menace basé sur les entités détectées
        for category, entities in security_entities.items():
            if entities and category != "iocs":
                threat_score += len(entities) * 10
                threat_categories.append(category)
        
        # Bonus pour les IoCs
        if security_entities.get("iocs"):
            threat_score += len(security_entities["iocs"]) * 20
            threat_categories.append("iocs")
        
        # Détermination du niveau de sévérité
        if threat_score >= 50:
            severity = "critical"
        elif threat_score >= 30:
            severity = "high"
        elif threat_score >= 15:
            severity = "medium"
        else:
            severity = "low"
        
        return {
            "score": threat_score,
            "severity": severity,
            "categories": threat_categories,
            "confidence": min(threat_score / 100, 1.0)
        }
    
    async def _generate_adaptive_response(
        self,
        message: str,
        context: ConversationContext,
        intent: str,
        security_entities: Dict[str, List[str]],
        linguistic_analysis: Dict[str, Any]
    ) -> str:
        """Génération d'une réponse adaptée au contexte et à l'utilisateur"""
        
        # Sélection du template basé sur le niveau d'expertise
        template = self.response_templates[context.user_expertise_level]
        
        # Construction du prompt pour le modèle
        prompt = await self._build_prompt(
            message, context, intent, security_entities, template
        )
        
        # Génération avec le modèle de langage
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + config.max_response_length,
                    num_return_sequences=1,
                    temperature=config.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Nettoyage de la réponse
            response = response[len(prompt):].strip()
            
            # Post-traitement adaptatif
            response = await self._post_process_response(response, context, security_entities)
            
            return response
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération: {e}")
            return self._get_fallback_response(intent, context.user_expertise_level)
    
    async def _build_prompt(
        self,
        message: str,
        context: ConversationContext,
        intent: str,
        security_entities: Dict[str, List[str]],
        template: Dict[str, str]
    ) -> str:
        """Construction du prompt pour le modèle de langage"""
        
        # Contexte de l'assistant
        system_context = f"""Tu es un expert en cybersécurité. Niveau utilisateur: {context.user_expertise_level}.
Style de réponse: {template['explanation_style']}.
Profondeur technique: {template['technical_depth']}."""
        
        # Historique récent de conversation
        history = ""
        if context.conversation_history:
            recent_history = context.conversation_history[-3:]  # 3 derniers échanges
            for entry in recent_history:
                history += f"Utilisateur: {entry['user']}\nAssistant: {entry['assistant']}\n"
        
        # Entités de sécurité détectées
        entities_context = ""
        if any(security_entities.values()):
            entities_context = f"Entités détectées: {security_entities}"
        
        # Construction du prompt final
        prompt = f"""{system_context}

{history}

{entities_context}

Utilisateur: {message}
Assistant:"""
        
        return prompt
    
    async def _post_process_response(
        self,
        response: str,
        context: ConversationContext,
        security_entities: Dict[str, List[str]]
    ) -> str:
        """Post-traitement adaptatif de la réponse"""
        
        # Limitation de longueur
        if len(response) > 1000:
            response = response[:1000] + "..."
        
        # Ajout de recommandations si des IoCs sont détectés
        if security_entities.get("iocs"):
            response += f"\n\n⚠️ J'ai détecté des indicateurs de compromission dans votre message. Je recommande une analyse approfondie."
        
        # Adaptation au niveau d'expertise
        if context.user_expertise_level == "novice":
            response += "\n\nSouhaitez-vous que j'explique certains termes techniques ?"
        elif context.user_expertise_level == "expert":
            if security_entities.get("malware") or security_entities.get("vulnerability"):
                response += "\n\nVoulez-vous que j'approfondisse l'analyse technique ?"
        
        return response
    
    async def _update_conversation_context(
        self,
        context: ConversationContext,
        user_message: str,
        assistant_response: str,
        security_entities: Dict[str, List[str]]
    ):
        """Mise à jour du contexte de conversation"""
        
        # Ajout à l'historique
        context.conversation_history.append({
            "user": user_message,
            "assistant": assistant_response,
            "timestamp": datetime.utcnow(),
            "entities": security_entities
        })
        
        # Limitation de l'historique
        if len(context.conversation_history) > config.max_conversation_history:
            context.conversation_history = context.conversation_history[-config.max_conversation_history:]
        
        # Mise à jour du topic actuel
        if security_entities:
            dominant_category = max(
                security_entities.keys(),
                key=lambda k: len(security_entities[k]) if security_entities[k] else 0
            )
            if security_entities[dominant_category]:
                context.current_topic = dominant_category
    
    async def _create_security_alert(
        self,
        threat_analysis: Dict[str, Any],
        security_entities: Dict[str, List[str]]
    ) -> SecurityAlert:
        """Création d'une alerte de sécurité"""
        
        alert_id = f"alert_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Agrégation des indicateurs
        indicators = []
        for category, entities in security_entities.items():
            indicators.extend(entities)
        
        # Génération de recommandations
        recommendations = await self._generate_recommendations(threat_analysis, security_entities)
        
        return SecurityAlert(
            alert_id=alert_id,
            severity=threat_analysis["severity"],
            category=", ".join(threat_analysis["categories"]),
            description=f"Menace détectée avec un score de {threat_analysis['score']}",
            indicators=indicators,
            recommendations=recommendations,
            confidence=threat_analysis["confidence"]
        )
    
    async def _generate_recommendations(
        self,
        threat_analysis: Dict[str, Any],
        security_entities: Dict[str, List[str]]
    ) -> List[str]:
        """Génération de recommandations de sécurité"""
        
        recommendations = []
        
        if "malware" in threat_analysis["categories"]:
            recommendations.extend([
                "Effectuer un scan antivirus complet",
                "Isoler les systèmes potentiellement compromis",
                "Vérifier les logs de sécurité"
            ])
        
        if "network" in threat_analysis["categories"]:
            recommendations.extend([
                "Analyser le trafic réseau",
                "Vérifier les configurations de pare-feu",
                "Surveiller les connexions suspectes"
            ])
        
        if "iocs" in threat_analysis["categories"]:
            recommendations.extend([
                "Corréler avec les bases de threat intelligence",
                "Bloquer les IPs/domaines malveillants",
                "Documenter pour analyse forensique"
            ])
        
        return recommendations
    
    def _get_error_response(self) -> str:
        """Réponse d'erreur générique"""
        return "Je rencontre actuellement des difficultés techniques. Veuillez réessayer dans quelques instants."
    
    def _get_fallback_response(self, intent: str, expertise_level: str) -> str:
        """Réponses de fallback par intention"""
        
        fallback_responses = {
            "analysis_request": {
                "novice": "Je peux vous aider à analyser cette situation de sécurité. Pouvez-vous me donner plus de détails ?",
                "intermediate": "Pour une analyse approfondie, j'aurais besoin de plus d'informations sur le contexte.",
                "expert": "Analyse en cours. Veuillez partager les logs ou IoCs pour une évaluation détaillée."
            },
            "explanation_request": {
                "novice": "Je serai ravi de vous expliquer ce concept de sécurité de manière simple.",
                "intermediate": "Voici une explication technique de ce sujet de cybersécurité.",
                "expert": "Analysons ensemble les aspects techniques avancés de cette question."
            }
        }
        
        return fallback_responses.get(intent, {}).get(
            expertise_level,
            "Comment puis-je vous aider avec votre question de cybersécurité ?"
        )
    
    async def get_conversation_summary(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """Génération d'un résumé de conversation"""
        context_key = f"{user_id}:{session_id}"
        
        if context_key not in self.conversation_contexts:
            return {"error": "Session non trouvée"}
        
        context = self.conversation_contexts[context_key]
        
        # Analyse des topics abordés
        topics = {}
        for entry in context.conversation_history:
            for category, entities in entry.get("entities", {}).items():
                if entities:
                    topics[category] = topics.get(category, 0) + len(entities)
        
        return {
            "session_id": session_id,
            "message_count": len(context.conversation_history),
            "main_topics": sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5],
            "expertise_level": context.user_expertise_level,
            "current_topic": context.current_topic,
            "session_duration": (datetime.utcnow() - context.timestamp).total_seconds()
        }
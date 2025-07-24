#!/usr/bin/env python3
"""
Démonstration Complète - IA de Sécurité Informatique Vocale Avancée
===================================================================

Script de démonstration des capacités complètes du système d'IA de sécurité
avec communication vocale haute qualité et intelligence de menaces.

Auteur: Assistant IA Avancé
Version: 1.0.0
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path
import sys

# Ajout du répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger
from core.ai_engine import CyberSecAI
from communication.interface import CommunicationInterface, CommunicationMode, UrgencyLevel
from communication.voice_engine import VoiceSettings, EmotionalTone, Language, VoiceQuality
from core.security_intelligence import NetworkEvent, ThreatLevel


class VoiceSecurityAIDemo:
    """
    Démonstration interactive du système d'IA de sécurité vocale
    """
    
    def __init__(self):
        self.ai_engine = None
        self.communication_interface = None
        self.demo_scenarios = []
        self.current_scenario = 0
        
    async def initialize(self):
        """Initialisation de la démonstration"""
        logger.info("🚀 Initialisation de la démonstration IA de Sécurité Vocale...")
        
        try:
            # Initialisation du moteur IA
            self.ai_engine = CyberSecAI()
            await self.ai_engine.initialize()
            
            # Initialisation de l'interface de communication
            self.communication_interface = CommunicationInterface(self.ai_engine)
            await self.communication_interface.initialize()
            
            # Configuration des handlers de démonstration
            self.communication_interface.set_security_alert_handler(self._demo_security_alert_handler)
            self.communication_interface.set_emergency_response_handler(self._demo_emergency_handler)
            
            # Préparation des scénarios de démonstration
            self._prepare_demo_scenarios()
            
            logger.success("✅ Démonstration initialisée avec succès!")
            
        except Exception as e:
            logger.error(f"❌ Erreur initialisation démonstration: {e}")
            raise
    
    def _prepare_demo_scenarios(self):
        """Préparation des scénarios de démonstration"""
        
        self.demo_scenarios = [
            {
                "name": "Communication Vocale Basique",
                "description": "Test des capacités vocales de base",
                "type": "voice_basic",
                "messages": [
                    "Bonjour, je suis votre assistant IA de sécurité. Comment puis-je vous aider ?",
                    "Quelles sont les menaces actuelles sur mon réseau ?",
                    "Comment puis-je améliorer la sécurité de mes systèmes ?"
                ]
            },
            {
                "name": "Détection d'Incident de Sécurité",
                "description": "Simulation d'un rapport d'incident avec escalade vocale",
                "type": "incident_report",
                "messages": [
                    "Je suspecte une intrusion sur mon serveur web",
                    "J'ai détecté des connexions suspectes depuis l'IP 185.220.100.240",
                    "Les logs montrent des tentatives d'injection SQL sur /admin/login"
                ]
            },
            {
                "name": "Analyse de Trafic Réseau Malicieux",
                "description": "Simulation d'analyse de trafic réseau avec détection d'anomalies",
                "type": "network_analysis",
                "network_events": [
                    {
                        "timestamp": datetime.now().isoformat(),
                        "source_ip": "185.220.100.240",
                        "destination_ip": "192.168.1.100",
                        "source_port": 12345,
                        "destination_port": 80,
                        "protocol": "HTTP",
                        "bytes_transferred": 1048576,
                        "uri": "/admin/login?id=1' OR '1'='1",
                        "user_agent": "sqlmap/1.0",
                        "http_method": "POST"
                    },
                    {
                        "timestamp": datetime.now().isoformat(),
                        "source_ip": "10.0.0.50",
                        "destination_ip": "8.8.8.8",
                        "source_port": 54321,
                        "destination_port": 53,
                        "protocol": "DNS",
                        "bytes_transferred": 512000000,  # 512MB - suspicieux pour DNS
                        "uri": "malware-example.com"
                    }
                ]
            },
            {
                "name": "Alerte Critique avec Communication d'Urgence",
                "description": "Test des alertes vocales critiques et escalades d'urgence",
                "type": "critical_alert",
                "messages": [
                    "ALERTE: Ransomware détecté sur le serveur de fichiers principal!",
                    "Encryption en cours détectée, 50% des fichiers déjà chiffrés",
                    "Besoin d'intervention immédiate pour isoler le système"
                ]
            },
            {
                "name": "Consultation de Threat Intelligence",
                "description": "Interrogation de l'intelligence de menaces avec réponses vocales",
                "type": "threat_intel",
                "messages": [
                    "Quelles sont les nouvelles campagnes APT cette semaine ?",
                    "L'IP 185.220.100.240 est-elle référencée dans vos bases de menaces ?",
                    "Y a-t-il des vulnérabilités critiques publiées aujourd'hui ?"
                ]
            }
        ]
    
    async def run_full_demo(self):
        """Exécution de la démonstration complète"""
        
        print("\n" + "="*80)
        print("🛡️  DÉMONSTRATION - IA DE SÉCURITÉ INFORMATIQUE VOCALE AVANCÉE")
        print("="*80)
        print()
        
        # Message de bienvenue vocal
        await self._welcome_message()
        
        # Exécution de tous les scénarios
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n📋 SCÉNARIO {i}/{len(self.demo_scenarios)}: {scenario['name']}")
            print("-" * 60)
            print(f"Description: {scenario['description']}")
            print()
            
            await self._run_scenario(scenario)
            
            # Pause entre les scénarios
            if i < len(self.demo_scenarios):
                await self._pause_between_scenarios()
        
        # Message de conclusion
        await self._conclusion_message()
    
    async def _welcome_message(self):
        """Message de bienvenue vocal"""
        welcome_text = """
        Bienvenue dans la démonstration de notre système d'Intelligence Artificielle 
        de sécurité informatique avec capacités vocales avancées. 
        
        Ce système combine:
        - Reconnaissance vocale en temps réel
        - Synthèse vocale émotionnelle haute qualité
        - Analyse de menaces avec IA
        - Détection d'anomalies comportementales
        - Escalade automatique des alertes critiques
        
        Commençons la démonstration...
        """
        
        # Configuration vocale pour le message de bienvenue
        welcome_settings = VoiceSettings(
            language=Language.FRENCH,
            tone=EmotionalTone.REASSURING,
            quality=VoiceQuality.HIGH,
            speed=1.0,
            volume=0.8
        )
        
        print("🎙️ Message de bienvenue vocal...")
        if self.communication_interface.voice_enabled:
            await self.communication_interface.voice_engine.speak(welcome_text, welcome_settings)
        else:
            print("⚠️ Mode vocal non disponible - affichage texte uniquement")
            print(welcome_text)
        
        await asyncio.sleep(2)
    
    async def _run_scenario(self, scenario: Dict[str, Any]):
        """Exécution d'un scénario spécifique"""
        
        scenario_type = scenario["type"]
        
        if scenario_type == "voice_basic":
            await self._demo_voice_basic(scenario)
        elif scenario_type == "incident_report":
            await self._demo_incident_report(scenario)
        elif scenario_type == "network_analysis":
            await self._demo_network_analysis(scenario)
        elif scenario_type == "critical_alert":
            await self._demo_critical_alert(scenario)
        elif scenario_type == "threat_intel":
            await self._demo_threat_intel(scenario)
    
    async def _demo_voice_basic(self, scenario: Dict[str, Any]):
        """Démonstration des capacités vocales de base"""
        
        print("🎯 Test des différents tons émotionnels...")
        
        tones = [
            (EmotionalTone.NEUTRAL, "Voici un message avec un ton neutre."),
            (EmotionalTone.REASSURING, "Ce message est rassurant et bienveillant."),
            (EmotionalTone.CONCERNED, "Attention, ce message exprime de l'inquiétude."),
            (EmotionalTone.URGENT, "URGENT! Ce message nécessite une action immédiate!"),
            (EmotionalTone.AUTHORITATIVE, "Directive: Respectez impérativement cette consigne de sécurité.")
        ]
        
        for tone, message in tones:
            print(f"   📢 Ton {tone.value}: {message}")
            
            settings = VoiceSettings(
                language=Language.FRENCH,
                tone=tone,
                speed=1.1 if tone == EmotionalTone.URGENT else 1.0
            )
            
            if self.communication_interface.voice_enabled:
                await self.communication_interface.voice_engine.speak(message, settings)
                await asyncio.sleep(1)
        
        # Test des messages utilisateur
        print("\n🎯 Traitement de messages utilisateur...")
        
        for message in scenario["messages"]:
            print(f"   👤 Utilisateur: {message}")
            
            response = await self.communication_interface.process_message(
                user_id="demo_user",
                content=message,
                mode=CommunicationMode.VOICE
            )
            
            print(f"   🤖 Assistant: {response.content[:100]}...")
            print(f"   📊 Confiance: {response.confidence:.2f} | Urgence: {response.urgency.value}")
            
            await asyncio.sleep(2)
    
    async def _demo_incident_report(self, scenario: Dict[str, Any]):
        """Démonstration de rapport d'incident avec escalade"""
        
        print("🚨 Simulation de rapport d'incident de sécurité...")
        
        for i, message in enumerate(scenario["messages"], 1):
            print(f"\n   📝 Rapport d'incident - Étape {i}")
            print(f"   👤 Utilisateur: {message}")
            
            # Traitement du message avec analyse de sécurité
            response = await self.communication_interface.process_message(
                user_id="security_analyst",
                content=message,
                mode=CommunicationMode.MIXED,
                session_id="incident_session_001"
            )
            
            print(f"   🤖 Analyse: {response.content[:150]}...")
            print(f"   ⚠️ Urgence détectée: {response.urgency.value}")
            print(f"   📋 Recommandations: {len(response.recommendations)} actions")
            
            # Affichage des recommandations
            for j, rec in enumerate(response.recommendations[:3], 1):
                print(f"      {j}. {rec}")
            
            # Simulation d'escalade pour les messages critiques
            if response.urgency in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]:
                print("   🚨 ESCALADE DÉCLENCHÉE!")
                await self._simulate_escalation(response.urgency)
            
            await asyncio.sleep(3)
    
    async def _demo_network_analysis(self, scenario: Dict[str, Any]):
        """Démonstration d'analyse de trafic réseau"""
        
        print("🌐 Analyse de trafic réseau en temps réel...")
        
        # Simulation d'événements réseau
        events_data = scenario["network_events"]
        
        print(f"   📊 Analyse de {len(events_data)} événements réseau...")
        
        # Envoi des événements pour analyse
        incidents = await self.communication_interface.simulate_network_traffic(events_data)
        
        print(f"   🚨 {len(incidents)} incidents de sécurité détectés:")
        
        for i, incident in enumerate(incidents, 1):
            print(f"\n   📋 Incident {i}: {incident.title}")
            print(f"      🎯 Niveau de menace: {incident.threat_level.value}")
            print(f"      🔍 Vecteur d'attaque: {incident.attack_vector.value}")
            print(f"      📈 Confiance: {incident.confidence_score:.2f}")
            print(f"      🛠️ Actions recommandées: {len(incident.recommended_actions)}")
            
            # Communication vocale pour les incidents critiques
            if incident.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.CATASTROPHIC]:
                critical_message = f"Incident critique détecté: {incident.title}. Intervention immédiate requise."
                
                critical_settings = VoiceSettings(
                    language=Language.FRENCH,
                    tone=EmotionalTone.URGENT,
                    speed=1.3
                )
                
                print("      🎙️ Alerte vocale critique émise...")
                if self.communication_interface.voice_enabled:
                    await self.communication_interface.voice_engine.speak(critical_message, critical_settings)
            
            await asyncio.sleep(2)
    
    async def _demo_critical_alert(self, scenario: Dict[str, Any]):
        """Démonstration d'alerte critique avec communication d'urgence"""
        
        print("🚨 SIMULATION D'ALERTE CRITIQUE MAXIMALE...")
        
        # Configuration vocale d'urgence maximale
        emergency_settings = VoiceSettings(
            language=Language.FRENCH,
            tone=EmotionalTone.URGENT,
            quality=VoiceQuality.HIGH,
            speed=1.4,
            volume=1.0
        )
        
        for message in scenario["messages"]:
            print(f"\n   🚨 ALERTE: {message}")
            
            # Traitement avec priorité maximale
            response = await self.communication_interface.process_message(
                user_id="security_manager",
                content=message,
                mode=CommunicationMode.MIXED
            )
            
            print(f"   📊 Urgence: {response.urgency.value}")
            
            # Communication vocale d'urgence
            if response.urgency == UrgencyLevel.CRITICAL:
                urgent_message = f"ALERTE CRITIQUE CONFIRMÉE: {message[:50]}... Protocole d'urgence activé."
                
                print("   🎙️ COMMUNICATION VOCALE D'URGENCE...")
                if self.communication_interface.voice_enabled:
                    await self.communication_interface.voice_engine.speak(urgent_message, emergency_settings)
                
                # Simulation de procédures d'urgence
                await self._simulate_emergency_procedures()
            
            await asyncio.sleep(3)
    
    async def _demo_threat_intel(self, scenario: Dict[str, Any]):
        """Démonstration de consultation de threat intelligence"""
        
        print("🔍 Consultation de l'intelligence de menaces...")
        
        # Récupération du statut des menaces
        threat_status = await self.communication_interface.get_threat_status()
        
        print("   📊 État actuel des menaces:")
        print(f"      • Incidents actifs: {threat_status.get('active_incidents', 0)}")
        print(f"      • Incidents 24h: {threat_status.get('total_incidents_24h', 0)}")
        
        threat_dist = threat_status.get('threat_distribution', {})
        for level, count in threat_dist.items():
            if count > 0:
                print(f"      • Niveau {level}: {count}")
        
        # Traitement des questions de threat intelligence
        for message in scenario["messages"]:
            print(f"\n   👤 Question: {message}")
            
            response = await self.communication_interface.process_message(
                user_id="threat_analyst",
                content=message,
                mode=CommunicationMode.MIXED
            )
            
            print(f"   🤖 Réponse: {response.content[:200]}...")
            
            # Questions de suivi
            if response.follow_up_questions:
                print("   ❓ Questions de suivi suggérées:")
                for q in response.follow_up_questions[:2]:
                    print(f"      • {q}")
            
            await asyncio.sleep(2)
    
    async def _simulate_escalation(self, urgency: UrgencyLevel):
        """Simulation d'escalade de sécurité"""
        
        escalation_messages = {
            UrgencyLevel.HIGH: "Escalade niveau élevé: Équipe de sécurité notifiée.",
            UrgencyLevel.CRITICAL: "Escalade critique: Cellule de crise activée. Intervention immédiate en cours."
        }
        
        message = escalation_messages.get(urgency, "Escalade déclenchée.")
        print(f"   📢 {message}")
        
        escalation_settings = VoiceSettings(
            language=Language.FRENCH,
            tone=EmotionalTone.AUTHORITATIVE,
            speed=1.2
        )
        
        if self.communication_interface.voice_enabled:
            await self.communication_interface.voice_engine.speak(message, escalation_settings)
        
        await asyncio.sleep(2)
    
    async def _simulate_emergency_procedures(self):
        """Simulation de procédures d'urgence"""
        
        procedures = [
            "Isolation des systèmes affectés en cours...",
            "Sauvegarde d'urgence initiée...",
            "Équipe de réponse aux incidents mobilisée...",
            "Communication de crise préparée..."
        ]
        
        for procedure in procedures:
            print(f"      ⚙️ {procedure}")
            await asyncio.sleep(1)
        
        print("      ✅ Procédures d'urgence activées")
    
    async def _pause_between_scenarios(self):
        """Pause entre les scénarios"""
        print("\n⏸️ Pause avant le prochain scénario...")
        await asyncio.sleep(3)
    
    async def _conclusion_message(self):
        """Message de conclusion de la démonstration"""
        
        print("\n" + "="*80)
        print("✅ DÉMONSTRATION TERMINÉE")
        print("="*80)
        
        conclusion_text = """
        La démonstration du système d'IA de sécurité informatique vocale est maintenant terminée.
        
        Vous avez pu observer:
        - Les capacités de communication vocale émotionnelle
        - L'analyse intelligente de menaces de sécurité
        - La détection d'anomalies en temps réel
        - L'escalade automatique des alertes critiques
        - L'intégration de la threat intelligence
        
        Ce système représente l'avenir de la cybersécurité assistée par IA.
        Merci de votre attention.
        """
        
        conclusion_settings = VoiceSettings(
            language=Language.FRENCH,
            tone=EmotionalTone.REASSURING,
            speed=1.0
        )
        
        print("🎙️ Message de conclusion...")
        if self.communication_interface.voice_enabled:
            await self.communication_interface.voice_engine.speak(conclusion_text, conclusion_settings)
        else:
            print(conclusion_text)
        
        # Statistiques finales
        await self._display_final_stats()
    
    async def _display_final_stats(self):
        """Affichage des statistiques finales"""
        
        print("\n📊 STATISTIQUES DE LA DÉMONSTRATION")
        print("-" * 40)
        
        # Récupération des stats de threat intelligence
        threat_status = await self.communication_interface.get_threat_status()
        
        print(f"💾 Indicateurs de menaces chargés:")
        threat_intel = threat_status.get('threat_intelligence_indicators', {})
        for indicator_type, count in threat_intel.items():
            print(f"   • {indicator_type}: {count}")
        
        print(f"\n🔊 Capacités vocales:")
        if self.communication_interface.voice_enabled:
            voices = await self.communication_interface.voice_engine.get_available_voices()
            print(f"   • Voix disponibles: {len(voices)}")
            print(f"   • Services configurés: Moteur vocal actif")
        else:
            print("   • Mode vocal: Non disponible")
        
        print(f"\n🎯 Scénarios exécutés: {len(self.demo_scenarios)}")
        print(f"⏱️ Durée totale: ~{len(self.demo_scenarios) * 2} minutes")
    
    async def _demo_security_alert_handler(self, alert_type: str, data: Any, context: Any):
        """Handler pour les alertes de sécurité de la démonstration"""
        print(f"   🚨 HANDLER ALERTE: {alert_type} - {type(data).__name__}")
    
    async def _demo_emergency_handler(self, response: Any, context: Any):
        """Handler pour les urgences de la démonstration"""
        print(f"   🆘 HANDLER URGENCE: Procédures d'urgence activées")
    
    async def run_interactive_mode(self):
        """Mode interactif pour tester l'IA vocale"""
        
        print("\n🎙️ MODE INTERACTIF - COMMUNICATION VOCALE")
        print("=" * 50)
        print("Tapez vos messages ou 'quit' pour quitter")
        print("Les réponses seront fournies en mode vocal et textuel")
        print()
        
        # Activation du mode vocal
        voice_activated = await self.communication_interface.enable_voice_mode()
        
        if voice_activated:
            print("✅ Mode vocal activé - L'IA vous écoute...")
        else:
            print("⚠️ Mode vocal non disponible - Mode texte seulement")
        
        session_id = "interactive_session"
        
        while True:
            try:
                # Saisie utilisateur
                user_input = input("\n👤 Vous: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                # Traitement du message
                print("🤖 Traitement en cours...")
                
                response = await self.communication_interface.process_message(
                    user_id="interactive_user",
                    content=user_input,
                    mode=CommunicationMode.MIXED,
                    session_id=session_id
                )
                
                # Affichage de la réponse
                print(f"\n🤖 Assistant: {response.content}")
                print(f"📊 Confiance: {response.confidence:.2f} | Urgence: {response.urgency.value}")
                
                # Recommandations si disponibles
                if response.recommendations:
                    print("💡 Recommandations:")
                    for i, rec in enumerate(response.recommendations[:3], 1):
                        print(f"   {i}. {rec}")
                
                # Questions de suivi
                if response.follow_up_questions:
                    print("❓ Questions suggérées:")
                    for q in response.follow_up_questions:
                        print(f"   • {q}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Erreur mode interactif: {e}")
        
        # Désactivation du mode vocal
        await self.communication_interface.disable_voice_mode()
        print("\n👋 Mode interactif terminé")


async def main():
    """Fonction principale de démonstration"""
    
    # Configuration du logging
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )
    
    demo = VoiceSecurityAIDemo()
    
    try:
        # Initialisation
        await demo.initialize()
        
        # Menu principal
        while True:
            print("\n" + "="*60)
            print("🛡️  IA DE SÉCURITÉ INFORMATIQUE VOCALE - MENU PRINCIPAL")
            print("="*60)
            print("1. 🎬 Démonstration complète (automatique)")
            print("2. 🎙️ Mode interactif (communication vocale)")
            print("3. 📊 Afficher les capacités du système")
            print("4. 🚪 Quitter")
            print()
            
            choice = input("Choisissez une option (1-4): ").strip()
            
            if choice == "1":
                await demo.run_full_demo()
            elif choice == "2":
                await demo.run_interactive_mode()
            elif choice == "3":
                await demo._display_final_stats()
            elif choice == "4":
                break
            else:
                print("❌ Option invalide, veuillez réessayer")
    
    except KeyboardInterrupt:
        print("\n\n👋 Démonstration interrompue par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
    finally:
        # Nettoyage
        if demo.communication_interface:
            await demo.communication_interface.shutdown()
        print("\n✅ Système arrêté proprement")


if __name__ == "__main__":
    asyncio.run(main())
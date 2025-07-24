#!/usr/bin/env python3
"""
Démonstration Simplifiée - IA de Sécurité Informatique Vocale
============================================================

Version allégée pour fonctionner avec les dépendances de base.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sys
import os

from loguru import logger
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


class SecurityThreatLevel:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class VoiceTone:
    NEUTRAL = "neutral"
    CONCERNED = "concerned"
    URGENT = "urgent"
    AUTHORITATIVE = "authoritative"


class SimpleVoiceEngine:
    """Moteur vocal simulé pour la démonstration"""
    
    def __init__(self):
        self.is_enabled = True
        
    async def speak(self, text: str, tone: str = VoiceTone.NEUTRAL):
        """Simulation de synthèse vocale"""
        tone_prefix = {
            VoiceTone.NEUTRAL: "[VOIX NEUTRE]",
            VoiceTone.CONCERNED: "[VOIX INQUIÈTE]",
            VoiceTone.URGENT: "[VOIX URGENTE]",
            VoiceTone.AUTHORITATIVE: "[VOIX AUTORITAIRE]"
        }
        
        prefix = tone_prefix.get(tone, "[VOIX]")
        print(f"\n🎙️ {prefix} {text}")
        
        # Simulation de délai de parole
        await asyncio.sleep(len(text) * 0.05)  # 50ms par caractère


class SecurityIntelligence:
    """Module d'intelligence de sécurité simplifié"""
    
    def __init__(self):
        self.threat_indicators = {
            "malicious_ips": [
                "192.168.1.100", "10.0.0.50", "185.220.100.240"
            ],
            "malicious_patterns": [
                "' OR '1'='1",
                "<script>",
                "union select",
                "../../../etc/passwd"
            ]
        }
        
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyse de sécurité d'un texte"""
        risk_score = 0.0
        detected_threats = []
        
        # Détection de patterns malicieux
        for pattern in self.threat_indicators["malicious_patterns"]:
            if pattern.lower() in text.lower():
                risk_score += 0.3
                detected_threats.append(f"Pattern malicieux: {pattern}")
        
        # Détection d'IPs suspectes
        for ip in self.threat_indicators["malicious_ips"]:
            if ip in text:
                risk_score += 0.4
                detected_threats.append(f"IP malicieuse: {ip}")
        
        # Mots-clés de sécurité
        security_keywords = [
            "ransomware", "malware", "intrusion", "attaque", "hack",
            "vulnérabilité", "exploit", "breach", "compromis"
        ]
        
        for keyword in security_keywords:
            if keyword.lower() in text.lower():
                risk_score += 0.2
                detected_threats.append(f"Mot-clé de sécurité: {keyword}")
        
        # Calcul du niveau de menace
        if risk_score >= 0.8:
            threat_level = SecurityThreatLevel.CRITICAL
        elif risk_score >= 0.6:
            threat_level = SecurityThreatLevel.HIGH
        elif risk_score >= 0.3:
            threat_level = SecurityThreatLevel.MEDIUM
        else:
            threat_level = SecurityThreatLevel.LOW
        
        return {
            "risk_score": min(risk_score, 1.0),
            "threat_level": threat_level,
            "detected_threats": detected_threats,
            "recommendations": self._generate_recommendations(threat_level)
        }
    
    def _generate_recommendations(self, threat_level: str) -> List[str]:
        """Génération de recommandations selon le niveau de menace"""
        recommendations = []
        
        if threat_level == SecurityThreatLevel.CRITICAL:
            recommendations = [
                "🚨 Isolation immédiate des systèmes affectés",
                "📞 Notification de l'équipe de crise",
                "🔒 Activation des procédures d'urgence",
                "📝 Documentation complète de l'incident"
            ]
        elif threat_level == SecurityThreatLevel.HIGH:
            recommendations = [
                "⚠️ Surveillance renforcée des systèmes",
                "🔍 Analyse approfondie des logs",
                "👥 Notification de l'équipe de sécurité",
                "🛡️ Renforcement des mesures défensives"
            ]
        elif threat_level == SecurityThreatLevel.MEDIUM:
            recommendations = [
                "📊 Monitoring continu",
                "🔎 Vérification des indicateurs",
                "📋 Mise à jour des alertes"
            ]
        else:
            recommendations = [
                "✅ Situation normale",
                "📈 Surveillance standard maintenue"
            ]
        
        return recommendations


class CyberSecAIDemo:
    """Démonstration simplifiée de l'IA de sécurité"""
    
    def __init__(self):
        self.voice_engine = SimpleVoiceEngine()
        self.security_intel = SecurityIntelligence()
        
    async def welcome_message(self):
        """Message de bienvenue"""
        welcome = """
        🛡️ Bienvenue dans la démonstration de l'IA de Sécurité Informatique Vocale !
        
        Ce système combine intelligence artificielle et cybersécurité pour:
        • Analyser les menaces en temps réel
        • Détecter les anomalies de sécurité
        • Communiquer les alertes par synthèse vocale
        • Recommander des actions de protection
        
        Commençons la démonstration...
        """
        
        print("="*80)
        print(welcome)
        print("="*80)
        
        await self.voice_engine.speak(
            "Bienvenue dans la démonstration de l'IA de sécurité informatique vocale. "
            "Je suis votre assistant de cybersécurité intelligent.",
            VoiceTone.NEUTRAL
        )
    
    async def demo_voice_tones(self):
        """Démonstration des différents tons vocaux"""
        print("\n🎯 DÉMONSTRATION DES TONS VOCAUX")
        print("-" * 40)
        
        tones = [
            (VoiceTone.NEUTRAL, "Voici un message d'information standard."),
            (VoiceTone.CONCERNED, "Attention, une anomalie a été détectée."),
            (VoiceTone.URGENT, "ALERTE! Intervention immédiate nécessaire!"),
            (VoiceTone.AUTHORITATIVE, "Consigne de sécurité: appliquez immédiatement le protocole.")
        ]
        
        for tone, message in tones:
            await self.voice_engine.speak(message, tone)
            await asyncio.sleep(1)
    
    async def demo_threat_analysis(self):
        """Démonstration d'analyse de menaces"""
        print("\n🔍 DÉMONSTRATION D'ANALYSE DE MENACES")
        print("-" * 40)
        
        test_scenarios = [
            {
                "name": "Injection SQL détectée",
                "input": "Connexion suspecte avec payload: ' OR '1'='1 depuis 192.168.1.100",
                "expected": "HIGH"
            },
            {
                "name": "Alerte Ransomware",
                "input": "URGENT: Ransomware détecté sur le serveur principal, chiffrement en cours!",
                "expected": "CRITICAL"
            },
            {
                "name": "Message normal",
                "input": "Mise à jour des politiques de sécurité terminée avec succès",
                "expected": "LOW"
            },
            {
                "name": "Intrusion détectée",
                "input": "Intrusion détectée depuis l'IP 185.220.100.240 avec exploit zero-day",
                "expected": "CRITICAL"
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n📋 Scénario {i}: {scenario['name']}")
            print(f"📝 Input: {scenario['input']}")
            
            # Analyse par l'IA de sécurité
            analysis = self.security_intel.analyze_text(scenario['input'])
            
            print(f"📊 Analyse:")
            print(f"   • Score de risque: {analysis['risk_score']:.2f}/1.0")
            print(f"   • Niveau de menace: {analysis['threat_level'].upper()}")
            
            if analysis['detected_threats']:
                print(f"   • Menaces détectées:")
                for threat in analysis['detected_threats']:
                    print(f"     - {threat}")
            
            # Communication vocale selon le niveau
            if analysis['threat_level'] == SecurityThreatLevel.CRITICAL:
                await self.voice_engine.speak(
                    f"ALERTE CRITIQUE! {scenario['name']}. Intervention immédiate requise!",
                    VoiceTone.URGENT
                )
            elif analysis['threat_level'] == SecurityThreatLevel.HIGH:
                await self.voice_engine.speak(
                    f"Alerte de sécurité élevée: {scenario['name']}. Action nécessaire.",
                    VoiceTone.CONCERNED
                )
            else:
                await self.voice_engine.speak(
                    f"Information de sécurité: {scenario['name']}.",
                    VoiceTone.NEUTRAL
                )
            
            # Recommandations
            print(f"💡 Recommandations:")
            for rec in analysis['recommendations']:
                print(f"   {rec}")
            
            await asyncio.sleep(2)
    
    async def demo_network_analysis(self):
        """Démonstration d'analyse de trafic réseau"""
        print("\n🌐 DÉMONSTRATION D'ANALYSE DE TRAFIC RÉSEAU")
        print("-" * 40)
        
        # Simulation de données réseau
        network_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-01 12:00:00', periods=100, freq='1min'),
            'source_ip': np.random.choice(['192.168.1.10', '192.168.1.100', '10.0.0.50'], 100),
            'bytes_transferred': np.random.normal(1000, 500, 100),
            'packets_count': np.random.poisson(10, 100),
            'duration': np.random.exponential(2, 100)
        })
        
        # Injection d'anomalies
        network_data.loc[50:55, 'bytes_transferred'] = 50000  # Pic suspect
        network_data.loc[70:75, 'packets_count'] = 100       # Trafic anormal
        
        print("📊 Analyse de 100 événements réseau...")
        
        # Préparation des données pour la détection d'anomalies
        features = network_data[['bytes_transferred', 'packets_count', 'duration']].values
        
        # Détection d'anomalies
        self.security_intel.anomaly_detector.fit(features)
        anomalies = self.security_intel.anomaly_detector.predict(features)
        
        anomaly_count = sum(1 for x in anomalies if x == -1)
        
        print(f"🚨 {anomaly_count} anomalies détectées dans le trafic réseau")
        
        if anomaly_count > 5:
            await self.voice_engine.speak(
                f"Attention! {anomaly_count} anomalies détectées dans le trafic réseau. "
                "Possible attaque en cours. Investigation recommandée.",
                VoiceTone.CONCERNED
            )
        else:
            await self.voice_engine.speak(
                f"{anomaly_count} anomalies mineures détectées. Surveillance standard maintenue.",
                VoiceTone.NEUTRAL
            )
        
        # Affichage des anomalies détectées
        anomaly_indices = [i for i, x in enumerate(anomalies) if x == -1]
        if anomaly_indices:
            print("\n📋 Détails des anomalies:")
            for idx in anomaly_indices[:5]:  # Afficher les 5 premières
                row = network_data.iloc[idx]
                print(f"   • {row['timestamp']}: {row['source_ip']} - "
                      f"{row['bytes_transferred']:.0f} bytes, "
                      f"{row['packets_count']} packets")
    
    async def demo_interactive_mode(self):
        """Mode interactif de démonstration"""
        print("\n💬 MODE INTERACTIF")
        print("-" * 40)
        print("Tapez vos messages de sécurité (ou 'quit' pour quitter)")
        print("L'IA analysera chaque message et répondra vocalement")
        print()
        
        await self.voice_engine.speak(
            "Mode interactif activé. Décrivez-moi vos préoccupations de sécurité.",
            VoiceTone.NEUTRAL
        )
        
        while True:
            try:
                user_input = input("\n👤 Vous: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    await self.voice_engine.speak(
                        "Session terminée. Merci d'avoir utilisé l'assistant de cybersécurité.",
                        VoiceTone.NEUTRAL
                    )
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Analyse en cours...")
                
                # Analyse du message
                analysis = self.security_intel.analyze_text(user_input)
                
                print(f"📊 Résultat:")
                print(f"   • Score de risque: {analysis['risk_score']:.2f}")
                print(f"   • Niveau: {analysis['threat_level'].upper()}")
                
                # Réponse vocale adaptée
                if analysis['threat_level'] == SecurityThreatLevel.CRITICAL:
                    response = "Situation critique détectée! Activation du protocole d'urgence."
                    tone = VoiceTone.URGENT
                elif analysis['threat_level'] == SecurityThreatLevel.HIGH:
                    response = "Menace élevée identifiée. Surveillance renforcée recommandée."
                    tone = VoiceTone.CONCERNED
                elif analysis['threat_level'] == SecurityThreatLevel.MEDIUM:
                    response = "Situation à surveiller. Précautions recommandées."
                    tone = VoiceTone.CONCERNED
                else:
                    response = "Situation normale. Aucune menace détectée."
                    tone = VoiceTone.NEUTRAL
                
                await self.voice_engine.speak(response, tone)
                
                # Affichage des recommandations
                if analysis['recommendations']:
                    print("💡 Recommandations:")
                    for rec in analysis['recommendations']:
                        print(f"   {rec}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")
    
    async def run_full_demo(self):
        """Exécution de la démonstration complète"""
        try:
            await self.welcome_message()
            await asyncio.sleep(2)
            
            await self.demo_voice_tones()
            await asyncio.sleep(2)
            
            await self.demo_threat_analysis()
            await asyncio.sleep(2)
            
            await self.demo_network_analysis()
            await asyncio.sleep(2)
            
            print("\n🎉 DÉMONSTRATION TERMINÉE")
            print("="*80)
            
            await self.voice_engine.speak(
                "Démonstration terminée. L'IA de sécurité informatique vocale est prête "
                "à protéger votre infrastructure. Merci de votre attention.",
                VoiceTone.NEUTRAL
            )
            
        except KeyboardInterrupt:
            print("\n\n👋 Démonstration interrompue")
            await self.voice_engine.speak("Démonstration interrompue. Au revoir!", VoiceTone.NEUTRAL)


async def main():
    """Fonction principale"""
    print("🚀 Initialisation de l'IA de Sécurité Informatique Vocale...")
    
    demo = CyberSecAIDemo()
    
    while True:
        print("\n" + "="*60)
        print("🛡️  IA DE SÉCURITÉ INFORMATIQUE VOCALE - MENU")
        print("="*60)
        print("1. 🎬 Démonstration complète")
        print("2. 🎙️ Test des tons vocaux")
        print("3. 🔍 Analyse de menaces")
        print("4. 🌐 Analyse de trafic réseau")
        print("5. 💬 Mode interactif")
        print("6. 🚪 Quitter")
        print()
        
        choice = input("Choisissez une option (1-6): ").strip()
        
        try:
            if choice == "1":
                await demo.run_full_demo()
            elif choice == "2":
                await demo.demo_voice_tones()
            elif choice == "3":
                await demo.demo_threat_analysis()
            elif choice == "4":
                await demo.demo_network_analysis()
            elif choice == "5":
                await demo.demo_interactive_mode()
            elif choice == "6":
                print("\n👋 Au revoir !")
                break
            else:
                print("❌ Option invalide")
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            logger.error(f"Erreur: {e}")


if __name__ == "__main__":
    asyncio.run(main())
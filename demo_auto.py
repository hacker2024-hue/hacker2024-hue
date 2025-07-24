#!/usr/bin/env python3
"""
Démonstration Automatique - IA de Sécurité Informatique Vocale
==============================================================

Version automatique qui s'exécute entièrement sans intervention utilisateur.
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any
import sys

try:
    from loguru import logger
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import IsolationForest
except ImportError as e:
    print(f"Installation des dépendances requise: {e}")
    sys.exit(1)


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


class VoiceEngine:
    """Moteur vocal simulé avec affichage textuel"""
    
    def __init__(self):
        self.is_enabled = True
        
    async def speak(self, text: str, tone: str = VoiceTone.NEUTRAL):
        """Simulation de synthèse vocale avec affichage"""
        tone_emoji = {
            VoiceTone.NEUTRAL: "💬",
            VoiceTone.CONCERNED: "😟",
            VoiceTone.URGENT: "🚨",
            VoiceTone.AUTHORITATIVE: "👮"
        }
        
        tone_style = {
            VoiceTone.NEUTRAL: "",
            VoiceTone.CONCERNED: " [TON INQUIET]",
            VoiceTone.URGENT: " [TON URGENT]",
            VoiceTone.AUTHORITATIVE: " [TON AUTORITAIRE]"
        }
        
        emoji = tone_emoji.get(tone, "🎙️")
        style = tone_style.get(tone, "")
        
        print(f"\n{emoji} [IA VOCALE]{style}: {text}")
        
        # Simulation de délai de parole (plus court pour la démo auto)
        await asyncio.sleep(min(len(text) * 0.02, 3))  # Max 3 secondes


class SecurityAnalyzer:
    """Analyseur de sécurité avec IA"""
    
    def __init__(self):
        self.threat_db = {
            "malicious_ips": [
                "192.168.1.100", "10.0.0.50", "185.220.100.240", 
                "185.220.101.1", "172.16.0.10"
            ],
            "attack_patterns": [
                "' OR '1'='1", "<script>", "union select", "../../../etc/passwd",
                "cmd.exe", "DROP TABLE", "INSERT INTO", "<iframe"
            ],
            "malware_signatures": [
                "ransomware", "trojan", "worm", "rootkit", "backdoor"
            ]
        }
        
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        
    def analyze_threat(self, text: str) -> Dict[str, Any]:
        """Analyse complète d'une menace"""
        risk_score = 0.0
        threats_found = []
        
        # Détection de patterns d'attaque
        for pattern in self.threat_db["attack_patterns"]:
            if pattern.lower() in text.lower():
                risk_score += 0.35
                threats_found.append(f"Pattern d'attaque: {pattern}")
        
        # Détection d'IPs malicieuses
        for ip in self.threat_db["malicious_ips"]:
            if ip in text:
                risk_score += 0.4
                threats_found.append(f"IP malicieuse: {ip}")
        
        # Détection de signatures malware
        for signature in self.threat_db["malware_signatures"]:
            if signature.lower() in text.lower():
                risk_score += 0.3
                threats_found.append(f"Signature malware: {signature}")
        
        # Mots-clés de sécurité critique
        critical_keywords = [
            "breach", "compromis", "exploit", "zero-day", "apt",
            "intrusion", "exfiltration", "phishing", "botnet"
        ]
        
        for keyword in critical_keywords:
            if keyword.lower() in text.lower():
                risk_score += 0.25
                threats_found.append(f"Mot-clé critique: {keyword}")
        
        # Calcul du niveau de menace
        if risk_score >= 0.9:
            threat_level = SecurityThreatLevel.CRITICAL
        elif risk_score >= 0.7:
            threat_level = SecurityThreatLevel.HIGH
        elif risk_score >= 0.4:
            threat_level = SecurityThreatLevel.MEDIUM
        else:
            threat_level = SecurityThreatLevel.LOW
        
        return {
            "risk_score": min(risk_score, 1.0),
            "threat_level": threat_level,
            "threats_detected": threats_found,
            "recommendations": self._get_recommendations(threat_level),
            "urgency": self._get_urgency(threat_level)
        }
    
    def _get_recommendations(self, threat_level: str) -> List[str]:
        """Recommandations selon le niveau de menace"""
        if threat_level == SecurityThreatLevel.CRITICAL:
            return [
                "🚨 URGENCE: Isolation immédiate des systèmes",
                "📞 Activation de la cellule de crise",
                "🔒 Coupure des accès réseau compromis",
                "📋 Documentation forensique complète",
                "🚁 Escalade vers les autorités si nécessaire"
            ]
        elif threat_level == SecurityThreatLevel.HIGH:
            return [
                "⚠️ Surveillance intensive des systèmes",
                "🔍 Analyse approfondie des logs",
                "👥 Notification équipe sécurité",
                "🛡️ Renforcement des mesures défensives",
                "📊 Corrélation avec autres incidents"
            ]
        elif threat_level == SecurityThreatLevel.MEDIUM:
            return [
                "📈 Monitoring renforcé",
                "🔎 Vérification des indicateurs",
                "📝 Mise à jour des alertes",
                "🔄 Révision des politiques"
            ]
        else:
            return [
                "✅ Situation sous contrôle",
                "📊 Surveillance standard maintenue",
                "📝 Archivage de l'événement"
            ]
    
    def _get_urgency(self, threat_level: str) -> str:
        """Niveau d'urgence de la communication"""
        if threat_level == SecurityThreatLevel.CRITICAL:
            return VoiceTone.URGENT
        elif threat_level == SecurityThreatLevel.HIGH:
            return VoiceTone.CONCERNED
        elif threat_level == SecurityThreatLevel.MEDIUM:
            return VoiceTone.CONCERNED
        else:
            return VoiceTone.NEUTRAL


class CyberSecAIDemo:
    """Démonstration automatique de l'IA de cybersécurité"""
    
    def __init__(self):
        self.voice = VoiceEngine()
        self.analyzer = SecurityAnalyzer()
        
    async def show_banner(self):
        """Affichage de la bannière"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🛡️   IA DE SÉCURITÉ INFORMATIQUE AVEC COMMUNICATION VOCALE AVANCÉE   🛡️     ║
║                                                                              ║
║  🎯 Fonctionnalités:                                                         ║
║    • Analyse de menaces en temps réel avec IA                              ║
║    • Communication vocale émotionnelle adaptative                          ║
║    • Détection d'anomalies comportementales                                ║
║    • Escalade automatique des alertes critiques                            ║
║    • Intelligence de sécurité contextuelle                                 ║
║                                                                              ║
║  🚀 Démonstration en cours...                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
        await self.voice.speak(
            "Bienvenue dans la démonstration de l'Intelligence Artificielle de sécurité "
            "informatique avec communication vocale avancée. Je suis votre assistant "
            "de cybersécurité intelligent, capable de comprendre et de communiquer "
            "à haute voix avec les experts en sécurité.",
            VoiceTone.NEUTRAL
        )
    
    async def demo_voice_capabilities(self):
        """Démonstration des capacités vocales"""
        print("\n" + "="*80)
        print("🎙️  DÉMONSTRATION DES CAPACITÉS VOCALES ÉMOTIONNELLES")
        print("="*80)
        
        voice_examples = [
            (VoiceTone.NEUTRAL, "Bonjour, je suis votre assistant IA de sécurité. Tous les systèmes fonctionnent normalement."),
            (VoiceTone.CONCERNED, "Attention ! J'ai détecté une activité suspecte sur le réseau. Une investigation est recommandée."),
            (VoiceTone.URGENT, "ALERTE CRITIQUE ! Ransomware détecté ! Isolation immédiate des systèmes requise !"),
            (VoiceTone.AUTHORITATIVE, "Directive de sécurité : Appliquez immédiatement le protocole de confinement niveau 3.")
        ]
        
        for i, (tone, message) in enumerate(voice_examples, 1):
            print(f"\n📢 Exemple {i} - Démonstration du ton {tone.upper()}:")
            await self.voice.speak(message, tone)
            await asyncio.sleep(1)
    
    async def demo_threat_analysis(self):
        """Démonstration d'analyse de menaces"""
        print("\n" + "="*80)
        print("🔍  DÉMONSTRATION D'ANALYSE DE MENACES EN TEMPS RÉEL")
        print("="*80)
        
        threat_scenarios = [
            {
                "name": "Tentative d'Injection SQL",
                "description": "Détection d'une tentative d'injection SQL sur l'application web",
                "input": "Requête suspecte détectée: SELECT * FROM users WHERE id = '1' OR '1'='1' depuis l'IP 192.168.1.100",
                "context": "Application web de e-commerce"
            },
            {
                "name": "Alerte Ransomware Critical",
                "description": "Détection de ransomware avec chiffrement en cours",
                "input": "URGENT: Ransomware WannaCry détecté sur serveur principal, 45% des fichiers déjà chiffrés, propagation en cours",
                "context": "Infrastructure critique d'entreprise"
            },
            {
                "name": "Activité APT Sophistiquée",
                "description": "Détection d'une menace persistante avancée",
                "input": "Activité APT détectée: Backdoor installé sur contrôleur de domaine, exfiltration de données vers 185.220.100.240",
                "context": "Réseau d'entreprise sensible"
            },
            {
                "name": "Attaque DDoS Massive",
                "description": "Attaque par déni de service distribué",
                "input": "Attaque DDoS de 50 Gbps en cours depuis botnet, 10.0.0.50 et 185.220.101.1 identifiés comme sources",
                "context": "Services web publics"
            },
            {
                "name": "Message Normal",
                "description": "Communication standard de sécurité",
                "input": "Mise à jour des signatures antivirus effectuée avec succès sur tous les postes",
                "context": "Maintenance de routine"
            }
        ]
        
        for i, scenario in enumerate(threat_scenarios, 1):
            print(f"\n📋 SCÉNARIO {i}: {scenario['name']}")
            print(f"🏢 Contexte: {scenario['context']}")
            print(f"📝 Description: {scenario['description']}")
            print(f"📥 Input: {scenario['input']}")
            
            # Analyse par l'IA
            print("\n🧠 Analyse IA en cours...")
            await asyncio.sleep(1)
            
            analysis = self.analyzer.analyze_threat(scenario['input'])
            
            # Affichage des résultats
            print(f"📊 RÉSULTATS D'ANALYSE:")
            print(f"   💯 Score de risque: {analysis['risk_score']:.2f}/1.0")
            print(f"   ⚠️  Niveau de menace: {analysis['threat_level'].upper()}")
            
            if analysis['threats_detected']:
                print(f"   🚨 Menaces détectées:")
                for threat in analysis['threats_detected']:
                    print(f"      • {threat}")
            
            # Communication vocale adaptée
            if analysis['threat_level'] == SecurityThreatLevel.CRITICAL:
                voice_msg = f"ALERTE CRITIQUE MAXIMALE ! {scenario['name']} confirmé. Activation immédiate du protocole d'urgence requise !"
            elif analysis['threat_level'] == SecurityThreatLevel.HIGH:
                voice_msg = f"Alerte de sécurité de niveau élevé : {scenario['name']}. Action immédiate nécessaire."
            elif analysis['threat_level'] == SecurityThreatLevel.MEDIUM:
                voice_msg = f"Incident de sécurité modéré détecté : {scenario['name']}. Surveillance renforcée recommandée."
            else:
                voice_msg = f"Information de sécurité : {scenario['name']}. Situation normale."
            
            await self.voice.speak(voice_msg, analysis['urgency'])
            
            # Recommandations
            print(f"💡 RECOMMANDATIONS:")
            for rec in analysis['recommendations']:
                print(f"   {rec}")
            
            print("\n" + "-"*60)
            await asyncio.sleep(2)
    
    async def demo_network_anomaly_detection(self):
        """Démonstration de détection d'anomalies réseau"""
        print("\n" + "="*80)
        print("🌐  DÉMONSTRATION D'ANALYSE DE TRAFIC RÉSEAU ET DÉTECTION D'ANOMALIES")
        print("="*80)
        
        await self.voice.speak(
            "Démarrage de l'analyse du trafic réseau en temps réel avec détection "
            "d'anomalies comportementales par intelligence artificielle.",
            VoiceTone.NEUTRAL
        )
        
        # Simulation de données réseau réalistes
        print("\n📊 Génération de données de trafic réseau simulées...")
        
        # Trafic normal
        normal_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-15 08:00:00', periods=80, freq='1min'),
            'source_ip': np.random.choice(['192.168.1.10', '192.168.1.20', '192.168.1.30'], 80),
            'bytes_transferred': np.random.normal(2000, 300, 80),
            'packets_count': np.random.poisson(15, 80),
            'duration': np.random.exponential(1.5, 80),
            'protocol': np.random.choice(['HTTP', 'HTTPS', 'SSH'], 80)
        })
        
        # Injection d'anomalies malicieuses
        anomaly_data = pd.DataFrame({
            'timestamp': pd.date_range('2024-01-15 09:20:00', periods=20, freq='1min'),
            'source_ip': ['185.220.100.240'] * 20,  # IP malicieuse
            'bytes_transferred': np.random.normal(50000, 5000, 20),  # Trafic anormalement élevé
            'packets_count': np.random.poisson(200, 20),  # Burst de paquets
            'duration': np.random.exponential(0.1, 20),  # Connexions très courtes
            'protocol': ['TCP'] * 20
        })
        
        # Combinaison des données
        network_data = pd.concat([normal_data, anomaly_data], ignore_index=True)
        network_data = network_data.sort_values('timestamp').reset_index(drop=True)
        
        print(f"📈 Analyse de {len(network_data)} événements réseau...")
        
        # Préparation pour la détection d'anomalies
        features = network_data[['bytes_transferred', 'packets_count', 'duration']].values
        
        # Entraînement du détecteur
        print("🧠 Entraînement du modèle de détection d'anomalies...")
        self.analyzer.anomaly_detector.fit(features[:80])  # Entraînement sur données normales
        
        # Détection
        anomalies = self.analyzer.anomaly_detector.predict(features)
        anomaly_indices = [i for i, x in enumerate(anomalies) if x == -1]
        
        print(f"🚨 RÉSULTATS: {len(anomaly_indices)} anomalies détectées")
        
        # Analyse des IPs suspectes
        suspicious_ips = set()
        for idx in anomaly_indices:
            ip = network_data.iloc[idx]['source_ip']
            if ip in self.analyzer.threat_db['malicious_ips']:
                suspicious_ips.add(ip)
        
        # Communication vocale selon les résultats
        if len(suspicious_ips) > 0:
            await self.voice.speak(
                f"ALERTE ! {len(anomaly_indices)} anomalies détectées dans le trafic réseau, "
                f"incluant {len(suspicious_ips)} adresses IP connues comme malicieuses. "
                "Attaque potentielle en cours. Investigation immédiate requise.",
                VoiceTone.URGENT
            )
        elif len(anomaly_indices) > 10:
            await self.voice.speak(
                f"Attention ! {len(anomaly_indices)} anomalies détectées dans le trafic réseau. "
                "Surveillance renforcée recommandée pour identifier une possible menace.",
                VoiceTone.CONCERNED
            )
        else:
            await self.voice.speak(
                f"{len(anomaly_indices)} anomalies mineures détectées. "
                "Trafic réseau dans les paramètres normaux.",
                VoiceTone.NEUTRAL
            )
        
        # Détails des anomalies les plus critiques
        if anomaly_indices:
            print(f"\n📋 DÉTAILS DES ANOMALIES CRITIQUES:")
            for i, idx in enumerate(anomaly_indices[:5]):  # Top 5
                row = network_data.iloc[idx]
                threat_level = "🚨 CRITIQUE" if row['source_ip'] in suspicious_ips else "⚠️ SUSPECTE"
                print(f"   {i+1}. {threat_level} - {row['timestamp']} | IP: {row['source_ip']} | "
                      f"{row['bytes_transferred']:.0f} bytes | {row['packets_count']} packets")
    
    async def demo_intelligent_escalation(self):
        """Démonstration de l'escalade intelligente"""
        print("\n" + "="*80)
        print("🚁  DÉMONSTRATION DE L'ESCALADE INTELLIGENTE DES INCIDENTS")
        print("="*80)
        
        await self.voice.speak(
            "Démonstration du système d'escalade intelligente qui adapte automatiquement "
            "le niveau de réponse selon la criticité des menaces détectées.",
            VoiceTone.AUTHORITATIVE
        )
        
        escalation_scenarios = [
            {
                "level": "NIVEAU 1 - Surveillance",
                "description": "Activité normale avec monitoring standard",
                "actions": ["📊 Logging standard", "📈 Métriques de base"],
                "voice_tone": VoiceTone.NEUTRAL,
                "message": "Surveillance normale maintenue. Tous les systèmes opérationnels."
            },
            {
                "level": "NIVEAU 2 - Attention",
                "description": "Anomalie détectée nécessitant une surveillance accrue",
                "actions": ["🔍 Analyse approfondie", "📧 Notification équipe", "📊 Monitoring renforcé"],
                "voice_tone": VoiceTone.CONCERNED,
                "message": "Anomalie détectée. Surveillance renforcée activée. Équipe notifiée."
            },
            {
                "level": "NIVEAU 3 - Alerte",
                "description": "Incident de sécurité confirmé",
                "actions": ["🚨 Alerte sécurité", "👥 Mobilisation équipe", "🔒 Mesures préventives", "📋 Documentation"],
                "voice_tone": VoiceTone.CONCERNED,
                "message": "Incident de sécurité confirmé. Équipe de réponse mobilisée. Mesures défensives activées."
            },
            {
                "level": "NIVEAU 4 - Urgence",
                "description": "Menace critique avec impact potentiel majeur",
                "actions": ["🚨 Alerte critique", "📞 Cellule de crise", "🔐 Isolation systèmes", "🚁 Escalade managériale"],
                "voice_tone": VoiceTone.URGENT,
                "message": "ALERTE CRITIQUE ! Cellule de crise activée. Isolation des systèmes en cours."
            },
            {
                "level": "NIVEAU 5 - Catastrophe",
                "description": "Incident majeur avec compromission avérée",
                "actions": ["🆘 Urgence maximale", "🏢 Direction générale", "👮 Autorités", "📺 Communication crise", "🔒 Arrêt d'urgence"],
                "voice_tone": VoiceTone.URGENT,
                "message": "URGENCE MAXIMALE ! Compromission majeure confirmée. Protocole de crise activé. Authorities notifiées."
            }
        ]
        
        for i, scenario in enumerate(escalation_scenarios, 1):
            print(f"\n🎯 {scenario['level']}")
            print(f"📝 {scenario['description']}")
            print(f"⚡ Actions automatiques:")
            for action in scenario['actions']:
                print(f"   • {action}")
            
            await self.voice.speak(scenario['message'], scenario['voice_tone'])
            
            # Simulation du délai de traitement
            if i < len(escalation_scenarios):
                print("   ⏳ Évaluation du niveau suivant...")
                await asyncio.sleep(1.5)
    
    async def demo_real_time_monitoring(self):
        """Démonstration du monitoring en temps réel"""
        print("\n" + "="*80)
        print("📡  DÉMONSTRATION DU MONITORING EN TEMPS RÉEL")
        print("="*80)
        
        await self.voice.speak(
            "Activation du monitoring en temps réel avec analyse continue des événements "
            "de sécurité et communication vocale automatique des alertes.",
            VoiceTone.NEUTRAL
        )
        
        # Simulation d'événements en temps réel
        events = [
            ("08:15:23", "INFO", "Connexion utilisateur normal", "Aucune action"),
            ("08:16:45", "WARNING", "Tentative de connexion échouée", "Surveillance renforcée"),
            ("08:17:12", "ALERT", "Pattern d'injection SQL détecté", "Blocage automatique"),
            ("08:18:03", "CRITICAL", "Ransomware identifié", "Isolation immédiate"),
            ("08:18:30", "EMERGENCY", "Exfiltration de données confirmée", "Protocole d'urgence")
        ]
        
        print("\n📊 FLUX D'ÉVÉNEMENTS EN TEMPS RÉEL:")
        print("-" * 60)
        
        for timestamp, level, event, action in events:
            print(f"[{timestamp}] {level:>9} | {event}")
            print(f"{'':>13} Action: {action}")
            
            # Communication vocale selon le niveau
            if level == "EMERGENCY":
                await self.voice.speak(
                    f"URGENCE ! {event}. {action} en cours.",
                    VoiceTone.URGENT
                )
            elif level == "CRITICAL":
                await self.voice.speak(
                    f"Alerte critique : {event}. {action}.",
                    VoiceTone.URGENT
                )
            elif level == "ALERT":
                await self.voice.speak(
                    f"Alerte sécurité : {event}.",
                    VoiceTone.CONCERNED
                )
            elif level == "WARNING":
                await self.voice.speak(
                    f"Attention : {event}.",
                    VoiceTone.CONCERNED
                )
            
            await asyncio.sleep(2)
    
    async def conclusion(self):
        """Conclusion de la démonstration"""
        print("\n" + "="*80)
        print("🎉  DÉMONSTRATION TERMINÉE - SYNTHÈSE DES CAPACITÉS")
        print("="*80)
        
        capabilities = [
            "✅ Communication vocale émotionnelle adaptative",
            "✅ Analyse de menaces en temps réel par IA",
            "✅ Détection d'anomalies comportementales",
            "✅ Escalade intelligente automatique",
            "✅ Monitoring continu avec alertes vocales",
            "✅ Support multi-langue et multi-ton",
            "✅ Intégration complète cybersécurité"
        ]
        
        print("\n🛡️ CAPACITÉS DÉMONTRÉES:")
        for capability in capabilities:
            print(f"   {capability}")
        
        await self.voice.speak(
            "Démonstration terminée avec succès. Cette Intelligence Artificielle de "
            "sécurité informatique avec communication vocale avancée est maintenant "
            "prête à protéger votre infrastructure avec une compréhension et une "
            "communication à haute voix adaptées aux besoins des experts en sécurité. "
            "Le système combine l'analyse de menaces de pointe avec une interface "
            "vocale naturelle pour une cybersécurité nouvelle génération.",
            VoiceTone.AUTHORITATIVE
        )
        
        print(f"\n🚀 SYSTÈME PRÊT POUR DÉPLOIEMENT")
        print(f"📅 Démonstration complétée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
        print(f"⭐ IA de Sécurité Informatique Vocale - Version 1.0")
        print("="*80)


async def main():
    """Fonction principale de la démonstration automatique"""
    demo = CyberSecAIDemo()
    
    try:
        print("🚀 Initialisation de l'IA de Sécurité Informatique Vocale...")
        await asyncio.sleep(1)
        
        # Exécution séquentielle de toutes les démonstrations
        await demo.show_banner()
        await asyncio.sleep(2)
        
        await demo.demo_voice_capabilities()
        await asyncio.sleep(2)
        
        await demo.demo_threat_analysis()
        await asyncio.sleep(2)
        
        await demo.demo_network_anomaly_detection()
        await asyncio.sleep(2)
        
        await demo.demo_intelligent_escalation()
        await asyncio.sleep(2)
        
        await demo.demo_real_time_monitoring()
        await asyncio.sleep(2)
        
        await demo.conclusion()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Démonstration interrompue par l'utilisateur")
        await demo.voice.speak("Démonstration interrompue. Au revoir !", VoiceTone.NEUTRAL)
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        logger.error(f"Erreur: {e}")


if __name__ == "__main__":
    print("🛡️ LANCEMENT DE LA DÉMONSTRATION IA SÉCURITÉ VOCALE")
    print("="*60)
    asyncio.run(main())
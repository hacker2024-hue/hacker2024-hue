#!/usr/bin/env python3
"""
CyberSec AI Assistant - Lanceur de Démonstration
===============================================

Version simplifiée fonctionnant sans dépendances externes.
"""

import sys
import json
import time
import random
from datetime import datetime
from pathlib import Path


class DemoCyberSecAI:
    """Version de démonstration du moteur IA"""
    
    def __init__(self):
        self.threat_keywords = {
            "malware": ["virus", "trojan", "ransomware", "spyware", "rootkit", "botnet"],
            "network": ["ddos", "phishing", "injection", "xss", "mitm", "spoofing"],
            "vulnerability": ["exploit", "zero-day", "buffer overflow", "cve", "rce"],
            "incident": ["breach", "leak", "compromise", "intrusion", "apt"]
        }
        
        self.responses = {
            "greeting": "🛡️ Bonjour ! Je suis CyberSec AI Assistant, votre expert IA en cybersécurité.",
            "malware": "🦠 J'ai détecté des indicateurs de malware. Recommandations : isoler le système, scanner avec antivirus, analyser les logs.",
            "network": "🌐 Activité réseau suspecte détectée. Actions : vérifier pare-feu, analyser trafic, bloquer IPs malveillantes.",
            "vulnerability": "🔍 Vulnérabilité identifiée. Priorité : appliquer les correctifs, scanner le système, évaluer l'exposition.",
            "incident": "🚨 Incident de sécurité potentiel. Procédure : contenir la menace, collecter preuves, notifier équipe.",
            "default": "💬 Je peux analyser des menaces, expliquer des concepts de sécurité, et vous assister dans vos investigations."
        }
    
    def analyze_message(self, message):
        """Analyse basique d'un message"""
        message_lower = message.lower()
        detected_threats = []
        
        for category, keywords in self.threat_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_threats.append(category)
        
        # Détection d'IoCs basique
        iocs = []
        import re
        
        # IPs
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, message)
        iocs.extend(ips)
        
        # Domaines
        domain_pattern = r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.([a-zA-Z]{2,})\b'
        domains = re.findall(domain_pattern, message)
        iocs.extend([f"{match[0]}.{match[1]}" for match in domains])
        
        return detected_threats, iocs
    
    def generate_response(self, message, threats, iocs):
        """Génération de réponse contextuelle"""
        if not threats and not iocs:
            if any(word in message.lower() for word in ["bonjour", "salut", "hello", "hi"]):
                return self.responses["greeting"]
            else:
                return self.responses["default"]
        
        # Réponse basée sur les menaces détectées
        primary_threat = threats[0] if threats else "default"
        response = self.responses.get(primary_threat, self.responses["default"])
        
        if iocs:
            response += f"\n\n🔍 IoCs détectés: {', '.join(iocs[:3])}"
            if len(iocs) > 3:
                response += f" (+{len(iocs)-3} autres)"
        
        return response


def print_banner():
    """Bannière de démarrage"""
    banner = """
    ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗    █████╗ ██╗
    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝   ██╔══██╗██║
    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██║        ███████║██║
    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║        ██╔══██║██║
    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗╚██████╗   ██║  ██║██║
     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝   ╚═╝  ╚═╝╚═╝
    """
    
    print("\033[96m" + banner + "\033[0m")
    print("\033[93m" + "🛡️  Assistant IA Avancé en Cybersécurité - MODE DÉMO" + "\033[0m")
    print("\033[92m" + "Version 1.0.0 - Développé par @hacker2024-hue" + "\033[0m")
    print("\033[94m" + "=" * 80 + "\033[0m")
    print()


def simulate_startup():
    """Simulation du démarrage du système"""
    
    startup_steps = [
        "🔧 Initialisation du système...",
        "🧠 Chargement du moteur IA...",
        "🛡️ Activation des modules de sécurité...", 
        "🌐 Configuration de l'interface...",
        "📊 Chargement de la threat intelligence...",
        "🚀 Système prêt !"
    ]
    
    for step in startup_steps:
        print(f"  {step}")
        time.sleep(0.8)
    
    print()


def demo_threat_analysis():
    """Démonstration d'analyse de menaces"""
    
    print("🎯 DÉMONSTRATION - Analyse de Menaces")
    print("=" * 50)
    
    sample_threats = [
        "Détection d'un trojan sur l'IP 192.168.1.100",
        "Attaque DDoS en cours depuis malicious.example.com", 
        "Exploitation de vulnérabilité CVE-2023-1234",
        "Tentative de phishing détectée",
        "Ransomware WannaCry identifié"
    ]
    
    ai = DemoCyberSecAI()
    
    for i, threat in enumerate(sample_threats, 1):
        print(f"\n📝 Exemple {i}: {threat}")
        print("-" * 40)
        
        threats, iocs = ai.analyze_message(threat)
        response = ai.generate_response(threat, threats, iocs)
        
        print(f"🤖 Réponse IA: {response}")
        
        if threats:
            print(f"🎯 Catégories: {', '.join(threats)}")
        
        time.sleep(1)


def interactive_chat():
    """Mode chat interactif"""
    
    print("\n💬 MODE CHAT INTERACTIF")
    print("=" * 50)
    print("Tapez vos questions sur la cybersécurité (ou 'quit' pour quitter)")
    print("Exemples:")
    print("  - Analyse cette IP: 192.168.1.100")
    print("  - Comment détecter un ransomware?")
    print("  - Que faire en cas d'incident?")
    print()
    
    ai = DemoCyberSecAI()
    session_count = 0
    
    while True:
        try:
            user_input = input("🛡️ Vous: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Au revoir ! Restez vigilants en cybersécurité !")
                break
            
            if not user_input:
                continue
            
            session_count += 1
            print(f"🤖 CyberSec AI [Session {session_count}]:")
            
            # Simulation du temps de traitement
            print("  🔄 Analyse en cours...")
            time.sleep(0.5)
            
            threats, iocs = ai.analyze_message(user_input)
            response = ai.generate_response(user_input, threats, iocs)
            
            print(f"  {response}")
            
            # Informations additionnelles
            if threats or iocs:
                print()
                if threats:
                    print(f"  📊 Menaces détectées: {', '.join(set(threats))}")
                if iocs:
                    print(f"  🔍 IoCs trouvés: {len(iocs)} indicateur(s)")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt demandé. Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")


def show_system_info():
    """Affichage des informations système"""
    
    print("ℹ️ INFORMATIONS SYSTÈME")
    print("=" * 50)
    print(f"📅 Démarré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📂 Répertoire: {Path.cwd()}")
    print(f"🛡️ Mode: Démonstration (sans dépendances)")
    print(f"🎯 Fonctionnalités:")
    print("   ✅ Détection d'IoCs (IPs, domaines)")
    print("   ✅ Classification de menaces")
    print("   ✅ Recommandations contextuelles")
    print("   ✅ Chat interactif")
    print("   ✅ Simulation d'escalade")
    print()


def main_menu():
    """Menu principal de démonstration"""
    
    while True:
        print("📋 MENU PRINCIPAL")
        print("=" * 30)
        print("1. 🎯 Démonstration d'analyse")
        print("2. 💬 Chat interactif")
        print("3. ℹ️ Informations système") 
        print("4. 🔄 Test de structure")
        print("5. 👋 Quitter")
        print()
        
        try:
            choice = input("Votre choix (1-5): ").strip()
            
            if choice == '1':
                demo_threat_analysis()
            elif choice == '2':
                interactive_chat()
            elif choice == '3':
                show_system_info()
            elif choice == '4':
                # Lancement du test de structure
                import subprocess
                result = subprocess.run([sys.executable, "test_structure.py"], 
                                      capture_output=True, text=True)
                print(result.stdout)
            elif choice == '5':
                print("👋 Arrêt de CyberSec AI Assistant")
                break
            else:
                print("❌ Choix invalide. Veuillez choisir entre 1 et 5.")
            
            input("\nAppuyez sur Entrée pour continuer...")
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt demandé. Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")


def main():
    """Fonction principale"""
    
    print_banner()
    show_system_info()
    simulate_startup()
    
    print("🎉 CyberSec AI Assistant est maintenant opérationnel !")
    print("🛡️ Prêt à analyser les menaces et assister les experts en cybersécurité")
    print()
    
    main_menu()


if __name__ == "__main__":
    main()
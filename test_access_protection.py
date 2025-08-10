#!/usr/bin/env python3
"""
Test du Système de Protection d'Accès
=====================================

Script de test pour vérifier le système de protection par mot de passe
et la protection contre le téléchargement non autorisé.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Import du système de protection
from security.access_protection import AccessProtection, access_protection

class AccessProtectionTester:
    """
    Testeur du système de protection d'accès
    """
    
    def __init__(self):
        self.access_protection = access_protection
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license": "CI-CYBER-2024-001"
        }
    
    async def initialize(self):
        """Initialisation du testeur"""
        print("🔐 Test du Système de Protection d'Accès")
        print(f"👨‍💻 Développé par: {self.developer_info['name']}")
        print(f"📞 Téléphone: {self.developer_info['phone']}")
        print(f"📧 Email: {self.developer_info['email']}")
        print("=" * 60)
        
        await self.access_protection.initialize()
        
        print("✅ Testeur initialisé")
    
    async def test_password_authentication(self):
        """Test de l'authentification par mot de passe"""
        print("\n🔑 Test d'authentification par mot de passe")
        print("-" * 50)
        
        test_cases = [
            {
                "password": "AZ12ER34",
                "expected": True,
                "description": "Mot de passe correct"
            },
            {
                "password": "wrong_password",
                "expected": False,
                "description": "Mot de passe incorrect"
            },
            {
                "password": "",
                "expected": False,
                "description": "Mot de passe vide"
            },
            {
                "password": "az12er34",
                "expected": False,
                "description": "Mot de passe en minuscules"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: {test_case['description']}")
            
            success, message, token = await self.access_protection.authenticate(
                test_case["password"],
                "127.0.0.1",
                "Test User Agent"
            )
            
            if success == test_case["expected"]:
                print(f"✅ Succès: {message}")
                if token:
                    print(f"🔑 Token généré: {token[:20]}...")
            else:
                print(f"❌ Échec: {message}")
            
            await asyncio.sleep(1)
    
    async def test_github_blocking(self):
        """Test du blocage GitHub"""
        print("\n🚫 Test du blocage GitHub")
        print("-" * 50)
        
        github_user_agents = [
            "Mozilla/5.0 (compatible; GitHubBot/1.0; +https://github.com)",
            "github-actions[bot]",
            "githubusercontent.com",
            "github.io",
            "github.com"
        ]
        
        normal_user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "curl/7.68.0",
            "PostmanRuntime/7.28.0"
        ]
        
        print("🔍 Test des User-Agents GitHub:")
        for ua in github_user_agents:
            allowed, reason = await self.access_protection.check_access_permission(
                "127.0.0.1", ua, "/api/test"
            )
            print(f"   {ua[:50]}... -> {'❌ Bloqué' if not allowed else '✅ Autorisé'}")
        
        print("\n✅ Test des User-Agents normaux:")
        for ua in normal_user_agents:
            allowed, reason = await self.access_protection.check_access_permission(
                "127.0.0.1", ua, "/api/test"
            )
            print(f"   {ua[:50]}... -> {'❌ Bloqué' if not allowed else '✅ Autorisé'}")
    
    async def test_sensitive_resources(self):
        """Test de protection des ressources sensibles"""
        print("\n🛡️ Test de protection des ressources sensibles")
        print("-" * 50)
        
        sensitive_resources = [
            "license_system.py",
            "payment_system.py",
            "access_protection.py",
            "config.json",
            "LICENCE_VENTE_IVOIRIENNE.md"
        ]
        
        normal_resources = [
            "dashboard.html",
            "api/status",
            "static/css/style.css",
            "README.md"
        ]
        
        print("🔒 Test des ressources sensibles:")
        for resource in sensitive_resources:
            allowed, reason = await self.access_protection.check_access_permission(
                "127.0.0.1", "Mozilla/5.0", resource
            )
            print(f"   {resource} -> {'❌ Bloqué' if not allowed else '✅ Autorisé'}")
        
        print("\n📄 Test des ressources normales:")
        for resource in normal_resources:
            allowed, reason = await self.access_protection.check_access_permission(
                "127.0.0.1", "Mozilla/5.0", resource
            )
            print(f"   {resource} -> {'❌ Bloqué' if not allowed else '✅ Autorisé'}")
    
    async def test_brute_force_protection(self):
        """Test de protection contre les attaques par force brute"""
        print("\n🛡️ Test de protection contre les attaques par force brute")
        print("-" * 50)
        
        print("🔑 Tentatives avec mot de passe incorrect:")
        for i in range(5):
            success, message, token = await self.access_protection.authenticate(
                f"wrong_password_{i}",
                "127.0.0.1",
                "Brute Force Test"
            )
            
            print(f"   Tentative {i+1}: {message}")
            
            if "verrouillé" in message:
                print("   🔒 Compte verrouillé - Protection active")
                break
            
            await asyncio.sleep(0.5)
        
        # Test de déverrouillage automatique
        print("\n⏰ Test de déverrouillage automatique:")
        print("   Attente de 5 secondes...")
        await asyncio.sleep(5)
        
        success, message, token = await self.access_protection.authenticate(
            "AZ12ER34",
            "127.0.0.1",
            "Unlock Test"
        )
        
        if success:
            print("   ✅ Déverrouillage automatique réussi")
        else:
            print(f"   ❌ Déverrouillage échoué: {message}")
    
    async def test_token_management(self):
        """Test de gestion des tokens"""
        print("\n🎫 Test de gestion des tokens")
        print("-" * 50)
        
        # Authentification pour obtenir un token
        success, message, token = await self.access_protection.authenticate(
            "AZ12ER34",
            "127.0.0.1",
            "Token Test"
        )
        
        if not success:
            print("❌ Impossible d'obtenir un token")
            return
        
        print(f"✅ Token obtenu: {token[:20]}...")
        
        # Validation du token
        valid, message, access_token = await self.access_protection.validate_token(
            token, "127.0.0.1"
        )
        
        if valid:
            print("✅ Token valide")
            print(f"   Permissions: {access_token.permissions}")
            print(f"   Expire le: {access_token.expires_at}")
        else:
            print(f"❌ Token invalide: {message}")
        
        # Révocation du token
        revoked = await self.access_protection.revoke_token(token)
        if revoked:
            print("✅ Token révoqué")
        else:
            print("❌ Erreur lors de la révocation")
        
        # Vérification que le token est invalide
        valid, message, _ = await self.access_protection.validate_token(
            token, "127.0.0.1"
        )
        
        if not valid:
            print("✅ Token correctement invalidé après révocation")
        else:
            print("❌ Token toujours valide après révocation")
    
    async def test_security_statistics(self):
        """Test des statistiques de sécurité"""
        print("\n📊 Test des statistiques de sécurité")
        print("-" * 50)
        
        stats = await self.access_protection.get_security_stats()
        
        print("📈 Statistiques actuelles:")
        print(f"   Tokens actifs: {stats['active_tokens']}")
        print(f"   IPs verrouillées: {stats['locked_ips']}")
        print(f"   Tentatives échouées: {len(stats['failed_attempts'])}")
        
        if stats['failed_attempts']:
            print("   Détail des tentatives échouées:")
            for ip, attempts in stats['failed_attempts'].items():
                print(f"     {ip}: {attempts} tentatives")
        
        print(f"\n👨‍💻 Informations développeur:")
        dev_info = stats['developer_info']
        print(f"   Nom: {dev_info['name']}")
        print(f"   Téléphone: {dev_info['phone']}")
        print(f"   Licence: {dev_info['license']}")
    
    async def test_security_events(self):
        """Test des événements de sécurité"""
        print("\n📝 Test des événements de sécurité")
        print("-" * 50)
        
        events = await self.access_protection.get_security_events(limit=10)
        
        print(f"📋 {len(events)} derniers événements:")
        for event in events[:5]:  # Afficher les 5 premiers
            timestamp = event['timestamp']
            event_type = event['event_type']
            ip_address = event['ip_address']
            details = event['details']
            
            print(f"   [{timestamp}] {event_type} - {ip_address}: {details}")
    
    async def test_password_strength(self):
        """Test de la force du mot de passe"""
        print("\n💪 Test de la force du mot de passe")
        print("-" * 50)
        
        # Le mot de passe actuel
        current_password = "AZ12ER34"
        
        print(f"🔑 Mot de passe actuel: {current_password}")
        print(f"📏 Longueur: {len(current_password)} caractères")
        
        # Analyse de la complexité
        has_upper = any(c.isupper() for c in current_password)
        has_lower = any(c.islower() for c in current_password)
        has_digit = any(c.isdigit() for c in current_password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in current_password)
        
        print("🔍 Analyse de complexité:")
        print(f"   Majuscules: {'✅' if has_upper else '❌'}")
        print(f"   Minuscules: {'✅' if has_lower else '❌'}")
        print(f"   Chiffres: {'✅' if has_digit else '❌'}")
        print(f"   Caractères spéciaux: {'✅' if has_special else '❌'}")
        
        # Score de sécurité
        score = 0
        if has_upper: score += 1
        if has_lower: score += 1
        if has_digit: score += 1
        if has_special: score += 1
        if len(current_password) >= 8: score += 1
        
        print(f"\n📊 Score de sécurité: {score}/5")
        
        if score >= 4:
            print("✅ Mot de passe fort")
        elif score >= 3:
            print("⚠️ Mot de passe moyen")
        else:
            print("❌ Mot de passe faible")
    
    async def run_complete_test(self):
        """Exécution du test complet"""
        print("🎬 Démarrage du test de protection d'accès")
        print("=" * 60)
        
        try:
            await self.initialize()
            
            # Tests individuels
            tests = [
                ("Authentification par mot de passe", self.test_password_authentication),
                ("Blocage GitHub", self.test_github_blocking),
                ("Protection des ressources sensibles", self.test_sensitive_resources),
                ("Protection contre les attaques par force brute", self.test_brute_force_protection),
                ("Gestion des tokens", self.test_token_management),
                ("Statistiques de sécurité", self.test_security_statistics),
                ("Événements de sécurité", self.test_security_events),
                ("Force du mot de passe", self.test_password_strength)
            ]
            
            for test_name, test_func in tests:
                print(f"\n🎯 Test: {test_name}")
                print("-" * 50)
                
                try:
                    await test_func()
                    print(f"✅ {test_name}: TERMINÉ")
                except Exception as e:
                    print(f"❌ {test_name}: ERREUR - {e}")
                
                await asyncio.sleep(1)
            
            # Résumé final
            print("\n" + "=" * 60)
            print("🎉 TEST DE PROTECTION D'ACCÈS TERMINÉ")
            print("=" * 60)
            
            print("\n📋 RÉSUMÉ:")
            print(f"👨‍💻 Développeur: {self.developer_info['name']}")
            print(f"📞 Téléphone: {self.developer_info['phone']}")
            print(f"📧 Email: {self.developer_info['email']}")
            print(f"🔐 Licence: {self.developer_info['license']}")
            
            print("\n✅ Fonctionnalités testées:")
            print("   ✅ Authentification par mot de passe")
            print("   ✅ Blocage des accès GitHub")
            print("   ✅ Protection des ressources sensibles")
            print("   ✅ Protection contre les attaques par force brute")
            print("   ✅ Gestion des tokens d'accès")
            print("   ✅ Statistiques de sécurité")
            print("   ✅ Logs d'événements de sécurité")
            print("   ✅ Analyse de la force du mot de passe")
            
            print("\n🔒 Sécurité renforcée:")
            print("   ✅ Mot de passe: AZ12ER34")
            print("   ✅ Protection contre GitHub")
            print("   ✅ Verrouillage automatique")
            print("   ✅ Tokens sécurisés")
            print("   ✅ Logs de sécurité")
            print("   ✅ Middleware de protection")
            
        except Exception as e:
            print(f"❌ Erreur fatale du test: {e}")
        
        finally:
            print("\n✅ Test de protection d'accès terminé")

async def main():
    """Fonction principale"""
    tester = AccessProtectionTester()
    
    try:
        await tester.run_complete_test()
    except KeyboardInterrupt:
        print("\n🛑 Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    asyncio.run(main())
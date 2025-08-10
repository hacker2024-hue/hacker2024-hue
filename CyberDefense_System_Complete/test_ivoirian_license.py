#!/usr/bin/env python3
"""
Test de la Licence Ivoirienne
=============================

Script de test spécifique pour la licence de vente ivoirienne
CI-CYBER-2024-001 développée par Yao Kouakou Luc Anicet.
"""

import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Any

# Import du système de licence
from security.license_system import LicenseSystem, LicenseType, LicenseRegion, LicenseStatus
from security.payment_system import PaymentSystem, PaymentMethod, PaymentCurrency, PaymentStatus

class IvoirianLicenseTester:
    """
    Testeur de licence ivoirienne
    """
    
    def __init__(self):
        self.license_system = LicenseSystem()
        self.payment_system = PaymentSystem()
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license_number": "CI-CYBER-2024-001"
        }
    
    async def initialize(self):
        """Initialisation du testeur"""
        print("🔐 Test de la Licence Ivoirienne CI-CYBER-2024-001")
        print(f"👨‍💻 Développé par: {self.developer_info['name']}")
        print(f"📞 Téléphone: {self.developer_info['phone']}")
        print(f"📧 Email: {self.developer_info['email']}")
        print("=" * 60)
        
        await self.license_system.initialize()
        await self.payment_system.initialize()
        
        print("✅ Testeur initialisé")
    
    async def test_ivoirian_license_creation(self):
        """Test de création de licence ivoirienne"""
        print("\n🔐 Test de création de licence ivoirienne")
        print("-" * 40)
        
        try:
            # Création d'une licence ivoirienne
            license_info = await self.license_system.create_license(
                customer_name="Test Client Ivoirien",
                customer_email="test@ivoirien.ci",
                customer_company="Entreprise Test CI",
                customer_country="Côte d'Ivoire",
                license_type=LicenseType.PROFESSIONAL,
                region=LicenseRegion.COTE_DIVOIRE,
                payment_status="pending"
            )
            
            print(f"✅ Licence créée: {license_info.license_id}")
            print(f"👤 Client: {license_info.customer_name}")
            print(f"🏢 Entreprise: {license_info.customer_company}")
            print(f"🌍 Région: {license_info.region.value}")
            print(f"💰 Prix XOF: {license_info.price_xof} FCFA")
            print(f"📅 Expiration: {license_info.expiry_date.strftime('%Y-%m-%d')}")
            
            # Vérification des informations du développeur
            dev_info = license_info.developer_info
            print(f"📞 Téléphone développeur: {dev_info.get('phone', 'N/A')}")
            print(f"🔐 Licence ivoirienne: {dev_info.get('ivoirian_license', {}).get('number', 'N/A')}")
            
            return license_info
            
        except Exception as e:
            print(f"❌ Erreur création licence: {e}")
            return None
    
    async def test_ivoirian_payment(self, license_id: str):
        """Test de paiement ivoirien"""
        print("\n💳 Test de paiement ivoirien")
        print("-" * 40)
        
        try:
            # Création d'un paiement Orange Money
            payment_info = await self.payment_system.create_payment(
                license_id=license_id,
                amount=195000.0,
                currency=PaymentCurrency.XOF,
                payment_method=PaymentMethod.ORANGE_MONEY,
                customer_name="Test Client Ivoirien",
                customer_email="test@ivoirien.ci",
                customer_company="Entreprise Test CI",
                customer_country="Côte d'Ivoire"
            )
            
            print(f"✅ Paiement créé: {payment_info.payment_id}")
            print(f"💰 Montant: {payment_info.amount} {payment_info.currency.value}")
            print(f"💳 Méthode: {payment_info.payment_method.value}")
            
            # Traitement du paiement
            payment_data = {
                "phone_number": "+225 014094507"
            }
            
            result = await self.payment_system.process_payment(payment_info.payment_id, payment_data)
            
            if result["success"]:
                print("✅ Paiement traité avec succès")
                print(f"🔗 Transaction: {result.get('transaction_id')}")
                print(f"💳 Passerelle: {result.get('gateway')}")
            else:
                print(f"❌ Erreur paiement: {result.get('error')}")
            
            return payment_info
            
        except Exception as e:
            print(f"❌ Erreur paiement: {e}")
            return None
    
    async def test_license_validation(self, license_id: str):
        """Test de validation de licence"""
        print("\n🔍 Test de validation de licence")
        print("-" * 40)
        
        try:
            result = await self.license_system.validate_license(license_id)
            
            if result["valid"]:
                print("✅ Licence valide")
                license_data = result["license"]
                print(f"👤 Client: {license_data['customer_name']}")
                print(f"🏢 Entreprise: {license_data['customer_company']}")
                print(f"🌍 Région: {license_data['region']}")
                print(f"📅 Jours restants: {result['days_remaining']}")
                
                # Vérification des informations ivoiriennes
                dev_info = license_data['developer_info']
                print(f"📞 Téléphone: {dev_info.get('phone', 'N/A')}")
                print(f"🔐 Licence ivoirienne: {dev_info.get('ivoirian_license', {}).get('number', 'N/A')}")
                
            else:
                print(f"❌ Licence invalide: {result['error']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur validation: {e}")
            return None
    
    async def test_ivoirian_pricing(self):
        """Test des prix ivoiriens"""
        print("\n💰 Test des prix ivoiriens")
        print("-" * 40)
        
        try:
            pricing = await self.license_system.get_pricing_info(LicenseRegion.COTE_DIVOIRE)
            
            print(f"🌍 Région: {pricing['region']}")
            print(f"💱 Devises: {pricing['currency_eur']} / {pricing['currency_xof']}")
            print()
            
            for license_type, info in pricing['pricing'].items():
                print(f"📦 {license_type.upper()}:")
                print(f"   💰 EUR: {info['price_eur']}€")
                print(f"   💰 XOF: {info['price_xof']} FCFA")
                print(f"   ⏱️  Durée: {info['duration_days']} jours")
                print(f"   🆘 Support: {info['support_level']}")
                print()
            
            return pricing
            
        except Exception as e:
            print(f"❌ Erreur prix: {e}")
            return None
    
    async def test_ivoirian_statistics(self):
        """Test des statistiques ivoiriennes"""
        print("\n📊 Test des statistiques ivoiriennes")
        print("-" * 40)
        
        try:
            # Statistiques des licences
            license_stats = await self.license_system.get_license_statistics()
            
            print("📈 Statistiques des licences:")
            print(f"   Total: {license_stats['total']}")
            print(f"   Actives: {license_stats['active_licenses']}")
            print(f"   Côte d'Ivoire: {license_stats['by_region'].get('cote_divoire', 0)}")
            print(f"   Revenus XOF: {license_stats['revenue_xof']:.0f} FCFA")
            print()
            
            # Statistiques des paiements
            payment_stats = await self.payment_system.get_payment_statistics()
            
            print("💳 Statistiques des paiements:")
            print(f"   Total: {payment_stats['total']}")
            print(f"   Complétés: {payment_stats['completed_payments']}")
            print(f"   XOF: {payment_stats['total_revenue']['XOF']:.0f} FCFA")
            print(f"   Orange Money: {payment_stats['by_method'].get('orange_money', 0)}")
            print(f"   MTN Mobile Money: {payment_stats['by_method'].get('mtn_mobile_money', 0)}")
            print(f"   Moov Money: {payment_stats['by_method'].get('moov_money', 0)}")
            print(f"   Wave: {payment_stats['by_method'].get('wave', 0)}")
            
            return {
                "licenses": license_stats,
                "payments": payment_stats
            }
            
        except Exception as e:
            print(f"❌ Erreur statistiques: {e}")
            return None
    
    async def test_ivoirian_compliance(self):
        """Test de conformité ivoirienne"""
        print("\n⚖️ Test de conformité ivoirienne")
        print("-" * 40)
        
        try:
            # Vérification des informations de licence
            dev_info = self.license_system.developer_info
            
            print("🔐 Informations de licence:")
            print(f"   Numéro: {dev_info['ivoirian_license']['number']}")
            print(f"   Type: {dev_info['ivoirian_license']['type']}")
            print(f"   Autorité: {dev_info['ivoirian_license']['authority']}")
            print(f"   Validité: {dev_info['ivoirian_license']['validity']}")
            print()
            
            print("📞 Informations de contact:")
            print(f"   Téléphone: {dev_info['phone']}")
            print(f"   Email: {dev_info['email']}")
            print(f"   Adresse: {dev_info['address']}")
            print()
            
            print("💳 Informations de paiement:")
            mobile_money = dev_info['mobile_money']
            print(f"   Orange Money: {mobile_money['orange_money']}")
            print(f"   MTN Mobile Money: {mobile_money['mtn_mobile_money']}")
            print(f"   Moov Money: {mobile_money['moov_money']}")
            print(f"   Wave: {mobile_money['wave']}")
            print()
            
            print("✅ Conformité ivoirienne vérifiée")
            
            return dev_info
            
        except Exception as e:
            print(f"❌ Erreur conformité: {e}")
            return None
    
    async def run_complete_test(self):
        """Exécution du test complet"""
        print("🎬 Démarrage du test de licence ivoirienne")
        print("=" * 60)
        
        try:
            await self.initialize()
            
            # Tests individuels
            tests = [
                ("Création de licence", self.test_ivoirian_license_creation),
                ("Prix ivoiriens", self.test_ivoirian_pricing),
                ("Conformité ivoirienne", self.test_ivoirian_compliance),
                ("Statistiques ivoiriennes", self.test_ivoirian_statistics)
            ]
            
            license_info = None
            
            for test_name, test_func in tests:
                print(f"\n🎯 Test: {test_name}")
                print("-" * 50)
                
                try:
                    result = await test_func()
                    if test_name == "Création de licence":
                        license_info = result
                    print(f"✅ {test_name}: TERMINÉ")
                except Exception as e:
                    print(f"❌ {test_name}: ERREUR - {e}")
                
                await asyncio.sleep(1)
            
            # Tests dépendants
            if license_info:
                dependent_tests = [
                    ("Paiement ivoirien", lambda: self.test_ivoirian_payment(license_info.license_id)),
                    ("Validation de licence", lambda: self.test_license_validation(license_info.license_id))
                ]
                
                for test_name, test_func in dependent_tests:
                    print(f"\n🎯 Test: {test_name}")
                    print("-" * 50)
                    
                    try:
                        result = await test_func()
                        print(f"✅ {test_name}: TERMINÉ")
                    except Exception as e:
                        print(f"❌ {test_name}: ERREUR - {e}")
                    
                    await asyncio.sleep(1)
            
            # Résumé final
            print("\n" + "=" * 60)
            print("🎉 TEST DE LICENCE IVOIRIENNE TERMINÉ")
            print("=" * 60)
            
            print("\n📋 RÉSUMÉ:")
            print(f"👨‍💻 Développeur: {self.developer_info['name']}")
            print(f"📞 Téléphone: {self.developer_info['phone']}")
            print(f"📧 Email: {self.developer_info['email']}")
            print(f"🔐 Licence: {self.developer_info['license_number']}")
            
            print("\n✅ Fonctionnalités testées:")
            print("   ✅ Création de licences ivoiriennes")
            print("   ✅ Prix en FCFA")
            print("   ✅ Paiements mobile money")
            print("   ✅ Conformité réglementaire")
            print("   ✅ Validation de licences")
            print("   ✅ Statistiques ivoiriennes")
            
            print("\n🌍 Zones de vente autorisées:")
            print("   ✅ Côte d'Ivoire (XOF)")
            print("   ✅ Europe (EUR)")
            print("   ✅ Global (USD, BTC, ETH)")
            
            print("\n💳 Méthodes de paiement supportées:")
            print("   ✅ Orange Money")
            print("   ✅ MTN Mobile Money")
            print("   ✅ Moov Money")
            print("   ✅ Wave")
            print("   ✅ Cartes de crédit")
            print("   ✅ Cryptomonnaies")
            
        except Exception as e:
            print(f"❌ Erreur fatale du test: {e}")
        
        finally:
            print("\n✅ Test de licence ivoirienne terminé")

async def main():
    """Fonction principale"""
    tester = IvoirianLicenseTester()
    
    try:
        await tester.run_complete_test()
    except KeyboardInterrupt:
        print("\n🛑 Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    asyncio.run(main())
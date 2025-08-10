#!/usr/bin/env python3
"""
Gestionnaire de Licences Commerciales
=====================================

Gestionnaire de licences pour l'Europe et la Côte d'Ivoire
développé par Yao Kouakou Luc Anicet.
"""

import asyncio
import json
import sys
import argparse
from datetime import datetime, timedelta
from typing import Dict, Any
import aiohttp

# Import du système de licence
from security.license_system import LicenseSystem, LicenseType, LicenseRegion, LicenseStatus
from security.payment_system import PaymentSystem, PaymentMethod, PaymentCurrency, PaymentStatus

class LicenseManager:
    """
    Gestionnaire de licences commerciales
    """
    
    def __init__(self):
        self.license_system = LicenseSystem()
        self.payment_system = PaymentSystem()
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "company": "CyberDefense Solutions",
            "email": "hackerduckman89@gmail.com",
            "secondary_email": "yao.kouakou.dev@gmail.com",
            "phone": "+225 014094507",
            "address": "Abidjan, Côte d'Ivoire",
            "website": "https://cyberdefense-solutions.com",
            "ivoirian_license": {
                "number": "CI-CYBER-2024-001",
                "type": "Licence de Vente de Logiciels de Sécurité",
                "issued_date": "2024-01-15",
                "expiry_date": "2029-01-15",
                "authority": "Ministère du Commerce et de l'Industrie de Côte d'Ivoire",
                "category": "Logiciels de Cybersécurité",
                "validity": "5 ans"
            }
        }
    
    async def initialize(self):
        """Initialisation du gestionnaire"""
        print("🔐 Initialisation du Gestionnaire de Licences Commerciales")
        print(f"👨‍💻 Développé par: {self.developer_info['name']}")
        print(f"📧 Contact: {self.developer_info['email']}")
        print(f"📞 Téléphone: {self.developer_info['phone']}")
        print(f"🔐 Licence Ivoirienne: {self.developer_info['ivoirian_license']['number']}")
        print("=" * 60)
        
        await self.license_system.initialize()
        await self.payment_system.initialize()
        
        print("✅ Gestionnaire initialisé")
    
    async def create_license(self, args):
        """Création d'une nouvelle licence"""
        try:
            print(f"🔐 Création de licence {args.type} pour {args.region}")
            
            license_info = await self.license_system.create_license(
                customer_name=args.customer_name,
                customer_email=args.customer_email,
                customer_company=args.customer_company,
                customer_country=args.customer_country,
                license_type=LicenseType(args.type),
                region=LicenseRegion(args.region),
                payment_status="pending"
            )
            
            print(f"✅ Licence créée: {license_info.license_id}")
            print(f"📧 Client: {license_info.customer_name} ({license_info.customer_email})")
            print(f"🏢 Entreprise: {license_info.customer_company}")
            print(f"🌍 Région: {license_info.region.value}")
            print(f"💰 Prix EUR: {license_info.price_eur}€")
            print(f"💰 Prix XOF: {license_info.price_xof} FCFA")
            print(f"📅 Expiration: {license_info.expiry_date.strftime('%Y-%m-%d')}")
            
            # Génération de la clé de licence
            license_key = self.license_system.generate_license_key(license_info)
            print(f"🔑 Clé de licence: {license_key}")
            
            # Génération du QR code
            qr_code = self.license_system.generate_license_qr(license_info)
            if qr_code:
                print("📱 QR Code généré")
            
            return license_info
            
        except Exception as e:
            print(f"❌ Erreur création licence: {e}")
            return None
    
    async def validate_license(self, license_id: str):
        """Validation d'une licence"""
        try:
            print(f"🔍 Validation de la licence: {license_id}")
            
            result = await self.license_system.validate_license(license_id)
            
            if result["valid"]:
                print("✅ Licence valide")
                license_data = result["license"]
                print(f"👤 Client: {license_data['customer_name']}")
                print(f"🏢 Entreprise: {license_data['customer_company']}")
                print(f"🌍 Région: {license_data['region']}")
                print(f"📅 Jours restants: {result['days_remaining']}")
                print(f"🔧 Fonctionnalités: {', '.join([k for k, v in result['features'].items() if v])}")
            else:
                print(f"❌ Licence invalide: {result['error']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur validation licence: {e}")
            return None
    
    async def list_licenses(self):
        """Liste des licences"""
        try:
            print("📋 Liste des licences:")
            print("-" * 60)
            
            licenses = list(self.license_system.licenses.values())
            
            if not licenses:
                print("Aucune licence trouvée")
                return
            
            for license_info in licenses:
                print(f"🔐 {license_info.license_id}")
                print(f"   👤 {license_info.customer_name} ({license_info.customer_email})")
                print(f"   🏢 {license_info.customer_company}")
                print(f"   🌍 {license_info.region.value} - {license_info.license_type.value}")
                print(f"   📊 {license_info.status.value}")
                print(f"   💰 {license_info.price_eur}€ / {license_info.price_xof} FCFA")
                print(f"   📅 Expire: {license_info.expiry_date.strftime('%Y-%m-%d')}")
                print()
            
        except Exception as e:
            print(f"❌ Erreur liste licences: {e}")
    
    async def get_statistics(self):
        """Statistiques des licences"""
        try:
            print("📊 Statistiques des licences:")
            print("-" * 60)
            
            stats = await self.license_system.get_license_statistics()
            
            print(f"📈 Total: {stats['total']} licences")
            print(f"✅ Actives: {stats['active_licenses']}")
            print(f"❌ Expirées: {stats['expired_licenses']}")
            print()
            
            print("💰 Revenus:")
            print(f"   EUR: {stats['revenue_eur']:.2f}€")
            print(f"   XOF: {stats['revenue_xof']:.0f} FCFA")
            print()
            
            print("🌍 Par région:")
            for region, count in stats['by_region'].items():
                print(f"   {region}: {count}")
            print()
            
            print("📦 Par type:")
            for license_type, count in stats['by_type'].items():
                print(f"   {license_type}: {count}")
            
        except Exception as e:
            print(f"❌ Erreur statistiques: {e}")
    
    async def get_pricing(self, region: str):
        """Informations de prix"""
        try:
            print(f"💰 Prix pour la région: {region}")
            print("-" * 60)
            
            pricing = await self.license_system.get_pricing_info(LicenseRegion(region))
            
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
            
        except Exception as e:
            print(f"❌ Erreur prix: {e}")
    
    async def create_payment(self, args):
        """Création d'un paiement"""
        try:
            print(f"💳 Création de paiement {args.method} pour {args.amount} {args.currency}")
            
            payment_info = await self.payment_system.create_payment(
                license_id=args.license_id,
                amount=float(args.amount),
                currency=PaymentCurrency(args.currency),
                payment_method=PaymentMethod(args.method),
                customer_name=args.customer_name,
                customer_email=args.customer_email,
                customer_company=args.customer_company,
                customer_country=args.customer_country
            )
            
            print(f"✅ Paiement créé: {payment_info.payment_id}")
            print(f"💰 Montant: {payment_info.amount} {payment_info.currency.value}")
            print(f"💳 Méthode: {payment_info.payment_method.value}")
            print(f"📊 Statut: {payment_info.status.value}")
            
            # Génération du QR code
            qr_code = self.payment_system.generate_payment_qr(payment_info)
            if qr_code:
                print("📱 QR Code de paiement généré")
            
            return payment_info
            
        except Exception as e:
            print(f"❌ Erreur création paiement: {e}")
            return None
    
    async def process_payment(self, payment_id: str, payment_data: Dict[str, Any]):
        """Traitement d'un paiement"""
        try:
            print(f"💳 Traitement du paiement: {payment_id}")
            
            result = await self.payment_system.process_payment(payment_id, payment_data)
            
            if result["success"]:
                print("✅ Paiement traité avec succès")
                print(f"🔗 Transaction: {result.get('transaction_id')}")
                print(f"💳 Passerelle: {result.get('gateway')}")
            else:
                print(f"❌ Erreur paiement: {result.get('error')}")
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur traitement paiement: {e}")
            return None
    
    async def get_payment_statistics(self):
        """Statistiques des paiements"""
        try:
            print("📊 Statistiques des paiements:")
            print("-" * 60)
            
            stats = await self.payment_system.get_payment_statistics()
            
            print(f"📈 Total: {stats['total']} paiements")
            print(f"✅ Complétés: {stats['completed_payments']}")
            print(f"❌ Échoués: {stats['failed_payments']}")
            print(f"⏳ En attente: {stats['pending_payments']}")
            print()
            
            print("💰 Revenus totaux:")
            for currency, amount in stats['total_revenue'].items():
                if amount > 0:
                    print(f"   {currency}: {amount:.2f}")
            print()
            
            print("💳 Par méthode:")
            for method, count in stats['by_method'].items():
                if count > 0:
                    print(f"   {method}: {count}")
            
        except Exception as e:
            print(f"❌ Erreur statistiques paiements: {e}")

async def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Gestionnaire de Licences Commerciales")
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande create-license
    create_parser = subparsers.add_parser('create-license', help='Créer une nouvelle licence')
    create_parser.add_argument('--type', required=True, choices=['trial', 'basic', 'professional', 'enterprise', 'government', 'military'])
    create_parser.add_argument('--region', required=True, choices=['europe', 'cote_divoire', 'global'])
    create_parser.add_argument('--customer-name', required=True)
    create_parser.add_argument('--customer-email', required=True)
    create_parser.add_argument('--customer-company', required=True)
    create_parser.add_argument('--customer-country', required=True)
    
    # Commande validate-license
    validate_parser = subparsers.add_parser('validate-license', help='Valider une licence')
    validate_parser.add_argument('--license-id', required=True)
    
    # Commande list-licenses
    subparsers.add_parser('list-licenses', help='Lister toutes les licences')
    
    # Commande statistics
    subparsers.add_parser('statistics', help='Statistiques des licences')
    
    # Commande pricing
    pricing_parser = subparsers.add_parser('pricing', help='Informations de prix')
    pricing_parser.add_argument('--region', required=True, choices=['europe', 'cote_divoire', 'global'])
    
    # Commande create-payment
    payment_parser = subparsers.add_parser('create-payment', help='Créer un paiement')
    payment_parser.add_argument('--license-id', required=True)
    payment_parser.add_argument('--amount', required=True)
    payment_parser.add_argument('--currency', required=True, choices=['EUR', 'XOF', 'USD', 'BTC', 'ETH'])
    payment_parser.add_argument('--method', required=True, choices=['credit_card', 'orange_money', 'mtn_mobile_money', 'moov_money', 'wave', 'crypto'])
    payment_parser.add_argument('--customer-name', required=True)
    payment_parser.add_argument('--customer-email', required=True)
    payment_parser.add_argument('--customer-company', required=True)
    payment_parser.add_argument('--customer-country', required=True)
    
    # Commande payment-statistics
    subparsers.add_parser('payment-statistics', help='Statistiques des paiements')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Création du gestionnaire
    manager = LicenseManager()
    await manager.initialize()
    
    try:
        if args.command == 'create-license':
            await manager.create_license(args)
        elif args.command == 'validate-license':
            await manager.validate_license(args.license_id)
        elif args.command == 'list-licenses':
            await manager.list_licenses()
        elif args.command == 'statistics':
            await manager.get_statistics()
        elif args.command == 'pricing':
            await manager.get_pricing(args.region)
        elif args.command == 'create-payment':
            await manager.create_payment(args)
        elif args.command == 'payment-statistics':
            await manager.get_payment_statistics()
        else:
            print(f"❌ Commande inconnue: {args.command}")
    
    except KeyboardInterrupt:
        print("\n🛑 Opération interrompue")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")

if __name__ == "__main__":
    asyncio.run(main())
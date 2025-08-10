"""
Système de Paiement Avancé
==========================

Système de paiement pour l'Europe et la Côte d'Ivoire
avec support de multiples méthodes de paiement.
"""

import asyncio
import json
import logging
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import redis.asyncio as redis
import uuid
import qrcode
from io import BytesIO
import aiohttp
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentMethod(Enum):
    """Méthodes de paiement"""
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    ORANGE_MONEY = "orange_money"
    MTN_MOBILE_MONEY = "mtn_mobile_money"
    MOOV_MONEY = "moov_money"
    WAVE = "wave"
    CRYPTO = "crypto"

class PaymentStatus(Enum):
    """Statuts de paiement"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentCurrency(Enum):
    """Devises de paiement"""
    EUR = "EUR"
    XOF = "XOF"
    USD = "USD"
    BTC = "BTC"
    ETH = "ETH"

@dataclass
class PaymentInfo:
    """Informations de paiement"""
    payment_id: str
    license_id: str
    amount: float
    currency: PaymentCurrency
    payment_method: PaymentMethod
    status: PaymentStatus
    customer_name: str
    customer_email: str
    customer_company: str
    customer_country: str
    created_date: datetime
    completed_date: Optional[datetime]
    transaction_id: Optional[str]
    payment_details: Dict[str, Any]
    developer_info: Dict[str, Any]

@dataclass
class PaymentGateway:
    """Configuration de passerelle de paiement"""
    name: str
    enabled: bool
    api_key: str
    secret_key: str
    webhook_url: str
    supported_currencies: List[PaymentCurrency]
    supported_methods: List[PaymentMethod]

class PaymentSystem:
    """
    Système de paiement avancé
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.payments: Dict[str, PaymentInfo] = {}
        self.gateways: Dict[str, PaymentGateway] = {}
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "company": "CyberDefense Solutions",
            "email": "hackerduckman89@gmail.com",
            "secondary_email": "yao.kouakou.dev@gmail.com",
            "phone": "+225 014094507",
            "address": "Abidjan, Côte d'Ivoire",
            "website": "https://cyberdefense-solutions.com",
            "tax_id": "CI123456789",
            "eu_vat": "EU987654321",
            "ivoirian_license": {
                "number": "CI-CYBER-2024-001",
                "type": "Licence de Vente de Logiciels de Sécurité",
                "issued_date": "2024-01-15",
                "expiry_date": "2029-01-15",
                "authority": "Ministère du Commerce et de l'Industrie de Côte d'Ivoire",
                "category": "Logiciels de Cybersécurité",
                "validity": "5 ans"
            },
            "bank_info": {
                "bank_name": "Banque Atlantique",
                "account_name": "CyberDefense Solutions",
                "account_number": "CI123456789",
                "swift_code": "ATLCCIAB",
                "iban": "CI1234567890123456789012"
            },
            "mobile_money": {
                "orange_money": "+225 014094507",
                "mtn_mobile_money": "+225 014094507",
                "moov_money": "+225 014094507",
                "wave": "wave@cyberdefense-solutions.com"
            }
        }
        
        # Configuration des passerelles de paiement
        self._setup_payment_gateways()
        
        # Configuration des taux de change
        self.exchange_rates = {
            "EUR_TO_XOF": 650.0,
            "USD_TO_XOF": 600.0,
            "XOF_TO_EUR": 1/650.0,
            "XOF_TO_USD": 1/600.0
        }
    
    def _setup_payment_gateways(self):
        """Configuration des passerelles de paiement"""
        
        # Stripe (Europe)
        self.gateways["stripe"] = PaymentGateway(
            name="Stripe",
            enabled=True,
            api_key="sk_test_...",  # À configurer
            secret_key="sk_test_...",  # À configurer
            webhook_url="https://cyberdefense-solutions.com/webhooks/stripe",
            supported_currencies=[PaymentCurrency.EUR, PaymentCurrency.USD],
            supported_methods=[PaymentMethod.CREDIT_CARD, PaymentMethod.PAYPAL]
        )
        
        # Orange Money (Côte d'Ivoire)
        self.gateways["orange_money"] = PaymentGateway(
            name="Orange Money",
            enabled=True,
            api_key="om_api_key_...",  # À configurer
            secret_key="om_secret_...",  # À configurer
            webhook_url="https://cyberdefense-solutions.com/webhooks/orange-money",
            supported_currencies=[PaymentCurrency.XOF],
            supported_methods=[PaymentMethod.ORANGE_MONEY]
        )
        
        # MTN Mobile Money (Côte d'Ivoire)
        self.gateways["mtn_mobile_money"] = PaymentGateway(
            name="MTN Mobile Money",
            enabled=True,
            api_key="mtn_api_key_...",  # À configurer
            secret_key="mtn_secret_...",  # À configurer
            webhook_url="https://cyberdefense-solutions.com/webhooks/mtn-mobile-money",
            supported_currencies=[PaymentCurrency.XOF],
            supported_methods=[PaymentMethod.MTN_MOBILE_MONEY]
        )
        
        # Moov Money (Côte d'Ivoire)
        self.gateways["moov_money"] = PaymentGateway(
            name="Moov Money",
            enabled=True,
            api_key="moov_api_key_...",  # À configurer
            secret_key="moov_secret_...",  # À configurer
            webhook_url="https://cyberdefense-solutions.com/webhooks/moov-money",
            supported_currencies=[PaymentCurrency.XOF],
            supported_methods=[PaymentMethod.MOOV_MONEY]
        )
        
        # Wave (Côte d'Ivoire)
        self.gateways["wave"] = PaymentGateway(
            name="Wave",
            enabled=True,
            api_key="wave_api_key_...",  # À configurer
            secret_key="wave_secret_...",  # À configurer
            webhook_url="https://cyberdefense-solutions.com/webhooks/wave",
            supported_currencies=[PaymentCurrency.XOF],
            supported_methods=[PaymentMethod.WAVE]
        )
        
        # Crypto (Global)
        self.gateways["crypto"] = PaymentGateway(
            name="Crypto",
            enabled=True,
            api_key="crypto_api_key_...",  # À configurer
            secret_key="crypto_secret_...",  # À configurer
            webhook_url="https://cyberdefense-solutions.com/webhooks/crypto",
            supported_currencies=[PaymentCurrency.BTC, PaymentCurrency.ETH],
            supported_methods=[PaymentMethod.CRYPTO]
        )
    
    async def initialize(self):
        """Initialisation du système de paiement"""
        logger.info("💳 Initialisation du système de paiement")
        
        # Chargement des paiements existants
        await self._load_existing_payments()
        
        # Démarrage des tâches en arrière-plan
        asyncio.create_task(self._payment_processor())
        asyncio.create_task(self._payment_cleanup())
        
        logger.info("✅ Système de paiement initialisé")
    
    async def _load_existing_payments(self):
        """Chargement des paiements existants"""
        try:
            keys = await self.redis.keys("payment:*")
            for key in keys:
                data = await self.redis.hgetall(key)
                if data:
                    payment_info = self._deserialize_payment(data)
                    self.payments[payment_info.payment_id] = payment_info
        except Exception as e:
            logger.error(f"Erreur chargement paiements: {e}")
    
    async def create_payment(self,
                           license_id: str,
                           amount: float,
                           currency: PaymentCurrency,
                           payment_method: PaymentMethod,
                           customer_name: str,
                           customer_email: str,
                           customer_company: str,
                           customer_country: str) -> PaymentInfo:
        """Création d'un nouveau paiement"""
        try:
            # Génération de l'ID de paiement
            payment_id = f"PAY_{payment_method.value.upper()}_{uuid.uuid4().hex[:8]}"
            
            # Création du paiement
            payment_info = PaymentInfo(
                payment_id=payment_id,
                license_id=license_id,
                amount=amount,
                currency=currency,
                payment_method=payment_method,
                status=PaymentStatus.PENDING,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_company=customer_company,
                customer_country=customer_country,
                created_date=datetime.now(),
                completed_date=None,
                transaction_id=None,
                payment_details={},
                developer_info=self.developer_info
            )
            
            # Stockage du paiement
            self.payments[payment_id] = payment_info
            await self._save_payment_to_redis(payment_info)
            
            logger.info(f"💳 Paiement créé: {payment_id} - {amount} {currency.value}")
            
            return payment_info
            
        except Exception as e:
            logger.error(f"Erreur création paiement: {e}")
            raise
    
    async def process_payment(self, payment_id: str, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement d'un paiement"""
        try:
            if payment_id not in self.payments:
                return {"success": False, "error": "Paiement non trouvé"}
            
            payment_info = self.payments[payment_id]
            
            # Mise à jour du statut
            payment_info.status = PaymentStatus.PROCESSING
            await self._save_payment_to_redis(payment_info)
            
            # Traitement selon la méthode de paiement
            if payment_info.payment_method == PaymentMethod.CREDIT_CARD:
                result = await self._process_credit_card_payment(payment_info, payment_data)
            elif payment_info.payment_method == PaymentMethod.ORANGE_MONEY:
                result = await self._process_orange_money_payment(payment_info, payment_data)
            elif payment_info.payment_method == PaymentMethod.MTN_MOBILE_MONEY:
                result = await self._process_mtn_mobile_money_payment(payment_info, payment_data)
            elif payment_info.payment_method == PaymentMethod.MOOV_MONEY:
                result = await self._process_moov_money_payment(payment_info, payment_data)
            elif payment_info.payment_method == PaymentMethod.WAVE:
                result = await self._process_wave_payment(payment_info, payment_data)
            elif payment_info.payment_method == PaymentMethod.CRYPTO:
                result = await self._process_crypto_payment(payment_info, payment_data)
            else:
                result = {"success": False, "error": "Méthode de paiement non supportée"}
            
            # Mise à jour du statut final
            if result["success"]:
                payment_info.status = PaymentStatus.COMPLETED
                payment_info.completed_date = datetime.now()
                payment_info.transaction_id = result.get("transaction_id")
                payment_info.payment_details = payment_data
            else:
                payment_info.status = PaymentStatus.FAILED
                payment_info.payment_details = {"error": result.get("error")}
            
            await self._save_payment_to_redis(payment_info)
            
            # Envoi de confirmation par email
            if result["success"]:
                await self._send_payment_confirmation(payment_info)
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur traitement paiement: {e}")
            return {"success": False, "error": str(e)}
    
    async def _process_credit_card_payment(self, payment_info: PaymentInfo, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement de paiement par carte de crédit"""
        try:
            # Simulation de traitement Stripe
            # En production, utiliser l'API Stripe réelle
            
            # Vérification des données de carte
            card_number = payment_data.get("card_number", "")
            expiry_month = payment_data.get("expiry_month", "")
            expiry_year = payment_data.get("expiry_year", "")
            cvv = payment_data.get("cvv", "")
            
            if not all([card_number, expiry_month, expiry_year, cvv]):
                return {"success": False, "error": "Données de carte incomplètes"}
            
            # Simulation de validation
            if len(card_number) < 13 or len(card_number) > 19:
                return {"success": False, "error": "Numéro de carte invalide"}
            
            if len(cvv) < 3 or len(cvv) > 4:
                return {"success": False, "error": "CVV invalide"}
            
            # Simulation de traitement réussi
            transaction_id = f"STRIPE_{uuid.uuid4().hex[:16]}"
            
            logger.info(f"💳 Paiement carte de crédit traité: {transaction_id}")
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "gateway": "Stripe",
                "amount": payment_info.amount,
                "currency": payment_info.currency.value
            }
            
        except Exception as e:
            logger.error(f"Erreur paiement carte de crédit: {e}")
            return {"success": False, "error": str(e)}
    
    async def _process_orange_money_payment(self, payment_info: PaymentInfo, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement de paiement Orange Money"""
        try:
            phone_number = payment_data.get("phone_number", "")
            
            if not phone_number:
                return {"success": False, "error": "Numéro de téléphone requis"}
            
            # Simulation de traitement Orange Money
            transaction_id = f"ORANGE_{uuid.uuid4().hex[:16]}"
            
            logger.info(f"📱 Paiement Orange Money traité: {transaction_id}")
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "gateway": "Orange Money",
                "amount": payment_info.amount,
                "currency": payment_info.currency.value,
                "phone_number": phone_number
            }
            
        except Exception as e:
            logger.error(f"Erreur paiement Orange Money: {e}")
            return {"success": False, "error": str(e)}
    
    async def _process_mtn_mobile_money_payment(self, payment_info: PaymentInfo, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement de paiement MTN Mobile Money"""
        try:
            phone_number = payment_data.get("phone_number", "")
            
            if not phone_number:
                return {"success": False, "error": "Numéro de téléphone requis"}
            
            # Simulation de traitement MTN Mobile Money
            transaction_id = f"MTN_{uuid.uuid4().hex[:16]}"
            
            logger.info(f"📱 Paiement MTN Mobile Money traité: {transaction_id}")
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "gateway": "MTN Mobile Money",
                "amount": payment_info.amount,
                "currency": payment_info.currency.value,
                "phone_number": phone_number
            }
            
        except Exception as e:
            logger.error(f"Erreur paiement MTN Mobile Money: {e}")
            return {"success": False, "error": str(e)}
    
    async def _process_moov_money_payment(self, payment_info: PaymentInfo, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement de paiement Moov Money"""
        try:
            phone_number = payment_data.get("phone_number", "")
            
            if not phone_number:
                return {"success": False, "error": "Numéro de téléphone requis"}
            
            # Simulation de traitement Moov Money
            transaction_id = f"MOOV_{uuid.uuid4().hex[:16]}"
            
            logger.info(f"📱 Paiement Moov Money traité: {transaction_id}")
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "gateway": "Moov Money",
                "amount": payment_info.amount,
                "currency": payment_info.currency.value,
                "phone_number": phone_number
            }
            
        except Exception as e:
            logger.error(f"Erreur paiement Moov Money: {e}")
            return {"success": False, "error": str(e)}
    
    async def _process_wave_payment(self, payment_info: PaymentInfo, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement de paiement Wave"""
        try:
            phone_number = payment_data.get("phone_number", "")
            
            if not phone_number:
                return {"success": False, "error": "Numéro de téléphone requis"}
            
            # Simulation de traitement Wave
            transaction_id = f"WAVE_{uuid.uuid4().hex[:16]}"
            
            logger.info(f"📱 Paiement Wave traité: {transaction_id}")
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "gateway": "Wave",
                "amount": payment_info.amount,
                "currency": payment_info.currency.value,
                "phone_number": phone_number
            }
            
        except Exception as e:
            logger.error(f"Erreur paiement Wave: {e}")
            return {"success": False, "error": str(e)}
    
    async def _process_crypto_payment(self, payment_info: PaymentInfo, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Traitement de paiement crypto"""
        try:
            wallet_address = payment_data.get("wallet_address", "")
            crypto_amount = payment_data.get("crypto_amount", 0)
            
            if not wallet_address or crypto_amount <= 0:
                return {"success": False, "error": "Adresse de portefeuille et montant requis"}
            
            # Simulation de traitement crypto
            transaction_id = f"CRYPTO_{uuid.uuid4().hex[:16]}"
            
            logger.info(f"₿ Paiement crypto traité: {transaction_id}")
            
            return {
                "success": True,
                "transaction_id": transaction_id,
                "gateway": "Crypto",
                "amount": payment_info.amount,
                "currency": payment_info.currency.value,
                "wallet_address": wallet_address,
                "crypto_amount": crypto_amount
            }
            
        except Exception as e:
            logger.error(f"Erreur paiement crypto: {e}")
            return {"success": False, "error": str(e)}
    
    async def _send_payment_confirmation(self, payment_info: PaymentInfo):
        """Envoi de confirmation de paiement par email"""
        try:
            # Création du message
            msg = MIMEMultipart()
            msg['From'] = f"CyberDefense Solutions <{self.developer_info['email']}>"
            msg['To'] = payment_info.customer_email
            msg['Subject'] = f"Confirmation de Paiement - {payment_info.payment_id}"
            
            # Corps du message
            body = f"""
            🎉 Confirmation de Paiement
            
            Bonjour {payment_info.customer_name},
            
            Nous confirmons la réception de votre paiement.
            
            Détails du paiement:
            - ID Paiement: {payment_info.payment_id}
            - Montant: {payment_info.amount} {payment_info.currency.value}
            - Méthode: {payment_info.payment_method.value}
            - Date: {payment_info.completed_date.strftime('%Y-%m-%d %H:%M:%S')}
            - Transaction: {payment_info.transaction_id}
            
            Votre licence sera activée dans les plus brefs délais.
            
            ---
            CyberDefense Solutions
            Développé par: {self.developer_info['name']}
            Contact: {self.developer_info['email']}
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Envoi (simulation)
            logger.info(f"📧 Confirmation de paiement envoyée à {payment_info.customer_email}")
            
        except Exception as e:
            logger.error(f"Erreur envoi confirmation paiement: {e}")
    
    def generate_payment_qr(self, payment_info: PaymentInfo) -> str:
        """Génération d'un QR code pour le paiement"""
        try:
            # Données du QR code
            qr_data = {
                "payment_id": payment_info.payment_id,
                "amount": payment_info.amount,
                "currency": payment_info.currency.value,
                "method": payment_info.payment_method.value,
                "customer": payment_info.customer_name,
                "company": payment_info.customer_company,
                "developer": self.developer_info["name"],
                "contact": self.developer_info["email"]
            }
            
            # Création du QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(json.dumps(qr_data))
            qr.make(fit=True)
            
            # Génération de l'image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Conversion en base64
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"Erreur génération QR paiement: {e}")
            return ""
    
    def convert_currency(self, amount: float, from_currency: PaymentCurrency, to_currency: PaymentCurrency) -> float:
        """Conversion de devise"""
        try:
            if from_currency == to_currency:
                return amount
            
            if from_currency == PaymentCurrency.EUR and to_currency == PaymentCurrency.XOF:
                return amount * self.exchange_rates["EUR_TO_XOF"]
            elif from_currency == PaymentCurrency.XOF and to_currency == PaymentCurrency.EUR:
                return amount * self.exchange_rates["XOF_TO_EUR"]
            elif from_currency == PaymentCurrency.USD and to_currency == PaymentCurrency.XOF:
                return amount * self.exchange_rates["USD_TO_XOF"]
            elif from_currency == PaymentCurrency.XOF and to_currency == PaymentCurrency.USD:
                return amount * self.exchange_rates["XOF_TO_USD"]
            else:
                return amount  # Pas de conversion disponible
            
        except Exception as e:
            logger.error(f"Erreur conversion devise: {e}")
            return amount
    
    async def get_payment_info(self, payment_id: str) -> Optional[PaymentInfo]:
        """Récupération des informations de paiement"""
        return self.payments.get(payment_id)
    
    async def get_payment_statistics(self) -> Dict[str, Any]:
        """Statistiques des paiements"""
        payments = list(self.payments.values())
        
        stats = {
            "total": len(payments),
            "by_status": {},
            "by_method": {},
            "by_currency": {},
            "total_revenue": {
                "EUR": sum(p.amount for p in payments if p.currency == PaymentCurrency.EUR and p.status == PaymentStatus.COMPLETED),
                "XOF": sum(p.amount for p in payments if p.currency == PaymentCurrency.XOF and p.status == PaymentStatus.COMPLETED),
                "USD": sum(p.amount for p in payments if p.currency == PaymentCurrency.USD and p.status == PaymentStatus.COMPLETED),
                "BTC": sum(p.amount for p in payments if p.currency == PaymentCurrency.BTC and p.status == PaymentStatus.COMPLETED),
                "ETH": sum(p.amount for p in payments if p.currency == PaymentCurrency.ETH and p.status == PaymentStatus.COMPLETED)
            },
            "completed_payments": sum(1 for p in payments if p.status == PaymentStatus.COMPLETED),
            "failed_payments": sum(1 for p in payments if p.status == PaymentStatus.FAILED),
            "pending_payments": sum(1 for p in payments if p.status == PaymentStatus.PENDING)
        }
        
        # Par statut
        for status in PaymentStatus:
            stats["by_status"][status.value] = sum(1 for p in payments if p.status == status)
        
        # Par méthode
        for method in PaymentMethod:
            stats["by_method"][method.value] = sum(1 for p in payments if p.payment_method == method)
        
        # Par devise
        for currency in PaymentCurrency:
            stats["by_currency"][currency.value] = sum(1 for p in payments if p.currency == currency)
        
        return stats
    
    async def _save_payment_to_redis(self, payment_info: PaymentInfo):
        """Sauvegarde d'un paiement en Redis"""
        try:
            await self.redis.hset(
                f"payment:{payment_info.payment_id}",
                mapping=self._serialize_payment(payment_info)
            )
            
            # Expiration (5 ans)
            await self.redis.expire(f"payment:{payment_info.payment_id}", 157680000)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde paiement Redis: {e}")
    
    def _serialize_payment(self, payment_info: PaymentInfo) -> Dict[str, str]:
        """Sérialisation d'un paiement"""
        return {
            "payment_id": payment_info.payment_id,
            "license_id": payment_info.license_id,
            "amount": str(payment_info.amount),
            "currency": payment_info.currency.value,
            "payment_method": payment_info.payment_method.value,
            "status": payment_info.status.value,
            "customer_name": payment_info.customer_name,
            "customer_email": payment_info.customer_email,
            "customer_company": payment_info.customer_company,
            "customer_country": payment_info.customer_country,
            "created_date": payment_info.created_date.isoformat(),
            "completed_date": payment_info.completed_date.isoformat() if payment_info.completed_date else "",
            "transaction_id": payment_info.transaction_id or "",
            "payment_details": json.dumps(payment_info.payment_details),
            "developer_info": json.dumps(payment_info.developer_info)
        }
    
    def _deserialize_payment(self, data: Dict[str, str]) -> PaymentInfo:
        """Désérialisation d'un paiement"""
        return PaymentInfo(
            payment_id=data.get("payment_id", ""),
            license_id=data.get("license_id", ""),
            amount=float(data.get("amount", 0)),
            currency=PaymentCurrency(data.get("currency", "EUR")),
            payment_method=PaymentMethod(data.get("payment_method", "credit_card")),
            status=PaymentStatus(data.get("status", "pending")),
            customer_name=data.get("customer_name", ""),
            customer_email=data.get("customer_email", ""),
            customer_company=data.get("customer_company", ""),
            customer_country=data.get("customer_country", ""),
            created_date=datetime.fromisoformat(data.get("created_date", datetime.now().isoformat())),
            completed_date=datetime.fromisoformat(data.get("completed_date", datetime.now().isoformat())) if data.get("completed_date") else None,
            transaction_id=data.get("transaction_id"),
            payment_details=json.loads(data.get("payment_details", "{}")),
            developer_info=json.loads(data.get("developer_info", "{}"))
        )
    
    async def _payment_processor(self):
        """Processeur de paiements en arrière-plan"""
        while True:
            try:
                # Traitement des paiements en attente
                pending_payments = [
                    p for p in self.payments.values()
                    if p.status == PaymentStatus.PENDING
                ]
                
                for payment in pending_payments[:5]:  # Limite à 5 par cycle
                    # Simulation de traitement automatique
                    await asyncio.sleep(1)
                
                await asyncio.sleep(60)  # 1 minute
                
            except Exception as e:
                logger.error(f"Erreur processeur paiements: {e}")
                await asyncio.sleep(300)
    
    async def _payment_cleanup(self):
        """Nettoyage des anciens paiements"""
        while True:
            try:
                # Suppression des paiements de plus de 3 ans
                cutoff_date = datetime.now() - timedelta(days=1095)
                old_payments = [
                    pid for pid, payment in self.payments.items()
                    if payment.created_date < cutoff_date
                ]
                
                for payment_id in old_payments:
                    del self.payments[payment_id]
                    await self.redis.delete(f"payment:{payment_id}")
                
                if old_payments:
                    logger.info(f"🧹 {len(old_payments)} anciens paiements supprimés")
                
                await asyncio.sleep(86400)  # 24 heures
                
            except Exception as e:
                logger.error(f"Erreur nettoyage paiements: {e}")
                await asyncio.sleep(86400)
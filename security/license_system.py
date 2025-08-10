"""
Système de Licence Commerciale
==============================

Système de licence commerciale pour l'Europe et la Côte d'Ivoire
avec validation cryptographique et gestion des droits.
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
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import uuid
import qrcode
from io import BytesIO

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LicenseType(Enum):
    """Types de licence"""
    TRIAL = "trial"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    GOVERNMENT = "government"
    MILITARY = "military"

class LicenseRegion(Enum):
    """Régions de licence"""
    EUROPE = "europe"
    COTE_DIVOIRE = "cote_divoire"
    GLOBAL = "global"

class LicenseStatus(Enum):
    """Statuts de licence"""
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    PENDING = "pending"

@dataclass
class LicenseFeatures:
    """Fonctionnalités de licence"""
    ai_models: bool = False
    world_map: bool = False
    notifications: bool = False
    intelligence_sharing: bool = False
    advanced_protection: bool = False
    api_access: bool = False
    websocket: bool = False
    dashboard: bool = False
    custom_integration: bool = False
    priority_support: bool = False
    training: bool = False
    updates: bool = False

@dataclass
class LicenseInfo:
    """Informations de licence"""
    license_id: str
    license_type: LicenseType
    region: LicenseRegion
    status: LicenseStatus
    customer_name: str
    customer_email: str
    customer_company: str
    customer_country: str
    issued_date: datetime
    expiry_date: datetime
    features: LicenseFeatures
    max_users: int
    max_threats_per_day: int
    support_level: str
    price_eur: float
    price_xof: float
    payment_status: str
    developer_info: Dict[str, Any]

class LicenseSystem:
    """
    Système de licence commerciale
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.licenses: Dict[str, LicenseInfo] = {}
        
        # Clé de chiffrement pour les licences
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "company": "CyberDefense Solutions",
            "email": "hackerduckman89@gmail.com",
            "secondary_email": "yao.kouakou.dev@gmail.com",
            "phone": "+225 0700000000",
            "address": "Abidjan, Côte d'Ivoire",
            "website": "https://cyberdefense-solutions.com",
            "tax_id": "CI123456789",
            "eu_vat": "EU987654321",
            "license_authority": "Autorité de Régulation des Télécommunications de Côte d'Ivoire",
            "eu_authority": "European Union Cybersecurity Agency (ENISA)"
        }
        
        # Configuration des prix (en EUR et XOF)
        self.pricing = {
            LicenseType.TRIAL: {"eur": 0, "xof": 0, "duration_days": 30},
            LicenseType.BASIC: {"eur": 99, "xof": 65000, "duration_days": 365},
            LicenseType.PROFESSIONAL: {"eur": 299, "xof": 195000, "duration_days": 365},
            LicenseType.ENTERPRISE: {"eur": 999, "xof": 650000, "duration_days": 365},
            LicenseType.GOVERNMENT: {"eur": 1999, "xof": 1300000, "duration_days": 365},
            LicenseType.MILITARY: {"eur": 4999, "xof": 3250000, "duration_days": 365}
        }
        
        # Configuration des fonctionnalités par type
        self.feature_configs = {
            LicenseType.TRIAL: LicenseFeatures(
                ai_models=True, world_map=True, notifications=True,
                intelligence_sharing=True, api_access=True, websocket=True,
                dashboard=True, max_users=5, max_threats_per_day=1000
            ),
            LicenseType.BASIC: LicenseFeatures(
                ai_models=True, world_map=True, notifications=True,
                intelligence_sharing=True, api_access=True, websocket=True,
                dashboard=True, max_users=25, max_threats_per_day=10000
            ),
            LicenseType.PROFESSIONAL: LicenseFeatures(
                ai_models=True, world_map=True, notifications=True,
                intelligence_sharing=True, advanced_protection=True,
                api_access=True, websocket=True, dashboard=True,
                custom_integration=True, priority_support=True,
                max_users=100, max_threats_per_day=50000
            ),
            LicenseType.ENTERPRISE: LicenseFeatures(
                ai_models=True, world_map=True, notifications=True,
                intelligence_sharing=True, advanced_protection=True,
                api_access=True, websocket=True, dashboard=True,
                custom_integration=True, priority_support=True,
                training=True, updates=True,
                max_users=500, max_threats_per_day=200000
            ),
            LicenseType.GOVERNMENT: LicenseFeatures(
                ai_models=True, world_map=True, notifications=True,
                intelligence_sharing=True, advanced_protection=True,
                api_access=True, websocket=True, dashboard=True,
                custom_integration=True, priority_support=True,
                training=True, updates=True,
                max_users=1000, max_threats_per_day=500000
            ),
            LicenseType.MILITARY: LicenseFeatures(
                ai_models=True, world_map=True, notifications=True,
                intelligence_sharing=True, advanced_protection=True,
                api_access=True, websocket=True, dashboard=True,
                custom_integration=True, priority_support=True,
                training=True, updates=True,
                max_users=5000, max_threats_per_day=2000000
            )
        }
    
    async def initialize(self):
        """Initialisation du système de licence"""
        logger.info("🔐 Initialisation du système de licence commerciale")
        
        # Chargement des licences existantes
        await self._load_existing_licenses()
        
        # Création de licences de démonstration
        await self._create_demo_licenses()
        
        # Démarrage des tâches en arrière-plan
        asyncio.create_task(self._license_validator())
        asyncio.create_task(self._license_cleanup())
        
        logger.info("✅ Système de licence initialisé")
    
    async def _load_existing_licenses(self):
        """Chargement des licences existantes"""
        try:
            keys = await self.redis.keys("license:*")
            for key in keys:
                data = await self.redis.hgetall(key)
                if data:
                    license_info = self._deserialize_license(data)
                    self.licenses[license_info.license_id] = license_info
        except Exception as e:
            logger.error(f"Erreur chargement licences: {e}")
    
    async def _create_demo_licenses(self):
        """Création de licences de démonstration"""
        demo_licenses = [
            {
                "customer_name": "Demo Europe",
                "customer_email": "demo@europe.com",
                "customer_company": "European Demo Corp",
                "customer_country": "France",
                "license_type": LicenseType.ENTERPRISE,
                "region": LicenseRegion.EUROPE
            },
            {
                "customer_name": "Demo Côte d'Ivoire",
                "customer_email": "demo@cotedivoire.ci",
                "customer_company": "Ivoirian Demo Corp",
                "customer_country": "Côte d'Ivoire",
                "license_type": LicenseType.PROFESSIONAL,
                "region": LicenseRegion.COTE_DIVOIRE
            }
        ]
        
        for demo in demo_licenses:
            try:
                await self.create_license(
                    customer_name=demo["customer_name"],
                    customer_email=demo["customer_email"],
                    customer_company=demo["customer_company"],
                    customer_country=demo["customer_country"],
                    license_type=demo["license_type"],
                    region=demo["region"],
                    payment_status="paid"
                )
            except Exception as e:
                logger.error(f"Erreur création licence demo: {e}")
    
    async def create_license(self, 
                           customer_name: str,
                           customer_email: str,
                           customer_company: str,
                           customer_country: str,
                           license_type: LicenseType,
                           region: LicenseRegion,
                           payment_status: str = "pending") -> LicenseInfo:
        """Création d'une nouvelle licence"""
        try:
            # Génération de l'ID de licence
            license_id = f"LIC_{region.value.upper()}_{license_type.value.upper()}_{uuid.uuid4().hex[:8]}"
            
            # Dates
            issued_date = datetime.now()
            duration_days = self.pricing[license_type]["duration_days"]
            expiry_date = issued_date + timedelta(days=duration_days)
            
            # Fonctionnalités
            features = self.feature_configs[license_type]
            
            # Prix
            price_eur = self.pricing[license_type]["eur"]
            price_xof = self.pricing[license_type]["xof"]
            
            # Création de la licence
            license_info = LicenseInfo(
                license_id=license_id,
                license_type=license_type,
                region=region,
                status=LicenseStatus.ACTIVE if payment_status == "paid" else LicenseStatus.PENDING,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_company=customer_company,
                customer_country=customer_country,
                issued_date=issued_date,
                expiry_date=expiry_date,
                features=features,
                max_users=features.max_users,
                max_threats_per_day=features.max_threats_per_day,
                support_level="Standard" if license_type in [LicenseType.TRIAL, LicenseType.BASIC] else "Priority",
                price_eur=price_eur,
                price_xof=price_xof,
                payment_status=payment_status,
                developer_info=self.developer_info
            )
            
            # Stockage de la licence
            self.licenses[license_id] = license_info
            await self._save_license_to_redis(license_info)
            
            logger.info(f"🔐 Licence créée: {license_id} pour {customer_company}")
            
            return license_info
            
        except Exception as e:
            logger.error(f"Erreur création licence: {e}")
            raise
    
    async def validate_license(self, license_id: str) -> Dict[str, Any]:
        """Validation d'une licence"""
        try:
            if license_id not in self.licenses:
                return {"valid": False, "error": "Licence non trouvée"}
            
            license_info = self.licenses[license_id]
            
            # Vérification de l'expiration
            if datetime.now() > license_info.expiry_date:
                license_info.status = LicenseStatus.EXPIRED
                await self._save_license_to_redis(license_info)
                return {"valid": False, "error": "Licence expirée"}
            
            # Vérification du statut
            if license_info.status != LicenseStatus.ACTIVE:
                return {"valid": False, "error": f"Licence {license_info.status.value}"}
            
            # Vérification du paiement
            if license_info.payment_status != "paid":
                return {"valid": False, "error": "Paiement en attente"}
            
            return {
                "valid": True,
                "license": asdict(license_info),
                "features": asdict(license_info.features),
                "days_remaining": (license_info.expiry_date - datetime.now()).days
            }
            
        except Exception as e:
            logger.error(f"Erreur validation licence: {e}")
            return {"valid": False, "error": str(e)}
    
    async def get_license_info(self, license_id: str) -> Optional[LicenseInfo]:
        """Récupération des informations de licence"""
        return self.licenses.get(license_id)
    
    async def update_license_status(self, license_id: str, status: LicenseStatus):
        """Mise à jour du statut de licence"""
        try:
            if license_id in self.licenses:
                license_info = self.licenses[license_id]
                license_info.status = status
                await self._save_license_to_redis(license_info)
                logger.info(f"🔐 Statut licence {license_id} mis à jour: {status.value}")
        except Exception as e:
            logger.error(f"Erreur mise à jour statut licence: {e}")
    
    async def renew_license(self, license_id: str, duration_days: int = 365) -> bool:
        """Renouvellement d'une licence"""
        try:
            if license_id not in self.licenses:
                return False
            
            license_info = self.licenses[license_id]
            license_info.expiry_date = datetime.now() + timedelta(days=duration_days)
            license_info.status = LicenseStatus.ACTIVE
            license_info.payment_status = "paid"
            
            await self._save_license_to_redis(license_info)
            logger.info(f"🔐 Licence {license_id} renouvelée")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur renouvellement licence: {e}")
            return False
    
    async def revoke_license(self, license_id: str, reason: str = "") -> bool:
        """Révocation d'une licence"""
        try:
            if license_id not in self.licenses:
                return False
            
            license_info = self.licenses[license_id]
            license_info.status = LicenseStatus.REVOKED
            
            await self._save_license_to_redis(license_info)
            logger.info(f"🔐 Licence {license_id} révoquée: {reason}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur révocation licence: {e}")
            return False
    
    def generate_license_key(self, license_info: LicenseInfo) -> str:
        """Génération d'une clé de licence cryptographique"""
        try:
            # Données à encoder
            data = {
                "license_id": license_info.license_id,
                "customer_email": license_info.customer_email,
                "license_type": license_info.license_type.value,
                "region": license_info.region.value,
                "issued_date": license_info.issued_date.isoformat(),
                "expiry_date": license_info.expiry_date.isoformat()
            }
            
            # Encodage JSON
            json_data = json.dumps(data, sort_keys=True)
            
            # Chiffrement
            encrypted_data = self.cipher_suite.encrypt(json_data.encode())
            
            # Encodage Base64
            license_key = base64.urlsafe_b64encode(encrypted_data).decode()
            
            return license_key
            
        except Exception as e:
            logger.error(f"Erreur génération clé licence: {e}")
            raise
    
    def validate_license_key(self, license_key: str) -> Optional[Dict[str, Any]]:
        """Validation d'une clé de licence"""
        try:
            # Décodage Base64
            encrypted_data = base64.urlsafe_b64decode(license_key.encode())
            
            # Déchiffrement
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            
            # Décodage JSON
            data = json.loads(decrypted_data.decode())
            
            return data
            
        except Exception as e:
            logger.error(f"Erreur validation clé licence: {e}")
            return None
    
    def generate_license_qr(self, license_info: LicenseInfo) -> str:
        """Génération d'un QR code pour la licence"""
        try:
            # Données du QR code
            qr_data = {
                "license_id": license_info.license_id,
                "customer": license_info.customer_name,
                "company": license_info.customer_company,
                "type": license_info.license_type.value,
                "region": license_info.region.value,
                "expiry": license_info.expiry_date.strftime("%Y-%m-%d"),
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
            logger.error(f"Erreur génération QR licence: {e}")
            return ""
    
    async def get_pricing_info(self, region: LicenseRegion) -> Dict[str, Any]:
        """Récupération des informations de prix"""
        pricing_info = {}
        
        for license_type, config in self.pricing.items():
            features = self.feature_configs[license_type]
            pricing_info[license_type.value] = {
                "price_eur": config["eur"],
                "price_xof": config["xof"],
                "duration_days": config["duration_days"],
                "features": asdict(features),
                "support_level": "Standard" if license_type in [LicenseType.TRIAL, LicenseType.BASIC] else "Priority"
            }
        
        return {
            "region": region.value,
            "currency_eur": "EUR",
            "currency_xof": "XOF",
            "exchange_rate": 1.0,  # À mettre à jour selon le taux actuel
            "pricing": pricing_info,
            "developer_info": self.developer_info
        }
    
    async def _save_license_to_redis(self, license_info: LicenseInfo):
        """Sauvegarde d'une licence en Redis"""
        try:
            await self.redis.hset(
                f"license:{license_info.license_id}",
                mapping=self._serialize_license(license_info)
            )
            
            # Expiration (10 ans)
            await self.redis.expire(f"license:{license_info.license_id}", 315360000)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde licence Redis: {e}")
    
    def _serialize_license(self, license_info: LicenseInfo) -> Dict[str, str]:
        """Sérialisation d'une licence"""
        return {
            "license_id": license_info.license_id,
            "license_type": license_info.license_type.value,
            "region": license_info.region.value,
            "status": license_info.status.value,
            "customer_name": license_info.customer_name,
            "customer_email": license_info.customer_email,
            "customer_company": license_info.customer_company,
            "customer_country": license_info.customer_country,
            "issued_date": license_info.issued_date.isoformat(),
            "expiry_date": license_info.expiry_date.isoformat(),
            "features": json.dumps(asdict(license_info.features)),
            "max_users": str(license_info.max_users),
            "max_threats_per_day": str(license_info.max_threats_per_day),
            "support_level": license_info.support_level,
            "price_eur": str(license_info.price_eur),
            "price_xof": str(license_info.price_xof),
            "payment_status": license_info.payment_status,
            "developer_info": json.dumps(license_info.developer_info)
        }
    
    def _deserialize_license(self, data: Dict[str, str]) -> LicenseInfo:
        """Désérialisation d'une licence"""
        return LicenseInfo(
            license_id=data.get("license_id", ""),
            license_type=LicenseType(data.get("license_type", "trial")),
            region=LicenseRegion(data.get("region", "global")),
            status=LicenseStatus(data.get("status", "pending")),
            customer_name=data.get("customer_name", ""),
            customer_email=data.get("customer_email", ""),
            customer_company=data.get("customer_company", ""),
            customer_country=data.get("customer_country", ""),
            issued_date=datetime.fromisoformat(data.get("issued_date", datetime.now().isoformat())),
            expiry_date=datetime.fromisoformat(data.get("expiry_date", datetime.now().isoformat())),
            features=LicenseFeatures(**json.loads(data.get("features", "{}"))),
            max_users=int(data.get("max_users", 5)),
            max_threats_per_day=int(data.get("max_threats_per_day", 1000)),
            support_level=data.get("support_level", "Standard"),
            price_eur=float(data.get("price_eur", 0)),
            price_xof=float(data.get("price_xof", 0)),
            payment_status=data.get("payment_status", "pending"),
            developer_info=json.loads(data.get("developer_info", "{}"))
        )
    
    async def _license_validator(self):
        """Validateur de licences en arrière-plan"""
        while True:
            try:
                for license_id, license_info in self.licenses.items():
                    # Vérification de l'expiration
                    if datetime.now() > license_info.expiry_date and license_info.status == LicenseStatus.ACTIVE:
                        license_info.status = LicenseStatus.EXPIRED
                        await self._save_license_to_redis(license_info)
                        logger.warning(f"🔐 Licence {license_id} expirée")
                
                await asyncio.sleep(3600)  # 1 heure
                
            except Exception as e:
                logger.error(f"Erreur validateur licences: {e}")
                await asyncio.sleep(3600)
    
    async def _license_cleanup(self):
        """Nettoyage des licences expirées"""
        while True:
            try:
                # Suppression des licences expirées depuis plus de 1 an
                cutoff_date = datetime.now() - timedelta(days=365)
                expired_licenses = [
                    lid for lid, license_info in self.licenses.items()
                    if license_info.expiry_date < cutoff_date and license_info.status == LicenseStatus.EXPIRED
                ]
                
                for license_id in expired_licenses:
                    del self.licenses[license_id]
                    await self.redis.delete(f"license:{license_id}")
                
                if expired_licenses:
                    logger.info(f"🧹 {len(expired_licenses)} licences expirées supprimées")
                
                await asyncio.sleep(86400)  # 24 heures
                
            except Exception as e:
                logger.error(f"Erreur nettoyage licences: {e}")
                await asyncio.sleep(86400)
    
    async def get_license_statistics(self) -> Dict[str, Any]:
        """Statistiques des licences"""
        licenses = list(self.licenses.values())
        
        stats = {
            "total": len(licenses),
            "by_type": {},
            "by_region": {},
            "by_status": {},
            "revenue_eur": sum(l.price_eur for l in licenses if l.payment_status == "paid"),
            "revenue_xof": sum(l.price_xof for l in licenses if l.payment_status == "paid"),
            "active_licenses": sum(1 for l in licenses if l.status == LicenseStatus.ACTIVE),
            "expired_licenses": sum(1 for l in licenses if l.status == LicenseStatus.EXPIRED)
        }
        
        # Par type
        for license_type in LicenseType:
            stats["by_type"][license_type.value] = sum(1 for l in licenses if l.license_type == license_type)
        
        # Par région
        for region in LicenseRegion:
            stats["by_region"][region.value] = sum(1 for l in licenses if l.region == region)
        
        # Par statut
        for status in LicenseStatus:
            stats["by_status"][status.value] = sum(1 for l in licenses if l.status == status)
        
        return stats
#!/usr/bin/env python3
"""
Système de Protection d'Accès
============================

Protection par mot de passe pour éviter le téléchargement non autorisé
sur GitHub et autres plateformes.
"""

import hashlib
import hmac
import time
import secrets
import base64
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import redis
import json

@dataclass
class AccessToken:
    """Token d'accès sécurisé"""
    token: str
    created_at: datetime
    expires_at: datetime
    user_agent: str
    ip_address: str
    permissions: list

@dataclass
class SecurityConfig:
    """Configuration de sécurité"""
    master_password: str = "AZ12ER34"
    salt: str = "CyberDefense2024"
    max_attempts: int = 3
    lockout_duration: int = 300  # 5 minutes
    token_expiry: int = 3600  # 1 heure
    require_2fa: bool = True

class AccessProtection:
    """
    Système de protection d'accès par mot de passe
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.config = SecurityConfig()
        self.failed_attempts: Dict[str, int] = {}
        self.lockout_until: Dict[str, datetime] = {}
        self.active_tokens: Dict[str, AccessToken] = {}
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license": "CI-CYBER-2024-001"
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash du mot de passe avec salt"""
        salted = password + self.config.salt
        return hashlib.sha256(salted.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Vérification du mot de passe"""
        return hmac.compare_digest(self._hash_password(password), hashed)
    
    def _generate_token(self) -> str:
        """Génération d'un token sécurisé"""
        random_bytes = secrets.token_bytes(32)
        timestamp = str(int(time.time()))
        data = f"{random_bytes.hex()}:{timestamp}"
        return base64.urlsafe_b64encode(data.encode()).decode()
    
    def _is_ip_locked(self, ip_address: str) -> bool:
        """Vérification si l'IP est verrouillée"""
        if ip_address in self.lockout_until:
            if datetime.now() < self.lockout_until[ip_address]:
                return True
            else:
                # Déverrouillage automatique
                del self.lockout_until[ip_address]
                self.failed_attempts[ip_address] = 0
        return False
    
    def _record_failed_attempt(self, ip_address: str):
        """Enregistrement d'une tentative échouée"""
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = 0
        
        self.failed_attempts[ip_address] += 1
        
        if self.failed_attempts[ip_address] >= self.config.max_attempts:
            lockout_time = datetime.now() + timedelta(seconds=self.config.lockout_duration)
            self.lockout_until[ip_address] = lockout_time
            
            # Log de sécurité
            self._log_security_event("LOCKOUT", ip_address, f"Trop de tentatives échouées")
    
    def _log_security_event(self, event_type: str, ip_address: str, details: str):
        """Log des événements de sécurité"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "ip_address": ip_address,
            "details": details,
            "developer": self.developer_info
        }
        
        # Stockage dans Redis
        self.redis.lpush("security_events", json.dumps(event))
        self.redis.ltrim("security_events", 0, 999)  # Garder les 1000 derniers événements
    
    async def authenticate(self, password: str, ip_address: str, user_agent: str) -> Tuple[bool, str, Optional[str]]:
        """
        Authentification avec mot de passe
        
        Returns:
            (success, message, token)
        """
        # Vérification du verrouillage
        if self._is_ip_locked(ip_address):
            remaining_time = self.lockout_until[ip_address] - datetime.now()
            return False, f"Compte verrouillé. Réessayez dans {int(remaining_time.total_seconds())} secondes.", None
        
        # Vérification du mot de passe
        if self._verify_password(password, self._hash_password(self.config.master_password)):
            # Authentification réussie
            self.failed_attempts[ip_address] = 0
            
            # Génération du token
            token = self._generate_token()
            expires_at = datetime.now() + timedelta(seconds=self.config.token_expiry)
            
            access_token = AccessToken(
                token=token,
                created_at=datetime.now(),
                expires_at=expires_at,
                user_agent=user_agent,
                ip_address=ip_address,
                permissions=["read", "write", "admin"]
            )
            
            self.active_tokens[token] = access_token
            
            # Log de succès
            self._log_security_event("LOGIN_SUCCESS", ip_address, f"Connexion réussie - {user_agent}")
            
            return True, "Authentification réussie", token
        
        else:
            # Authentification échouée
            self._record_failed_attempt(ip_address)
            remaining_attempts = self.config.max_attempts - self.failed_attempts[ip_address]
            
            if remaining_attempts > 0:
                message = f"Mot de passe incorrect. {remaining_attempts} tentatives restantes."
            else:
                message = f"Compte verrouillé pour {self.config.lockout_duration} secondes."
            
            # Log d'échec
            self._log_security_event("LOGIN_FAILED", ip_address, f"Tentative échouée - {user_agent}")
            
            return False, message, None
    
    async def validate_token(self, token: str, ip_address: str) -> Tuple[bool, str, Optional[AccessToken]]:
        """
        Validation d'un token d'accès
        
        Returns:
            (valid, message, access_token)
        """
        if token not in self.active_tokens:
            return False, "Token invalide", None
        
        access_token = self.active_tokens[token]
        
        # Vérification de l'expiration
        if datetime.now() > access_token.expires_at:
            del self.active_tokens[token]
            return False, "Token expiré", None
        
        # Vérification de l'IP (optionnel)
        if access_token.ip_address != ip_address:
            self._log_security_event("TOKEN_IP_MISMATCH", ip_address, f"Token utilisé depuis une IP différente")
        
        return True, "Token valide", access_token
    
    async def revoke_token(self, token: str) -> bool:
        """Révoquer un token"""
        if token in self.active_tokens:
            del self.active_tokens[token]
            return True
        return False
    
    async def get_security_stats(self) -> Dict:
        """Statistiques de sécurité"""
        return {
            "active_tokens": len(self.active_tokens),
            "failed_attempts": dict(self.failed_attempts),
            "locked_ips": len(self.lockout_until),
            "developer_info": self.developer_info
        }
    
    async def get_security_events(self, limit: int = 50) -> list:
        """Récupération des événements de sécurité"""
        events = self.redis.lrange("security_events", 0, limit - 1)
        return [json.loads(event) for event in events]
    
    def _check_github_access(self, user_agent: str) -> bool:
        """Détection d'accès depuis GitHub"""
        github_indicators = [
            "github.com",
            "githubusercontent.com",
            "github.io",
            "github-actions",
            "github-bot"
        ]
        
        user_agent_lower = user_agent.lower()
        for indicator in github_indicators:
            if indicator in user_agent_lower:
                return True
        return False
    
    async def check_access_permission(self, ip_address: str, user_agent: str, requested_resource: str) -> Tuple[bool, str]:
        """
        Vérification des permissions d'accès
        
        Returns:
            (allowed, reason)
        """
        # Détection GitHub
        if self._check_github_access(user_agent):
            self._log_security_event("GITHUB_BLOCKED", ip_address, f"Accès GitHub bloqué - {requested_resource}")
            return False, "Accès non autorisé depuis GitHub"
        
        # Vérification du verrouillage
        if self._is_ip_locked(ip_address):
            return False, "IP verrouillée"
        
        # Vérification des ressources sensibles
        sensitive_resources = [
            "license_system.py",
            "payment_system.py",
            "access_protection.py",
            "config.json",
            "LICENCE_VENTE_IVOIRIENNE.md"
        ]
        
        if any(resource in requested_resource for resource in sensitive_resources):
            self._log_security_event("SENSITIVE_ACCESS", ip_address, f"Tentative d'accès à {requested_resource}")
            return False, "Accès aux ressources sensibles non autorisé"
        
        return True, "Accès autorisé"

class SecurityMiddleware:
    """
    Middleware de sécurité pour FastAPI
    """
    
    def __init__(self, access_protection: AccessProtection):
        self.access_protection = access_protection
    
    async def __call__(self, request, call_next):
        """Middleware de sécurité"""
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")
        path = request.url.path
        
        # Vérification des permissions d'accès
        allowed, reason = await self.access_protection.check_access_permission(
            ip_address, user_agent, path
        )
        
        if not allowed:
            return {
                "error": "Accès non autorisé",
                "reason": reason,
                "developer": self.access_protection.developer_info,
                "contact": "+225 014094507"
            }
        
        # Vérification du token pour les routes protégées
        if path.startswith("/api/") and path not in ["/api/auth", "/api/health"]:
            token = request.headers.get("authorization", "").replace("Bearer ", "")
            
            if token:
                valid, message, access_token = await self.access_protection.validate_token(token, ip_address)
                if not valid:
                    return {
                        "error": "Token invalide",
                        "message": message,
                        "developer": self.access_protection.developer_info
                    }
            else:
                return {
                    "error": "Token requis",
                    "message": "Authentification requise pour cette ressource",
                    "developer": self.access_protection.developer_info
                }
        
        response = await call_next(request)
        return response

# Configuration de sécurité globale
SECURITY_CONFIG = {
    "master_password": "AZ12ER34",
    "salt": "CyberDefense2024",
    "max_attempts": 3,
    "lockout_duration": 300,
    "token_expiry": 3600,
    "require_2fa": True,
    "developer": {
        "name": "Yao Kouakou Luc Anicet",
        "phone": "+225 014094507",
        "email": "hackerduckman89@gmail.com",
        "license": "CI-CYBER-2024-001"
    }
}

# Instance globale
access_protection = AccessProtection()
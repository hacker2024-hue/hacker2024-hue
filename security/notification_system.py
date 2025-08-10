"""
Système de Notification Avancé
==============================

Système de notification multi-canal pour les alertes de sécurité
avec support email, SMS, webhook et notifications push.
"""

import asyncio
import json
import logging
import smtplib
import ssl
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import redis.asyncio as redis
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from fastapi import WebSocket

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Types de notification"""
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    PUSH = "push"
    SLACK = "slack"
    TELEGRAM = "telegram"
    DISCORD = "discord"

class NotificationPriority(Enum):
    """Priorités de notification"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class NotificationConfig:
    """Configuration de notification"""
    type: NotificationType
    enabled: bool
    config: Dict[str, Any]
    recipients: List[str]
    priority_threshold: NotificationPriority

@dataclass
class NotificationMessage:
    """Message de notification"""
    id: str
    timestamp: datetime
    type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    data: Dict[str, Any]
    recipients: List[str]
    sent: bool = False
    error: Optional[str] = None

class NotificationSystem:
    """
    Système de notification avancé
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.notifications: Dict[str, NotificationMessage] = {}
        self.configs: Dict[NotificationType, NotificationConfig] = {}
        self.websocket_connections: Set[WebSocket] = set()
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "email": "hackerduckman89@gmail.com",
            "secondary_email": "yao.kouakou.dev@gmail.com",
            "title": "Expert en Cybersécurité"
        }
        
        # Configuration par défaut
        self._setup_default_configs()
        
    def _setup_default_configs(self):
        """Configuration par défaut des notifications"""
        
        # Configuration Email
        self.configs[NotificationType.EMAIL] = NotificationConfig(
            type=NotificationType.EMAIL,
            enabled=True,
            config={
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "hackerduckman89@gmail.com",
                "password": "",  # À configurer
                "use_tls": True,
                "from_name": "Système de Défense Cybernétique - Yao Kouakou"
            },
            recipients=[
                "hackerduckman89@gmail.com",
                "yao.kouakou.dev@gmail.com"
            ],
            priority_threshold=NotificationPriority.MEDIUM
        )
        
        # Configuration Webhook
        self.configs[NotificationType.WEBHOOK] = NotificationConfig(
            type=NotificationType.WEBHOOK,
            enabled=True,
            config={
                "url": "https://hooks.slack.com/services/YOUR_WEBHOOK_URL",
                "timeout": 30,
                "retry_count": 3
            },
            recipients=[],
            priority_threshold=NotificationPriority.HIGH
        )
        
        # Configuration Slack
        self.configs[NotificationType.SLACK] = NotificationConfig(
            type=NotificationType.SLACK,
            enabled=False,
            config={
                "webhook_url": "https://hooks.slack.com/services/YOUR_SLACK_WEBHOOK",
                "channel": "#security-alerts",
                "username": "CyberDefense Bot"
            },
            recipients=[],
            priority_threshold=NotificationPriority.MEDIUM
        )
        
        # Configuration Telegram
        self.configs[NotificationType.TELEGRAM] = NotificationConfig(
            type=NotificationType.TELEGRAM,
            enabled=False,
            config={
                "bot_token": "YOUR_BOT_TOKEN",
                "chat_id": "YOUR_CHAT_ID"
            },
            recipients=[],
            priority_threshold=NotificationPriority.HIGH
        )
        
        # Configuration Discord
        self.configs[NotificationType.DISCORD] = NotificationConfig(
            type=NotificationType.DISCORD,
            enabled=False,
            config={
                "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK",
                "username": "CyberDefense Bot"
            },
            recipients=[],
            priority_threshold=NotificationPriority.MEDIUM
        )
    
    async def initialize(self):
        """Initialisation du système de notification"""
        logger.info("🔔 Initialisation du système de notification")
        
        # Chargement des notifications existantes
        await self._load_existing_notifications()
        
        # Démarrage des tâches en arrière-plan
        asyncio.create_task(self._notification_processor())
        asyncio.create_task(self._notification_cleanup())
        
        logger.info("✅ Système de notification initialisé")
    
    async def _load_existing_notifications(self):
        """Chargement des notifications existantes"""
        try:
            keys = await self.redis.keys("notification:*")
            for key in keys:
                data = await self.redis.hgetall(key)
                if data:
                    notification = NotificationMessage(
                        id=data.get("id", ""),
                        timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
                        type=NotificationType(data.get("type", "email")),
                        priority=NotificationPriority(data.get("priority", "medium")),
                        title=data.get("title", ""),
                        message=data.get("message", ""),
                        data=json.loads(data.get("data", "{}")),
                        recipients=json.loads(data.get("recipients", "[]")),
                        sent=data.get("sent", "false").lower() == "true",
                        error=data.get("error")
                    )
                    self.notifications[notification.id] = notification
        except Exception as e:
            logger.error(f"Erreur chargement notifications: {e}")
    
    async def send_notification(self, 
                               title: str, 
                               message: str, 
                               priority: NotificationPriority = NotificationPriority.MEDIUM,
                               notification_type: Optional[NotificationType] = None,
                               data: Optional[Dict[str, Any]] = None,
                               recipients: Optional[List[str]] = None) -> str:
        """Envoi d'une notification"""
        try:
            # Génération de l'ID
            notification_id = f"notification_{int(datetime.now().timestamp())}_{hash(title)}"
            
            # Création du message
            notification = NotificationMessage(
                id=notification_id,
                timestamp=datetime.now(),
                type=notification_type or NotificationType.EMAIL,
                priority=priority,
                title=title,
                message=message,
                data=data or {},
                recipients=recipients or []
            )
            
            # Stockage de la notification
            self.notifications[notification_id] = notification
            await self._save_notification_to_redis(notification)
            
            # Envoi immédiat si priorité critique
            if priority == NotificationPriority.CRITICAL:
                await self._send_notification_immediate(notification)
            
            # Notification WebSocket
            await self._notify_websocket(notification)
            
            logger.info(f"🔔 Notification créée: {notification_id} ({priority.value})")
            
            return notification_id
            
        except Exception as e:
            logger.error(f"Erreur création notification: {e}")
            raise
    
    async def _send_notification_immediate(self, notification: NotificationMessage):
        """Envoi immédiat d'une notification"""
        try:
            config = self.configs.get(notification.type)
            if not config or not config.enabled:
                return
            
            if notification.type == NotificationType.EMAIL:
                await self._send_email_notification(notification, config)
            elif notification.type == NotificationType.WEBHOOK:
                await self._send_webhook_notification(notification, config)
            elif notification.type == NotificationType.SLACK:
                await self._send_slack_notification(notification, config)
            elif notification.type == NotificationType.TELEGRAM:
                await self._send_telegram_notification(notification, config)
            elif notification.type == NotificationType.DISCORD:
                await self._send_discord_notification(notification, config)
            
            # Marquer comme envoyée
            notification.sent = True
            await self._save_notification_to_redis(notification)
            
        except Exception as e:
            logger.error(f"Erreur envoi notification {notification.id}: {e}")
            notification.error = str(e)
            await self._save_notification_to_redis(notification)
    
    async def _send_email_notification(self, notification: NotificationMessage, config: NotificationConfig):
        """Envoi de notification email"""
        try:
            # Création du message
            msg = MIMEMultipart()
            msg['From'] = f"{config.config['from_name']} <{config.config['username']}>"
            msg['To'] = ", ".join(notification.recipients or config.recipients)
            msg['Subject'] = f"[{notification.priority.value.upper()}] {notification.title}"
            
            # Corps du message
            body = f"""
            🚨 ALERTE DE SÉCURITÉ 🚨
            
            {notification.message}
            
            ---
            Détails:
            - Priorité: {notification.priority.value.upper()}
            - Timestamp: {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
            - Type: {notification.type.value}
            
            ---
            Système Mondial de Défense Cybernétique
            Développé par: {self.developer_info['name']}
            Contact: {self.developer_info['email']}
            Version: 2.0.0 - Edition Mondiale
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Envoi
            context = ssl.create_default_context()
            with smtplib.SMTP(config.config['smtp_server'], config.config['smtp_port']) as server:
                if config.config['use_tls']:
                    server.starttls(context=context)
                if config.config['username'] and config.config['password']:
                    server.login(config.config['username'], config.config['password'])
                server.send_message(msg)
            
            logger.info(f"📧 Email envoyé à {msg['To']}")
            
        except Exception as e:
            logger.error(f"Erreur envoi email: {e}")
            raise
    
    async def _send_webhook_notification(self, notification: NotificationMessage, config: NotificationConfig):
        """Envoi de notification webhook"""
        try:
            payload = {
                "text": f"🚨 *{notification.title}*",
                "attachments": [{
                    "color": self._get_priority_color(notification.priority),
                    "fields": [
                        {
                            "title": "Message",
                            "value": notification.message,
                            "short": False
                        },
                        {
                            "title": "Priorité",
                            "value": notification.priority.value.upper(),
                            "short": True
                        },
                        {
                            "title": "Timestamp",
                            "value": notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                            "short": True
                        },
                        {
                            "title": "Développeur",
                            "value": f"{self.developer_info['name']} ({self.developer_info['email']})",
                            "short": False
                        }
                    ]
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config.config['url'],
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=config.config['timeout'])
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Webhook error: {response.status}")
            
            logger.info(f"🔗 Webhook envoyé à {config.config['url']}")
            
        except Exception as e:
            logger.error(f"Erreur envoi webhook: {e}")
            raise
    
    async def _send_slack_notification(self, notification: NotificationMessage, config: NotificationConfig):
        """Envoi de notification Slack"""
        try:
            payload = {
                "channel": config.config['channel'],
                "username": config.config['username'],
                "text": f"🚨 *{notification.title}*",
                "attachments": [{
                    "color": self._get_priority_color(notification.priority),
                    "fields": [
                        {
                            "title": "Message",
                            "value": notification.message,
                            "short": False
                        },
                        {
                            "title": "Priorité",
                            "value": notification.priority.value.upper(),
                            "short": True
                        },
                        {
                            "title": "Développeur",
                            "value": f"{self.developer_info['name']}",
                            "short": True
                        }
                    ]
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(config.config['webhook_url'], json=payload) as response:
                    if response.status != 200:
                        raise Exception(f"Slack error: {response.status}")
            
            logger.info(f"💬 Slack notification envoyée")
            
        except Exception as e:
            logger.error(f"Erreur envoi Slack: {e}")
            raise
    
    async def _send_telegram_notification(self, notification: NotificationMessage, config: NotificationConfig):
        """Envoi de notification Telegram"""
        try:
            message = f"""
🚨 *{notification.title}*

{notification.message}

*Priorité:* {notification.priority.value.upper()}
*Timestamp:* {notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

---
Système Mondial de Défense Cybernétique
Développé par: {self.developer_info['name']}
Contact: {self.developer_info['email']}
            """
            
            url = f"https://api.telegram.org/bot{config.config['bot_token']}/sendMessage"
            payload = {
                "chat_id": config.config['chat_id'],
                "text": message,
                "parse_mode": "Markdown"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        raise Exception(f"Telegram error: {response.status}")
            
            logger.info(f"📱 Telegram notification envoyée")
            
        except Exception as e:
            logger.error(f"Erreur envoi Telegram: {e}")
            raise
    
    async def _send_discord_notification(self, notification: NotificationMessage, config: NotificationConfig):
        """Envoi de notification Discord"""
        try:
            embed = {
                "title": f"🚨 {notification.title}",
                "description": notification.message,
                "color": self._get_priority_color_int(notification.priority),
                "fields": [
                    {
                        "name": "Priorité",
                        "value": notification.priority.value.upper(),
                        "inline": True
                    },
                    {
                        "name": "Timestamp",
                        "value": notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        "inline": True
                    },
                    {
                        "name": "Développeur",
                        "value": f"{self.developer_info['name']} ({self.developer_info['email']})",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Système Mondial de Défense Cybernétique - Yao Kouakou"
                }
            }
            
            payload = {
                "username": config.config['username'],
                "embeds": [embed]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(config.config['webhook_url'], json=payload) as response:
                    if response.status != 204:
                        raise Exception(f"Discord error: {response.status}")
            
            logger.info(f"🎮 Discord notification envoyée")
            
        except Exception as e:
            logger.error(f"Erreur envoi Discord: {e}")
            raise
    
    def _get_priority_color(self, priority: NotificationPriority) -> str:
        """Couleur selon la priorité"""
        colors = {
            NotificationPriority.LOW: "#36a64f",
            NotificationPriority.MEDIUM: "#ffa500",
            NotificationPriority.HIGH: "#ff6b6b",
            NotificationPriority.CRITICAL: "#ff0000"
        }
        return colors.get(priority, "#36a64f")
    
    def _get_priority_color_int(self, priority: NotificationPriority) -> int:
        """Couleur (int) selon la priorité pour Discord"""
        colors = {
            NotificationPriority.LOW: 0x36a64f,
            NotificationPriority.MEDIUM: 0xffa500,
            NotificationPriority.HIGH: 0xff6b6b,
            NotificationPriority.CRITICAL: 0xff0000
        }
        return colors.get(priority, 0x36a64f)
    
    async def _save_notification_to_redis(self, notification: NotificationMessage):
        """Sauvegarde d'une notification en Redis"""
        try:
            await self.redis.hset(
                f"notification:{notification.id}",
                mapping={
                    "id": notification.id,
                    "timestamp": notification.timestamp.isoformat(),
                    "type": notification.type.value,
                    "priority": notification.priority.value,
                    "title": notification.title,
                    "message": notification.message,
                    "data": json.dumps(notification.data),
                    "recipients": json.dumps(notification.recipients),
                    "sent": str(notification.sent).lower(),
                    "error": notification.error or ""
                }
            )
            
            # Expiration (7 jours)
            await self.redis.expire(f"notification:{notification.id}", 604800)
            
        except Exception as e:
            logger.error(f"Erreur sauvegarde notification Redis: {e}")
    
    async def _notification_processor(self):
        """Processeur de notifications en arrière-plan"""
        while True:
            try:
                # Traitement des notifications en attente
                pending_notifications = [
                    n for n in self.notifications.values()
                    if not n.sent and n.priority != NotificationPriority.CRITICAL
                ]
                
                for notification in pending_notifications[:10]:  # Limite à 10 par cycle
                    await self._send_notification_immediate(notification)
                
                await asyncio.sleep(60)  # 1 minute
                
            except Exception as e:
                logger.error(f"Erreur processeur notifications: {e}")
                await asyncio.sleep(300)
    
    async def _notification_cleanup(self):
        """Nettoyage des anciennes notifications"""
        while True:
            try:
                # Suppression des notifications de plus de 30 jours
                cutoff_date = datetime.now() - timedelta(days=30)
                old_notifications = [
                    nid for nid, notification in self.notifications.items()
                    if notification.timestamp < cutoff_date
                ]
                
                for nid in old_notifications:
                    del self.notifications[nid]
                    await self.redis.delete(f"notification:{nid}")
                
                if old_notifications:
                    logger.info(f"🧹 {len(old_notifications)} anciennes notifications supprimées")
                
                await asyncio.sleep(3600)  # 1 heure
                
            except Exception as e:
                logger.error(f"Erreur nettoyage notifications: {e}")
                await asyncio.sleep(3600)
    
    async def _notify_websocket(self, notification: NotificationMessage):
        """Notification via WebSocket"""
        message = {
            "type": "notification",
            "notification": asdict(notification),
            "timestamp": datetime.now().isoformat(),
            "developer_info": self.developer_info
        }
        
        for websocket in self.websocket_connections.copy():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erreur WebSocket notification: {e}")
                self.websocket_connections.discard(websocket)
    
    async def add_websocket_connection(self, websocket: WebSocket):
        """Ajout d'une connexion WebSocket"""
        self.websocket_connections.add(websocket)
    
    async def remove_websocket_connection(self, websocket: WebSocket):
        """Suppression d'une connexion WebSocket"""
        self.websocket_connections.discard(websocket)
    
    async def get_notifications(self, limit: int = 100) -> List[NotificationMessage]:
        """Récupération des notifications"""
        notifications = list(self.notifications.values())
        notifications.sort(key=lambda x: x.timestamp, reverse=True)
        return notifications[:limit]
    
    async def get_notification_stats(self) -> Dict[str, Any]:
        """Statistiques des notifications"""
        notifications = list(self.notifications.values())
        
        stats = {
            "total": len(notifications),
            "sent": sum(1 for n in notifications if n.sent),
            "failed": sum(1 for n in notifications if n.error),
            "by_priority": {},
            "by_type": {},
            "recent_24h": sum(1 for n in notifications if (datetime.now() - n.timestamp).days < 1)
        }
        
        # Par priorité
        for priority in NotificationPriority:
            stats["by_priority"][priority.value] = sum(1 for n in notifications if n.priority == priority)
        
        # Par type
        for ntype in NotificationType:
            stats["by_type"][ntype.value] = sum(1 for n in notifications if n.type == ntype)
        
        return stats
    
    async def update_config(self, notification_type: NotificationType, config: NotificationConfig):
        """Mise à jour de la configuration"""
        self.configs[notification_type] = config
        logger.info(f"⚙️ Configuration {notification_type.value} mise à jour")
    
    async def test_notification(self, notification_type: NotificationType) -> bool:
        """Test d'une notification"""
        try:
            test_message = NotificationMessage(
                id=f"test_{int(datetime.now().timestamp())}",
                timestamp=datetime.now(),
                type=notification_type,
                priority=NotificationPriority.MEDIUM,
                title="Test de Notification",
                message="Ceci est un test du système de notification.",
                data={},
                recipients=[]
            )
            
            await self._send_notification_immediate(test_message)
            return True
            
        except Exception as e:
            logger.error(f"Erreur test notification {notification_type.value}: {e}")
            return False
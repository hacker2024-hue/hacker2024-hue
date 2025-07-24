"""
Configuration système pour CyberSec AI Assistant
"""

import os
from typing import List, Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    """Configuration principale du système"""
    
    # Application
    app_name: str = "CyberSec AI Assistant"
    version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    
    # Database
    database_url: str = Field(
        default="postgresql://cybersec:password@localhost/cybersec_ai",
        env="DATABASE_URL"
    )
    
    # Redis Cache
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    
    # AI Model Configuration
    model_name: str = Field(default="microsoft/DialoGPT-large", env="AI_MODEL")
    model_device: str = Field(default="cpu", env="MODEL_DEVICE")  # cpu or cuda
    max_response_length: int = Field(default=512, env="MAX_RESPONSE_LENGTH")
    temperature: float = Field(default=0.7, env="AI_TEMPERATURE")
    
    # Security
    secret_key: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    access_token_expire: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE")  # minutes
    algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    
    # Threat Intelligence
    threat_feeds: List[str] = Field(
        default=[
            "https://feeds.alienvault.com/reputation/generic",
            "https://www.malwaredomainlist.com/hostslist/hosts.txt"
        ],
        env="THREAT_FEEDS"
    )
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Communication
    max_conversation_history: int = Field(default=50, env="MAX_CONVERSATION_HISTORY")
    response_timeout: int = Field(default=30, env="RESPONSE_TIMEOUT")  # seconds
    
    # Analysis
    malware_analysis_enabled: bool = Field(default=True, env="MALWARE_ANALYSIS")
    network_monitoring_enabled: bool = Field(default=True, env="NETWORK_MONITORING")
    vulnerability_scanning_enabled: bool = Field(default=True, env="VULN_SCANNING")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instance globale de configuration
config = Config()
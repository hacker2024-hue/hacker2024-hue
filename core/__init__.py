"""
CyberSec AI Assistant - Core Module
===================================

Moteur principal d'intelligence artificielle pour la cybersécurité.
"""

__version__ = "1.0.0"
__author__ = "Yao Kouakou Luc Annicet"

from .ai_engine import CyberSecAI
from .config import Config

__all__ = ["CyberSecAI", "Config"]
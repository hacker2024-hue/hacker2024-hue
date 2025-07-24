"""
Communication Module - CyberSec AI Assistant
============================================

Interface de communication avancée avec les humains.
"""

from .interface import CommunicationInterface
from .voice_handler import VoiceHandler
from .chat_manager import ChatManager

__all__ = [
    "CommunicationInterface",
    "VoiceHandler", 
    "ChatManager"
]
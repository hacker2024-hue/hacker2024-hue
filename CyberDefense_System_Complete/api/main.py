"""
Application FastAPI principale
==============================

API REST pour CyberSec AI Assistant avec interface WebSocket et REST.
"""

import asyncio
import uvicorn
from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger
import json
from datetime import datetime

from core.ai_engine import CyberSecAI
from core.config import config
from communication.interface import CommunicationInterface, CommunicationMode, UrgencyLevel
from security.threat_analyzer import ThreatAnalyzer
from .routes import router
from .models import *


# Instances globales
ai_engine = None
comm_interface = None
threat_analyzer = None
websocket_connections: Dict[str, WebSocket] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire de cycle de vie de l'application"""
    
    # Initialisation
    logger.info("🚀 Démarrage de CyberSec AI Assistant...")
    
    global ai_engine, comm_interface, threat_analyzer
    
    try:
        # Initialisation du moteur IA
        logger.info("Initialisation du moteur IA...")
        ai_engine = CyberSecAI()
        await ai_engine.initialize()
        
        # Initialisation de l'interface de communication
        logger.info("Initialisation de l'interface de communication...")
        comm_interface = CommunicationInterface(ai_engine)
        await comm_interface.initialize()
        
        # Initialisation de l'analyseur de menaces
        logger.info("Initialisation de l'analyseur de menaces...")
        threat_analyzer = ThreatAnalyzer()
        await threat_analyzer.initialize()
        
        logger.success("✅ CyberSec AI Assistant initialisé avec succès!")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}")
        raise
    
    finally:
        # Nettoyage
        logger.info("🔧 Arrêt de l'application...")
        
        # Fermeture des connexions WebSocket
        for connection in websocket_connections.values():
            try:
                await connection.close()
            except:
                pass
        
        logger.info("👋 Application arrêtée")


# Création de l'application FastAPI
app = FastAPI(
    title="CyberSec AI Assistant",
    description="""
    🛡️ **Système d'Intelligence Artificielle Avancé en Sécurité Informatique**
    
    Une IA sophistiquée capable de:
    - 🔍 Analyser les menaces en temps réel
    - 💬 Communiquer naturellement avec les experts
    - 📊 Fournir des analyses détaillées
    - ⚡ Répondre aux incidents de sécurité
    - 🎯 S'adapter au niveau d'expertise de l'utilisateur
    
    ## Fonctionnalités Principales
    
    ### 🤖 IA Conversationnelle
    - Communication naturelle multilingue
    - Adaptation au niveau d'expertise
    - Contexte de conversation maintenu
    
    ### 🔐 Analyse de Sécurité
    - Détection de malwares et IoCs
    - Corrélation de menaces
    - Scoring de risques automatique
    - Recommandations personnalisées
    
    ### 📡 Communication Temps Réel
    - Interface WebSocket pour chat en direct
    - Escalade automatique des alertes critiques
    - Notifications push
    
    ### 📈 Rapports et Analytics
    - Rapports de menaces détaillés
    - Analyse de tendances
    - Prédictions de sécurité
    """,
    version=config.version,
    contact={
        "name": "hacker2024-hue",
        "url": "https://github.com/hacker2024-hue",
    },
    license_info={
        "name": "MIT License",
    },
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compression Gzip
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Sécurité
security = HTTPBearer()

# Routes
app.include_router(router, prefix="/api/v1")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil avec interface web"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CyberSec AI Assistant 🛡️</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                text-align: center;
            }
            .header {
                margin-bottom: 50px;
            }
            .logo {
                font-size: 4em;
                margin-bottom: 20px;
            }
            .tagline {
                font-size: 1.5em;
                opacity: 0.9;
                margin-bottom: 30px;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin: 50px 0;
            }
            .feature {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            .feature h3 {
                font-size: 1.5em;
                margin-bottom: 15px;
                color: #ffd700;
            }
            .cta {
                margin-top: 50px;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                background: #ffd700;
                color: #333;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                margin: 0 10px;
                transition: transform 0.3s;
            }
            .btn:hover {
                transform: translateY(-3px);
            }
            .status {
                margin-top: 30px;
                padding: 20px;
                background: rgba(0,255,0,0.2);
                border-radius: 10px;
                border: 1px solid rgba(0,255,0,0.5);
            }
            .chat-container {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 20px;
                margin-top: 30px;
                text-align: left;
            }
            #chatMessages {
                height: 300px;
                overflow-y: auto;
                background: rgba(0,0,0,0.3);
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 15px;
            }
            .message {
                margin-bottom: 10px;
                padding: 8px 12px;
                border-radius: 8px;
                max-width: 80%;
            }
            .user-message {
                background: rgba(100,149,237,0.7);
                margin-left: auto;
                text-align: right;
            }
            .ai-message {
                background: rgba(50,205,50,0.7);
            }
            .input-group {
                display: flex;
                gap: 10px;
            }
            #messageInput {
                flex: 1;
                padding: 10px;
                border: none;
                border-radius: 25px;
                background: rgba(255,255,255,0.9);
                color: #333;
            }
            #sendButton {
                padding: 10px 20px;
                background: #ffd700;
                color: #333;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header class="header">
                <div class="logo">🛡️</div>
                <h1>CyberSec AI Assistant</h1>
                <div class="tagline">Intelligence Artificielle Avancée en Cybersécurité</div>
            </header>
            
            <div class="status">
                <h3>🟢 Système Opérationnel</h3>
                <p>Prêt à analyser les menaces et à vous assister</p>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🔍 Analyse de Menaces</h3>
                    <p>Détection automatique de malwares, IoCs et comportements suspects avec corrélation intelligente des indicateurs.</p>
                </div>
                <div class="feature">
                    <h3>💬 Communication Naturelle</h3>
                    <p>Interface conversationnelle adaptée à votre niveau d'expertise, du novice à l'expert en cybersécurité.</p>
                </div>
                <div class="feature">
                    <h3>⚡ Réponse Temps Réel</h3>
                    <p>Escalade automatique des alertes critiques avec recommandations immédiates d'actions à entreprendre.</p>
                </div>
                <div class="feature">
                    <h3>📊 Intelligence Prédictive</h3>
                    <p>Prédiction de menaces futures basée sur l'analyse des tendances et des patterns d'attaque.</p>
                </div>
            </div>
            
            <div class="chat-container">
                <h3>💬 Chat en Direct avec l'IA</h3>
                <div id="chatMessages"></div>
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Posez votre question sur la cybersécurité..." onkeypress="handleKeyPress(event)">
                    <button id="sendButton" onclick="sendMessage()">Envoyer</button>
                </div>
                <p style="font-size: 0.9em; opacity: 0.7; margin-top: 10px;">
                    💡 Exemples: "Analyse cette adresse IP", "Comment détecter un ransomware?", "Que faire en cas d'incident?"
                </p>
            </div>
            
            <div class="cta">
                <a href="/docs" class="btn">📚 Documentation API</a>
                <a href="/api/v1/health" class="btn">🔧 Status Système</a>
            </div>
        </div>
        
        <script>
            // WebSocket pour le chat en temps réel
            let ws = null;
            let currentSessionId = 'session_' + Math.random().toString(36).substr(2, 9);
            
            function connectWebSocket() {
                ws = new WebSocket(`ws://localhost:8000/api/v1/ws/${currentSessionId}`);
                
                ws.onopen = function(event) {
                    console.log('WebSocket connecté');
                    addMessage('Connexion établie avec CyberSec AI Assistant 🛡️', 'ai');
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    addMessage(data.content, 'ai');
                    
                    if (data.urgency === 'critical') {
                        document.body.style.background = 'linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)';
                        setTimeout(() => {
                            document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                        }, 3000);
                    }
                };
                
                ws.onclose = function(event) {
                    console.log('WebSocket fermé');
                    addMessage('Connexion fermée. Tentative de reconnexion...', 'ai');
                    setTimeout(connectWebSocket, 3000);
                };
                
                ws.onerror = function(error) {
                    console.error('Erreur WebSocket:', error);
                    addMessage('Erreur de connexion. Utilisation du mode API REST.', 'ai');
                };
            }
            
            function addMessage(content, sender) {
                const messagesDiv = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = content;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        content: message,
                        user_id: 'web_user',
                        session_id: currentSessionId
                    }));
                } else {
                    // Fallback vers API REST
                    try {
                        const response = await fetch('/api/v1/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                content: message,
                                user_id: 'web_user',
                                session_id: currentSessionId
                            })
                        });
                        
                        const data = await response.json();
                        addMessage(data.content, 'ai');
                    } catch (error) {
                        addMessage('Erreur lors de l\'envoi du message: ' + error.message, 'ai');
                    }
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            // Démarrage automatique
            connectWebSocket();
        </script>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Vérification de l'état du système"""
    
    global ai_engine, comm_interface, threat_analyzer
    
    status = {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": config.version,
        "components": {
            "ai_engine": ai_engine is not None and ai_engine.model is not None,
            "communication_interface": comm_interface is not None,
            "threat_analyzer": threat_analyzer is not None,
            "websocket_connections": len(websocket_connections)
        }
    }
    
    # Vérification des composants critiques
    if not all([ai_engine, comm_interface, threat_analyzer]):
        status["status"] = "degraded"
        raise HTTPException(status_code=503, detail="Certains composants ne sont pas initialisés")
    
    return status


@app.websocket("/api/v1/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """Endpoint WebSocket pour communication en temps réel"""
    
    await websocket.accept()
    websocket_connections[session_id] = websocket
    
    logger.info(f"Nouvelle connexion WebSocket: {session_id}")
    
    try:
        while True:
            # Réception du message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Traitement par l'interface de communication
            response = await comm_interface.process_message(
                content=message_data.get("content"),
                user_id=message_data.get("user_id", "anonymous"),
                session_id=session_id,
                mode=CommunicationMode.TEXT
            )
            
            # Envoi de la réponse
            await websocket.send_text(json.dumps({
                "content": response.content,
                "urgency": response.urgency.value,
                "recommendations": response.recommendations,
                "follow_up_questions": response.follow_up_questions,
                "timestamp": response.timestamp.isoformat()
            }))
            
    except WebSocketDisconnect:
        logger.info(f"Connexion WebSocket fermée: {session_id}")
        if session_id in websocket_connections:
            del websocket_connections[session_id]
        
        # Fermeture de la session
        if comm_interface:
            await comm_interface.close_session(session_id)


# Fonction utilitaire pour obtenir les instances globales
def get_ai_engine() -> CyberSecAI:
    """Dépendance pour obtenir le moteur IA"""
    if ai_engine is None:
        raise HTTPException(status_code=503, detail="Moteur IA non initialisé")
    return ai_engine


def get_comm_interface() -> CommunicationInterface:
    """Dépendance pour obtenir l'interface de communication"""
    if comm_interface is None:
        raise HTTPException(status_code=503, detail="Interface de communication non initialisée")
    return comm_interface


def get_threat_analyzer() -> ThreatAnalyzer:
    """Dépendance pour obtenir l'analyseur de menaces"""
    if threat_analyzer is None:
        raise HTTPException(status_code=503, detail="Analyseur de menaces non initialisé")
    return threat_analyzer


async def send_notification(user_id: str, message: str, urgency: str = "medium"):
    """Envoi de notification via WebSocket si connecté"""
    
    # Recherche de la session active de l'utilisateur
    for session_id, ws in websocket_connections.items():
        try:
            await ws.send_text(json.dumps({
                "type": "notification",
                "content": message,
                "urgency": urgency,
                "timestamp": datetime.utcnow().isoformat()
            }))
        except:
            # Connexion fermée, nettoyage
            if session_id in websocket_connections:
                del websocket_connections[session_id]


if __name__ == "__main__":
    # Démarrage en mode développement
    uvicorn.run(
        "api.main:app",
        host=config.api_host,
        port=config.api_port,
        reload=config.debug,
        workers=1 if config.debug else config.api_workers,
        log_level=config.log_level.lower()
    )
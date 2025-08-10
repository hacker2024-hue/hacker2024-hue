#!/usr/bin/env python3
"""
Interface d'Authentification
===========================

Interface utilisateur pour l'authentification avec protection par mot de passe.
"""

import asyncio
import json
from typing import Dict, Optional
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from security.access_protection import AccessProtection, access_protection

# Modèles Pydantic
class LoginRequest(BaseModel):
    password: str

class TokenResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    developer_info: Dict

class SecurityResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None

# Sécurité HTTP
security = HTTPBearer()

class AuthInterface:
    """
    Interface d'authentification
    """
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.templates = Jinja2Templates(directory="templates")
        self.access_protection = access_protection
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license": "CI-CYBER-2024-001"
        }
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Configuration des routes d'authentification"""
        
        @self.app.get("/auth", response_class=HTMLResponse)
        async def auth_page(request: Request):
            """Page d'authentification"""
            return self.templates.TemplateResponse("auth.html", {
                "request": request,
                "developer": self.developer_info
            })
        
        @self.app.post("/api/auth/login", response_model=TokenResponse)
        async def login(request: Request, login_data: LoginRequest):
            """Authentification"""
            ip_address = request.client.host
            user_agent = request.headers.get("user-agent", "")
            
            success, message, token = await self.access_protection.authenticate(
                login_data.password, ip_address, user_agent
            )
            
            return TokenResponse(
                success=success,
                message=message,
                token=token,
                developer_info=self.developer_info
            )
        
        @self.app.post("/api/auth/logout", response_model=SecurityResponse)
        async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
            """Déconnexion"""
            token = credentials.credentials
            success = await self.access_protection.revoke_token(token)
            
            return SecurityResponse(
                success=success,
                message="Déconnexion réussie" if success else "Erreur lors de la déconnexion"
            )
        
        @self.app.get("/api/auth/validate", response_model=SecurityResponse)
        async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
            """Validation de token"""
            token = credentials.credentials
            valid, message, access_token = await self.access_protection.validate_token(token, "127.0.0.1")
            
            return SecurityResponse(
                success=valid,
                message=message,
                data={"permissions": access_token.permissions if access_token else None}
            )
        
        @self.app.get("/api/auth/stats", response_model=SecurityResponse)
        async def get_security_stats(credentials: HTTPAuthorizationCredentials = Depends(security)):
            """Statistiques de sécurité"""
            token = credentials.credentials
            valid, message, access_token = await self.access_protection.validate_token(token, "127.0.0.1")
            
            if not valid:
                raise HTTPException(status_code=401, detail=message)
            
            stats = await self.access_protection.get_security_stats()
            
            return SecurityResponse(
                success=True,
                message="Statistiques récupérées",
                data=stats
            )
        
        @self.app.get("/api/auth/events", response_model=SecurityResponse)
        async def get_security_events(
            limit: int = 50,
            credentials: HTTPAuthorizationCredentials = Depends(security)
        ):
            """Événements de sécurité"""
            token = credentials.credentials
            valid, message, access_token = await self.access_protection.validate_token(token, "127.0.0.1")
            
            if not valid:
                raise HTTPException(status_code=401, detail=message)
            
            events = await self.access_protection.get_security_events(limit)
            
            return SecurityResponse(
                success=True,
                message=f"{len(events)} événements récupérés",
                data={"events": events}
            )

# Template HTML pour l'authentification
AUTH_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔐 Authentification - Système de Défense Cybernétique</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .auth-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
            text-align: center;
        }
        
        .logo {
            font-size: 3em;
            margin-bottom: 20px;
        }
        
        .title {
            color: #333;
            font-size: 1.5em;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .success {
            background: #efe;
            color: #3c3;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .developer-info {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e1e5e9;
            color: #666;
            font-size: 0.9em;
        }
        
        .developer-info h4 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .developer-info p {
            margin-bottom: 5px;
        }
        
        .developer-info a {
            color: #667eea;
            text-decoration: none;
        }
        
        .security-notice {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #ffc107;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin-top: 10px;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="logo">🔐</div>
        <h1 class="title">Système de Défense Cybernétique</h1>
        <p class="subtitle">Authentification requise</p>
        
        <div class="security-notice">
            <strong>⚠️ Sécurité renforcée</strong><br>
            Accès protégé par mot de passe pour éviter le téléchargement non autorisé.
        </div>
        
        <div class="error" id="error-message"></div>
        <div class="success" id="success-message"></div>
        
        <form id="auth-form">
            <div class="form-group">
                <label for="password">Mot de passe</label>
                <input type="password" id="password" name="password" required 
                       placeholder="Entrez le mot de passe">
            </div>
            
            <button type="submit" class="btn" id="login-btn">
                🔓 Se connecter
            </button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Authentification en cours...</p>
        </div>
        
        <div class="developer-info">
            <h4>👨‍💻 Développé par</h4>
            <p><strong>{{ developer.name }}</strong></p>
            <p>📞 <a href="tel:{{ developer.phone }}">{{ developer.phone }}</a></p>
            <p>📧 <a href="mailto:{{ developer.email }}">{{ developer.email }}</a></p>
            <p>🔐 Licence: {{ developer.license }}</p>
        </div>
    </div>
    
    <script>
        document.getElementById('auth-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const loginBtn = document.getElementById('login-btn');
            const loading = document.getElementById('loading');
            const errorDiv = document.getElementById('error-message');
            const successDiv = document.getElementById('success-message');
            
            // Masquer les messages précédents
            errorDiv.style.display = 'none';
            successDiv.style.display = 'none';
            
            // Afficher le loading
            loginBtn.disabled = true;
            loading.style.display = 'block';
            
            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ password: password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Stocker le token
                    localStorage.setItem('auth_token', data.token);
                    
                    // Afficher le succès
                    successDiv.textContent = data.message;
                    successDiv.style.display = 'block';
                    
                    // Rediriger vers le dashboard
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1500);
                    
                } else {
                    // Afficher l'erreur
                    errorDiv.textContent = data.message;
                    errorDiv.style.display = 'block';
                }
                
            } catch (error) {
                errorDiv.textContent = 'Erreur de connexion. Veuillez réessayer.';
                errorDiv.style.display = 'block';
            } finally {
                // Masquer le loading
                loginBtn.disabled = false;
                loading.style.display = 'none';
            }
        });
        
        // Vérifier si déjà connecté
        window.addEventListener('load', function() {
            const token = localStorage.getItem('auth_token');
            if (token) {
                // Vérifier la validité du token
                fetch('/api/auth/validate', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Token valide, rediriger
                        window.location.href = '/dashboard';
                    } else {
                        // Token invalide, le supprimer
                        localStorage.removeItem('auth_token');
                    }
                })
                .catch(() => {
                    localStorage.removeItem('auth_token');
                });
            }
        });
    </script>
</body>
</html>
"""

# Création du template
def create_auth_template():
    """Création du template d'authentification"""
    import os
    
    # Créer le répertoire templates s'il n'existe pas
    os.makedirs("templates", exist_ok=True)
    
    # Écrire le template
    with open("templates/auth.html", "w", encoding="utf-8") as f:
        f.write(AUTH_HTML_TEMPLATE)

# Création automatique du template
create_auth_template()
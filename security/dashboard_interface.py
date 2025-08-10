"""
Dashboard Interface Avancé
==========================

Interface graphique moderne pour le système de défense cybernétique
avec visualisations en temps réel et informations du développeur.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import plotly.graph_objs as go
import plotly.utils
import pandas as pd
import numpy as np

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DashboardMetrics:
    """Métriques du dashboard"""
    total_threats: int
    active_threats: int
    blocked_threats: int
    ai_accuracy: float
    response_time: float
    network_throughput: float
    cpu_usage: float
    memory_usage: float
    global_risk_level: str
    last_update: datetime

@dataclass
class ThreatTimeline:
    """Timeline des menaces"""
    timestamp: datetime
    threat_type: str
    source_ip: str
    destination_ip: str
    threat_level: str
    country: str
    description: str

class DashboardInterface:
    """
    Interface de dashboard avancé
    """
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.templates = Jinja2Templates(directory="templates")
        
        # Informations du développeur
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "title": "Expert en Cybersécurité",
            "contacts": {
                "primary": "hackerduckman89@gmail.com",
                "secondary": "yao.kouakou.dev@gmail.com"
            },
            "version": "2.0.0 - Edition Mondiale",
            "description": "Développeur du Système Mondial de Défense Cybernétique",
            "expertise": [
                "Intelligence Artificielle",
                "Cybersécurité",
                "Développement de Systèmes",
                "Analyse de Menaces",
                "Protection Proactive"
            ]
        }
        
        # Données simulées pour les graphiques
        self.sample_data = self._generate_sample_data()
        
        # Configuration des routes
        self._setup_routes()
    
    def _generate_sample_data(self) -> Dict[str, Any]:
        """Génération de données d'exemple pour les graphiques"""
        # Données des 24 dernières heures
        hours = 24
        timestamps = [datetime.now() - timedelta(hours=i) for i in range(hours, 0, -1)]
        
        # Menaces par heure
        threats_per_hour = np.random.poisson(15, hours)  # Moyenne de 15 menaces/heure
        
        # Types de menaces
        threat_types = ["APT", "DDoS", "Malware", "Phishing", "Ransomware", "Insider"]
        threat_counts = np.random.multinomial(100, [0.2, 0.3, 0.25, 0.15, 0.05, 0.05])
        
        # Pays d'origine
        countries = ["China", "Russia", "USA", "North Korea", "Iran", "Others"]
        country_counts = np.random.multinomial(100, [0.3, 0.25, 0.2, 0.1, 0.1, 0.05])
        
        # Performance IA
        ai_accuracy = np.random.normal(0.94, 0.02, hours)
        ai_accuracy = np.clip(ai_accuracy, 0.85, 0.99)
        
        # Utilisation système
        cpu_usage = np.random.normal(0.45, 0.1, hours)
        cpu_usage = np.clip(cpu_usage, 0.2, 0.8)
        
        memory_usage = np.random.normal(0.6, 0.15, hours)
        memory_usage = np.clip(memory_usage, 0.3, 0.9)
        
        return {
            "timestamps": timestamps,
            "threats_per_hour": threats_per_hour.tolist(),
            "threat_types": dict(zip(threat_types, threat_counts.tolist())),
            "countries": dict(zip(countries, country_counts.tolist())),
            "ai_accuracy": ai_accuracy.tolist(),
            "cpu_usage": cpu_usage.tolist(),
            "memory_usage": memory_usage.tolist()
        }
    
    def _setup_routes(self):
        """Configuration des routes du dashboard"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home(request: Request):
            """Page d'accueil du dashboard"""
            return await self._render_dashboard(request)
        
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard_main(request: Request):
            """Dashboard principal"""
            return await self._render_dashboard(request)
        
        @self.app.get("/dashboard/metrics")
        async def get_dashboard_metrics():
            """API pour les métriques du dashboard"""
            return await self._get_current_metrics()
        
        @self.app.get("/dashboard/charts")
        async def get_dashboard_charts():
            """API pour les graphiques"""
            return await self._generate_charts()
        
        @self.app.get("/dashboard/developer")
        async def get_developer_info():
            """API pour les informations du développeur"""
            return self.developer_info
    
    async def _render_dashboard(self, request: Request) -> HTMLResponse:
        """Rendu du dashboard principal"""
        try:
            # Génération des graphiques
            charts = await self._generate_charts()
            
            # Métriques actuelles
            metrics = await self._get_current_metrics()
            
            # Données pour le template
            context = {
                "request": request,
                "developer": self.developer_info,
                "metrics": metrics,
                "charts": charts,
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "system_status": "OPERATIONAL",
                "version": self.developer_info["version"]
            }
            
            # Rendu du template HTML
            html_content = self._generate_dashboard_html(context)
            return HTMLResponse(content=html_content, status_code=200)
            
        except Exception as e:
            logger.error(f"Erreur rendu dashboard: {e}")
            return HTMLResponse(content=self._generate_error_html(str(e)), status_code=500)
    
    async def _get_current_metrics(self) -> DashboardMetrics:
        """Récupération des métriques actuelles"""
        # Simulation de métriques en temps réel
        total_threats = sum(self.sample_data["threats_per_hour"])
        active_threats = np.random.randint(5, 25)
        blocked_threats = int(total_threats * 0.85)  # 85% de blocage
        
        return DashboardMetrics(
            total_threats=total_threats,
            active_threats=active_threats,
            blocked_threats=blocked_threats,
            ai_accuracy=np.random.uniform(0.92, 0.97),
            response_time=np.random.uniform(1.5, 3.0),
            network_throughput=np.random.uniform(100, 500),
            cpu_usage=np.random.uniform(0.3, 0.7),
            memory_usage=np.random.uniform(0.4, 0.8),
            global_risk_level=np.random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
            last_update=datetime.now()
        )
    
    async def _generate_charts(self) -> Dict[str, str]:
        """Génération des graphiques"""
        charts = {}
        
        try:
            # Graphique 1: Menaces par heure
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=[t.strftime("%H:%M") for t in self.sample_data["timestamps"]],
                y=self.sample_data["threats_per_hour"],
                mode='lines+markers',
                name='Menaces',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=8)
            ))
            fig1.update_layout(
                title="Menaces Détectées (24h)",
                xaxis_title="Heure",
                yaxis_title="Nombre de Menaces",
                template="plotly_white",
                height=400
            )
            charts["threats_timeline"] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
            
            # Graphique 2: Types de menaces
            fig2 = go.Figure(data=[go.Pie(
                labels=list(self.sample_data["threat_types"].keys()),
                values=list(self.sample_data["threat_types"].values()),
                hole=0.4,
                marker_colors=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
            )])
            fig2.update_layout(
                title="Répartition par Type de Menace",
                template="plotly_white",
                height=400
            )
            charts["threat_types"] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            
            # Graphique 3: Pays d'origine
            fig3 = go.Figure(data=[go.Bar(
                x=list(self.sample_data["countries"].keys()),
                y=list(self.sample_data["countries"].values()),
                marker_color='#74b9ff'
            )])
            fig3.update_layout(
                title="Menaces par Pays d'Origine",
                xaxis_title="Pays",
                yaxis_title="Nombre de Menaces",
                template="plotly_white",
                height=400
            )
            charts["countries"] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
            
            # Graphique 4: Performance IA
            fig4 = go.Figure()
            fig4.add_trace(go.Scatter(
                x=[t.strftime("%H:%M") for t in self.sample_data["timestamps"]],
                y=[acc * 100 for acc in self.sample_data["ai_accuracy"]],
                mode='lines+markers',
                name='Précision IA',
                line=dict(color='#00b894', width=3),
                marker=dict(size=6)
            ))
            fig4.update_layout(
                title="Performance IA (Précision %)",
                xaxis_title="Heure",
                yaxis_title="Précision (%)",
                template="plotly_white",
                height=400
            )
            charts["ai_performance"] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
            
            # Graphique 5: Utilisation système
            fig5 = go.Figure()
            fig5.add_trace(go.Scatter(
                x=[t.strftime("%H:%M") for t in self.sample_data["timestamps"]],
                y=[cpu * 100 for cpu in self.sample_data["cpu_usage"]],
                mode='lines+markers',
                name='CPU',
                line=dict(color='#e17055', width=3)
            ))
            fig5.add_trace(go.Scatter(
                x=[t.strftime("%H:%M") for t in self.sample_data["timestamps"]],
                y=[mem * 100 for mem in self.sample_data["memory_usage"]],
                mode='lines+markers',
                name='Mémoire',
                line=dict(color='#6c5ce7', width=3)
            ))
            fig5.update_layout(
                title="Utilisation Système",
                xaxis_title="Heure",
                yaxis_title="Utilisation (%)",
                template="plotly_white",
                height=400
            )
            charts["system_usage"] = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
            
        except Exception as e:
            logger.error(f"Erreur génération graphiques: {e}")
            charts = {"error": str(e)}
        
        return charts
    
    def _generate_dashboard_html(self, context: Dict[str, Any]) -> str:
        """Génération du HTML du dashboard"""
        metrics = context["metrics"]
        charts = context["charts"]
        developer = context["developer"]
        
        return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Système Mondial de Défense Cybernétique - Yao Kouakou</title>
    
    <!-- Plotly.js -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            color: #2d3436;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-align: center;
        }}
        
        .header .subtitle {{
            color: #636e72;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }}
        
        .developer-info {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .developer-info h3 {{
            font-size: 1.3rem;
            margin-bottom: 10px;
        }}
        
        .developer-info p {{
            margin: 5px 0;
            font-size: 0.95rem;
        }}
        
        .developer-info a {{
            color: #74b9ff;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .developer-info a:hover {{
            text-decoration: underline;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        
        .metric-icon {{
            font-size: 2.5rem;
            margin-bottom: 15px;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            color: #636e72;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .chart-title {{
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: #2d3436;
            text-align: center;
        }}
        
        .status-bar {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00b894;
            margin-right: 10px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9rem;
        }}
        
        .footer a {{
            color: #74b9ff;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            .metrics-grid {{
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🌐 Système Mondial de Défense Cybernétique</h1>
            <p class="subtitle">Protection proactive contre les cyberattaques en temps réel</p>
            
            <div class="developer-info">
                <h3>👨‍💻 Développé par: {developer['name']}</h3>
                <p><strong>Expertise:</strong> {', '.join(developer['expertise'])}</p>
                <p><strong>Contact Principal:</strong> <a href="mailto:{developer['contacts']['primary']}">{developer['contacts']['primary']}</a></p>
                <p><strong>Contact Secondaire:</strong> <a href="mailto:{developer['contacts']['secondary']}">{developer['contacts']['secondary']}</a></p>
                <p><strong>Version:</strong> {developer['version']}</p>
            </div>
        </div>
        
        <!-- Métriques -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-icon">⚠️</div>
                <div class="metric-value">{metrics.total_threats}</div>
                <div class="metric-label">Menaces Totales</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">🔥</div>
                <div class="metric-value">{metrics.active_threats}</div>
                <div class="metric-label">Menaces Actives</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">🛡️</div>
                <div class="metric-value">{metrics.blocked_threats}</div>
                <div class="metric-label">Menaces Bloquées</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">🧠</div>
                <div class="metric-value">{metrics.ai_accuracy:.1%}</div>
                <div class="metric-label">Précision IA</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">⚡</div>
                <div class="metric-value">{metrics.response_time:.1f}s</div>
                <div class="metric-label">Temps de Réponse</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon">🌍</div>
                <div class="metric-value">{metrics.global_risk_level}</div>
                <div class="metric-label">Risque Global</div>
            </div>
        </div>
        
        <!-- Graphiques -->
        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-title">📈 Menaces Détectées (24h)</div>
                <div id="threats-timeline"></div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">🍰 Types de Menaces</div>
                <div id="threat-types"></div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">🌍 Menaces par Pays</div>
                <div id="countries"></div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">🧠 Performance IA</div>
                <div id="ai-performance"></div>
            </div>
            
            <div class="chart-card">
                <div class="chart-title">💻 Utilisation Système</div>
                <div id="system-usage"></div>
            </div>
        </div>
        
        <!-- Barre de statut -->
        <div class="status-bar">
            <span class="status-indicator"></span>
            <strong>Système Opérationnel</strong> | 
            Dernière mise à jour: {context['current_time']} | 
            <a href="/docs" target="_blank">📚 API Documentation</a> | 
            <a href="/world-map" target="_blank">🌍 Carte Mondiale</a>
        </div>
    </div>
    
    <!-- Scripts -->
    <script>
        // Chargement des graphiques
        document.addEventListener('DOMContentLoaded', function() {{
            const charts = {charts};
            
            if (charts.threats_timeline) {{
                Plotly.newPlot('threats-timeline', JSON.parse(charts.threats_timeline).data, JSON.parse(charts.threats_timeline).layout);
            }}
            
            if (charts.threat_types) {{
                Plotly.newPlot('threat-types', JSON.parse(charts.threat_types).data, JSON.parse(charts.threat_types).layout);
            }}
            
            if (charts.countries) {{
                Plotly.newPlot('countries', JSON.parse(charts.countries).data, JSON.parse(charts.countries).layout);
            }}
            
            if (charts.ai_performance) {{
                Plotly.newPlot('ai-performance', JSON.parse(charts.ai_performance).data, JSON.parse(charts.ai_performance).layout);
            }}
            
            if (charts.system_usage) {{
                Plotly.newPlot('system-usage', JSON.parse(charts.system_usage).data, JSON.parse(charts.system_usage).layout);
            }}
        }});
        
        // Auto-refresh toutes les 30 secondes
        setInterval(function() {{
            location.reload();
        }}, 30000);
    </script>
    
    <div class="footer">
        <p>🌐 Système Mondial de Défense Cybernétique | 
        Développé avec passion par <a href="mailto:{developer['contacts']['primary']}">{developer['name']}</a> | 
        Version {developer['version']}</p>
    </div>
</body>
</html>
"""
    
    def _generate_error_html(self, error_message: str) -> str:
        """Génération de la page d'erreur"""
        return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Erreur - Système de Défense Cybernétique</title>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }}
        .error-container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            max-width: 500px;
        }}
        .error-icon {{
            font-size: 4rem;
            margin-bottom: 20px;
        }}
        .error-title {{
            font-size: 1.5rem;
            margin-bottom: 15px;
        }}
        .error-message {{
            margin-bottom: 20px;
            opacity: 0.9;
        }}
        .contact-info {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }}
        .contact-info a {{
            color: #74b9ff;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <div class="error-title">Erreur du Dashboard</div>
        <div class="error-message">{error_message}</div>
        <div class="contact-info">
            <p>Contactez le développeur:</p>
            <p><a href="mailto:hackerduckman89@gmail.com">hackerduckman89@gmail.com</a></p>
            <p><a href="mailto:yao.kouakou.dev@gmail.com">yao.kouakou.dev@gmail.com</a></p>
        </div>
    </div>
</body>
</html>
"""
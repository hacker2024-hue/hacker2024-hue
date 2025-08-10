# 🌐 Système Mondial de Détection et Protection contre les Cyberattaques

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com)
[![Redis](https://img.shields.io/badge/Redis-6.0%2B-red.svg)](https://redis.io)
[![Scapy](https://img.shields.io/badge/Scapy-2.5%2B-orange.svg)](https://scapy.net)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Vue d'ensemble

Le **Système Mondial de Détection et Protection contre les Cyberattaques** est une solution de cybersécurité avancée qui combine :

- 🔍 **Détection en temps réel** des menaces cybernétiques
- 🛡️ **Protection proactive** avec réponse automatique
- 📡 **Surveillance réseau** avancée avec capture de paquets
- 🧠 **Intelligence artificielle** pour l'analyse comportementale
- 🌐 **Corrélation globale** des menaces
- ⚡ **Réponse automatique** aux incidents

## ✨ Fonctionnalités Principales

### 🔍 Détection Globale des Menaces
- **Analyse en temps réel** du trafic réseau
- **Corrélation d'indicateurs** de compromission (IoCs)
- **Détection d'anomalies** comportementales
- **Intégration de flux** de menaces externes
- **Scoring de risques** automatique
- **Mapping MITRE ATT&CK** des techniques d'attaque

### 🛡️ Protection Proactive
- **Blocage automatique** d'IPs malveillantes
- **Isolation d'endpoints** compromis
- **Mise en quarantaine** de fichiers suspects
- **Terminaison de processus** malveillants
- **Mise à jour de firewalls** en temps réel
- **Sauvegarde automatique** des données critiques

### 📊 Surveillance Réseau Avancée
- **Capture de paquets** en temps réel
- **Analyse de flux** réseau
- **Détection de scans** de ports
- **Identification d'attaques** DDoS
- **Monitoring de protocoles** suspects
- **Géolocalisation** des menaces

### 🧠 Intelligence Artificielle
- **Machine Learning** pour la détection d'anomalies
- **Analyse comportementale** des utilisateurs
- **Prédiction de menaces** basée sur l'historique
- **Classification automatique** des attaques
- **Optimisation continue** des modèles

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CyberDefense System - Architecture                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🌐 Interface Web & API REST                                               │
│     ├── Dashboard temps réel                                               │
│     ├── API REST complète                                                  │
│     ├── WebSocket pour notifications                                       │
│     └── Documentation interactive                                          │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  🧠 Moteur Principal de Défense                                            │
│     ├── Orchestration des composants                                       │
│     ├── Gestion des alertes                                                │
│     ├── Collecte de métriques                                              │
│     └── Corrélation des menaces                                            │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  🔍 Détection Globale des Menaces                                          │
│     ├── Analyse d'événements réseau                                        │
│     ├── Intégration de flux de menaces                                     │
│     ├── Corrélation d'indicateurs                                          │
│     └── Détection d'anomalies                                              │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  🛡️ Protection Proactive                                                   │
│     ├── Blocage d'IPs                                                      │
│     ├── Isolation d'endpoints                                              │
│     ├── Mise en quarantaine                                                │
│     └── Réponse aux incidents                                              │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  📡 Surveillance Réseau                                                    │
│     ├── Capture de paquets                                                 │
│     ├── Analyse de flux                                                    │
│     ├── Détection d'anomalies                                              │
│     └── Statistiques réseau                                                │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  💾 Stockage & Cache                                                       │
│     ├── Redis (cache & sessions)                                           │
│     ├── PostgreSQL (données persistantes)                                  │
│     ├── Elasticsearch (logs & recherche)                                   │
│     └── Système de fichiers (captures)                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📦 Installation

### Prérequis

- **Python 3.8+**
- **Redis 6.0+**
- **Permissions root** (pour la capture de paquets)
- **Interface réseau** configurée

### Installation Rapide

```bash
# 1. Cloner le repository
git clone <repository-url>
cd cyber-defense-system

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Démarrer Redis
sudo systemctl start redis

# 4. Créer un template de configuration
python launch_cyber_defense.py --create-config

# 5. Démarrer le système
sudo python launch_cyber_defense.py
```

### Installation Détaillée

#### 1. Préparation de l'environnement

```bash
# Créer un environnement virtuel
python -m venv cyber_defense_env
source cyber_defense_env/bin/activate  # Linux/Mac
# ou
cyber_defense_env\Scripts\activate     # Windows

# Mettre à jour pip
pip install --upgrade pip
```

#### 2. Installation des dépendances

```bash
# Installation des packages Python
pip install -r requirements.txt

# Installation des outils système (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y redis-server tcpdump wireshark nmap

# Installation des outils système (CentOS/RHEL)
sudo yum install -y redis tcpdump wireshark nmap
```

#### 3. Configuration de Redis

```bash
# Démarrer Redis
sudo systemctl start redis
sudo systemctl enable redis

# Vérifier que Redis fonctionne
redis-cli ping
# Réponse attendue: PONG
```

#### 4. Configuration du système

```bash
# Créer un template de configuration
python launch_cyber_defense.py --create-config

# Éditer la configuration selon vos besoins
nano cyber_defense_config.json
```

## 🚀 Utilisation

### Démarrage Rapide

```bash
# Démarrage avec configuration par défaut
sudo python launch_cyber_defense.py

# Démarrage avec configuration personnalisée
sudo python launch_cyber_defense.py -c cyber_defense_config.json

# Démarrage sans capture de paquets (mode test)
python launch_cyber_defense.py --no-capture
```

### Vérification des Prérequis

```bash
# Vérifier que tout est prêt
python launch_cyber_defense.py --check-only
```

### Mode Debug

```bash
# Démarrage avec logs détaillés
sudo python launch_cyber_defense.py --debug
```

## 📊 Interface Web

Une fois le système démarré, accédez à :

- **Dashboard principal** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Interface interactive** : http://localhost:8000/redoc
- **WebSocket** : ws://localhost:8000/ws

## 🔧 Configuration

### Fichier de Configuration

Le système utilise un fichier JSON pour la configuration :

```json
{
  "redis_url": "redis://localhost:6379",
  "network_interface": "eth0",
  "api_host": "0.0.0.0",
  "api_port": 8000,
  "websocket_enabled": true,
  "auto_response_enabled": true,
  "threat_feed_update_interval": 300,
  "metrics_collection_interval": 30,
  "alert_retention_days": 30,
  "max_concurrent_incidents": 100,
  "emergency_threshold": 10,
  "capture_packets": true,
  "enable_ai_analysis": true,
  "enable_global_sharing": true,
  "enable_auto_mitigation": true
}
```

### Variables d'Environnement

Vous pouvez également utiliser des variables d'environnement :

```bash
export CYBER_DEFENSE_REDIS_URL="redis://localhost:6379"
export CYBER_DEFENSE_NETWORK_INTERFACE="eth0"
export CYBER_DEFENSE_API_PORT="8000"
export CYBER_DEFENSE_DEBUG="true"
```

## 🔌 API REST

### Endpoints Principaux

#### Statut du Système
```http
GET /status
```

#### Menaces Actives
```http
GET /threats
GET /threats/statistics
```

#### Incidents
```http
GET /incidents
```

#### Protection
```http
GET /protection/status
```

#### Réseau
```http
GET /network/statistics
GET /network/flows
GET /network/anomalies
```

#### Alertes
```http
GET /alerts
```

#### Métriques
```http
GET /metrics
```

#### Simulation de Menace
```http
POST /threats/simulate
Content-Type: application/json

{
  "source_ip": "192.168.1.100",
  "destination_ip": "10.0.0.1",
  "source_port": 12345,
  "destination_port": 80,
  "protocol": "tcp",
  "threat_score": 0.8
}
```

## 📡 WebSocket

Le système fournit des notifications en temps réel via WebSocket :

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'threat_detected':
            console.log('Menace détectée:', data.threat);
            break;
        case 'incident_response':
            console.log('Réponse incident:', data.incident);
            break;
        case 'network_anomaly':
            console.log('Anomalie réseau:', data.anomaly);
            break;
        case 'system_alert':
            console.log('Alerte système:', data.alert);
            break;
    }
};
```

## 🧪 Tests

### Simulation de Menaces

```bash
# Simulation d'une attaque DDoS
curl -X POST http://localhost:8000/threats/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.1",
    "source_port": 12345,
    "destination_port": 80,
    "protocol": "tcp",
    "payload_size": 1500,
    "threat_score": 0.9,
    "attack_type": "ddos"
  }'

# Simulation d'une attaque APT
curl -X POST http://localhost:8000/threats/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "203.0.113.1",
    "destination_ip": "10.0.0.1",
    "source_port": 12345,
    "destination_port": 22,
    "protocol": "tcp",
    "threat_score": 0.8,
    "attack_type": "apt"
  }'
```

### Tests Automatisés

```bash
# Exécuter les tests
pytest tests/

# Tests avec couverture
pytest --cov=security tests/

# Tests spécifiques
pytest tests/test_threat_detection.py
pytest tests/test_protection.py
pytest tests/test_network_monitor.py
```

## 📈 Monitoring

### Métriques Disponibles

- **CPU Usage** : Utilisation du processeur
- **Memory Usage** : Utilisation de la mémoire
- **Disk Usage** : Utilisation du disque
- **Network Throughput** : Débit réseau
- **Active Threats** : Nombre de menaces actives
- **Active Incidents** : Nombre d'incidents actifs
- **Blocked IPs** : Nombre d'IPs bloquées
- **Anomalies Detected** : Nombre d'anomalies détectées

### Logs

Les logs sont disponibles dans :
- **Fichier** : `cyber_defense.log`
- **Console** : Sortie standard
- **Syslog** : `/var/log/syslog` (Linux)

### Alertes

Le système génère différents types d'alertes :
- **INFO** : Informations générales
- **WARNING** : Avertissements
- **CRITICAL** : Problèmes critiques
- **EMERGENCY** : Situations d'urgence

## 🔒 Sécurité

### Bonnes Pratiques

1. **Exécuter en tant que service** dédié
2. **Limiter les permissions** réseau
3. **Chiffrer les communications** sensibles
4. **Sauvegarder régulièrement** les données
5. **Monitorer les logs** système
6. **Mettre à jour régulièrement** les flux de menaces

### Configuration Sécurisée

```json
{
  "security": {
    "enable_encryption": true,
    "enable_authentication": true,
    "enable_authorization": true,
    "enable_audit_logging": true,
    "enable_rate_limiting": true,
    "max_connections": 1000,
    "session_timeout": 3600
  }
}
```

## 🚨 Dépannage

### Problèmes Courants

#### Redis non accessible
```bash
# Vérifier que Redis fonctionne
sudo systemctl status redis

# Redémarrer Redis
sudo systemctl restart redis

# Vérifier la connectivité
redis-cli ping
```

#### Permissions réseau insuffisantes
```bash
# Vérifier les permissions
ls -la /dev/bpf*

# Donner les permissions nécessaires
sudo chmod 644 /dev/bpf*
```

#### Interface réseau non trouvée
```bash
# Lister les interfaces disponibles
ip addr show

# Modifier la configuration
# Dans cyber_defense_config.json, changer "network_interface"
```

#### Erreurs de capture de paquets
```bash
# Vérifier les permissions root
whoami

# Démarrer avec sudo
sudo python launch_cyber_defense.py

# Ou désactiver la capture
python launch_cyber_defense.py --no-capture
```

### Logs de Débogage

```bash
# Activer le mode debug
python launch_cyber_defense.py --debug

# Consulter les logs
tail -f cyber_defense.log

# Filtrer les erreurs
grep "ERROR" cyber_defense.log
```

## 🤝 Contribution

### Développement

1. **Fork** le repository
2. **Créer** une branche feature
3. **Développer** les fonctionnalités
4. **Tester** avec `pytest`
5. **Soumettre** une pull request

### Tests

```bash
# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Exécuter les tests
pytest

# Vérifier la qualité du code
black security/
flake8 security/
mypy security/
```

### Documentation

- **Code** : Docstrings Python
- **API** : Documentation automatique FastAPI
- **Architecture** : Diagrammes et schémas
- **Utilisation** : Exemples et tutoriels

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

### Ressources

- **Documentation** : [Wiki du projet](wiki-url)
- **Issues** : [GitHub Issues](issues-url)
- **Discussions** : [GitHub Discussions](discussions-url)
- **Email** : support@cyberdefense.com

### Communauté

- **Forum** : [Forum communautaire](forum-url)
- **Slack** : [Slack workspace](slack-url)
- **Discord** : [Discord server](discord-url)

## 🔮 Roadmap

### Version 1.1
- [ ] Interface graphique avancée
- [ ] Intégration avec SIEM
- [ ] Support des conteneurs Docker
- [ ] API GraphQL

### Version 1.2
- [ ] Machine Learning avancé
- [ ] Détection de ransomwares
- [ ] Analyse de malware
- [ ] Threat hunting automatisé

### Version 2.0
- [ ] Architecture distribuée
- [ ] Support multi-cloud
- [ ] Intelligence artificielle avancée
- [ ] Intégration blockchain

---

**🌐 Système Mondial de Détection et Protection contre les Cyberattaques**

*Protection intelligente pour un monde numérique sécurisé*
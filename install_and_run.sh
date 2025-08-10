#!/bin/bash

# Système Mondial de Détection et Protection contre les Cyberattaques
# Développé par: Yao Kouakou Luc Anicet
# Contact: hackerduckman89@gmail.com
# Contact: yao.kouakou.dev@gmail.com
# Téléphone: +225 014094507
# Version: 3.0.0 - Edition Commerciale Europe & Côte d'Ivoire

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'affichage avec couleurs
print_banner() {
    echo -e "${CYAN}"
    echo "================================================================"
    echo "    🌐 SYSTÈME MONDIAL DE DÉTECTION ET PROTECTION CYBERNÉTIQUE"
    echo "================================================================"
    echo "    Développé par: Yao Kouakou Luc Anicet"
    echo "    Contact: hackerduckman89@gmail.com"
    echo "    Contact: yao.kouakou.dev@gmail.com"
    echo "    Téléphone: +225 014094507"
    echo "    Version: 3.0.0 - Edition Commerciale Europe & Côte d'Ivoire"
    echo "================================================================"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[$1/8]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${PURPLE}ℹ️ $1${NC}"
}

# Vérification de Python
print_step "1" "🔍 Vérification de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    print_success "Python3 détecté"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    print_success "Python détecté"
else
    print_error "Python n'est pas installé. Veuillez installer Python 3.8+"
    print_info "📥 Téléchargez depuis: https://www.python.org/downloads/"
    exit 1
fi

# Vérification de la version Python
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
print_info "Version Python: $PYTHON_VERSION"

# Vérification de pip
print_step "2" "📦 Vérification de pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    print_success "pip3 détecté"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    print_success "pip détecté"
else
    print_error "pip n'est pas installé"
    exit 1
fi

# Installation des dépendances
print_step "3" "📥 Installation des dépendances Python..."
$PIP_CMD install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dépendances installées"
else
    print_error "Erreur lors de l'installation des dépendances"
    exit 1
fi

# Vérification de Redis
print_step "4" "🔍 Vérification de Redis..."
if command -v redis-server &> /dev/null; then
    print_success "Redis détecté"
else
    print_warning "Redis n'est pas installé. Tentative d'installation..."
    
    # Détection du système d'exploitation
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            print_info "Installation Redis via apt-get..."
            sudo apt-get update
            sudo apt-get install -y redis-server
        elif command -v yum &> /dev/null; then
            print_info "Installation Redis via yum..."
            sudo yum install -y redis
        elif command -v dnf &> /dev/null; then
            print_info "Installation Redis via dnf..."
            sudo dnf install -y redis
        else
            print_error "Impossible d'installer Redis automatiquement"
            print_info "📥 Installez Redis manuellement: https://redis.io/download"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            print_info "Installation Redis via Homebrew..."
            brew install redis
        else
            print_error "Homebrew n'est pas installé"
            print_info "📥 Installez Homebrew: https://brew.sh/"
        fi
    else
        print_error "Système d'exploitation non supporté"
        print_info "📥 Installez Redis manuellement: https://redis.io/download"
    fi
fi

# Création des répertoires
print_step "5" "📁 Création des répertoires..."
mkdir -p models logs data config
print_success "Répertoires créés"

# Création de la configuration
print_step "6" "⚙️ Création de la configuration..."
if [ ! -f "config.json" ]; then
    print_info "Création du fichier de configuration..."
    $PYTHON_CMD -c "
import json
config = {
    'system': {
        'name': 'CyberDefense Mondial - Yao Kouakou',
        'version': '2.0.0',
        'developer': 'Yao Kouakou Luc Anicet',
        'contact': {
            'primary': 'hackerduckman89@gmail.com',
            'secondary': 'yao.kouakou.dev@gmail.com',
            'phone': '+225 014094507'
        },
        'environment': 'production'
    },
    'redis': {
        'url': 'redis://localhost:6379',
        'max_connections': 100
    },
    'network': {
        'interface': 'eth0',
        'capture_enabled': True,
        'packet_filters': ['TCP', 'UDP', 'ICMP']
    },
    'ai': {
        'models_dir': 'models',
        'retrain_interval': 86400,
        'confidence_threshold': 0.7
    },
    'intelligence': {
        'feeds_enabled': True,
        'update_interval': 1800,
        'correlation_enabled': True
    },
    'protection': {
        'auto_response': True,
        'escalation_enabled': True,
        'learning_mode': False
    },
    'api': {
        'host': '0.0.0.0',
        'port': 8000,
        'cors_enabled': True
    },
    'world_map': {
        'enabled': True,
        'api_key': '',
        'update_interval': 300
    }
}
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
"
    print_success "Configuration créée"
else
    print_success "Configuration existante"
fi

# Démarrage de Redis
print_step "7" "🚀 Démarrage de Redis..."
if pgrep redis-server > /dev/null; then
    print_success "Redis déjà en cours d'exécution"
else
    print_info "Démarrage de Redis..."
    redis-server --daemonize yes
    sleep 3
    print_success "Redis démarré"
fi

# Démarrage du système
print_step "8" "🌐 Démarrage du système de défense cybernétique..."
echo
print_banner
echo -e "${GREEN}================================================================"
echo "    🚀 LANCEMENT DU SYSTÈME MONDIAL"
echo "================================================================"
echo "    Dashboard: http://localhost:8000"
echo "    API Docs:  http://localhost:8000/docs"
echo "    WebSocket: ws://localhost:8000/ws"
echo "    Carte Monde: http://localhost:8000/world-map"
echo "================================================================"
echo -e "${NC}"

# Vérification des permissions pour la capture de paquets
if [ "$EUID" -ne 0 ]; then
    print_warning "Le système n'est pas lancé en tant que root"
    print_info "Certaines fonctionnalités (capture de paquets) peuvent ne pas fonctionner"
    print_info "Pour un fonctionnement optimal, lancez avec: sudo $0"
fi

# Lancement du système
$PYTHON_CMD launch_cyber_defense.py

echo
print_banner
echo -e "${GREEN}================================================================"
echo "    ✅ SYSTÈME ARRÊTÉ"
echo "================================================================"
echo "    Développé par: Yao Kouakou Luc Anicet"
echo "    Contact: hackerduckman89@gmail.com"
echo "    Contact: yao.kouakou.dev@gmail.com"
echo "================================================================"
echo -e "${NC}"

read -p "Appuyez sur Entrée pour continuer..."
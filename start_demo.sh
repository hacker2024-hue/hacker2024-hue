#!/bin/bash

# =============================================================================
# Script de Démarrage Rapide - IA de Sécurité Informatique Vocale
# =============================================================================

set -e  # Arrêt en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonctions utilitaires
print_header() {
    echo -e "${CYAN}================================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}================================================${NC}"
}

print_step() {
    echo -e "${GREEN}[ÉTAPE]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCÈS]${NC} $1"
}

# Vérification de Python
check_python() {
    print_step "Vérification de Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_info "Python ${PYTHON_VERSION} détecté"
        
        # Vérification de la version minimum (3.9)
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
            print_success "Version Python compatible (≥ 3.9)"
        else
            print_error "Python 3.9+ requis. Version actuelle: ${PYTHON_VERSION}"
            exit 1
        fi
    else
        print_error "Python 3 non trouvé. Veuillez l'installer."
        exit 1
    fi
}

# Installation des dépendances
install_dependencies() {
    print_step "Installation des dépendances..."
    
    if [ -f "requirements.txt" ]; then
        print_info "Installation depuis requirements.txt..."
        pip3 install -r requirements.txt
        print_success "Dépendances installées"
    else
        print_warning "requirements.txt non trouvé, installation des dépendances de base..."
        pip3 install loguru fastapi uvicorn pydantic python-dotenv
    fi
}

# Installation des modèles spaCy
install_spacy_models() {
    print_step "Installation des modèles spaCy..."
    
    print_info "Téléchargement du modèle anglais..."
    python3 -m spacy download en_core_web_sm 2>/dev/null || print_warning "Modèle anglais non installé"
    
    print_info "Téléchargement du modèle français..."
    python3 -m spacy download fr_core_news_sm 2>/dev/null || print_warning "Modèle français non installé"
    
    print_success "Modèles spaCy configurés"
}

# Configuration de l'environnement
setup_environment() {
    print_step "Configuration de l'environnement..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            print_info "Création du fichier .env depuis .env.example..."
            cp .env.example .env
            print_warning "Veuillez éditer .env avec vos clés API pour les services vocaux"
        else
            print_info "Création d'un fichier .env basique..."
            cat > .env << EOF
# Configuration basique
DEBUG=true
LOG_LEVEL=INFO
MOCK_VOICE_SERVICES=true
DEMO_MODE=true
EOF
        fi
        print_success "Fichier .env créé"
    else
        print_info "Fichier .env déjà présent"
    fi
}

# Vérification des permissions audio
check_audio_permissions() {
    print_step "Vérification des permissions audio..."
    
    if command -v pactl &> /dev/null; then
        if pactl info &> /dev/null; then
            print_success "Système audio PulseAudio détecté"
        else
            print_warning "PulseAudio non accessible"
        fi
    elif command -v aplay &> /dev/null; then
        print_info "Système audio ALSA détecté"
    else
        print_warning "Système audio non détecté - mode texte seulement"
    fi
}

# Création des répertoires nécessaires
create_directories() {
    print_step "Création des répertoires..."
    
    mkdir -p logs
    mkdir -p models
    mkdir -p temp
    
    print_success "Répertoires créés"
}

# Test de base du système
test_basic_functionality() {
    print_step "Test des fonctionnalités de base..."
    
    print_info "Test d'import des modules..."
    if python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from core.config import config
    from communication.voice_engine import VoiceEngine
    from core.security_intelligence import SecurityIntelligenceEngine
    print('✅ Tous les modules importés avec succès')
except ImportError as e:
    print(f'❌ Erreur d\\'import: {e}')
    sys.exit(1)
" 2>/dev/null; then
        print_success "Modules principaux fonctionnels"
    else
        print_error "Erreur lors du test des modules"
        print_info "Certaines dépendances peuvent être manquantes"
    fi
}

# Affichage des informations de démarrage
show_startup_info() {
    print_header "🛡️  IA DE SÉCURITÉ INFORMATIQUE VOCALE"
    
    echo -e "${PURPLE}Système initialisé avec succès!${NC}"
    echo ""
    echo -e "${CYAN}Options de démarrage:${NC}"
    echo -e "  ${GREEN}1.${NC} Démonstration complète:"
    echo -e "     ${YELLOW}python3 demo_voice_security_ai.py${NC}"
    echo ""
    echo -e "  ${GREEN}2.${NC} Serveur API:"
    echo -e "     ${YELLOW}python3 main.py${NC}"
    echo ""
    echo -e "  ${GREEN}3.${NC} Mode interactif direct:"
    echo -e "     ${YELLOW}python3 -c \"
import asyncio
from demo_voice_security_ai import VoiceSecurityAIDemo
demo = VoiceSecurityAIDemo()
asyncio.run(demo.initialize())
asyncio.run(demo.run_interactive_mode())
\"${NC}"
    echo ""
    echo -e "${CYAN}Configuration:${NC}"
    echo -e "  📁 Logs: ${YELLOW}logs/${NC}"
    echo -e "  ⚙️  Config: ${YELLOW}.env${NC}"
    echo -e "  🤖 Modèles: ${YELLOW}models/${NC}"
    echo ""
    echo -e "${BLUE}Pour des services vocaux avancés, configurez dans .env:${NC}"
    echo -e "  • ${YELLOW}AZURE_SPEECH_KEY${NC} (Azure Speech Services)"
    echo -e "  • ${YELLOW}OPENAI_API_KEY${NC} (OpenAI Whisper/TTS)"
    echo -e "  • ${YELLOW}ELEVENLABS_API_KEY${NC} (Voix premium)"
    echo ""
}

# Menu principal
show_menu() {
    print_header "🚀 MENU DE DÉMARRAGE"
    
    echo "Que souhaitez-vous faire ?"
    echo ""
    echo "1. 🎬 Lancer la démonstration complète"
    echo "2. 🎙️ Mode interactif (communication vocale)"
    echo "3. 🌐 Démarrer le serveur API"
    echo "4. 🔧 Installer/mettre à jour les dépendances"
    echo "5. 📊 Tester les fonctionnalités"
    echo "6. ℹ️  Afficher les informations système"
    echo "7. 🚪 Quitter"
    echo ""
    read -p "Choix (1-7): " choice
    
    case $choice in
        1)
            print_info "Lancement de la démonstration..."
            python3 demo_voice_security_ai.py
            ;;
        2)
            print_info "Lancement du mode interactif..."
            python3 -c "
import asyncio
import sys
sys.path.insert(0, '.')
from demo_voice_security_ai import VoiceSecurityAIDemo
async def main():
    demo = VoiceSecurityAIDemo()
    await demo.initialize()
    await demo.run_interactive_mode()
asyncio.run(main())
"
            ;;
        3)
            print_info "Démarrage du serveur API..."
            python3 main.py
            ;;
        4)
            install_dependencies
            install_spacy_models
            print_success "Dépendances mises à jour"
            ;;
        5)
            test_basic_functionality
            ;;
        6)
            show_startup_info
            ;;
        7)
            print_info "Au revoir!"
            exit 0
            ;;
        *)
            print_error "Choix invalide"
            show_menu
            ;;
    esac
}

# Script principal
main() {
    clear
    print_header "🛡️  CONFIGURATION IA SÉCURITÉ VOCALE"
    
    # Vérifications préliminaires
    check_python
    create_directories
    
    # Installation si nécessaire
    if [ "$1" = "--install" ] || [ "$1" = "-i" ]; then
        install_dependencies
        install_spacy_models
        setup_environment
        check_audio_permissions
        test_basic_functionality
        show_startup_info
    elif [ "$1" = "--demo" ] || [ "$1" = "-d" ]; then
        print_info "Lancement direct de la démonstration..."
        python3 demo_voice_security_ai.py
    elif [ "$1" = "--interactive" ] || [ "$1" = "-I" ]; then
        print_info "Lancement direct du mode interactif..."
        python3 -c "
import asyncio
import sys
sys.path.insert(0, '.')
from demo_voice_security_ai import VoiceSecurityAIDemo
async def main():
    demo = VoiceSecurityAIDemo()
    await demo.initialize()
    await demo.run_interactive_mode()
asyncio.run(main())
"
    elif [ "$1" = "--server" ] || [ "$1" = "-s" ]; then
        print_info "Démarrage direct du serveur..."
        python3 main.py
    elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  -i, --install      Installation complète"
        echo "  -d, --demo         Démonstration directe"
        echo "  -I, --interactive  Mode interactif direct"
        echo "  -s, --server       Serveur API direct"
        echo "  -h, --help         Afficher cette aide"
        echo ""
        echo "Sans option: menu interactif"
        exit 0
    else
        # Menu interactif par défaut
        setup_environment
        check_audio_permissions
        show_menu
    fi
}

# Point d'entrée
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
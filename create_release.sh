#!/bin/bash

# Script de création d'archive - CyberSec AI Assistant
# Par Yao Kouakou Luc Annicet

echo "🎯 Création d'archive CyberSec AI Assistant"
echo "=========================================="

# Variables
DATE=$(date +%Y%m%d_%H%M%S)
VERSION="1.0.0"
ARCHIVE_NAME="cybersec-ai-assistant_v${VERSION}_${DATE}"

echo "📦 Version: $VERSION"
echo "📅 Date: $DATE"
echo "📁 Archive: ${ARCHIVE_NAME}.zip"
echo ""

# Nettoyage préalable
echo "🧹 Nettoyage des fichiers temporaires..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null
find . -name ".DS_Store" -delete 2>/dev/null

# Création de l'archive
echo "📦 Création de l'archive ZIP..."
zip -r "${ARCHIVE_NAME}.zip" . \
    -x "venv/*" \
    -x ".git/*" \
    -x "__pycache__/*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x ".DS_Store" \
    -x "node_modules/*" \
    -x ".env" \
    -x "*.log" \
    -x "logs/*" \
    -x ".pytest_cache/*"

# Vérification
if [ -f "${ARCHIVE_NAME}.zip" ]; then
    SIZE=$(ls -lh "${ARCHIVE_NAME}.zip" | awk '{print $5}')
    echo "✅ Archive créée avec succès !"
    echo "📊 Taille: $SIZE"
    echo "📁 Fichier: ${ARCHIVE_NAME}.zip"
    
    # Création d'un lien symbolique vers la dernière version
    ln -sf "${ARCHIVE_NAME}.zip" "cybersec-ai-assistant-latest.zip"
    echo "🔗 Lien symbolique créé: cybersec-ai-assistant-latest.zip"
    
    # Checksum pour vérification
    sha256sum "${ARCHIVE_NAME}.zip" > "${ARCHIVE_NAME}.zip.sha256"
    echo "🔐 Checksum SHA256 créé: ${ARCHIVE_NAME}.zip.sha256"
    
else
    echo "❌ Erreur lors de la création de l'archive"
    exit 1
fi

echo ""
echo "🎉 Processus terminé avec succès !"
echo "📥 Votre projet est prêt à être téléchargé !"
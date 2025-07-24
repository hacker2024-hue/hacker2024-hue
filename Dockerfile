# Dockerfile pour CyberSec AI Assistant
# ====================================

# Image de base Python 3.11 slim pour un build optimisé
FROM python:3.11-slim as base

# Métadonnées
LABEL maintainer="Yao Kouakou Luc Annicet"
LABEL description="CyberSec AI Assistant - Intelligence Artificielle en Cybersécurité"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Création d'un utilisateur non-root pour la sécurité
RUN groupadd -r cybersec && useradd -r -g cybersec cybersec

# Répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .
COPY setup.py .

# Installation des dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

# Installation du modèle spaCy
RUN python -m spacy download en_core_web_sm

# Stage de production
FROM base as production

# Copie du code source
COPY --chown=cybersec:cybersec . .

# Création des répertoires nécessaires
RUN mkdir -p logs data models reports uploads && \
    chown -R cybersec:cybersec /app

# Changement vers l'utilisateur non-root
USER cybersec

# Configuration des variables d'environnement pour production
ENV DEBUG=false \
    API_HOST=0.0.0.0 \
    API_PORT=8000 \
    API_WORKERS=4 \
    LOG_LEVEL=INFO \
    MODEL_DEVICE=cpu

# Exposition du port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Point d'entrée
ENTRYPOINT ["python", "main.py"]

# Stage de développement
FROM base as development

# Installation des outils de développement
RUN pip install pytest pytest-asyncio black flake8 mypy pre-commit

# Copie du code source
COPY --chown=cybersec:cybersec . .

# Configuration pour le développement
ENV DEBUG=true \
    API_WORKERS=1 \
    LOG_LEVEL=DEBUG

USER cybersec

# Volume pour le développement
VOLUME ["/app"]

EXPOSE 8000

CMD ["python", "main.py"]

# Stage GPU (optionnel)
FROM nvidia/cuda:11.8-runtime-ubuntu22.04 as gpu

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Installation de Python et des dépendances
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-pip \
    python3.11-dev \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.11 /usr/bin/python

WORKDIR /app

COPY requirements.txt .
COPY setup.py .

# Installation avec support GPU
RUN pip install --upgrade pip && \
    pip install torch[cuda] && \
    pip install -r requirements.txt && \
    pip install .

RUN python -m spacy download en_core_web_sm

RUN groupadd -r cybersec && useradd -r -g cybersec cybersec

COPY --chown=cybersec:cybersec . .

RUN mkdir -p logs data models reports uploads && \
    chown -R cybersec:cybersec /app

USER cybersec

ENV MODEL_DEVICE=cuda \
    API_HOST=0.0.0.0 \
    API_PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["python", "main.py"]
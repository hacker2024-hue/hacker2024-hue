# 📥 Guide de Téléchargement - CyberSec AI Assistant

## 🌐 **Où Télécharger CyberSec AI Assistant**

### 🐙 **GitHub (Source Officielle)**

#### **Méthode 1: Téléchargement Direct ZIP**
1. **Visitez** : [https://github.com/hackerduckman89/cybersec-ai-assistant](https://github.com/hackerduckman89/cybersec-ai-assistant)
2. **Cliquez** sur le bouton vert `Code`
3. **Sélectionnez** `Download ZIP`
4. **Décompressez** le fichier dans votre dossier de travail

#### **Méthode 2: Clone Git (Recommandé)**
```bash
# Clonage du repository complet
git clone https://github.com/hackerduckman89/cybersec-ai-assistant.git
cd cybersec-ai-assistant
```

#### **Méthode 3: GitHub CLI**
```bash
# Avec GitHub CLI
gh repo clone hackerduckman89/cybersec-ai-assistant
```

---

## 💾 **Releases Officielles**

### 📦 **Versions Stables**

| Version | Date | Taille | Télécharger |
|---------|------|--------|-------------|
| **v1.0.0** | 2024 | ~15MB | [📥 ZIP](https://github.com/hackerduckman89/cybersec-ai-assistant/archive/v1.0.0.zip) |
| **Latest** | Current | ~15MB | [📥 ZIP](https://github.com/hackerduckman89/cybersec-ai-assistant/archive/main.zip) |

---

## 🖥️ **Instructions par Système d'Exploitation**

### 🪟 **Windows**
```bash
# Téléchargement PowerShell
Invoke-WebRequest -Uri "https://github.com/hackerduckman89/cybersec-ai-assistant/archive/main.zip" -OutFile "cybersec-ai.zip"
Expand-Archive -Path "cybersec-ai.zip" -DestinationPath "."
```

### 🐧 **Linux/Ubuntu**
```bash
# Téléchargement wget
wget https://github.com/hackerduckman89/cybersec-ai-assistant/archive/main.zip
unzip main.zip
cd cybersec-ai-assistant-main/
```

### 🍎 **macOS**
```bash
# Téléchargement curl
curl -L https://github.com/hackerduckman89/cybersec-ai-assistant/archive/main.zip -o cybersec-ai.zip
unzip cybersec-ai.zip
cd cybersec-ai-assistant-main/
```

---

## 🐳 **Docker (Alternative)**

### **Image Docker Prête**
```bash
# Téléchargement et lancement direct
docker pull hackerduckman89/cybersec-ai-assistant:latest
docker run -p 8000:8000 hackerduckman89/cybersec-ai-assistant:latest
```

### **Docker Compose**
```bash
# Téléchargement du projet
git clone https://github.com/hackerduckman89/cybersec-ai-assistant.git
cd cybersec-ai-assistant

# Lancement avec Docker Compose
docker-compose up -d
```

---

## 📋 **Après le Téléchargement**

### ✅ **Vérification de l'Installation**
```bash
# Vérifiez la structure des fichiers
ls -la
# Vous devriez voir:
# - README.md
# - requirements.txt
# - main.py
# - demo_launcher.py
# - *.bat (pour Windows)
```

### 🚀 **Démarrage Rapide**

#### **Windows**
```batch
# Double-cliquez sur:
start.bat
```

#### **Linux/macOS**
```bash
# Installation et lancement
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 demo_launcher.py
```

---

## 🔐 **Vérification de Sécurité**

### **Checksums SHA256**
```
main.zip: a1b2c3d4e5f6...
v1.0.0.zip: 1a2b3c4d5e6f...
```

### **Signature GPG**
```bash
# Vérification de la signature (optionnel)
gpg --verify cybersec-ai-assistant.zip.sig
```

---

## 📞 **Support Téléchargement**

### 🆘 **Problèmes de Téléchargement**

| Problème | Solution |
|----------|----------|
| **Connexion lente** | Utilisez un gestionnaire de téléchargement |
| **Fichier corrompu** | Re-téléchargez en vérifiant le checksum |
| **Accès GitHub bloqué** | Utilisez un VPN ou proxy |
| **Zip endommagé** | Téléchargez via `git clone` |

### 📧 **Contact**
- **Email** : yao.kouakou.dev@gmaii.com
- **GitHub Issues** : [Signaler un problème](https://github.com/hackerduckman89/cybersec-ai-assistant/issues)

---

## 🎁 **Téléchargements Bonus**

### 📚 **Documentation Supplémentaire**
- [📖 Manuel Utilisateur](https://github.com/hackerduckman89/cybersec-ai-assistant/wiki)
- [🔧 Guide Installation](README_WINDOWS.md)
- [💼 Licence Commerciale](COMMERCIAL_PRICING.md)

### 🛠️ **Outils Complémentaires**
- **Scripts d'installation automatique**
- **Configurations Docker personnalisées**
- **Templates de déploiement**

---

## 🔄 **Mises à Jour**

### **Notification de Nouvelles Versions**
```bash
# Vérifier les mises à jour
git fetch origin
git status
```

### **Mise à Jour Automatique**
```bash
# Mise à jour vers la dernière version
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**✨ Développé par [Yao Kouakou Luc Annicet](https://github.com/hackerduckman89)**
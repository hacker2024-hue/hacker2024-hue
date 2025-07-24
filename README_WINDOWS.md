# 🪟 CyberSec AI Assistant - Guide Windows

## 🚀 Installation Rapide

### Prérequis
- **Windows 10/11** ou version ultérieure
- **Python 3.8+** installé depuis [python.org](https://python.org)
- **4GB RAM** minimum (8GB recommandé)

### 📦 Installation Automatique

1. **Téléchargez** le projet
2. **Double-cliquez** sur `install.bat`
3. **Suivez** les instructions à l'écran
4. **Patientez** pendant l'installation

```batch
# Installation complète automatique
install.bat
```

## 🎯 Lancement

### Option 1: Démarrage Rapide
```batch
# Double-cliquez sur start.bat
start.bat
```

### Option 2: Menu Complet
```batch
# Double-cliquez sur launch_cybersec_ai.bat
launch_cybersec_ai.bat
```

### Option 3: Manuel
```batch
# Activez l'environnement virtuel
venv\Scripts\activate.bat

# Lancez l'application
python demo_launcher.py
```

## 📋 Scripts Disponibles

| Script | Description | Usage |
|--------|-------------|-------|
| `install.bat` | Installation complète | Installation initiale |
| `start.bat` | Démarrage rapide | Usage quotidien |
| `launch_cybersec_ai.bat` | Menu interactif | Options avancées |

## 🛠️ Fonctionnalités du Menu

Le script `launch_cybersec_ai.bat` offre un menu interactif avec :

1. **Lancer le serveur principal** - Démarre FastAPI sur http://localhost:8000
2. **Lancer la démonstration** - Mode démo sans dépendances lourdes
3. **Exécuter les tests** - Vérification de l'intégrité
4. **Installer les dépendances** - Installation complète
5. **Console Python** - Accès direct à Python
6. **Informations système** - Diagnostic de l'environnement

## 🔧 Configuration

### Variables d'Environnement
Les scripts créent automatiquement :
- `venv/` - Environnement virtuel Python
- `.env` - Configuration (optionnel)

### Ports Utilisés
- **8000** - Serveur principal FastAPI
- **8001** - Interface d'administration (si activée)

## 🐛 Résolution de Problèmes

### Python non trouvé
```batch
# Vérifiez l'installation Python
python --version

# Si erreur, ajoutez Python au PATH ou réinstallez
```

### Erreur de permissions
```batch
# Exécutez en tant qu'administrateur
# Clic droit > "Exécuter en tant qu'administrateur"
```

### Modules manquants
```batch
# Réinstallez les dépendances
pip install -r requirements.txt
```

### Environnement virtuel corrompu
```batch
# Supprimez et recréez l'environnement
rmdir /s venv
python -m venv venv
```

## 📁 Structure des Fichiers Windows

```
cybersec-ai-assistant/
├── 📄 install.bat              # Installation automatique
├── 📄 start.bat                # Démarrage rapide  
├── 📄 launch_cybersec_ai.bat   # Menu interactif
├── 📁 venv/                    # Environnement virtuel
│   └── Scripts/
│       ├── activate.bat        # Activation environnement
│       ├── python.exe          # Python isolé
│       └── pip.exe             # Gestionnaire packages
├── 📄 demo_launcher.py         # Démonstration
├── 📄 main.py                  # Application principale
└── 📄 requirements.txt         # Dépendances Python
```

## 🌐 Accès Web

Une fois démarré, accédez à l'application via :

- **Interface principale** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Monitoring** : http://localhost:8000/health

## 🔄 Mise à Jour

Pour mettre à jour l'application :

1. **Sauvegardez** vos configurations
2. **Téléchargez** la nouvelle version
3. **Exécutez** `install.bat` à nouveau
4. **Relancez** avec `start.bat`

## 📞 Support Windows

### Logs de Débogage
Les logs sont disponibles dans :
- Console Windows (affichage direct)
- Fichier `logs/` (si configuré)

### Contact Support
- **Email** : yao.kouakou.dev@gmaii.com
- **GitHub** : https://github.com/hackerduckman89/cybersec-ai-assistant

### Problèmes Courants Windows

| Problème | Solution |
|----------|----------|
| Antivirus bloque | Ajoutez une exception |
| Firewall bloque | Autorisez Python.exe |
| Permissions UAC | Exécutez en admin |
| Python 3.13 | Certains modules incompatibles |

## 🎨 Personnalisation

### Couleurs Terminal
Les scripts utilisent des couleurs :
- **Vert** (0A) : Démarrage normal
- **Bleu** (0B) : Installation
- **Rouge** : Erreurs

### Modification des Scripts
Pour personnaliser :
1. **Copiez** le script original
2. **Modifiez** selon vos besoins
3. **Testez** avant utilisation

## 🚀 Performance Windows

### Optimisations Recommandées
- **SSD** pour de meilleures performances
- **8GB+ RAM** pour l'IA
- **Antivirus** en liste blanche
- **Windows Defender** exception

### Surveillance Ressources
- **Gestionnaire de tâches** : Ctrl+Shift+Esc
- **Moniteur performances** : perfmon.msc

---

## 📋 Checklist Installation

- [ ] Python 3.8+ installé
- [ ] PATH Python configuré
- [ ] Exécution `install.bat` réussie
- [ ] Test avec `start.bat`
- [ ] Accès http://localhost:8000
- [ ] Démonstration fonctionnelle

## 🎯 Prochaines Étapes

1. **Explorez** la démonstration
2. **Lisez** la documentation complète
3. **Configurez** selon vos besoins
4. **Contactez** le support si besoin

---

*Guide créé pour Windows 10/11 - CyberSec AI Assistant v1.0.0*
*Par Yao Kouakou Luc Annicet - yao.kouakou.dev@gmaii.com*
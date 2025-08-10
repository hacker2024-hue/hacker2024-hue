#!/usr/bin/env python3
"""
🧹 Nettoyeur de Dossier - Système Mondial de Défense Cybernétique
Dossier Complet - Yao Kouakou Luc Anicet
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict

class DossierNettoyeur:
    def __init__(self):
        self.developer_info = {
            "name": "Yao Kouakou Luc Anicet",
            "phone": "+225 014094507",
            "email": "hackerduckman89@gmail.com",
            "license": "CI-CYBER-2024-001"
        }
        self.current_dir = Path(__file__).parent
        
    def print_banner(self):
        """Affiche la bannière du nettoyeur"""
        print("=" * 80)
        print("🧹 NETTOYEUR DE DOSSIER - SYSTÈME DE DÉFENSE CYBERNÉTIQUE")
        print("📁 DOSSIER COMPLET - ORGANISATION ET NETTOYAGE")
        print("=" * 80)
        print(f"👨‍💻 Développé par: {self.developer_info['name']}")
        print(f"📞 Téléphone: {self.developer_info['phone']}")
        print(f"📧 Email: {self.developer_info['email']}")
        print(f"🔐 Licence: {self.developer_info['license']}")
        print("=" * 80)
        print()
        
    def get_file_stats(self) -> Dict[str, int]:
        """Obtient les statistiques des fichiers"""
        stats = {
            "total_files": 0,
            "total_dirs": 0,
            "python_files": 0,
            "markdown_files": 0,
            "config_files": 0,
            "other_files": 0
        }
        
        for root, dirs, files in os.walk(self.current_dir):
            stats["total_dirs"] += len(dirs)
            stats["total_files"] += len(files)
            
            for file in files:
                if file.endswith('.py'):
                    stats["python_files"] += 1
                elif file.endswith('.md'):
                    stats["markdown_files"] += 1
                elif file.endswith(('.json', '.yml', '.yaml', '.ini', '.cfg')):
                    stats["config_files"] += 1
                else:
                    stats["other_files"] += 1
                    
        return stats
        
    def show_current_structure(self):
        """Affiche la structure actuelle"""
        print("📊 STRUCTURE ACTUELLE DU DOSSIER")
        print("=" * 50)
        
        stats = self.get_file_stats()
        print(f"📁 Dossiers: {stats['total_dirs']}")
        print(f"📄 Fichiers totaux: {stats['total_files']}")
        print(f"🐍 Fichiers Python: {stats['python_files']}")
        print(f"📝 Fichiers Markdown: {stats['markdown_files']}")
        print(f"⚙️  Fichiers de config: {stats['config_files']}")
        print(f"📄 Autres fichiers: {stats['other_files']}")
        
        print("\n📂 Dossiers principaux:")
        main_dirs = [
            "security", "core", "api", "templates", "config",
            "data", "logs", "models", "scripts", "communication"
        ]
        
        for dir_name in main_dirs:
            dir_path = self.current_dir / dir_name
            if dir_path.exists():
                file_count = len(list(dir_path.rglob("*")))
                print(f"   ✅ {dir_name}/ ({file_count} éléments)")
            else:
                print(f"   ❌ {dir_name}/ (manquant)")
                
        print()
        
    def identify_duplicate_files(self) -> List[Dict]:
        """Identifie les fichiers en double"""
        print("🔍 Recherche de fichiers en double...")
        duplicates = []
        file_hashes = {}
        
        for file_path in self.current_dir.rglob("*"):
            if file_path.is_file():
                try:
                    # Utiliser la taille et le nom comme identifiant simple
                    file_id = f"{file_path.name}_{file_path.stat().st_size}"
                    
                    if file_id in file_hashes:
                        duplicates.append({
                            "original": file_hashes[file_id],
                            "duplicate": file_path,
                            "size": file_path.stat().st_size
                        })
                    else:
                        file_hashes[file_id] = file_path
                except Exception:
                    continue
                    
        return duplicates
        
    def identify_unused_files(self) -> List[Path]:
        """Identifie les fichiers potentiellement inutilisés"""
        print("🔍 Recherche de fichiers potentiellement inutilisés...")
        unused_files = []
        
        # Fichiers essentiels (ne jamais supprimer)
        essential_files = {
            "minimal_start.py", "test_system_live.py", "config.json",
            "requirements.txt", "README_PRINCIPAL.md", "SECURITE_ACCES.md",
            "LANCER_DOSSIER_COMPLET.py", "TEST_DOSSIER_COMPLET.py",
            "NETTOYER_DOSSIER.py"
        }
        
        # Fichiers potentiellement redondants
        redundant_patterns = [
            "*.pyc", "__pycache__", "*.log", "*.tmp", "*.bak",
            "*.old", "*.backup", "*.orig"
        ]
        
        for file_path in self.current_dir.rglob("*"):
            if file_path.is_file():
                # Ignorer les fichiers essentiels
                if file_path.name in essential_files:
                    continue
                    
                # Vérifier les patterns redondants
                is_redundant = False
                for pattern in redundant_patterns:
                    if file_path.match(pattern):
                        is_redundant = True
                        break
                        
                if is_redundant:
                    unused_files.append(file_path)
                    
        return unused_files
        
    def create_backup(self):
        """Crée une sauvegarde avant nettoyage"""
        print("💾 Création d'une sauvegarde...")
        
        backup_dir = self.current_dir.parent / f"CyberDefense_Backup_{int(time.time())}"
        
        try:
            shutil.copytree(self.current_dir, backup_dir, ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", "*.log", "cyberdefense_env"
            ))
            print(f"✅ Sauvegarde créée: {backup_dir}")
            return backup_dir
        except Exception as e:
            print(f"❌ Erreur lors de la création de la sauvegarde: {e}")
            return None
            
    def clean_pycache(self):
        """Nettoie les fichiers __pycache__"""
        print("🧹 Nettoyage des fichiers __pycache__...")
        
        removed_count = 0
        for pycache_dir in self.current_dir.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
                removed_count += 1
                print(f"   ✅ Supprimé: {pycache_dir}")
            except Exception as e:
                print(f"   ❌ Erreur: {pycache_dir} - {e}")
                
        print(f"📊 {removed_count} dossiers __pycache__ supprimés")
        
    def clean_logs(self):
        """Nettoie les fichiers de logs"""
        print("🧹 Nettoyage des fichiers de logs...")
        
        removed_count = 0
        for log_file in self.current_dir.rglob("*.log"):
            try:
                log_file.unlink()
                removed_count += 1
                print(f"   ✅ Supprimé: {log_file}")
            except Exception as e:
                print(f"   ❌ Erreur: {log_file} - {e}")
                
        print(f"📊 {removed_count} fichiers de logs supprimés")
        
    def organize_files(self):
        """Organise les fichiers dans des dossiers appropriés"""
        print("📁 Organisation des fichiers...")
        
        # Créer des dossiers d'organisation si nécessaire
        org_dirs = {
            "docs": ["*.md"],
            "scripts": ["*.bat", "*.sh"],
            "tests": ["test_*.py"],
            "demos": ["demo_*.py"],
            "configs": ["*.json", "*.yml", "*.yaml", "*.ini"]
        }
        
        for dir_name, patterns in org_dirs.items():
            org_dir = self.current_dir / dir_name
            if not org_dir.exists():
                org_dir.mkdir()
                print(f"   📁 Créé: {dir_name}/")
                
            # Déplacer les fichiers correspondants
            for pattern in patterns:
                for file_path in self.current_dir.glob(pattern):
                    if file_path.is_file() and file_path.parent == self.current_dir:
                        try:
                            shutil.move(str(file_path), str(org_dir / file_path.name))
                            print(f"   📄 Déplacé: {file_path.name} → {dir_name}/")
                        except Exception as e:
                            print(f"   ❌ Erreur: {file_path.name} - {e}")
                            
    def create_index_file(self):
        """Crée un fichier d'index pour faciliter la navigation"""
        print("📝 Création du fichier d'index...")
        
        index_content = f"""# 📁 Index du Dossier Complet - Système de Défense Cybernétique

## 👨‍💻 Développé par: {self.developer_info['name']}
**Contact:** {self.developer_info['email']} | **Téléphone:** {self.developer_info['phone']}
**Licence:** {self.developer_info['license']}

## 🚀 Lancement Rapide
```bash
python LANCER_DOSSIER_COMPLET.py
```

## 📁 Structure Organisée

### 🚀 Lancement
- `LANCER_DOSSIER_COMPLET.py` - Lanceur principal
- `minimal_start.py` - Version minimale
- `install_and_run.bat` - Installation Windows
- `install_and_run.sh` - Installation Linux/Mac

### 🧪 Tests
- `TEST_DOSSIER_COMPLET.py` - Testeur unifié
- `test_system_live.py` - Test en ligne
- `test_access_protection.py` - Test sécurité
- `test_ivoirian_license.py` - Test licences

### 📚 Documentation
- `README_PRINCIPAL.md` - Guide principal
- `SECURITE_ACCES.md` - Documentation sécurité
- `LICENCE_VENTE_IVOIRIENNE.md` - Licence commerciale
- `COMMERCIAL_PRICING.md` - Tarification

### 🏗️ Architecture
- `security/` - Système de sécurité
- `core/` - Composants principaux
- `api/` - Interface API
- `templates/` - Templates HTML
- `config/` - Configuration
- `data/` - Données
- `logs/` - Journaux
- `models/` - Modèles IA
- `scripts/` - Scripts utilitaires
- `communication/` - Communication

## 🔐 Accès
- **Mot de passe:** AZ12ER34
- **URL:** http://localhost:8000/
- **Dashboard:** http://localhost:8000/dashboard

## 📞 Support
- **Développeur:** {self.developer_info['name']}
- **Téléphone:** {self.developer_info['phone']}
- **Email:** {self.developer_info['email']}
- **Licence:** {self.developer_info['license']}

---
*Généré automatiquement par NETTOYER_DOSSIER.py*
"""
        
        index_file = self.current_dir / "INDEX_DOSSIER.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
            
        print(f"✅ Fichier d'index créé: {index_file}")
        
    def run_cleaning(self):
        """Exécute le nettoyage complet"""
        self.print_banner()
        
        print("🧹 DÉMARRAGE DU NETTOYAGE")
        print("=" * 50)
        
        # Afficher la structure actuelle
        self.show_current_structure()
        
        # Demander confirmation
        print("\n⚠️  ATTENTION: Cette opération va nettoyer et réorganiser le dossier.")
        confirm = input("Voulez-vous continuer? (oui/non): ").strip().lower()
        
        if confirm not in ['oui', 'o', 'yes', 'y']:
            print("❌ Nettoyage annulé")
            return
            
        # Créer une sauvegarde
        backup_dir = self.create_backup()
        
        # Nettoyer les fichiers temporaires
        self.clean_pycache()
        self.clean_logs()
        
        # Organiser les fichiers
        self.organize_files()
        
        # Créer l'index
        self.create_index_file()
        
        # Afficher les résultats
        print("\n" + "=" * 50)
        print("✅ NETTOYAGE TERMINÉ")
        print("=" * 50)
        
        if backup_dir:
            print(f"💾 Sauvegarde: {backup_dir}")
            
        print("📊 Nouvelle structure:")
        self.show_current_structure()
        
        print("\n🎯 Prochaines étapes:")
        print("1. Lancer le système: python LANCER_DOSSIER_COMPLET.py")
        print("2. Tester le système: python TEST_DOSSIER_COMPLET.py")
        print("3. Consulter l'index: INDEX_DOSSIER.md")

def main():
    """Fonction principale"""
    import time
    nettoyeur = DossierNettoyeur()
    nettoyeur.run_cleaning()

if __name__ == "__main__":
    main()
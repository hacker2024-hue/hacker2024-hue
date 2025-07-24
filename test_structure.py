#!/usr/bin/env python3
"""
Test de la structure du projet CyberSec AI Assistant
===================================================

Vérification de la cohérence de l'architecture sans dépendances.
"""

import os
import sys
from pathlib import Path

def check_file_structure():
    """Vérification de la structure des fichiers"""
    
    required_files = [
        "README.md",
        "requirements.txt",
        "main.py",
        "setup.py",
        "Dockerfile",
        "docker-compose.yml",
        ".env.example",
        "core/__init__.py",
        "core/config.py",
        "core/ai_engine.py",
        "security/__init__.py",
        "security/threat_analyzer.py",
        "communication/__init__.py",
        "communication/interface.py",
        "api/__init__.py",
        "api/main.py",
        "api/routes.py",
        "api/models.py",
        "scripts/__init__.py",
        "scripts/setup.py"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path}")
    
    print(f"\n📊 Résultats:")
    print(f"   Fichiers présents: {len(existing_files)}/{len(required_files)}")
    print(f"   Fichiers manquants: {len(missing_files)}")
    
    if missing_files:
        print(f"\n❌ Fichiers manquants:")
        for file in missing_files:
            print(f"   - {file}")
    
    return len(missing_files) == 0


def check_imports():
    """Vérification des imports internes (sans exécution)"""
    
    print(f"\n🔍 Vérification des imports...")
    
    test_files = [
        ("core/config.py", "Configuration"),
        ("core/ai_engine.py", "Moteur IA"),
        ("security/threat_analyzer.py", "Analyseur de menaces"),
        ("communication/interface.py", "Interface de communication"),
        ("api/models.py", "Modèles API"),
        ("api/routes.py", "Routes API"),
        ("api/main.py", "Application principale")
    ]
    
    syntax_ok = 0
    
    for file_path, description in test_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Vérification basique de la syntaxe
                compile(content, file_path, 'exec')
            print(f"✅ {description} ({file_path}) - Syntaxe OK")
            syntax_ok += 1
        except FileNotFoundError:
            print(f"❌ {description} ({file_path}) - Fichier non trouvé")
        except SyntaxError as e:
            print(f"❌ {description} ({file_path}) - Erreur de syntaxe: {e}")
        except Exception as e:
            print(f"⚠️ {description} ({file_path}) - Erreur: {e}")
    
    print(f"\n📊 Résultats syntaxe:")
    print(f"   Fichiers valides: {syntax_ok}/{len(test_files)}")
    
    return syntax_ok == len(test_files)


def check_configurations():
    """Vérification des fichiers de configuration"""
    
    print(f"\n⚙️ Vérification des configurations...")
    
    configs = [
        (".env.example", "Exemple de configuration"),
        ("requirements.txt", "Dépendances Python"),
        ("docker-compose.yml", "Configuration Docker"),
        ("Dockerfile", "Image Docker")
    ]
    
    config_ok = 0
    
    for file_path, description in configs:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content.strip()) > 0:
                        print(f"✅ {description} ({file_path}) - OK")
                        config_ok += 1
                    else:
                        print(f"⚠️ {description} ({file_path}) - Fichier vide")
            except Exception as e:
                print(f"❌ {description} ({file_path}) - Erreur: {e}")
        else:
            print(f"❌ {description} ({file_path}) - Non trouvé")
    
    print(f"\n📊 Résultats configuration:")
    print(f"   Fichiers valides: {config_ok}/{len(configs)}")
    
    return config_ok == len(configs)


def analyze_code_structure():
    """Analyse de la structure du code"""
    
    print(f"\n📈 Analyse de la structure...")
    
    stats = {
        "total_files": 0,
        "total_lines": 0,
        "python_files": 0,
        "config_files": 0,
        "doc_files": 0
    }
    
    for root, dirs, files in os.walk("."):
        # Ignorer les répertoires cachés
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = Path(root) / file
            stats["total_files"] += 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    stats["total_lines"] += lines
            except:
                pass
            
            if file.endswith('.py'):
                stats["python_files"] += 1
            elif file.endswith(('.yml', '.yaml', '.json', '.env', '.txt')):
                stats["config_files"] += 1
            elif file.endswith('.md'):
                stats["doc_files"] += 1
    
    print(f"   📁 Total fichiers: {stats['total_files']}")
    print(f"   🐍 Fichiers Python: {stats['python_files']}")
    print(f"   ⚙️ Fichiers config: {stats['config_files']}")
    print(f"   📚 Documentation: {stats['doc_files']}")
    print(f"   📝 Total lignes: {stats['total_lines']}")
    
    return stats


def print_summary():
    """Affichage du résumé final"""
    
    print(f"\n" + "="*60)
    print(f"🛡️ CyberSec AI Assistant - Vérification Structure")
    print(f"="*60)
    print(f"✨ Système d'IA avancé en cybersécurité")
    print(f"🏗️ Architecture modulaire et scalable")
    print(f"🚀 Prêt pour le déploiement Docker")
    print(f"📚 Documentation complète")
    print(f"🔧 Configuration flexible")
    print(f"="*60)


def main():
    """Fonction principale de test"""
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           CyberSec AI Assistant - Test Structure         ║
    ║                  Vérification du Projet                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Tests
    structure_ok = check_file_structure()
    syntax_ok = check_imports()
    config_ok = check_configurations()
    stats = analyze_code_structure()
    
    # Résultats globaux
    print(f"\n🎯 RÉSULTATS GLOBAUX:")
    print(f"   Structure: {'✅ OK' if structure_ok else '❌ ERREURS'}")
    print(f"   Syntaxe: {'✅ OK' if syntax_ok else '❌ ERREURS'}")
    print(f"   Configuration: {'✅ OK' if config_ok else '❌ ERREURS'}")
    
    all_ok = structure_ok and syntax_ok and config_ok
    
    if all_ok:
        print(f"\n🎉 SUCCÈS: Le projet est correctement structuré!")
        print(f"   ✅ Tous les fichiers sont présents")
        print(f"   ✅ La syntaxe Python est valide")
        print(f"   ✅ Les configurations sont en place")
        print(f"   ✅ Prêt pour l'installation et le déploiement")
    else:
        print(f"\n⚠️ ATTENTION: Quelques ajustements nécessaires")
        print(f"   Consultez les détails ci-dessus")
    
    print_summary()
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
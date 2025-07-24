#!/usr/bin/env python3
"""
Setup script pour CyberSec AI Assistant
=======================================

Installation et configuration du package.
"""

from setuptools import setup, find_packages
import os

# Lecture du fichier README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Lecture des requirements
def read_requirements(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

requirements = read_requirements("requirements.txt")

setup(
    name="cybersec-ai-assistant",
    version="1.0.0",
    author="Yao Kouakou Luc Annicet",
    author_email="luc.annicet@cybersec-ai.com",
    description="Assistant IA avancé spécialisé en cybersécurité",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yao-kouakou-luc-annicet/cybersec-ai-assistant",
    project_urls={
        "Bug Tracker": "https://github.com/yao-kouakou-luc-annicet/cybersec-ai-assistant/issues",
        "Documentation": "https://cybersec-ai-docs.readthedocs.io/",
        "Source Code": "https://github.com/yao-kouakou-luc-annicet/cybersec-ai-assistant",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
            "pre-commit>=3.4.0",
        ],
        "gpu": [
            "torch[cuda]>=2.1.0",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "psycopg2-binary>=2.9.0",
            "redis>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cybersec-ai=main:main",
            "cybersec-setup=scripts.setup:main",
            "cybersec-cli=scripts.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml", "*.json"],
    },
    keywords=[
        "cybersecurity", "artificial intelligence", "threat analysis", 
        "malware detection", "security automation", "incident response",
        "threat intelligence", "machine learning", "nlp"
    ],
    zip_safe=False,
)
# 🛡️ GestionnaireServer - Bot Discord Modulaire

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Discord.py](https://img.shields.io/badge/library-discord.py-blueviolet)
![License](https://img.shields.io/badge/license-MIT-green)

**GestionnaireServer** est une solution d'automatisation Discord conçue pour offrir une expérience utilisateur fluide et une administration simplifiée. Ce projet met l'accent sur la propreté du code (Clean Code) et une architecture modulaire robuste.

## 🚀 Fonctionnalités Clés

* **👋 Accueil Volatile :** Système de bienvenue intelligent qui supprime automatiquement le message précédent pour maintenir la propreté des salons.
* **📢 Annonces Dynamiques :** Commande `/annonce` riche avec support des Embeds, titres personnalisés et couleurs hexadécimales.
* **🗂️ Architecture par Cogs :** Utilisation de modules indépendants pour une maintenance et une évolutivité facilitées.
* **💾 Persistance des Données :** Gestion d'état via fichiers JSON pour conserver la mémoire des interactions après redémarrage.

## 🏗️ Architecture Technique

Le bot suit une structure organisée pour séparer les responsabilités :
* `main.py` : Cœur du système, gestion de l'allumage et synchronisation des commandes.
* `cogs/` : Logique métier divisée par fonctionnalités (Admin, Welcome).
* `config.py` : Centralisation des IDs et configurations globales.

## 📦 Installation

```bash
# 1. Cloner le dépôt
git clone [https://github.com/Ebelielk/discord-management-bot.git](https://github.com/Ebelielk/discord-management-bot.git)
cd discord-management-bot

# 2. Installer l'environnement
python -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur Linux/Mac :
# source venv/bin/activate
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
# Créez un fichier .env dans le répertoire racine du projet
# et ajoutez votre token Discord :

DISCORD_TOKEN=votre_token_discord_ici

# Pour obtenir un token Discord :
# 1. Allez sur https://discord.com/developers/applications
# 2. Créez une nouvelle application ou sélectionnez-en une existante
# 3. Dans l'onglet "Bot", cliquez sur "Add Bot"
# 4. Copiez le token sous "Token" et collez-le dans le fichier .env

# 4. Lancer le bot
python main.py

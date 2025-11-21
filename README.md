# EcoTrack — API FastAPI (mini-squelette)

Ce dépôt contient une implémentation minimale d'une API FastAPI pour le projet EcoTrack (scaffold d'authentification et script d'initialisation). Le README ci‑dessous explique comment démarrer localement, initialiser la base et tester les endpoints essentiels.

## Prérequis
- Python 3.10+ recommandé
- Windows PowerShell (instructions fournies pour PowerShell)

## Installation

1. Créez et activez un environnement virtuel :

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Installez les dépendances :

```powershell
pip install -r .\requirements.txt
```

## Lancer l'API

Depuis la racine du projet :

```powershell
uvicorn app.main:app --reload
```

L'API sera disponible sur http://127.0.0.1:8000.

## Endpoints d'authentification

- POST `/auth/register` — envoie JSON {"email":"...","password":"..."} pour créer un utilisateur.
- POST `/auth/login` — authentification (form data: `username`, `password`) ; retourne `access_token` (JWT).

Utilisez l'en-tête HTTP `Authorization: Bearer <token>` pour accéder aux routes protégées.

## Script d'initialisation (seed)

Un script `scripts/seed_db.py` permet de créer les tables et d'insérer des données de démonstration :

```powershell
python .\scripts\seed_db.py
```

Le script crée :
- Un administrateur : `admin@example.com` / `adminpass`
- Un utilisateur : `user@example.com` / `userpass`
- Quelques `Zone`, `Source` et `Indicator` exemples

Après exécution, connectez-vous avec `/auth/login` et utilisez le token pour appeler les endpoints protégés.

> Sécurité : changez la valeur `SECRET_KEY` dans `app/core/config.py` avant toute utilisation en production.

## Structure minimale créée

- `app/main.py` — point d'entrée FastAPI
- `app/database.py` — configuration SQLAlchemy (SQLite par défaut)
- `app/core/` — config et sécurité JWT
- `app/models/` — modèles SQLAlchemy (User, Zone, Source, Indicator)
- `app/routers/` — routes `auth` et `users`
- `scripts/seed_db.py` — script de peuplement

## Prochaines étapes recommandées

- Ajouter les routes CRUD pour `Indicator`, `Zone`, `Source` avec filtres, pagination et tests d'intégration.
- Mettre en place Alembic pour gérer les migrations.
- Améliorer la gestion des rôles et politiques d'autorisation fines.

Si vous voulez, je peux implémenter la suite : endpoints CRUD, endpoints de statistiques et tests. Dites‑moi par quoi vous voulez que je commence.

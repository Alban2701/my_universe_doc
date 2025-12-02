# MyUniverseDoc Backend - Guide d'initialisation

## Prérequis

- python 3.19 minimum installé
- Docker et Docker Compose installés
- Fichier .env avec les variables POSTGRES_HOST POSTGRES_PORT DATABASE_NAME POSTGRES_USER POSTGRES_PASSWORD définies
- PGAdmin conseillé pour consulter la base de données

## Installation

### 1. Cloner le dépôt

```pwsh
git clone git@github.com:Alban2701/my_universe_doc.git
```

cd backend

### 2. Construire et lancer les conteneurs

```pwsh
docker compose up -d --build
```

## Vérification

- Vérifier que la base de données tourne

```pwsh
docker compose logs -f server
```

## Lancer l'application

### Construire un environnement virtuel python et installer les dépendances

#### Create the virtual environment

`python -m venv .venv`

#### Activate the virtual environment

- on windows : `.venv/Scripts/activate`
- on linux : `source .venv/bin/activate`

`deactivate` to deactivate the Python venv

#### Installer les dépendances

Dans l'environnement virtuel : `pip install -r requirements.txt`

#### Lancer le serveur

`cd src` puis `uvicorn server:app`

- L’API est accessible sur <http://localhost:8000>

## Gestion des conteneurs

- Arrêter les conteneurs :

```pwsh
docker compose down
```

- Rebuild si Dockerfile change :

```pwsh
docker compose build
docker compose up -d
```

## Base de données

- PostgreSQL est disponible sur le port interne 5432.
- Les données sont persistées via le volume Docker db-data.

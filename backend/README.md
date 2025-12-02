# MyUniverseDoc Backend - Guide d'initialisation

## Prérequis

- Docker et Docker Compose installés
- Fichier .env avec la variable POSTGRES_PASSWORD définie

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

- Vérifier que le serveur tourne

```pwsh
docker compose logs -f server
```

- L’API est accessible sur <http://localhost:8000>

## Gestion des conteneurs

- Arrêter les conteneurs :

```pwsh
docker compose down
```

- Rebuild si requirements.txt ou Dockerfile change :

```pwsh
docker compose build
docker compose up -d
```

## Développement

- Le code est monté en volume, les modifications sont prises en compte automatiquement par Uvicorn.
- L’API se recharge automatiquement grâce au mode --reload.

## Base de données

- PostgreSQL est disponible sur le port interne 5432.
- Les données sont persistées via le volume Docker db-data.

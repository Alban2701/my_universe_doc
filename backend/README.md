# MyUniverseDoc Backend - Guide d'initialisation

## Prérequis

- python 3.13 minimum installé
- Docker et Docker Compose installés
- git installé et configuré
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

```pwsh
docker compose logs -f
```

Devrait s'afficher des message  

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

## Backend

L'api tourne sur le port 8000

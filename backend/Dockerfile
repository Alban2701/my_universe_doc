# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13.9
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer les dépendances système minimales (si besoin)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer pip
RUN python -m pip install --upgrade pip

# Copier uniquement requirements.txt pour tirer parti du cache
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Créer un utilisateur non privilégié
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

USER appuser

# Copier le code sera fait via volume dans dev, donc pas strictement nécessaire
# COPY . .

EXPOSE 8000

# Commande par défaut pour le développement
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

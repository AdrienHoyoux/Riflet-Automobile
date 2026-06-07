#!/bin/sh
# Déploiement manuel Riflet Automobile sur VPS Hostinger (SSH + Traefik)
# Usage : ./deploy/hostinger.sh [install|update|logs|stop|reset-volumes]

set -e

PROJECT_NAME=riflet-automobile
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -f .env ]; then
  echo "Fichier .env manquant. Copiez .env.production.example vers .env et éditez-le."
  echo "  cp .env.production.example .env && nano .env"
  exit 1
fi

cmd="${1:-update}"

case "$cmd" in
  install)
    echo "==> Build et démarrage (première installation)..."
    docker compose -p "$PROJECT_NAME" --env-file .env up -d --build
    echo "==> Attendez les logs backend (seed_data automatique) :"
    echo "    ./deploy/hostinger.sh logs"
    ;;
  update)
    echo "==> Mise à jour (git pull + rebuild)..."
    git pull origin main
    docker compose -p "$PROJECT_NAME" --env-file .env up -d --build
    ;;
  logs)
    docker logs -f riflet_backend
    ;;
  stop)
    docker compose -p "$PROJECT_NAME" --env-file .env down
    ;;
  reset-volumes)
    echo "ATTENTION : supprime la base MySQL et les médias uploadés."
    printf "Continuer ? [y/N] "
    read -r ans
    case "$ans" in
      y|Y) docker compose -p "$PROJECT_NAME" --env-file .env down -v ;;
      *) echo "Annulé." ;;
    esac
    ;;
  *)
    echo "Usage: $0 {install|update|logs|stop|reset-volumes}"
    exit 1
    ;;
esac
